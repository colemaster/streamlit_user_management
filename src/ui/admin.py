"""
Admin Dashboard component.

Displays user access details, Entra ID metrics, and auth logs.
"""

import streamlit as st
import pandas as pd
from src.auth.claims import extract_user_claims
from src.auth.permissions import (
    get_current_permission,
    UserPermission,
    SESSION_PERMISSION_KEY,
)
from src.auth.logging import get_recent_logs
from src.auth.config import PermissionLevel


def render_admin_dashboard():
    """Render the Admin Dashboard."""
    st.title("🛡️ Admin Dashboard")

    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["User Info", "Entra ID Metrics", "Auth Logs"])

    with tab1:
        st.header("Current User Information")

        claims = extract_user_claims()
        if claims:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Identity Claims")
                st.json(
                    {
                        "Name": claims.name,
                        "Email": claims.email,
                        "OID": claims.oid,
                        "Tenant ID": claims.tenant_id,
                        "Preferred Username": claims.preferred_username,
                    }
                )

            with col2:
                st.subheader("Raw st.user Object")
                # Display raw st.user to verify if 'groups' claim is present
                try:
                    st.json(dict(st.user))
                except Exception:
                    st.warning("Could not access raw st.user")
        else:
            st.error("No user claims found.")

    with tab2:
        st.header("Entra ID & Permissions")

        # Get current permission details
        permission_data = st.session_state.get(SESSION_PERMISSION_KEY)

        if permission_data:
            user_perm = UserPermission.from_dict(permission_data)

            with st.container(border=True):
                st.subheader("Assigned Permission")
                st.info(f"Level: **{user_perm.permission_level.name}**")

            st.subheader("Group Memberships")
            if user_perm.group_oids:
                st.write(f"User belongs to {len(user_perm.group_oids)} groups:")

                # Convert to DataFrame for better display
                df_groups = pd.DataFrame(user_perm.group_oids, columns=["Group OID"])
                # Use data_editor for better interactivity (copy/paste support)
                st.data_editor(
                    df_groups,
                    use_container_width=True,
                    disabled=True,
                    hide_index=True,
                    column_config={
                        "Group OID": st.column_config.TextColumn(
                            "Group Object ID",
                            help="The unique identifier for the group in Entra ID",
                        )
                    },
                )
            else:
                st.warning("No group memberships found for this user.")
        else:
            st.warning("Permission data not initialized.")

    with tab3:
        st.header("Authentication Logs")
        st.caption("Showing recent authentication events from memory buffer.")

        # Filter logs using st.pills (New in Streamlit 1.40+)
        log_filter = st.pills(
            "Filter by Level", ["ALL", "INFO", "WARNING", "ERROR"], default="ALL"
        )

        logs = get_recent_logs(100)

        if logs:
            filtered_logs = logs
            if log_filter != "ALL":
                filtered_logs = [log for log in logs if log_filter in log]

            if filtered_logs:
                # Display as a code block for readability
                st.code("\n".join(filtered_logs), language="text")
            else:
                st.info(f"No logs found for level: {log_filter}")
        else:
            st.info("No logs available.")
