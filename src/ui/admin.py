"""
Admin Dashboard - Streamlit 1.52+
User access details, Entra ID metrics, and auth logs.
"""

import streamlit as st
import pandas as pd
from src.auth.claims import extract_user_claims
from src.auth.permissions import (
    UserPermission,
    SESSION_PERMISSION_KEY,
)
from src.auth.logging import get_recent_logs


def render_admin_dashboard():
    """Render the Admin Dashboard."""
    st.title("🛡️ Admin Dashboard")
    st.space(1)

    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["👤 User Info", "🔑 Entra ID", "📋 Auth Logs"])

    with tab1:
        _render_user_info()

    with tab2:
        _render_entra_metrics()

    with tab3:
        _render_auth_logs()


def _render_user_info():
    """Render current user information."""
    st.subheader("Current User Information")

    claims = extract_user_claims()
    if not claims:
        st.error("No user claims found.")
        return

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("#### Identity Claims")
            st.dataframe(
                pd.DataFrame(
                    {
                        "Field": ["Name", "Email", "OID", "Tenant ID", "Username"],
                        "Value": [
                            claims.name or "N/A",
                            claims.email or "N/A",
                            claims.oid or "N/A",
                            claims.tenant_id or "N/A",
                            claims.preferred_username or "N/A",
                        ],
                    }
                ),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Field": st.column_config.TextColumn("Field", width="small"),
                    "Value": st.column_config.TextColumn("Value", width="large"),
                },
            )

    with col2:
        with st.container(border=True):
            st.markdown("#### Raw Token Claims")
            st.caption("Full claims from Identity Provider")
            if claims.raw_claims:
                st.json(claims.raw_claims, expanded=False)
            else:
                st.warning("No raw claims available.")


def _render_entra_metrics():
    """Render Entra ID and permissions info."""
    st.subheader("Entra ID & Permissions")

    permission_data = st.session_state.get(SESSION_PERMISSION_KEY)

    if not permission_data:
        st.warning("Permission data not initialized.")
        return

    user_perm = UserPermission.from_dict(permission_data)

    # Permission level card
    col1, col2 = st.columns([1, 2])

    with col1:
        with st.container(border=True):
            st.markdown("#### Assigned Permission")
            st.metric(
                "Level",
                user_perm.permission_level.name,
                delta_arrow="off",
            )
            st.badge(
                "Active",
                icon="✅",
            )

    with col2:
        with st.container(border=True):
            st.markdown("#### Group Memberships")

            if user_perm.group_oids:
                st.caption(f"User belongs to {len(user_perm.group_oids)} groups")

                df_groups = pd.DataFrame(user_perm.group_oids, columns=["Group OID"])
                st.dataframe(
                    df_groups,
                    use_container_width=True,
                    hide_index=True,
                    height=200,
                    column_config={
                        "Group OID": st.column_config.TextColumn(
                            "Group Object ID",
                            help="Unique identifier in Entra ID",
                        )
                    },
                )
            else:
                st.info("No group memberships found.")


def _render_auth_logs():
    """Render authentication logs."""
    st.subheader("Authentication Logs")
    st.caption("Recent authentication events from memory buffer")

    # Filter controls
    filter_cols = st.columns([2, 1])

    with filter_cols[0]:
        log_filter = st.segmented_control(
            "Filter by Level",
            ["ALL", "INFO", "WARNING", "ERROR"],
            default="ALL",
            selection_mode="single",
        )

    with filter_cols[1]:
        if st.button("🔄 Refresh Logs", use_container_width=True):
            st.rerun()

    st.space(1)

    logs = get_recent_logs(100)

    if not logs:
        st.info("No logs available.")
        return

    # Filter logs
    filtered_logs = logs
    if log_filter and log_filter != "ALL":
        filtered_logs = [log for log in logs if log_filter in log]

    if not filtered_logs:
        st.info(f"No logs found for level: {log_filter}")
        return

    # Display logs in a container
    with st.container(border=True, height=400):
        st.code("\n".join(filtered_logs), language="text")

    # Log stats
    stat_cols = st.columns(4)
    with stat_cols[0]:
        st.metric("Total Logs", len(logs), delta_arrow="off")
    with stat_cols[1]:
        info_count = len([l for l in logs if "INFO" in l])
        st.metric("Info", info_count, delta_arrow="off")
    with stat_cols[2]:
        warn_count = len([l for l in logs if "WARNING" in l])
        st.metric("Warnings", warn_count, delta_arrow="off")
    with stat_cols[3]:
        error_count = len([l for l in logs if "ERROR" in l])
        st.metric("Errors", error_count, delta_arrow="off")
