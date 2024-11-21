import streamlit as st
import time
from datetime import datetime
import logging
from utils.HFManager import fetch_training_metrics_commits
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Page config
st.set_page_config(
    page_title="Alpha9 Training Dashboard",
    page_icon="🧠",
    layout="wide",
    menu_items={
        'Get Help': 'https://github.com/Alpha9-Omega/YoGPT',
        'Report a bug': "https://github.com/Alpha9-Omega/YoGPT/issues",
        'About': "Dashboard for monitoring Alpha9 Bittensor network"
    }
)

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

        # Get the latest job
        latest_job_id = max(jobs.keys())
        return jobs[latest_job_id]

    def get_historical_metrics(self):
        metrics = self.fetch_latest_metrics()
        if not metrics:
            return pd.DataFrame()

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
        
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d_%H%M%S')
        except ValueError:
            try:
                df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
            except:
                st.warning("Could not parse some timestamp values")
        
        return df.sort_values('timestamp')

# Get configuration
hf_token = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN"))
central_repo = st.secrets.get("CENTRAL_REPO", os.getenv("CENTRAL_REPO", "Tobius/yogpt_test"))

if not hf_token:
    st.error("No Hugging Face token found")
    st.stop()

# Initialize metrics manager
if 'metrics_manager' not in st.session_state:
    st.session_state.metrics_manager = MetricsManager(central_repo, hf_token)

# Dashboard UI
st.title("🧠 Alpha9 Training Dashboard")
st.markdown("Real-time monitoring dashboard for the Alpha9 Bittensor network.")

col1, col2 = st.columns([3, 2])

with col1:
    with st.expander("📈 Training Progress", expanded=True):
        latest_metrics = st.session_state.metrics_manager.get_latest_job_metrics()
        if latest_metrics:
            latest_entry = latest_metrics[-1]
            st.metric("Current Job ID", latest_entry['metrics']['job_id'])
            st.metric("Active Miners", len(latest_metrics))
            if 'final_loss' in latest_entry['metrics']:
                st.metric("Best Loss", f"{latest_entry['metrics']['final_loss']:.4f}")

    with st.expander("📊 Historical Analysis", expanded=True):
        df = st.session_state.metrics_manager.get_historical_metrics()
        if not df.empty:
            st.line_chart(df.set_index('timestamp')['final_loss'])
            st.dataframe(df.groupby('job_id').agg({
                'final_loss': ['min', 'mean', 'count']
            }).round(4))

with col2:
    with st.expander("🏆 Miner Performance", expanded=True):
        if latest_metrics:
            miner_df = pd.DataFrame([
                {
                    'Miner UID': m['miner_uid'],
                    'Final Loss': m['metrics'].get('final_loss', float('inf')),
                    'Model Repo': m['model_repo']
                }
                for m in latest_metrics
            ]).sort_values('Final Loss')
            st.dataframe(miner_df)

    with st.expander("🌐 Network Status", expanded=True):
        last_update_str = st.session_state.metrics_manager.last_update.strftime("%Y-%m-%d %H:%M:%S") if st.session_state.metrics_manager.last_update else "Never"
        st.metric("Last Update", last_update_str)
        if latest_metrics:
            st.metric("Active Jobs", len(set(m['metrics']['job_id'] for m in latest_metrics)))

# Auto-refresh
time.sleep(5)
st.rerun()
