"""
Microsoft Graph API client module.

Retrieves group memberships from Microsoft Graph API.
"""

from typing import List, Optional
import logging
import httpx


logger = logging.getLogger("auth.graph_client")


class GraphAPIError(Exception):
    """Exception raised for Graph API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class TokenAcquisitionError(GraphAPIError):
    """Exception raised when token acquisition fails."""
    pass


class GroupRetrievalError(GraphAPIError):
    """Exception raised when group retrieval fails."""
    pass


class GraphAPIClient:
    """Client for Microsoft Graph API."""
    
    GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"
    TOKEN_URL_TEMPLATE = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    
    def __init__(self, client_id: str, client_secret: str, tenant_id: str):
        """
        Initialize the Graph API client with client credentials.
        
        Args:
            client_id: The Entra ID application client ID
            client_secret: The Entra ID application client secret
            tenant_id: The Entra ID tenant ID
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self._access_token: Optional[str] = None
    
    async def get_user_groups(self, user_oid: str) -> List[str]:
        """
        Get group OIDs for a user.
        
        Args:
            user_oid: The user's Object ID
            
        Returns:
            List of group OIDs the user belongs to
            
        Raises:
            GroupRetrievalError: If API call fails
        """
        try:
            token = await self._get_access_token()
        except TokenAcquisitionError:
            raise GroupRetrievalError(
                "Failed to retrieve groups: unable to acquire access token"
            )
        
        url = f"{self.GRAPH_BASE_URL}/users/{user_oid}/memberOf"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                
                if response.status_code == 404:
                    logger.warning(f"User not found in Graph API: {user_oid}")
                    return []
                
                if response.status_code == 401:
                    # Token may have expired, clear it and retry once
                    self._access_token = None
                    token = await self._get_access_token()
                    headers["Authorization"] = f"Bearer {token}"
                    response = await client.get(url, headers=headers)
                
                response.raise_for_status()
                
                data = response.json()
                group_oids = []
                
                for item in data.get("value", []):
                    if item.get("@odata.type") == "#microsoft.graph.group":
                        group_id = item.get("id")
                        if group_id:
                            group_oids.append(group_id)
                
                logger.debug(f"Retrieved {len(group_oids)} groups for user {user_oid}")
                return group_oids
                
        except httpx.HTTPStatusError as e:
            logger.error(f"Graph API HTTP error: {e.response.status_code}")
            raise GroupRetrievalError(
                f"Failed to retrieve groups: HTTP {e.response.status_code}",
                status_code=e.response.status_code
            )
        except httpx.RequestError as e:
            logger.error(f"Graph API request error: {str(e)}")
            raise GroupRetrievalError(f"Failed to retrieve groups: {str(e)}")
    
    async def _get_access_token(self) -> str:
        """
        Get access token using client credentials flow.
        
        Returns:
            Access token string
            
        Raises:
            TokenAcquisitionError: If token acquisition fails
        """
        if self._access_token:
            return self._access_token
        
        url = self.TOKEN_URL_TEMPLATE.format(tenant_id=self.tenant_id)
        
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials",
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data)
                
                if response.status_code != 200:
                    error_data = response.json() if response.content else {}
                    error_desc = error_data.get("error_description", "Unknown error")
                    logger.error(f"Token acquisition failed: {error_desc}")
                    raise TokenAcquisitionError(
                        f"Failed to acquire token: {error_desc}",
                        status_code=response.status_code
                    )
                
                token_data = response.json()
                self._access_token = token_data.get("access_token")
                
                if not self._access_token:
                    raise TokenAcquisitionError(
                        "Token response did not contain access_token"
                    )
                
                logger.debug("Successfully acquired Graph API access token")
                return self._access_token
                
        except httpx.RequestError as e:
            logger.error(f"Token request error: {str(e)}")
            raise TokenAcquisitionError(f"Failed to acquire token: {str(e)}")
    
    def clear_token_cache(self) -> None:
        """Clear the cached access token."""
        self._access_token = None
