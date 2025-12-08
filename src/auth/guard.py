"""
Authentication guard module.

Main authentication flow controller.
"""

import streamlit as st
import os
from typing import Optional

from src.auth.config import (
    load_auth_config,
    PermissionLevel,
    AuthConfig,
)
from src.auth.claims import extract_user_claims, check_login_status
from src.auth.permissions import (
    PermissionService,
    UserPermission,
    has_permission,
    SESSION_PERMISSION_KEY,
)
from src.auth.graph_client import GraphAPIClient
from src.auth.logging import (
    log_auth_event,
    log_auth_failure,
    log_logout,
    log_access_denied,
)


class AuthGuard:
    """Guards application access with Entra ID authentication."""

    def __init__(self, config: Optional[AuthConfig] = None):
        """
        Initialize AuthGuard.

        Args:
            config: Optional AuthConfig. If not provided, loads from secrets.
        """
        if config is None:
            self.config = load_auth_config()
        else:
            self.config = config

        self.graph_client = GraphAPIClient(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            tenant_id=self.config.tenant_id,
        )
        self.permission_service = PermissionService(self.config, self.graph_client)

    def require_auth(self) -> bool:
        """
        Require authentication, show login if not authenticated.

        This is the main gatekeeper. It checks if the user is logged in via
        Streamlit's native authentication mechanism (st.user).

        Flow:
        1. Check if st.user is populated (user is logged in).
        2. If not, show the login page (which triggers st.login()).
        3. If logged in, validate that the token hasn't expired.

        Returns:
            True if user is authenticated, False otherwise
        """
        # 1. Check if Streamlit has populated st.user (Native Auth)
        # This happens automatically after a successful OAuth flow.
        if not check_login_status():
            # 2. If not, trigger the login flow (Redirect to Microsoft)
            self.render_login_page()
            return False

        # 3. Check for expired token
        # Even if st.user exists, the underlying token might be stale.
        claims = extract_user_claims()
        if claims and claims.is_expired():
            st.warning("Session expired. Please sign in again.")
            self.logout()
            self.render_login_page()
            return False

        return True

    def require_permission(self, level: PermissionLevel) -> bool:
        """
        Require specific permission level.

        Args:
            level: Required permission level

        Returns:
            True if user has required permission, False otherwise
        """
        if not self.require_auth():
            return False

        if not has_permission(level):
            claims = extract_user_claims()
            if claims:
                log_access_denied(claims.oid, "protected_feature", level)
            self.render_access_denied(level)
            return False

        return True

    def login(self) -> None:
        """Initiate login flow."""
        st.toast("Redirecting to Microsoft Login...", icon="🔒")
        st.login()

    def logout(self) -> None:
        """Logout and clear session."""
        claims = extract_user_claims()
        if claims:
            log_logout(claims.email)

        # Clear permission cache
        if SESSION_PERMISSION_KEY in st.session_state:
            del st.session_state[SESSION_PERMISSION_KEY]

        st.toast("Logging out...", icon="👋")
        st.logout()

    def render_login_page(self) -> None:
        """Render the login interface."""
        st.title("FinOps AI Dashboard")
        st.markdown("### Welcome")
        st.markdown("Please sign in with your organization account to continue.")

        st.info(
            "**Why sign in?**\n"
            "This application handles sensitive financial data. "
            "Authentication ensures you have the correct permissions to view cost reports and budgets."
        )

        if st.button("Sign in with Microsoft", type="primary"):
            self.login()

        log_auth_failure("User not logged in")

    def render_access_denied(self, required: PermissionLevel) -> None:
        """
        Render access denied message.

        Args:
            required: The permission level that was required
        """
        st.error(f"Access Denied: {required.name} role required")

        with st.container(border=True):
            st.markdown(
                f"""
                ### 🚧 Authorization Required
                You currently do not have the **{required.name}** permission level required to access this feature.
                
                **What can you do?**
                1. **Check your role:** Go to the Admin Dashboard to see your current permissions.
                2. **Request Access:** Contact the FinOps team or your IT administrator to request the `{required.name}` role for your account.
                """
            )

        if st.button("Return to Dashboard"):
            st.rerun()

    async def initialize_user_permission(self) -> Optional[UserPermission]:
        """
        Initialize user permission after successful authentication.

        Returns:
            UserPermission if successful, None otherwise
        """
        claims = extract_user_claims()
        if not claims:
            return None

        # Check if already cached
        cached = self.permission_service.get_cached_permission()
        if cached and cached.user_oid == claims.oid:
            return cached

        if os.getenv("NO_AUTH"):
            # Mock Admin Permission
            permission = UserPermission(
                user_oid=claims.oid,
                permission_level=PermissionLevel.ADMIN,
                group_oids=["mock-admin-group"],
            )
        else:
            # Determine permission from groups
            # This calls Microsoft Graph API to get the user's group memberships
            # and maps them to an application permission level (VIEWER, ANALYST, ADMIN)
            permission = await self.permission_service.determine_user_permission(
                claims.oid
            )

        # Cache and log
        self.permission_service.cache_permission(permission)
        log_auth_event(claims.email, claims.oid, permission.permission_level)

        return permission
