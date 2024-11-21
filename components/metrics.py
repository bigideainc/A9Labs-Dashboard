import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_metric_chart(data, title, y_axis_type="linear"):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data['x'],
            y=data['y'],
            mode='lines',
            line=dict(color='#9146FF'),
            fill='tozeroy',
            fillcolor='rgba(145, 70, 255, 0.1)'
        )
    )
    
    fig.update_layout(
        title=title,
        template="plotly_dark",
        showlegend=False,
        height=200,
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_type=y_axis_type
    )
    
    return fig

def display_metrics():
    data_generator = st.session_state.data_generator
    
    # Create 2x2 grid of metrics
    col1, col2 = st.columns(2)
    
    with col1:
        # Loss
        loss_data = data_generator.get_loss_data()
        st.plotly_chart(
            create_metric_chart(loss_data, "Network Training Loss", "log"),
            use_container_width=True
        )
        
        # Tokens per Second
        tps_data = data_generator.get_tps_data()
        st.plotly_chart(
            create_metric_chart(tps_data, "Network Throughput (tokens/s)"),
            use_container_width=True
        )
        
    with col2:
        # Perplexity
        perplexity_data = data_generator.get_perplexity_data()
        st.plotly_chart(
            create_metric_chart(perplexity_data, "Model Perplexity", "log"),
            use_container_width=True
        )
        
        # Learning Rate
        lr_data = data_generator.get_lr_data()
        st.plotly_chart(
            create_metric_chart(lr_data, "Network Learning Rate"),
            use_container_width=True
        )
