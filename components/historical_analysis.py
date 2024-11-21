import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

def create_analysis_chart(data, title):
    x = data['x']
    y = data['y']
    
    fig = go.Figure()
    
    # Plot actual data
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name='Actual',
        line=dict(color='#9146FF')
    ))
    
    fig.update_layout(
        title=title,
        height=300,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        showlegend=True
    )
    
    return fig

def display_historical_analysis():
    st.subheader("Historical Analysis")
    
    data_generator = st.session_state.data_generator
    
    # Add time range selector
    time_range = st.selectbox(
        "Analysis Time Range",
        ["Last Hour", "Last 24 Hours", "Last Week"],
        index=0
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Network Loss Analysis
        loss_data = data_generator.get_loss_data()  # Ensure this method fetches the required data
        st.plotly_chart(
            create_analysis_chart(loss_data, "Network Loss Trend Analysis"),
            use_container_width=True
        )
        
    with col2:
        # Network Throughput Analysis
        tps_data = data_generator.get_tps_data()  # Ensure this method fetches the required data
        st.plotly_chart(
            create_analysis_chart(tps_data, "Network Throughput Trend Analysis"),
            use_container_width=True
        )
