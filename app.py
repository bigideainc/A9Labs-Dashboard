import streamlit as st
import time
from datetime import datetime
import logging
from utils.HFManager import fetch_training_metrics_commits
import pandas as pd
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import pydeck as pdk

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Page config
st.set_page_config(page_title="Alpha9 Training Dashboard",
                   page_icon="🧠",
                   layout="wide",
                   menu_items={
                       'Get Help': 'https://github.com/Alpha9-Omega/YoGPT',
                       'Report a bug': "https://github.com/Alpha9-Omega/YoGPT/issues",
                       'About': "Dashboard for monitoring Alpha9 Bittensor network"
                   })

# Custom CSS for progress bar and styling
st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #9146FF, #784CBD);
    }
    .metric-container {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .plot-container {
        background-color: #262730;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

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
                self.metrics_cache = fetch_training_metrics_commits(self.repo_name, token=self.token)
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
                'perplexity': entry['metrics'].get('perplexity', None),
                'tokens_per_second': entry['metrics'].get('tokens_per_second', None),
                'inner_lr': entry['metrics'].get('inner_lr', None),
                'location': entry.get('location', 'Unknown'),
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
try:
    hf_token = st.secrets["HF_TOKEN"]
except:
    hf_token = os.getenv("HF_TOKEN")

try:
    central_repo = st.secrets["CENTRAL_REPO"]
except:
    central_repo = os.getenv("CENTRAL_REPO", "Tobius/yogpt_test")

if not hf_token:
    st.error("No Hugging Face token found. Please set HF_TOKEN in environment variables.")
    st.stop()

# Initialize metrics manager
if 'metrics_manager' not in st.session_state:
    st.session_state.metrics_manager = MetricsManager(central_repo, hf_token)

# Dashboard UI
st.title("🧠 Alpha9 Training Dashboard")

# Progress Bar Section
latest_metrics = st.session_state.metrics_manager.get_latest_job_metrics()
if latest_metrics:
    progress = 0.7158  # This should be calculated from actual data
    tokens_progress = "715,899,792,640/1T tokens"
    
    st.markdown("### Training Progress")
    st.progress(progress)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Progress", f"{progress*100:.2f}%")
    with col2:
        st.metric("Tokens", tokens_progress)

# Metrics Grid
st.markdown("### Training Metrics")
metric_cols = st.columns(2)
with metric_cols[0]:
    # Loss Plot
    fig_loss = go.Figure()
    fig_loss.add_trace(go.Scatter(x=[1, 2, 3], y=[12, 3, 2], 
                                 mode='lines', 
                                 line=dict(color='#9146FF', width=2),
                                 name='Loss'))
    fig_loss.update_layout(
        title='Loss',
        xaxis_title='Steps',
        yaxis_title='Loss',
        yaxis_type="log",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig_loss, use_container_width=True)

    # Tokens per Second Plot
    fig_tps = go.Figure()
    fig_tps.add_trace(go.Scatter(x=[1, 2, 3], y=[40000, 42000, 41000], 
                                mode='lines', 
                                line=dict(color='#9146FF', width=2),
                                name='Tokens/s'))
    fig_tps.update_layout(
        title='Tokens per Second',
        xaxis_title='Time',
        yaxis_title='Tokens/s',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig_tps, use_container_width=True)

with metric_cols[1]:
    # Perplexity Plot
    fig_perp = go.Figure()
    fig_perp.add_trace(go.Scatter(x=[1, 2, 3], y=[200, 50, 20], 
                                 mode='lines', 
                                 line=dict(color='#9146FF', width=2),
                                 name='Perplexity'))
    fig_perp.update_layout(
        title='Perplexity',
        xaxis_title='Steps',
        yaxis_title='Perplexity',
        yaxis_type="log",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig_perp, use_container_width=True)

    # Inner LR Plot
    fig_lr = go.Figure()
    fig_lr.add_trace(go.Scatter(x=[1, 2, 3], y=[0.0001, 0.0001, 0.0001], 
                               mode='lines', 
                               line=dict(color='#9146FF', width=2),
                               name='Inner LR'))
    fig_lr.update_layout(
        title='Inner Learning Rate',
        xaxis_title='Steps',
        yaxis_title='Learning Rate',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig_lr, use_container_width=True)

# Leaderboard and Map
st.markdown("### Network Overview")
col1, col2 = st.columns([3, 2])

with col1:
    if latest_metrics:
        miner_df = pd.DataFrame([{
            'Miner UID': m['miner_uid'],
            'MH/s': round(m['metrics'].get('hashrate', 0) / 1e6, 2),
            'Location': m.get('location', 'Unknown'),
            'Status': 'Active'
        } for m in latest_metrics]).sort_values('MH/s', ascending=False)
        
        st.dataframe(miner_df, use_container_width=True)

with col2:
    # Sample map data
    map_data = pd.DataFrame({
        'lat': [32.7767, 40.7128, 51.5074],
        'lon': [-96.7970, -74.0060, -0.1278],
        'size': [10, 15, 20]
    })
    
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=pdk.ViewState(
            latitude=20,
            longitude=0,
            zoom=1,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=map_data,
                get_position='[lon, lat]',
                get_color='[145, 70, 255, 160]',
                get_radius='size',
                pickable=True
            ),
        ]
    ))

# Auto-refresh
time.sleep(5)
st.rerun()
