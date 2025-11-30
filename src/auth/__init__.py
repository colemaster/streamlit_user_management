"""
Entra ID Authentication Module for FinOps AI Dashboard.

This module provides Microsoft Entra ID (Azure AD) authentication using
Streamlit's native OIDC features (st.login, st.logout, st.user).
"""

from src.auth.config import PermissionLevel, AuthConfig, load_auth_config, build_metadata_url
from src.auth.claims import UserClaims, extract_user_claims, check_login_status
from src.auth.permissions import UserPermission, PermissionService, has_permission, get_current_permission
from src.auth.guard import AuthGuard
from src.auth.logging import log_auth_event, log_auth_failure, log_logout, log_access_denied
from src.auth.graph_client import GraphAPIClient, GraphAPIError, TokenAcquisitionError, GroupRetrievalError

__all__ = [
    # Config
    "PermissionLevel",
    "AuthConfig",
    "load_auth_config",
    "build_metadata_url",
    # Claims
    "UserClaims",
    "extract_user_claims",
    "check_login_status",
    # Permissions
    "UserPermission",
    "PermissionService",
    "has_permission",
    "get_current_permission",
    # Guard
    "AuthGuard",
    # Logging
    "log_auth_event",
    "log_auth_failure",
    "log_logout",
    "log_access_denied",
    # Graph API Client
    "GraphAPIClient",
    "GraphAPIError",
    "TokenAcquisitionError",
    "GroupRetrievalError",
]
