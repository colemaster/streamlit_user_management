"""
Unit tests for the Microsoft Graph API client module.

**Feature: entraid-authentication**

Tests cover:
- Token acquisition with mocked responses
- Group retrieval with mocked responses
- Error handling scenarios

_Requirements: 4.1_
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from src.auth.graph_client import (
    GraphAPIClient,
    GraphAPIError,
    TokenAcquisitionError,
    GroupRetrievalError,
)



@pytest.mark.asyncio(loop_scope="class")
class TestTokenAcquisition:
    """Tests for token acquisition using client credentials flow."""

    async def test_successful_token_acquisition(self):
        """Token acquisition should return access token on successful response."""
        client = GraphAPIClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
        )
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "test-access-token"}
        
        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance
            
            token = await client._get_access_token()
            
            assert token == "test-access-token"
            assert client._access_token == "test-access-token"
            
            # Verify correct URL was called
            call_args = mock_client_instance.post.call_args
            expected_url = "https://login.microsoftonline.com/test-tenant-id/oauth2/v2.0/token"
            assert call_args[0][0] == expected_url

    async def test_token_caching(self):
        """Subsequent calls should return cached token without making API call."""
        client = GraphAPIClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
        )
        
        # Pre-set the cached token
        client._access_token = "cached-token"
        
        with patch("httpx.AsyncClient") as mock_async_client:
            token = await client._get_access_token()
            
            assert token == "cached-token"
            # Should not have made any HTTP calls
            mock_async_client.assert_not_called()

    async def test_token_acquisition_failure_invalid_credentials(self):
        """Token acquisition should raise TokenAcquisitionError on 401 response."""
        client = GraphAPIClient(
            client_id="invalid-client-id",
            client_secret="invalid-secret",
            tenant_id="test-tenant-id",
        )
        
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.content = b'{"error": "invalid_client", "error_description": "Invalid client credentials"}'
        mock_response.json.return_value = {
            "error": "invalid_client",
            "error_description": "Invalid client credentials"
        }
        
        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance
            
            with pytest.raises(TokenAcquisitionError) as exc_info:
                await client._get_access_token()
            
            assert "Invalid client credentials" in str(exc_info.value)
            assert exc_info.value.status_code == 401

    async def test_token_acquisition_failure_missing_token_in_response(self):
        """Token acquisition should raise error when response lacks access_token."""
        client = GraphAPIClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
        )
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"token_type": "Bearer"}  # Missing access_token
        
        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance
            
            with pytest.raises(TokenAcquisitionError) as exc_info:
                await client._get_access_token()
            
            assert "access_token" in str(exc_info.value)

    async def test_token_acquisition_network_error(self):
        """Token acquisition should raise TokenAcquisitionError on network failure."""
        client = GraphAPIClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
        )
        
        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.post.side_effect = httpx.RequestError("Connection failed")
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance
            
            with pytest.raises(TokenAcquisitionError) as exc_info:
                await client._get_access_token()
            
            assert "Connection failed" in str(exc_info.value)


@pytest.mark.asyncio(loop_scope="class")
class TestGroupRetrieval:
    """Tests for retrieving user group memberships."""

    async def test_successful_group_retrieval(self):
        """Group retrieval should return list of group OIDs."""
        client = GraphAPIClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
        )
        client._access_token = "test-token"
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "value": [
                {"@odata.type": "#microsoft.graph.group", "id": "group-1"},
                {"@odata.type": "#microsoft.graph.group", "id": "group-2"},
                {"@odata.type": "#microsoft.graph.directoryRole", "id": "role-1"},  # Should be filtered out
            ]
        }
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance
            
            groups = await client.get_user_groups("user-oid-123")
            
            assert groups == ["group-1", "group-2"]
            
            # Verify correct URL was called
            call_args = mock_client_instance.get.call_args
            expected_url = "https://graph.microsoft.com/v1.0/users/user-oid-123/memberOf"
            assert call_args[0][0] == expected_url

    async def test_group_retrieval_empty_groups(self):
        """Group retrieval should return empty list when user has no groups."""
        client = GraphAPIClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
        )
        client._access_token = "test-token"
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"value": []}
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance
            
            groups = await client.get_user_groups("user-oid-123")
            
            assert groups == []

    async def test_group_retrieval_user_not_found(self):
        """Group retrieval should return empty list when user is not found (404)."""
        client = GraphAPIClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
        )
        client._access_token = "test-token"
        
        mock_response = MagicMock()
        mock_response.status_code = 404
        
        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance
            
            groups = await client.get_user_groups("nonexistent-user")
            
            assert groups == []

    async def test_group_retrieval_token_refresh_on_401(self):
        """Group retrieval should refresh token and retry on 401 response."""
        client = GraphAPIClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
        )
        client._access_token = "expired-token"
        
        # First response is 401, second is success
        mock_401_response = MagicMock()
        mock_401_response.status_code = 401
        
        mock_success_response = MagicMock()
        mock_success_response.status_code = 200
        mock_success_response.json.return_value = {
            "value": [{"@odata.type": "#microsoft.graph.group", "id": "group-1"}]
        }
        mock_success_response.raise_for_status = MagicMock()
        
        # Token refresh response
        mock_token_response = MagicMock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "new-token"}
        
        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.side_effect = [mock_401_response, mock_success_response]
            mock_client_instance.post.return_value = mock_token_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance
            
            groups = await client.get_user_groups("user-oid-123")
            
            assert groups == ["group-1"]
            # Verify token was refreshed (post was called for token)
            assert mock_client_instance.post.called

    async def test_group_retrieval_http_error(self):
        """Group retrieval should raise GroupRetrievalError on HTTP error."""
        client = GraphAPIClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
        )
        client._access_token = "test-token"
        
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server Error",
            request=MagicMock(),
            response=MagicMock(status_code=500)
        )
        
        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.return_value = mock_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance
            
            with pytest.raises(GroupRetrievalError) as exc_info:
                await client.get_user_groups("user-oid-123")
            
            assert exc_info.value.status_code == 500

    async def test_group_retrieval_network_error(self):
        """Group retrieval should raise GroupRetrievalError on network failure."""
        client = GraphAPIClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
        )
        client._access_token = "test-token"
        
        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.side_effect = httpx.RequestError("Network unreachable")
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance
            
            with pytest.raises(GroupRetrievalError) as exc_info:
                await client.get_user_groups("user-oid-123")
            
            assert "Network unreachable" in str(exc_info.value)

    async def test_group_retrieval_token_acquisition_failure(self):
        """Group retrieval should raise GroupRetrievalError when token acquisition fails."""
        client = GraphAPIClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
        )
        # No cached token, so it will try to acquire one
        
        mock_token_response = MagicMock()
        mock_token_response.status_code = 401
        mock_token_response.content = b'{"error": "invalid_client"}'
        mock_token_response.json.return_value = {"error_description": "Invalid client"}
        
        with patch("httpx.AsyncClient") as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.post.return_value = mock_token_response
            mock_async_client.return_value.__aenter__.return_value = mock_client_instance
            
            with pytest.raises(GroupRetrievalError) as exc_info:
                await client.get_user_groups("user-oid-123")
            
            assert "unable to acquire access token" in str(exc_info.value)


class TestTokenCacheManagement:
    """Tests for token cache management."""

    def test_clear_token_cache(self):
        """clear_token_cache should remove the cached token."""
        client = GraphAPIClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
        )
        client._access_token = "cached-token"
        
        client.clear_token_cache()
        
        assert client._access_token is None

    def test_initial_token_is_none(self):
        """New client should have no cached token."""
        client = GraphAPIClient(
            client_id="test-client-id",
            client_secret="test-client-secret",
            tenant_id="test-tenant-id",
        )
        
        assert client._access_token is None


class TestClientInitialization:
    """Tests for client initialization."""

    def test_client_stores_credentials(self):
        """Client should store provided credentials."""
        client = GraphAPIClient(
            client_id="my-client-id",
            client_secret="my-client-secret",
            tenant_id="my-tenant-id",
        )
        
        assert client.client_id == "my-client-id"
        assert client.client_secret == "my-client-secret"
        assert client.tenant_id == "my-tenant-id"

    def test_client_constants(self):
        """Client should have correct API constants."""
        assert GraphAPIClient.GRAPH_BASE_URL == "https://graph.microsoft.com/v1.0"
        assert "{tenant_id}" in GraphAPIClient.TOKEN_URL_TEMPLATE
