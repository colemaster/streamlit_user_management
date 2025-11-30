import streamlit as st
from src.ui.styles import get_css
from src.ui.chat import render_chat
from src.ui.dashboard import render_dashboard

# --- Page Config ---
st.set_page_config(
    page_title="FinOps AI Dashboard",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Inject CSS ---
st.markdown(get_css(), unsafe_allow_html=True)

# --- Sidebar Filters ---
with st.sidebar:
    st.title("💸 FinOps Agent")
    st.markdown("---")
    
    st.subheader("Filters")
    date_range = st.date_input("Date Range", [])
    service_filter = st.multiselect("Services", ["Amazon EC2", "Amazon S3", "Amazon RDS", "AWS Lambda"], default=["Amazon EC2", "Amazon S3"])
    region_filter = st.multiselect("Regions", ["us-east-1", "us-west-2", "eu-west-1"], default=["us-east-1"])
    
    st.markdown("---")
    st.markdown("### AI Settings")
    st.toggle("Stream Responses", value=True)
    st.toggle("Show Thinking", value=True)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- Main Layout ---
# st.title("Cloud Cost Intelligence")

# Create two columns: Dashboard (75%) and Chat Sideprompt (25%)
col_dashboard, col_chat = st.columns([0.75, 0.25], gap="medium")

with col_dashboard:
    render_dashboard()

with col_chat:
    st.markdown("### 💬 AI Assistant")
    render_chat()
