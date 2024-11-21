import streamlit as st
import plotly.graph_objects as go

def display_map():
    # Create a dark-themed map centered on Europe
    fig = go.Figure(go.Scattergeo())
    
    fig.update_geos(
        showcountries=True,
        countrycolor="rgb(80, 80, 80)",
        showland=True,
        landcolor="rgb(40, 40, 40)",
        showocean=True,
        oceancolor="rgb(20, 20, 20)",
        projection_type="orthographic",
        projection_rotation=dict(lon=15, lat=50, roll=0),
        showframe=False,
        bgcolor='rgba(0,0,0,0)'
    )
    
    # Add node locations
    locations = st.session_state.data_generator.get_node_locations()
    
    fig.add_trace(go.Scattergeo(
        lon=locations['lon'],
        lat=locations['lat'],
        mode='markers',
        marker=dict(
            size=8,
            color='#9146FF',
            symbol='circle'
        ),
        hoverinfo='text',
        text=locations['location']
    ))
    
    fig.update_layout(
        title="Node Locations",
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
