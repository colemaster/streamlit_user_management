"""Handles routing and layout rendering with Entra ID authentication"""

import streamlit as st
from src.auth.guard import AuthGuard
from src.auth.claims import extract_user_claims
from src.auth.permissions import get_current_permission, PermissionLevel


def render(auth_guard: AuthGuard):
    """
    Render the main application navigation and routing.
    """
    claims = extract_user_claims()
    if not claims:
        st.error("Authentication Context Missing")
        return

    permission = get_current_permission()

    # --------------------------------------------------------------------------
    #                                SIDEBAR
    # --------------------------------------------------------------------------
    with st.sidebar:
        st.markdown('<div style="padding: 1rem 0;">', unsafe_allow_html=True)

        # User Profile
        with st.container(border=True):
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown("👤")
            with col2:
                st.markdown(f"**{claims.name or 'User'}**")
                st.caption(f"{permission.name if permission else 'Guest'}")

            if st.button("Sign Out", use_container_width=True):
                auth_guard.logout()
                st.rerun()

        st.markdown("---")

        # Navigation Options
        options = ["Assistant"]

        if permission:
            if permission >= PermissionLevel.ANALYST:
                options.append("Analytics")
            if permission >= PermissionLevel.ADMIN:
                options.append("Admin Console")

        selected_page = st.radio("Navigate", options, label_visibility="collapsed")

        st.markdown(
            '<div style="margin-top: auto; padding-top: 2rem; color: #444; font-size: 0.8rem; text-align: center;">FinOps AI v2.0</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    #                                ROUTING
    # --------------------------------------------------------------------------
    if selected_page == "Assistant":
        from src.ui.chat import render_chat

        render_chat()

    elif selected_page == "Analytics":
        from src.ui.dashboard import render_dashboard

        render_dashboard()

    elif selected_page == "Admin Console":
        from src.ui.admin import render_admin_dashboard

        render_admin_dashboard()
