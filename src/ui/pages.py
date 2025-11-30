"""Handles routing and layout rendering with Entra ID authentication"""

import streamlit as st
from src.auth.guard import AuthGuard
from src.auth.claims import extract_user_claims
from src.auth.permissions import get_current_permission


def render(auth_guard: AuthGuard):
    """
    Render the main application with Entra ID authentication.

    Args:
        auth_guard: Initialized AuthGuard instance
    """
    # Get user claims
    claims = extract_user_claims()

    # Sidebar with user info and logout
    if claims:
        # Get permission level (needed for navigation and display)
        permission = get_current_permission()

        # User Profile Popover (New in Streamlit 1.29+, enhanced in 1.51)
        with st.sidebar.popover(
            f"👋 {claims.name or claims.email}", use_container_width=True
        ):
            st.markdown(f"**Email:** {claims.email}")

            # Show permission level
            if permission:
                st.info(f"🔑 Permission: {permission.name}")

            if st.button("🚪 Logout", type="primary", use_container_width=True):
                auth_guard.logout()
                st.rerun()

        st.sidebar.markdown("---")

        # Navigation
        page = st.sidebar.radio(
            "Navigation",
            ["Chat", "Admin Dashboard"]
            if permission and permission.name == "ADMIN"
            else ["Chat"],
        )

        # Routing
        if page == "Admin Dashboard":
            from src.ui.admin import render_admin_dashboard

            render_admin_dashboard()
        else:
            # Main Chat Interface
            st.title("💬 FinOps Assistant")
            from src.ui.chat import render_chat

            render_chat()
