"""
FinOps AI Dashboard - Main Entry Point
Modern Streamlit 1.52+ Application
"""

import streamlit as st
from src.ui.styles import get_css
from src.ui.chat import render_chat
from src.ui.dashboard import render_dashboard

# Page Config
st.set_page_config(
    page_title="FinOps AI Dashboard",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject CSS
st.markdown(get_css(), unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## ☁️ FinOps AI")
    st.caption("Cloud Cost Intelligence Platform")
    st.markdown("---")

    # Navigation using segmented control
    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "💬 Assistant"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Quick filters
    with st.expander("🎛️ Quick Filters", expanded=False):
        st.multiselect(
            "Services",
            ["Amazon EC2", "Amazon S3", "Amazon RDS", "AWS Lambda", "CloudFront"],
            default=["Amazon EC2", "Amazon S3"],
            key="service_filter",
        )
        st.multiselect(
            "Regions",
            ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-2"],
            default=["us-east-1"],
            key="region_filter",
        )

    st.markdown("---")

    # Settings
    with st.expander("⚙️ Settings", expanded=False):
        st.toggle("Dark Mode", value=False, key="dark_mode", disabled=True)
        st.toggle("Notifications", value=True, key="notifications")
        st.selectbox(
            "Currency",
            ["USD ($)", "EUR (€)", "GBP (£)"],
            key="currency",
        )

    # Footer
    st.markdown("---")
    st.caption("v2.0 • Streamlit 1.52")

# Main Content
if "Dashboard" in page:
    render_dashboard()
else:
    # Full-width chat view
    st.markdown("## 💬 FinOps Assistant", text_alignment="center")
    st.caption("Ask questions about your cloud costs", unsafe_allow_html=False)
    st.space(1)
    render_chat()
