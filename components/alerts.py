import streamlit as st
from datetime import datetime

ALERT_LEVELS = {
    'critical': '🔴',
    'warning': '🟡',
    'info': '🔵'
}

class AlertSystem:
    def __init__(self):
        if 'alerts' not in st.session_state:
            st.session_state.alerts = []
        
    def add_alert(self, message, level='info', timestamp=None):
        if timestamp is None:
            timestamp = datetime.now()
        
        alert = {
            'message': message,
            'level': level,
            'timestamp': timestamp,
            'read': False
        }
        
        st.session_state.alerts.insert(0, alert)
        # Keep only last 50 alerts
        st.session_state.alerts = st.session_state.alerts[:50]
    
    def display_alerts(self):
        st.subheader("Network Alerts")
        
        if not st.session_state.alerts:
            st.info("No alerts to display")
            return
            
        for alert in st.session_state.alerts:
            icon = ALERT_LEVELS[alert['level']]
            time_str = alert['timestamp'].strftime("%H:%M:%S")
            
            with st.container():
                col1, col2 = st.columns([0.15, 0.85])
                with col1:
                    st.write(f"{icon} {time_str}")
                with col2:
                    st.write(alert['message'])
                st.divider()

def check_network_alerts(data_generator):
    alert_system = AlertSystem()
    
    # Check loss changes
    loss_data = data_generator.get_loss_data()
    current_loss = loss_data['y'][-1]
    if current_loss > 5:
        alert_system.add_alert(
            f"High network loss detected: {current_loss:.2f}",
            level='critical'
        )
    
    # Check network throughput
    tps_data = data_generator.get_tps_data()
    current_tps = tps_data['y'][-1]
    if current_tps < 40000:
        alert_system.add_alert(
            f"Network throughput dropped below threshold: {current_tps:.0f} tokens/s",
            level='warning'
        )
    
    # Check perplexity
    perplexity_data = data_generator.get_perplexity_data()
    current_perplexity = perplexity_data['y'][-1]
    if current_perplexity > 50:
        alert_system.add_alert(
            f"High model perplexity: {current_perplexity:.2f}",
            level='warning'
        )
    
    # Check learning rate changes
    lr_data = data_generator.get_lr_data()
    current_lr = lr_data['y'][-1]
    if current_lr != 7.5e-5:
        alert_system.add_alert(
            f"Learning rate changed to {current_lr:.2e}",
            level='info'
        )
    
    return alert_system
