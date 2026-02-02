"""
Enhanced Authentication Handler for Streamlit Nightly 2026.

Integrates new st.logout functionality with existing MSAL authentication
to ensure secure session termination with OIDC provider.
"""

import streamlit as st
import msal
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from src.auth.config import load_auth_config, AuthConfig, PermissionLevel
from src.auth.claims import extract_user_claims, UserClaims
from src.auth.permissions import (
    PermissionService,
    UserPermission,
    SESSION_PERMISSION_KEY,
)
from src.auth.graph_client import GraphAPIClient
from src.auth.logging import log_auth_event, log_auth_failure, log_logout, log_access_denied


class EnhancedAuthHandler:
    """
    Enhanced authentication handler that integrates new Streamlit nightly features
    with existing MSAL authentication system.
    """

    def __init__(self, config: Optional[AuthConfig] = None):
        """
        Initialize Enhanced Auth Handler.

        Args:
            config: Optional AuthConfig. If not provided, loads from secrets.
        """
        if config is None:
            self.config = load_auth_config()
        else:
            self.config = config

        self.msal_app = msal.ConfidentialClientApplication(
            self.config.client_id,
            authority=f"https://login.microsoftonline.com/{self.config.tenant_id}",
            client_credential=self.config.client_secret,
        )

        self.graph_client = GraphAPIClient(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            tenant_id=self.config.tenant_id,
        )
        self.permission_service = PermissionService(self.config, self.graph_client)

    def handle_streamlit_logout(self) -> None:
        """
        Handle logout using new st.logout functionality with OIDC provider integration.
        
        This method implements the enhanced logout flow that:
        1. Logs the logout event for audit purposes
        2. Clears all authentication-related session state
        3. Uses the new st.logout() to terminate session with OIDC provider
        4. Provides fallback error handling for logout failures
        """
        # Extract user information for logging
        claims = extract_user_claims()
        if claims:
            log_logout(claims.email)
            st.toast(f"Logging out {claims.name}...", icon="👋")
        else:
            st.toast("Logging out...", icon="👋")

        # Clear all authentication-related session state
        self._clear_authentication_state()

        try:
            # Enhanced st.logout() in Streamlit nightly 2026
            # This now logs users out of their identity provider if supported by OIDC setup
            st.logout()
        except Exception as e:
            # Fallback error handling
            log_auth_failure(f"Enhanced logout failed: {str(e)}")
            st.error("⚠️ Logout from identity provider failed. Clearing local session...")
            
            # Manual session clearing as fallback
            self._manual_session_cleanup()
            st.rerun()

    def _clear_authentication_state(self) -> None:
        """Clear all authentication-related session state."""
        auth_keys_to_clear = [
            # Streamlit native auth
            "access_token",
            "id_token", 
            "refresh_token",
            "token_expires_at",
            
            # MSAL specific
            "msal_account",
            "msal_token_cache",
            
            # Application specific
            "permissions_initialized",
            "user_groups",
            "auth_timestamp",
            SESSION_PERMISSION_KEY,
            
            # User claims cache
            "user_claims_cache",
            "claims_expiry",
        ]
        
        for key in auth_keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]

    def _manual_session_cleanup(self) -> None:
        """Manual session cleanup as fallback when st.logout() fails."""
        # Clear entire session state as last resort
        st.session_state.clear()
        
        # Log the fallback action
        log_auth_failure("Used manual session cleanup fallback")

    def maintain_session_security(self) -> bool:
        """
        Ensure secure session management with updated SDKs.
        
        Returns:
            True if session is secure and valid, False otherwise
        """
        # Check if user is logged in by checking if user info is available
        # In Streamlit nightly, st.user will be populated if user is authenticated
        user_info = dict(st.user) if st.user else {}
        if not user_info:
            return False

        # Validate token expiry
        claims = extract_user_claims()
        if claims and claims.is_expired():
            st.warning("⚠️ Session expired. Please sign in again.")
            self.handle_streamlit_logout()
            return False

        # Check for session timeout (optional additional security)
        auth_timestamp = st.session_state.get("auth_timestamp")
        if auth_timestamp:
            session_duration = datetime.now() - auth_timestamp
            # 8 hour session timeout
            if session_duration > timedelta(hours=8):
                st.warning("⚠️ Session timed out for security. Please sign in again.")
                self.handle_streamlit_logout()
                return False

        return True

    def integrate_with_dialogs(self) -> None:
        """
        Integrate auth flows with enhanced st.dialog functionality.
        
        Uses the new st.dialog with icon parameter for better modal interactions.
        """
        from src.ui.enhanced_dialogs import EnhancedDialogManager, MaterialSymbols
        
        # Enhanced logout confirmation dialog
        EnhancedDialogManager.confirmation_dialog(
            title="Confirm Logout",
            message="Are you sure you want to log out?\n\nThis will:\n- End your current session\n- Log you out from the identity provider\n- Clear all cached data",
            icon=MaterialSymbols.LOGOUT,
            confirm_text="Logout",
            cancel_text="Cancel",
            confirm_type="primary",
            on_confirm=self.handle_streamlit_logout,
            session_key="show_logout_confirmation"
        )
        
        # Session timeout warning dialog
        EnhancedDialogManager.info_dialog(
            title="Session Timeout Warning",
            content="⚠️ Your session will expire in 5 minutes due to inactivity.\n\nPlease save any unsaved work.",
            icon=MaterialSymbols.WARNING,
            session_key="show_session_timeout_warning"
        )
        
        # Authentication error dialog
        EnhancedDialogManager.info_dialog(
            title="Authentication Error",
            content="❌ Authentication failed. Please try signing in again.\n\nIf the problem persists, contact your administrator.",
            icon=MaterialSymbols.ERROR,
            session_key="show_auth_error_dialog"
        )

    def secure_logout_with_confirmation(self) -> None:
        """
        Initiate secure logout with user confirmation dialog.
        
        This provides an additional layer of security by confirming logout intent.
        """
        st.session_state["show_logout_confirmation"] = True
        self.integrate_with_dialogs()

    def get_logout_status(self) -> Dict[str, Any]:
        """
        Get current logout/session status for monitoring.
        
        Returns:
            Dictionary containing session and logout status information
        """
        claims = extract_user_claims()
        user_info = dict(st.user) if st.user else {}
        
        return {
            "is_logged_in": bool(user_info),
            "user_email": claims.email if claims else None,
            "session_valid": self.maintain_session_security(),
            "auth_timestamp": st.session_state.get("auth_timestamp"),
            "permissions_initialized": st.session_state.get("permissions_initialized", False),
            "streamlit_nightly_features": {
                "enhanced_logout": True,
                "oidc_provider_logout": True,
                "dialog_with_icons": True,
            }
        }

    async def initialize_enhanced_session(self) -> Optional[UserPermission]:
        """
        Initialize user session with enhanced security features.
        
        Returns:
            UserPermission if successful, None otherwise
        """
        claims = extract_user_claims()
        if not claims:
            return None

        # Set authentication timestamp for session timeout tracking
        st.session_state["auth_timestamp"] = datetime.now()

        # Initialize permissions using existing service
        permission = await self.permission_service.determine_user_permission(claims.oid)
        
        if permission:
            self.permission_service.cache_permission(permission)
            log_auth_event(claims.email, claims.oid, permission.permission_level)
            st.session_state["permissions_initialized"] = True

        return permission