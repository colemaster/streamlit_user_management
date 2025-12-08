"""
External API connectivity module.

Provides helpers for making authenticated requests to downstream APIs
using the current user's credentials (On-Behalf-Of flow or direct token reuse).
"""

import httpx
from typing import Optional
from src.auth.claims import extract_user_claims, UserClaims

def get_authenticated_client(base_url: Optional[str] = None, timeout: int = 10) -> httpx.Client:
    """
    Get an httpx.Client configured with the current user's auth token.

    This allows the application to call external APIs (e.g., a backend service)
    using the identity of the currently logged-in user.

    Args:
        base_url: Optional base URL for the client.
        timeout: Request timeout in seconds.

    Returns:
        httpx.Client: Configured client instance.
    
    Raises:
        ValueError: If no user is logged in or no access token is available.
    """
    claims = extract_user_claims()
    if not claims:
        raise ValueError("No user logged in.")
    
    headers = claims.get_auth_header()
    if not headers:
        # Note: Streamlit native auth usually provides an ID Token. 
        # Whether this ID token can be used as an Access Token depends on the 
        # target API's configuration (e.g. same audience).
        # If using MSAL flow, a proper access token is more likely available.
        raise ValueError("No access token found in user claims.")

    return httpx.Client(
        base_url=base_url or "",
        headers=headers,
        timeout=timeout
    )

def get_auth_headers_safe() -> dict:
    """
    Safely retrieve auth headers, returning empty dict if not available.
    
    Useful for optional authentication scenarios.
    """
    claims = extract_user_claims()
    if claims:
        return claims.get_auth_header()
    return {}
