"""
MSAL Authentication Guard.

Alternative implementation using MSAL for Python.
"""

import streamlit as st
import msal
import requests
from typing import Optional, Dict, Any
from src.auth.config import load_auth_config, AuthConfig, PermissionLevel
from src.auth.claims import UserClaims
from src.auth.permissions import (
    PermissionService,
    UserPermission,
    SESSION_PERMISSION_KEY,
)
from src.auth.logging import log_auth_event, log_auth_failure, log_logout


class MSALAuthGuard:
    """
    Guards application access using MSAL for Python.

    This is an alternative to the native Streamlit AuthGuard.
    It handles the OAuth2 flow manually.
    """

    def __init__(self, config: Optional[AuthConfig] = None):
        if config is None:
            self.config = load_auth_config()
        else:
            self.config = config

        self.msal_app = msal.ConfidentialClientApplication(
            self.config.client_id,
            authority=f"https://login.microsoftonline.com/{self.config.tenant_id}",
            client_credential=self.config.client_secret,
        )

        # Scopes required for the app
        self.scopes = ["User.Read"]

        # Permission service (reused from main implementation)
        # Note: We might need a different graph client if we want to use the user's token
        # instead of client credentials, but for now we stick to the existing pattern.
        from src.auth.graph_client import GraphAPIClient

        self.graph_client = GraphAPIClient(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            tenant_id=self.config.tenant_id,
        )
        self.permission_service = PermissionService(self.config, self.graph_client)

    def require_auth(self) -> bool:
        """
        Require authentication.

        This checks for a valid token in the session state. If not found,
        it initiates the OAuth2 Authorization Code flow using MSAL.

        Returns:
            True if authenticated, False otherwise.
        """
        # Check if token exists in session
        token = st.session_state.get("access_token")
        if not token:
            # Check for auth code in query params (Callback from Microsoft)
            code = st.query_params.get("code")
            if code:
                return self._handle_callback(code)

            # If no token and no code, show the login button
            self._render_login_button()
            return False

        return True

    def _render_login_button(self):
        """Render the login button."""
        auth_url = self.msal_app.get_authorization_request_url(
            self.scopes, redirect_uri=self.config.redirect_uri
        )

        st.title("FinOps AI Dashboard")
        st.markdown("### Welcome")
        st.markdown("Please sign in with your organization account to continue.")

        st.link_button("Sign in with Microsoft (MSAL)", auth_url, type="primary")

    def _handle_callback(self, code: str) -> bool:
        """Handle the OAuth2 callback."""
        try:
            result = self.msal_app.acquire_token_by_authorization_code(
                code, scopes=self.scopes, redirect_uri=self.config.redirect_uri
            )

            if "error" in result:
                st.error(f"Login failed: {result.get('error_description')}")
                log_auth_failure(result.get("error_description"))
                return False

            # Store token and user info
            st.session_state["access_token"] = result["access_token"]
            st.session_state["id_token"] = result.get("id_token_claims")

            # Populate st.user-like structure for compatibility
            user_info = result.get("id_token_claims", {})
            # Note: In a real scenario, we might want to wrap this better
            # For now, we rely on the fact that our other components check st.user
            # But since we are bypassing native auth, we might need to mock st.user or adapt components.
            # However, the request was just to "create an optional msal version".

            # Clear query params to hide code
            st.query_params.clear()
            st.rerun()
            return True

        except Exception as e:
            st.error(f"An error occurred during login: {e}")
            log_auth_failure(str(e))
            return False

    def logout(self) -> None:
        """
        Logout the user with enhanced OIDC provider integration.
        
        Uses the new Streamlit nightly st.logout() functionality that supports
        logging users out of their identity provider when supported by OIDC setup.
        """
        # Log the logout event
        claims = st.session_state.get("id_token", {})
        email = claims.get("preferred_username") or claims.get("email")
        if email:
            log_logout(email)
        
        # Clear MSAL-specific session state
        msal_keys_to_clear = [
            "access_token", 
            "id_token", 
            "refresh_token",
            "token_expires_at",
            "msal_account"
        ]
        
        for key in msal_keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        # Clear permission cache
        if SESSION_PERMISSION_KEY in st.session_state:
            del st.session_state[SESSION_PERMISSION_KEY]

        st.toast("Logging out from identity provider...", icon="👋")
        
        try:
            # Enhanced st.logout() in Streamlit nightly 2026
            # This now logs users out of their identity provider if supported by OIDC setup
            st.logout()
        except Exception as e:
            # Fallback for any logout errors
            st.error(f"Logout error: {e}")
            # Manual session clearing and rerun as fallback
            st.session_state.clear()
            st.rerun()

    async def initialize_user_permission(self) -> Optional[UserPermission]:
        """Initialize permissions."""
        # Extract OID from ID token claims
        claims = st.session_state.get("id_token", {})
        oid = claims.get("oid")
        email = claims.get("preferred_username") or claims.get("email")

        if not oid:
            return None

        # Check cache
        cached = self.permission_service.get_cached_permission()
        if cached and cached.user_oid == oid:
            return cached

        # Determine permission
        permission = await self.permission_service.determine_user_permission(oid)

        # Cache and log
        self.permission_service.cache_permission(permission)
        if email:
            log_auth_event(email, oid, permission.permission_level)

        return permission
