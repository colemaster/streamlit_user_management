"""Handles routing and layout rendering with Entra ID authentication"""

import streamlit as st
from src.auth.guard import AuthGuard
from src.auth.claims import extract_user_claims
from src.auth.permissions import get_current_permission, PermissionLevel


def render(auth_guard: AuthGuard):
    """
    Render the main application navigation and routing using st.navigation.
    """
    claims = extract_user_claims()
    if not claims:
        st.error("Authentication Context Missing")
        return

    permission = get_current_permission()

    # --------------------------------------------------------------------------
    #                                SIDEBAR PROFILE
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
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    #                                PAGES SETUP
    # --------------------------------------------------------------------------
    from src.ui.chat import render_chat
    from src.ui.dashboard import render_dashboard
    from src.ui.admin import render_admin_dashboard

    # Define pages
    pages = [st.Page(render_chat, title="Assistant", icon="🤖", default=True)]

    if permission:
        if permission >= PermissionLevel.ANALYST:
            pages.append(st.Page(render_dashboard, title="Analytics", icon="📈"))
        if permission >= PermissionLevel.ADMIN:
            pages.append(
                st.Page(render_admin_dashboard, title="Admin Console", icon="🛡️")
            )

    # Render navigation
    pg = st.navigation(pages)

    # Custom footer in sidebar
    with st.sidebar:
        st.markdown(
            '<div style="margin-top: auto; padding-top: 2rem; color: #444; font-size: 0.8rem; text-align: center;">FinOps AI v2.1</div>',
            unsafe_allow_html=True,
        )

    # Run the selected page
    pg.run()
