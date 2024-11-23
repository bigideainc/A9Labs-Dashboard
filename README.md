---
title: Alpha9 Training Dashboard
emoji: 🧠
colorFrom: indigo
colorTo: purple
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
---

# Alpha9 Training Dashboard 🧠

Real-time monitoring dashboard for the Alpha9 Bittensor network, displaying training metrics and performance data from decentralized AI training operations.

You can find the dashboard here: [Hermit11/A9-Dashboard](https://huggingface.co/spaces/Hermit11/A9-Dashboard).

## Features
- Real-time training progress monitoring
- Historical analysis of training metrics
- Miner performance rankings and geographical distribution
- Network status overview
- Auto-refreshing metrics

## System Requirements
- Python 3.8+
- 2GB RAM minimum
- Internet connection for real-time updates
- Hugging Face account and API token

## Getting Started

### Prerequisites

1. Get a Hugging Face Account and Token:
   - Create an account at [Hugging Face](https://huggingface.co/)
   - Generate an access token from [Settings → Access Tokens](https://huggingface.co/settings/tokens)
   - Make sure you have read access to the metrics repository

2. Clone the repository:
```bash
git clone https://github.com/bigideainc/A9Labs-Dashboard.git
cd A9Labs-Dashboard
```

3. Set up your Python environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file in the project root:
```bash
HF_TOKEN="your_hugging_face_token_here"
CENTRAL_REPO="Tobius/yogpt_test"  # or your metrics repository
```

### Running Locally

1. Start the dashboard:
```bash
streamlit run app.py
```

2. Access the dashboard in your browser:
- The dashboard will automatically open at `http://localhost:8501`
- For remote access, use the network URL provided in the terminal

## Dashboard Sections

### Training Progress
- Overall progress bar showing completion percentage
- Total tokens processed
- Target token goal

### Training Metrics
- Loss curves
- Perplexity measurements
- Tokens per second performance
- Learning rate adaptation

### Network Overview
- Active miners leaderboard
- Geographical distribution map
- Real-time status indicators

## Development

### Project Structure
```
A9-Dashboard/
├── app.py              # Main dashboard application
├── utils/
│   └── HFManager.py    # Hugging Face integration utilities
├── requirements.txt    # Project dependencies
└── .env               # Environment configuration
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Accessing the Hosted Dashboard

The dashboard is hosted as a Hugging Face Space at [Hermit11/A9-Dashboard](https://huggingface.co/spaces/Hermit11/A9-Dashboard).

### Authentication
- No authentication required for viewing
- HF token required for deployment and modifications

## Troubleshooting

### Common Issues

1. "No Hugging Face token found":
   - Ensure your `.env` file contains a valid `HF_TOKEN`
   - Check token permissions on Hugging Face

2. "Cannot connect to metrics repository":
   - Verify repository access permissions
   - Check internet connection
   - Confirm repository name in `.env`

### Support
- Create an issue in the GitHub repository
- Contact the development team through [GitHub Issues](https://github.com/bigideainc/A9Labs-Dashboard/issues)

## License
This project is licensed under the MIT License - see the LICENSE file for details.