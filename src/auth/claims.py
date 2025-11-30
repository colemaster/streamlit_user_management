"""
User claims extraction module.

Extracts and validates user claims from st.user.
"""

from dataclasses import dataclass
from typing import Optional
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

    @classmethod
    def from_st_user(cls, st_user: dict) -> "UserClaims":
        """
        Extract claims from st.user dict.

        Streamlit's native auth populates st.user with claims from the ID Token.
        We extract the standard OIDC claims here.

        Args:
            st_user: Dictionary containing user claims from Streamlit

        Returns:
            UserClaims instance with extracted values
        """
        return cls(
            oid=st_user.get("oid", ""),  # Object ID (Unique User ID)
            email=st_user.get("email", ""),
            name=st_user.get("name", ""),
            preferred_username=st_user.get("preferred_username", ""),
            tenant_id=st_user.get("tid", ""),  # Tenant ID
            exp=st_user.get("exp"),  # Expiration Timestamp
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


def check_login_status() -> bool:
    """
    Verify user is logged in before accessing claims.

    Returns:
        True if user is logged in, False otherwise
    """
    try:
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

    try:
        import streamlit as st

        return UserClaims.from_st_user(dict(st.user))
    except Exception:
        return None
