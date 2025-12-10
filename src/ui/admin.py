"""
Admin Dashboard - Streamlit 1.52+
"""

import streamlit as st

from src.auth.claims import extract_user_claims
from src.auth.permissions import UserPermission, SESSION_PERMISSION_KEY
from src.auth.logging import get_recent_logs
from src.ui.components import animated_header, render_metric_card, render_status_badge


def render_admin_dashboard():
    """Render the Admin Dashboard."""
    animated_header(
        "Admin Console", "System status, security log, and identity management"
    )

    # Tabs with custom styling wrapper (implicit via global CSS)
    tab1, tab2, tab3 = st.tabs(["👤 Identity", "🔐 Entra ID", "📜 Audit Logs"])

    with tab1:
        _render_user_info()
    with tab2:
        _render_entra_metrics()
    with tab3:
        _render_auth_logs()


def _render_user_info():
    claims = extract_user_claims()
    if not claims:
        st.error("No identity context found.")
        return

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.caption("Active Session Context")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(
            "https://ui-avatars.com/api/?name="
            + (claims.name or "User")
            + "&background=FF5500&color=fff",
            width=80,
        )
        st.markdown(f"### {claims.name}")
        st.markdown(f"*{claims.email}*")
        render_status_badge("active", "Authenticated")

    with col2:
        data = {
            "Principal ID (OID)": claims.oid,
            "Tenant ID": claims.tenant_id,
            "Username": claims.preferred_username,
            "Issuer": claims.raw_claims.get("iss", "N/A")
            if claims.raw_claims
            else "N/A",
        }
        for k, v in data.items():
            st.markdown(f"**{k}:** `{v}`")

    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Show Raw JWT Claims"):
        st.json(claims.raw_claims)


def _render_entra_metrics():
    permission_data = st.session_state.get(SESSION_PERMISSION_KEY)
    if not permission_data:
        st.warning("Permissions not initialized")
        return

    user_perm = UserPermission.from_dict(permission_data)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.caption("Access Control")
        render_metric_card(
            "Permission Level", user_perm.permission_level.name, None, "neutral"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        render_status_badge("active", "Entra ID Synced")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.caption("Security Group Membership")

        if user_perm.group_oids:
            for group in user_perm.group_oids:
                st.markdown(f"- `{group}`")
        else:
            st.info("No mapped security groups")
        st.markdown("</div>", unsafe_allow_html=True)


def _render_auth_logs():
    st.markdown(
        '<div style="display:flex; justify-content:space-between; align-items:center;"><h3>Security Audit</h3>',
        unsafe_allow_html=True,
    )
    if st.button("🔄 Refresh", key="refresh_logs"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    logs = get_recent_logs(50)

    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric_card("Total Events", str(len(logs)), None, "neutral")
    with col2:
        errs = len([l for l in logs if "ERROR" in l])
        render_metric_card(
            "Errors",
            str(errs),
            "Low" if errs < 5 else "High",
            "success" if errs == 0 else "error",
        )
    with col3:
        warns = len([l for l in logs if "WARNING" in l])
        render_metric_card(
            "Warnings", str(warns), None, "warning" if warns > 0 else "neutral"
        )

    st.markdown("### Log Stream")
    with st.container(height=400):
        for log in logs:
            color = (
                "#FF3333"
                if "ERROR" in log
                else "#FFB020"
                if "WARNING" in log
                else "#00D16C"
            )
            st.markdown(
                f'<div style="border-left: 2px solid {color}; padding-left: 10px; margin-bottom: 4px; font-family: monospace; font-size: 0.85rem; background: rgba(255,255,255,0.03);">{log}</div>',
                unsafe_allow_html=True,
            )
