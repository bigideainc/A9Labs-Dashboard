import streamlit as st
from app import create_dashboard

if __name__ == "__main__":
    st.set_page_config(
        page_title="Alpha9 Training Dashboard",
        page_icon="🧠",
        layout="wide"
    )
    create_dashboard()