"""
Authentication configuration module.

Manages Entra ID authentication configuration loaded from Streamlit secrets.
"""

from dataclasses import dataclass, field
from typing import Dict
from enum import IntEnum
import streamlit as st


class PermissionLevel(IntEnum):
    """Application permission levels ordered by privilege."""
    VIEWER = 1
    ANALYST = 2
    ADMIN = 3


class ConfigurationError(Exception):
    """Raised when authentication configuration is invalid or missing."""
    pass


@dataclass
class AuthConfig:
    """Authentication configuration from secrets.toml."""
    client_id: str
    client_secret: str
    tenant_id: str
    redirect_uri: str
    cookie_secret: str
    server_metadata_url: str
    group_mappings: Dict[str, PermissionLevel] = field(default_factory=dict)
    
    @classmethod
    def from_secrets(cls, secrets: dict) -> 'AuthConfig':
        """
        Load configuration from Streamlit secrets dict.
        
        Args:
            secrets: Dictionary containing auth configuration (typically st.secrets["auth"])
            
        Returns:
            AuthConfig instance with all fields populated
            
        Raises:
            ConfigurationError: If required fields are missing
        """
        auth_section = secrets.get("auth", secrets)
        
        # Extract required fields
        client_id = auth_section.get("client_id")
        client_secret = auth_section.get("client_secret")
        tenant_id = auth_section.get("tenant_id")
        redirect_uri = auth_section.get("redirect_uri")
        cookie_secret = auth_section.get("cookie_secret")
        server_metadata_url = auth_section.get("server_metadata_url")
        
        # Parse group mappings
        group_mappings_raw = auth_section.get("group_mappings", {})
        group_mappings = {}
        
        permission_map = {
            "viewer": PermissionLevel.VIEWER,
            "analyst": PermissionLevel.ANALYST,
            "admin": PermissionLevel.ADMIN,
        }
        
        for oid, level_str in group_mappings_raw.items():
            level_str_lower = str(level_str).lower()
            if level_str_lower in permission_map:
                group_mappings[oid] = permission_map[level_str_lower]
            elif isinstance(level_str, int) and level_str in [1, 2, 3]:
                group_mappings[oid] = PermissionLevel(level_str)
        
        config = cls(
            client_id=client_id or "",
            client_secret=client_secret or "",
            tenant_id=tenant_id or "",
            redirect_uri=redirect_uri or "",
            cookie_secret=cookie_secret or "",
            server_metadata_url=server_metadata_url or "",
            group_mappings=group_mappings,
        )
        
        return config
    
    def validate(self) -> None:
        """
        Validate all required configuration is present.
        
        Raises:
            ConfigurationError: If any required field is missing or empty
        """
        required_fields = [
            ("client_id", self.client_id),
            ("client_secret", self.client_secret),
            ("tenant_id", self.tenant_id),
            ("redirect_uri", self.redirect_uri),
            ("cookie_secret", self.cookie_secret),
            ("server_metadata_url", self.server_metadata_url),
        ]
        
        missing = [name for name, value in required_fields if not value]
        
        if missing:
            raise ConfigurationError(
                f"Missing required authentication configuration: {', '.join(missing)}"
            )


def build_metadata_url(tenant_id: str) -> str:
    """
    Build the OIDC metadata URL for a tenant.
    
    Args:
        tenant_id: The Entra ID tenant ID (GUID)
        
    Returns:
        The full OIDC metadata URL
    """
    return f"https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration"


def load_auth_config() -> AuthConfig:
    """
    Load and validate authentication configuration from Streamlit secrets
    with session-scoped caching.
    
    Uses Streamlit nightly 2026 session-scoped caching to avoid
    repeated configuration loading within the same session.
    
    Returns:
        Validated AuthConfig instance
        
    Raises:
        ConfigurationError: If configuration is missing or invalid
    """
    return _load_auth_config_cached()


@st.cache_data(scope="session", ttl=3600, show_spinner="Loading auth configuration...")
def _load_auth_config_cached() -> AuthConfig:
    """Internal cached implementation of auth config loading."""
    try:
        import streamlit as st
        config = AuthConfig.from_secrets(dict(st.secrets))
        config.validate()
        return config
    except Exception as e:
        if isinstance(e, ConfigurationError):
            raise
        raise ConfigurationError(f"Failed to load authentication configuration: {e}")


@st.cache_data(scope="session", ttl=1800, show_spinner="Loading group mappings...")
def get_group_mappings() -> Dict[str, PermissionLevel]:
    """
    Get group to permission mappings with session-scoped caching.
    
    Returns:
        Dictionary mapping group OIDs to permission levels
    """
    config = load_auth_config()
    return config.group_mappings


def clear_auth_cache():
    """Clear all authentication-related caches."""
    _load_auth_config_cached.clear()
    get_group_mappings.clear()


def refresh_auth_configuration():
    """Refresh all authentication configuration from secrets."""
    clear_auth_cache()
    
    # Pre-load fresh configuration
    load_auth_config()
    get_group_mappings()
