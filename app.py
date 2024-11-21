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

# Get configuration from multiple sources
def get_config():
    # Try to get from Streamlit secrets first
    try:
        hf_token = st.secrets["HF_TOKEN"]
    except (FileNotFoundError, KeyError):
        # Fall back to environment variables
        hf_token = os.getenv("HF_TOKEN")
    
    try:
        central_repo = st.secrets["CENTRAL_REPO"]
    except (FileNotFoundError, KeyError):
        central_repo = os.getenv("CENTRAL_REPO", "Tobius/yogpt_test")
    
    return hf_token, central_repo

def create_dashboard():
    # All the existing code from the start until the page config
    # Move it inside this function
    
    # Get configuration from multiple sources
    hf_token, central_repo = get_config()
    
    # Initialize metrics manager
    if 'metrics_manager' not in st.session_state:
        try:
            st.session_state.metrics_manager = MetricsManager(
                repo_name=central_repo,
                token=hf_token
            )
        except Exception as e:
            st.error(f"Failed to initialize metrics manager: {str(e)}")
            st.stop()
    
    # Rest of the dashboard code...
    # All the UI components and logic
