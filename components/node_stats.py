import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

def create_gauge_chart(value, title, min_val=0, max_val=100, suffix=""):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        number={'suffix': suffix},
        gauge={
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': "#9146FF"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, max_val/3], 'color': 'rgba(255, 0, 0, 0.2)'},
                {'range': [max_val/3, 2*max_val/3], 'color': 'rgba(255, 255, 0, 0.2)'},
                {'range': [2*max_val/3, max_val], 'color': 'rgba(0, 255, 0, 0.2)'}
            ]
        }
    ))
    
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'}
    )
    
    return fig

def create_timeline_chart(data, title):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['x'],
        y=data['y'],
        mode='lines',
        line=dict(color='#9146FF', width=2),
        fill='tozeroy',
        fillcolor='rgba(145, 70, 255, 0.1)'
    ))
    
    fig.update_layout(
        title=title,
        height=200,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
    )
    
    return fig

def display_node_stats():
    st.subheader("Node Statistics")
    
    # Get data from the generator
    data_generator = st.session_state.data_generator
    node_stats = data_generator.get_node_stats()
    
    # Node selector
    selected_node = st.selectbox(
        "Select Node",
        options=[node['name'] for node in node_stats],
        index=0
    )
    
    # Get selected node data
    node_data = next(node for node in node_stats if node['name'] == selected_node)
    
    # Create three columns for gauges
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.plotly_chart(
            create_gauge_chart(
                node_data['cpu_usage'],
                "CPU Usage",
                suffix="%"
            ),
            use_container_width=True
        )
        
    with col2:
        st.plotly_chart(
            create_gauge_chart(
                node_data['memory_usage'],
                "Memory Usage",
                suffix="%"
            ),
            use_container_width=True
        )
        
    with col3:
        st.plotly_chart(
            create_gauge_chart(
                node_data['gpu_usage'],
                "GPU Usage",
                suffix="%"
            ),
            use_container_width=True
        )
    
    # Network metrics
    st.markdown("### Network Metrics")
    col4, col5 = st.columns(2)
    
    with col4:
        st.metric(
            "Response Time",
            f"{node_data['response_time']:.2f} ms",
            f"{node_data['response_time_change']:.1f} ms"
        )
        st.metric(
            "Uptime",
            f"{node_data['uptime']:.1f}%",
            f"{node_data['uptime_change']:.1f}%"
        )
    
    with col5:
        st.metric(
            "Successful Responses",
            f"{node_data['success_rate']:.1f}%",
            f"{node_data['success_rate_change']:.1f}%"
        )
        st.metric(
            "Network Score",
            f"{node_data['network_score']:.2f}",
            f"{node_data['network_score_change']:.2f}"
        )
    
    # Historical performance charts
    st.markdown("### Historical Performance")
    
    # Response time history
    st.plotly_chart(
        create_timeline_chart(
            node_data['response_time_history'],
            "Response Time History (ms)"
        ),
        use_container_width=True
    )
    
    # Network score history
    st.plotly_chart(
        create_timeline_chart(
            node_data['network_score_history'],
            "Network Score History"
        ),
        use_container_width=True
    )
