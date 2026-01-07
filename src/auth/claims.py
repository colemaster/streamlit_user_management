"""
User claims extraction module.

Extracts and validates user claims from st.user.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import os
from datetime import datetime


@dataclass
class UserClaims:
    """User identity claims from Entra ID."""

    oid: str  # User Object ID
    email: str
    name: str
    preferred_username: str
    tenant_id: str
    exp: Optional[int] = None  # Token expiration timestamp
    raw_claims: Dict[str, Any] = field(default_factory=dict)  # Full raw token data
    access_token: Optional[str] = None  # Raw Access Token (if available)

    @classmethod
    def from_st_user(cls, st_user: Any) -> "UserClaims":
        """
        Extract claims from st.user.

        Streamlit's native auth populates st.user with claims from the ID Token.
        In streamlit-nightly (and newer), st.user.tokens provides access to
        the raw ID and Access tokens if configured.

        Args:
            st_user: st.user object from Streamlit

        Returns:
            UserClaims instance with extracted values
        """
        # Dictionary-like access for claims
        claims_dict = dict(st_user) if hasattr(st_user, "items") else {}

        # Access tokens from st.user.tokens (new in nightly)
        tokens = getattr(st_user, "tokens", {})
        access_token = tokens.get("access") if hasattr(tokens, "get") else None

        return cls(
            oid=claims_dict.get("oid", ""),  # Object ID (Unique User ID)
            email=claims_dict.get("email", ""),
            name=claims_dict.get("name", ""),
            preferred_username=claims_dict.get("preferred_username", ""),
            tenant_id=claims_dict.get("tid", ""),  # Tenant ID
            exp=claims_dict.get("exp"),  # Expiration Timestamp
            raw_claims=claims_dict,  # Store the full raw dictionary
            access_token=access_token or claims_dict.get("access_token"),
        )

    def is_expired(self) -> bool:
        """
        Check if the token has expired.

        Returns:
            True if token is expired, False otherwise
        """
        if self.exp is None:
            return False
        return datetime.now().timestamp() >= self.exp

    def get_auth_header(self) -> Dict[str, str]:
        """
        Get Authorization header for external API calls.

        Returns:
            Dictionary with Authorization header if token exists, else empty dict.
        """
        if self.access_token:
            return {"Authorization": f"Bearer {self.access_token}"}
        return {}


def check_login_status() -> bool:
    """
    Verify user is logged in before accessing claims.

    Returns:
        True if user is logged in, False otherwise
    """
    try:
        if os.getenv("NO_AUTH"):
            return True

        import streamlit as st

        return getattr(st.user, "is_logged_in", False)
    except Exception:
        return False


def extract_user_claims() -> Optional[UserClaims]:
    """
    Extract claims from st.user if logged in.

    Returns:
        UserClaims if user is logged in, None otherwise
    """
    if not check_login_status():
        return None

    if os.getenv("NO_AUTH"):
        return UserClaims(
            oid="mock-admin-oid",
            email="admin@example.com",
            name="Test Admin (Mock)",
            preferred_username="admin@test.local",
            tenant_id="mock-tenant",
            exp=32503680000,  # Year 3000
        )

    try:
        import streamlit as st

        return UserClaims.from_st_user(dict(st.user))
    except Exception:
        return None
