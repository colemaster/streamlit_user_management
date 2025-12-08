"""Entry point for the Streamlit application"""

import asyncio
import os
import streamlit as st
from src.ui.pages import render
from src.database.database import Base, engine
from src.auth.guard import AuthGuard
from src.auth.config import ConfigurationError

# Initialize database
Base.metadata.create_all(engine)

# Initialize authentication guard
try:
    auth_guard = AuthGuard()
except ConfigurationError as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

if os.getenv("NO_AUTH"):
    st.toast("⚠️ Running in NO_AUTH Mode (Mock Admin)", icon="🛡️")

# Add Logo (New in 1.35+)
st.logo(
    "/home/sean/.gemini/antigravity/brain/28584ee8-5cc9-47b9-900e-3117bed716a2/bhp_mining_logo_dark_1765185101973.png",
    icon_image="/home/sean/.gemini/antigravity/brain/28584ee8-5cc9-47b9-900e-3117bed716a2/bhp_mining_logo_dark_1765185101973.png",
)

# Check authentication before rendering pages
if auth_guard.require_auth():
    # Initialize user permissions if not already cached
    if "permissions_initialized" not in st.session_state:
        with st.status("Initializing User Permissions...", expanded=True) as status:
            try:
                st.write("Fetching user groups from Entra ID...")
                permission = asyncio.run(auth_guard.initialize_user_permission())
                if permission:
                    st.session_state["permissions_initialized"] = True
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

    # Render the main application
    render(auth_guard)
