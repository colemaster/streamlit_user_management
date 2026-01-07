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

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(
            "🔄 Refresh Access Token",
            use_container_width=True,
            help="Re-triggers OIDC login flow to refresh tokens",
        ):
            st.toast("Re-authenticating...", icon="🔒")
            st.login()

    with col2:
        data = {
            "Principal ID (OID)": claims.oid,
            "Tenant ID": claims.tenant_id,
            "Username": claims.preferred_username,
            "Issuer": claims.raw_claims.get("iss", "N/A")
            if claims.raw_claims
            else "N/A",
            "Authenticated via": "Native Streamlit OIDC",
        }
        for k, v in data.items():
            st.markdown(f"**{k}:** `{v}`")

    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Show Raw JWT Claims"):
        # Create tabs for better organization
        jwt_tab1, jwt_tab2, jwt_tab3 = st.tabs(
            ["🔍 Claims Viewer", "📋 Claims Summary", "ℹ️ Claims Guide"]
        )

        with jwt_tab1:
            st.json(claims.raw_claims)

        with jwt_tab2:
            # Display JWT claims in a more user-friendly format
            st.markdown("### JWT Claims Summary")

            # Basic user info
            if claims.raw_claims:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**👤 User Information**")
                    st.write(f"**Name:** `{claims.raw_claims.get('name', 'N/A')}`")
                    st.write(f"**Email:** `{claims.raw_claims.get('email', 'N/A')}`")
                    st.write(
                        f"**Username:** `{claims.raw_claims.get('preferred_username', 'N/A')}`"
                    )
                    st.write(
                        f"**Object ID (OID):** `{claims.raw_claims.get('oid', 'N/A')}`"
                    )

                with col2:
                    st.markdown("**🏢 Organization Info**")
                    st.write(f"**Tenant ID:** `{claims.raw_claims.get('tid', 'N/A')}`")
                    st.write(f"**Issuer:** `{claims.raw_claims.get('iss', 'N/A')}`")
                    st.write(f"**Audience:** `{claims.raw_claims.get('aud', 'N/A')}`")

                    # Show expiration info
                    exp_timestamp = claims.raw_claims.get("exp")
                    if exp_timestamp:
                        from datetime import datetime

                        exp_datetime = datetime.fromtimestamp(exp_timestamp)
                        is_expired = exp_datetime < datetime.now()
                        status = "❌ Expired" if is_expired else "✅ Valid"
                        st.write(
                            f"**Expiration:** `{exp_datetime.strftime('%Y-%m-%d %H:%M:%S')} UTC` ({status})"
                        )

                # Raw Tokens (Nightly Feature)
                if claims.access_token:
                    st.markdown("**🎫 Raw Tokens**")
                    with st.expander("Show Access Token"):
                        st.code(claims.access_token, wrap_lines=True)
                        st.caption(
                            "⚠️ Never share this token. It allows acting on your behalf."
                        )

                # Additional claims
                st.markdown("**🔑 Additional Claims**")
                additional_claims = {
                    k: v
                    for k, v in claims.raw_claims.items()
                    if k
                    not in [
                        "name",
                        "email",
                        "preferred_username",
                        "oid",
                        "tid",
                        "iss",
                        "aud",
                        "exp",
                    ]
                }

                if additional_claims:
                    for key, value in additional_claims.items():
                        if key == "groups" and isinstance(value, list):
                            st.write(f"**{key}:**")
                            for group in value[
                                :5
                            ]:  # Limit to first 5 groups to avoid long lists
                                st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;• `{group}`")
                            if len(value) > 5:
                                st.write(
                                    f"&nbsp;&nbsp;&nbsp;&nbsp;... and {len(value) - 5} more"
                                )
                        elif key == "roles" and isinstance(value, list):
                            st.write(f"**{key}:** `{', '.join(value)}`")
                        else:
                            st.write(f"**{key}:** `{value}`")
                else:
                    st.info("No additional claims found")

        with jwt_tab3:
            st.markdown("""
            ### JWT Claims Guide

            A JWT (JSON Web Token) contains the following standard claims:

            | Claim | Description | Example |
            |-------|-------------|---------|
            | **`aud`** | Audience - the intended recipient of the token | `api://client-id` |
            | **`iss`** | Issuer - who issued the token | `https://sts.windows.net/tenant-id/` |
            | **`sub`** | Subject - identifier for the user | `12345678-1234-1234-1234-123456789abc` |
            | **`oid`** | Object ID - unique user identifier in Entra ID | `12345678-1234-1234-1234-123456789abc` |
            | **`tid`** | Tenant ID - organization identifier | `881dcd49-53e3-4f7d-8a74-0a4d2b936183` |
            | **`name`** | Display name of the user | `John Doe` |
            | **`email`** | Email address of the user | `john.doe@example.com` |
            | **`preferred_username`** | Username for display | `john.doe@example.com` |
            | **`exp`** | Expiration time (Unix timestamp) | `1700003599` |
            | **`nbf`** | Not before time (Unix timestamp) | `1699999999` |
            | **`iat`** | Issued at time (Unix timestamp) | `1699999999` |
            | **`groups`** | List of group OIDs user belongs to | `["group-oid-1", "group-oid-2"]` |
            | **`roles`** | Application roles assigned to user | `["Admin", "User"]` |
            | **`ver`** | Version of the token | `1.0` or `2.0` |

            **Security Note:** The `exp` field indicates when the token expires. Tokens should have a reasonable lifetime to balance security and usability.
            """)


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
        errs = len([log_entry for log_entry in logs if "ERROR" in log_entry])
        render_metric_card(
            "Errors",
            str(errs),
            "Low" if errs < 5 else "High",
            "success" if errs == 0 else "error",
        )
    with col3:
        warns = len([log_entry for log_entry in logs if "WARNING" in log_entry])
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
