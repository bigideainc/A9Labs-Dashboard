import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import logging
from utils.HFManager import fetch_training_metrics_commits
import os
from dotenv import load_dotenv

# Load environment variables and configure logging
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MetricsManager:
    def __init__(self, repo_name, token):
        if not repo_name:
            raise ValueError("Repository name is required")
        if not token:
            raise ValueError("Hugging Face token is required")
            
        self.repo_name = repo_name
        self.token = token
        self.last_update = None
        self.metrics_cache = []
        self.update_interval = 60  # seconds
        logging.info(f"MetricsManager initialized for repo: {repo_name}")

    def needs_update(self):
        if not self.last_update:
            return True
        return (datetime.now() - self.last_update).total_seconds() > self.update_interval

    def fetch_latest_metrics(self):
        if self.needs_update():
            logging.info("Fetching fresh metrics from HuggingFace...")
            try:
                self.metrics_cache = fetch_training_metrics_commits(
                    self.repo_name, 
                    token=self.token
                )
                self.last_update = datetime.now()
                logging.info(f"Fetched {len(self.metrics_cache)} metrics entries")
            except Exception as e:
                logging.error(f"Error fetching metrics: {str(e)}")
                return []
        return self.metrics_cache

    def get_latest_job_metrics(self):
        metrics = self.fetch_latest_metrics()
        if not metrics:
            return None

        # Group metrics by job_id
        jobs = {}
        for entry in metrics:
            job_id = entry['metrics']['job_id']
            if job_id not in jobs:
                jobs[job_id] = []
            jobs[job_id].append(entry)

        # Get the latest job (assuming job_ids are timestamp-based or sequential)
        latest_job_id = max(jobs.keys())
        return jobs[latest_job_id]

    def get_historical_metrics(self):
        metrics = self.fetch_latest_metrics()
        if not metrics:
            return pd.DataFrame()

        # Convert metrics to DataFrame for easier analysis
        records = []
        for entry in metrics:
            record = {
                'timestamp': entry['timestamp'],
                'miner_uid': entry['miner_uid'],
                'job_id': entry['metrics']['job_id'],
                'final_loss': entry['metrics'].get('final_loss', None),
                'model_repo': entry['model_repo']
            }
            records.append(record)
        
        df = pd.DataFrame(records)
        
        # Convert timestamp string to datetime
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d_%H%M%S')
        except ValueError:
            try:
                df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
            except:
                logging.warning("Could not parse some timestamp values")
        
        return df.sort_values('timestamp')

def create_loss_chart(df):
    if df.empty:
        return go.Figure()
    
    fig = px.line(df, x='timestamp', y='final_loss', title='Historical Loss')
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Final Loss",
        template="plotly_dark"
    )
    return fig

def create_miner_performance_table(metrics):
    if not metrics:
        return pd.DataFrame()
    
    miner_df = pd.DataFrame([
        {
            'Miner UID': m['miner_uid'],
            'Final Loss': m['metrics'].get('final_loss', float('inf')),
            'Model Repo': m['model_repo']
        }
        for m in metrics
    ]).sort_values('Final Loss')
    
    return miner_df

def update_dashboard(metrics_manager):
    try:
        latest_metrics = metrics_manager.get_latest_job_metrics()
        if not latest_metrics:
            return (
                "No data", "No data", "No data",  # Metrics
                go.Figure(),  # Loss chart
                pd.DataFrame(),  # Performance table
                "No data", "No data"  # Network status
            )

        # Get latest entry
        latest_entry = latest_metrics[-1]
        job_id = latest_entry['metrics']['job_id']
        active_miners = len(latest_metrics)
        best_loss = f"{latest_entry['metrics'].get('final_loss', 'N/A'):.4f}"

        # Historical metrics
        df = metrics_manager.get_historical_metrics()
        loss_chart = create_loss_chart(df)
        
        # Miner performance
        performance_table = create_miner_performance_table(latest_metrics)
        
        # Network status
        last_update = metrics_manager.last_update.strftime("%Y-%m-%d %H:%M:%S") if metrics_manager.last_update else "Never"
        active_jobs = len(set(m['metrics']['job_id'] for m in latest_metrics))

        return (
            job_id, str(active_miners), best_loss,
            loss_chart,
            performance_table,
            last_update,
            str(active_jobs)
        )
    except Exception as e:
        logging.error(f"Error updating dashboard: {str(e)}")
        return ("Error", "Error", "Error", go.Figure(), pd.DataFrame(), "Error", "Error")

def create_dashboard():
    # Get configuration
    hf_token = os.getenv("HF_TOKEN")
    central_repo = os.getenv("CENTRAL_REPO", "Tobius/yogpt_test")
    
    if not hf_token:
        raise ValueError("No Hugging Face token found in environment variables")

    # Initialize metrics manager
    metrics_manager = MetricsManager(central_repo, hf_token)

    with gr.Blocks(theme=gr.themes.Monochrome()) as dashboard:
        gr.Markdown("# 🧠 Alpha9 Training Dashboard")
        gr.Markdown("Real-time monitoring dashboard for the Alpha9 Bittensor network.")
        
        # Add refresh interval input
        refresh_interval = gr.Slider(
            minimum=1,
            maximum=60,
            value=5,
            step=1,
            label="Refresh Interval (seconds)"
        )
        
        with gr.Row():
            with gr.Column(scale=3):
                with gr.Group():
                    gr.Markdown("### 📈 Training Progress")
                    with gr.Row():
                        job_id = gr.Textbox(label="Current Job ID")
                        active_miners = gr.Textbox(label="Active Miners")
                        best_loss = gr.Textbox(label="Best Loss")
                
                with gr.Group():
                    gr.Markdown("### 📊 Historical Analysis")
                    loss_plot = gr.Plot()
            
            with gr.Column(scale=2):
                with gr.Group():
                    gr.Markdown("### 🏆 Miner Performance")
                    performance_table = gr.Dataframe()
                
                with gr.Group():
                    gr.Markdown("### 🌐 Network Status")
                    last_update = gr.Textbox(label="Last Update")
                    active_jobs = gr.Textbox(label="Active Jobs")

        # Update function
        def update():
            return update_dashboard(metrics_manager)

        # Manual refresh button
        refresh_btn = gr.Button("Refresh")
        refresh_btn.click(
            fn=update,
            outputs=[
                job_id, active_miners, best_loss,
                loss_plot,
                performance_table,
                last_update, active_jobs
            ]
        )

        # Auto-refresh using interval
        interval = gr.Number(value=5, visible=False)  # Hidden interval component
        
        def set_interval(value):
            return value

        refresh_interval.change(
            fn=set_interval,
            inputs=[refresh_interval],
            outputs=[interval]
        )

        gr.on(
            triggers=[interval],
            fn=update,
            outputs=[
                job_id, active_miners, best_loss,
                loss_plot,
                performance_table,
                last_update, active_jobs
            ],
            every=5
        )

    return dashboard

if __name__ == "__main__":
    dashboard = create_dashboard()
    dashboard.launch(server_port=5001)
