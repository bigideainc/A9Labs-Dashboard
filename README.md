---
title: Alpha9 Training Dashboard
emoji: 🧠
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# Alpha9 Training Dashboard

Real-time monitoring dashboard for the Alpha9 Bittensor network. This dashboard displays training metrics and performance data from decentralized AI training operations.

## Features
- Real-time training progress monitoring
- Historical analysis of training metrics
- Miner performance rankings
- Network status overview

## Usage
The dashboard automatically fetches and displays metrics from the Alpha9 training network through Hugging Face repositories.

## Development
To run locally:
1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables: `cp .env.example .env`
3. Run the app: `streamlit run app.py`