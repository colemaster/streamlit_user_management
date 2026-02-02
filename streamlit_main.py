"""Entry point for the Streamlit application"""

import asyncio
import os
import streamlit as st
from src.ui.pages import render
from src.database.database import Base, engine
from src.auth.guard import AuthGuard
from src.auth.enhanced_auth import EnhancedAuthHandler
from src.auth.config import ConfigurationError
from src.ui.styles import get_css


# --------------------------------------------------------------------------
#                                 CONFIG
# --------------------------------------------------------------------------
def setup():
    st.set_page_config(
        page_title="BHP FinOps Intelligence",
        page_icon="💸",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Nightly Feature: Global Logo
    st.logo(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/BHP_2017_logo.svg/800px-BHP_2017_logo.svg.png",
        link="https://bhp.com",
        icon_image="https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/BHP_2017_logo.svg/800px-BHP_2017_logo.svg.png",
    )

    # Inject Global CSS
    st.markdown(get_css(), unsafe_allow_html=True)


# Call the setup function
setup()

# Initialize database
Base.metadata.create_all(engine)

# Initialize authentication guard and enhanced auth handler
try:
    auth_guard = AuthGuard()
    enhanced_auth = EnhancedAuthHandler()
except ConfigurationError as e:
    if os.getenv("NO_AUTH"):
        auth_guard = AuthGuard(config=None)  # We will bypass internal checks later
        enhanced_auth = EnhancedAuthHandler(config=None)
        st.warning("Running without Auth Config (NO_AUTH active)")
    else:
        st.error(f"Configuration Error: {e}")
        st.stop()

if os.getenv("NO_AUTH"):
    st.toast("⚠️ Running in NO_AUTH Mode (Mock Admin)", icon="🛡️")

# Add Logo
st.logo(
    "/home/sean/.gemini/antigravity/brain/28584ee8-5cc9-47b9-900e-3117bed716a2/bhp_mining_logo_dark_1765185101973.png",
    icon_image="/home/sean/.gemini/antigravity/brain/28584ee8-5cc9-47b9-900e-3117bed716a2/bhp_mining_logo_dark_1765185101973.png",
    size="large",
)

# Check authentication before rendering pages
if auth_guard.require_auth():
    # Maintain session security with enhanced features
    if not enhanced_auth.maintain_session_security():
        st.stop()  # Session security check failed, user will be logged out
    
    # Handle any logout confirmation dialogs
    enhanced_auth.integrate_with_dialogs()
    
    # Initialize user permissions if not already cached
    if "permissions_initialized" not in st.session_state:
        with st.status("Initializing User Permissions...", expanded=True) as status:
            try:
                st.write("Fetching user groups from Entra ID...")
                permission = asyncio.run(enhanced_auth.initialize_enhanced_session())
                if permission:
                    st.write("Permissions mapped successfully.")
                    status.update(
                        label="Permissions Initialized",
                        state="complete",
                        expanded=False,
                    )
            except Exception as e:
                status.update(
                    label="Permission Initialization Failed",
                    state="error",
                    expanded=True,
                )
                st.error(f"Error initializing permissions: {e}")

    # Render the main application with enhanced auth handler
    render(auth_guard, enhanced_auth)
