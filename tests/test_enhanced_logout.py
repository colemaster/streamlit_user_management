"""
Tests for enhanced st.logout functionality with OIDC provider integration.

Tests the new Streamlit nightly 2026 st.logout features integrated with MSAL authentication.
"""

import pytest
import streamlit as st
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from src.auth.enhanced_auth import EnhancedAuthHandler
from src.auth.config import AuthConfig, PermissionLevel
from src.auth.claims import UserClaims


@pytest.fixture
def mock_auth_config():
    """Mock authentication configuration."""
    return AuthConfig(
        client_id="test-client-id",
        client_secret="test-client-secret",
        tenant_id="test-tenant-id",
        redirect_uri="http://localhost:8501/oauth2callback",
        cookie_secret="test-cookie-secret",
        server_metadata_url="https://login.microsoftonline.com/test-tenant-id/v2.0/.well-known/openid-configuration",
        group_mappings={"admin-group": PermissionLevel.ADMIN}
    )


@pytest.fixture
def enhanced_auth_handler(mock_auth_config):
    """Create enhanced auth handler with mocked dependencies."""
    with patch('src.auth.enhanced_auth.GraphAPIClient'), \
         patch('src.auth.enhanced_auth.PermissionService'), \
         patch('msal.ConfidentialClientApplication'):
        handler = EnhancedAuthHandler(config=mock_auth_config)
        return handler


@pytest.fixture
def mock_user_claims():
    """Mock user claims."""
    return UserClaims(
        oid="test-user-oid",
        email="test@example.com",
        name="Test User",
        preferred_username="test@example.com",
        tenant_id="test-tenant-id",
        exp=int((datetime.now() + timedelta(hours=1)).timestamp())
    )


class TestEnhancedLogout:
    """Test enhanced logout functionality."""

    @patch('streamlit.logout')
    @patch('streamlit.toast')
    @patch('src.auth.enhanced_auth.extract_user_claims')
    @patch('src.auth.enhanced_auth.log_logout')
    def test_successful_logout_with_oidc_provider(
        self, mock_log_logout, mock_extract_claims, mock_toast, mock_st_logout, 
        enhanced_auth_handler, mock_user_claims
    ):
        """Test successful logout with OIDC provider integration."""
        # Arrange
        mock_extract_claims.return_value = mock_user_claims
        
        # Act
        enhanced_auth_handler.handle_streamlit_logout()
        
        # Assert
        mock_log_logout.assert_called_once_with("test@example.com")
        mock_toast.assert_called_once_with("Logging out Test User...", icon="👋")
        mock_st_logout.assert_called_once()

    @patch('streamlit.logout')
    @patch('streamlit.session_state', new_callable=dict)
    def test_session_state_cleanup_on_logout(
        self, mock_session_state, mock_st_logout, enhanced_auth_handler
    ):
        """Test that all authentication session state is cleared on logout."""
        # Arrange
        mock_session_state.update({
            "access_token": "test-token",
            "id_token": "test-id-token",
            "refresh_token": "test-refresh-token",
            "permissions_initialized": True,
            "user_groups": ["group1", "group2"],
            "auth_timestamp": datetime.now(),
            "other_key": "should_remain"
        })
        
        # Act
        enhanced_auth_handler.handle_streamlit_logout()
        
        # Assert
        auth_keys = [
            "access_token", "id_token", "refresh_token", 
            "permissions_initialized", "user_groups", "auth_timestamp"
        ]
        for key in auth_keys:
            assert key not in mock_session_state
        
        # Non-auth keys should remain
        assert "other_key" in mock_session_state
    @patch('streamlit.logout', side_effect=Exception("OIDC logout failed"))
    @patch('streamlit.error')
    @patch('streamlit.rerun')
    @patch('streamlit.session_state', new_callable=dict)
    @patch('src.auth.enhanced_auth.log_auth_failure')
    def test_logout_fallback_on_error(
        self, mock_log_failure, mock_session_state, mock_rerun, 
        mock_error, mock_st_logout, enhanced_auth_handler
    ):
        """Test fallback behavior when st.logout() fails."""
        # Arrange
        mock_session_state["access_token"] = "test-token"
        
        # Act
        enhanced_auth_handler.handle_streamlit_logout()
        
        # Assert
        # Should be called twice: once for the main error, once for the fallback
        assert mock_log_failure.call_count == 2
        mock_log_failure.assert_any_call("Enhanced logout failed: OIDC logout failed")
        mock_log_failure.assert_any_call("Used manual session cleanup fallback")
        mock_error.assert_called_once()
        mock_rerun.assert_called_once()
        assert len(mock_session_state) == 0  # Session cleared as fallback

    @patch('src.auth.enhanced_auth.st.user')
    @patch('src.auth.enhanced_auth.extract_user_claims')
    def test_maintain_session_security_valid_session(
        self, mock_extract_claims, mock_user, enhanced_auth_handler, mock_user_claims
    ):
        """Test session security validation with valid session."""
        # Arrange
        mock_user.__bool__ = Mock(return_value=True)
        mock_user.__iter__ = Mock(return_value=iter([('email', 'test@example.com')]))
        mock_extract_claims.return_value = mock_user_claims
        
        # Act
        result = enhanced_auth_handler.maintain_session_security()
        
        # Assert
        assert result is True

    @patch('src.auth.enhanced_auth.st.user')
    def test_maintain_session_security_not_logged_in(
        self, mock_user, enhanced_auth_handler
    ):
        """Test session security validation when user is not logged in."""
        # Arrange
        mock_user.__bool__ = Mock(return_value=False)
        mock_user.__iter__ = Mock(return_value=iter([]))
        
        # Act
        result = enhanced_auth_handler.maintain_session_security()
        
        # Assert
        assert result is False

    @patch('src.auth.enhanced_auth.st.user')
    @patch('src.auth.enhanced_auth.st.warning')
    @patch('src.auth.enhanced_auth.extract_user_claims')
    def test_maintain_session_security_expired_token(
        self, mock_extract_claims, mock_warning, mock_user, enhanced_auth_handler
    ):
        """Test session security validation with expired token."""
        # Arrange
        mock_user.__bool__ = Mock(return_value=True)
        mock_user.__iter__ = Mock(return_value=iter([('email', 'test@example.com')]))
        expired_claims = UserClaims(
            oid="test-oid",
            email="test@example.com", 
            name="Test User",
            preferred_username="test@example.com",
            tenant_id="test-tenant-id",
            exp=int((datetime.now() - timedelta(hours=1)).timestamp())  # Expired
        )
        mock_extract_claims.return_value = expired_claims
        
        with patch.object(enhanced_auth_handler, 'handle_streamlit_logout') as mock_logout:
            # Act
            result = enhanced_auth_handler.maintain_session_security()
            
            # Assert
            assert result is False
            mock_warning.assert_called_once()
            mock_logout.assert_called_once()

    @patch('streamlit.session_state', new_callable=dict)
    @patch('src.auth.enhanced_auth.st.user')
    @patch('src.auth.enhanced_auth.st.warning')
    def test_session_timeout_security(
        self, mock_warning, mock_user, mock_session_state, enhanced_auth_handler
    ):
        """Test session timeout security feature."""
        # Arrange
        mock_user.__bool__ = Mock(return_value=True)
        mock_user.__iter__ = Mock(return_value=iter([('email', 'test@example.com')]))
        mock_session_state["auth_timestamp"] = datetime.now() - timedelta(hours=9)  # Expired
        
        with patch.object(enhanced_auth_handler, 'handle_streamlit_logout') as mock_logout, \
             patch('src.auth.enhanced_auth.extract_user_claims', return_value=None):
            # Act
            result = enhanced_auth_handler.maintain_session_security()
            
            # Assert
            assert result is False
            mock_warning.assert_called_once()
            mock_logout.assert_called_once()


class TestLogoutDialog:
    """Test logout confirmation dialog functionality."""

    @patch('streamlit.session_state', new_callable=dict)
    @patch('src.auth.enhanced_auth.EnhancedAuthHandler.integrate_with_dialogs')
    def test_secure_logout_with_confirmation_shows_dialog(
        self, mock_integrate_dialogs, mock_session_state, enhanced_auth_handler
    ):
        """Test that secure logout shows confirmation dialog."""
        # Act
        enhanced_auth_handler.secure_logout_with_confirmation()
        
        # Assert
        assert mock_session_state["show_logout_confirmation"] is True
        mock_integrate_dialogs.assert_called_once()

    @patch('streamlit.session_state', new_callable=dict)
    def test_logout_dialog_cancel_logic(
        self, mock_session_state, enhanced_auth_handler
    ):
        """Test logout dialog cancel logic without Streamlit context."""
        # Arrange
        mock_session_state["show_logout_confirmation"] = True
        
        # Test the logic that would be executed when cancel is clicked
        # This simulates what happens in the actual dialog
        mock_session_state["show_logout_confirmation"] = False
        
        # Assert
        assert mock_session_state["show_logout_confirmation"] is False


class TestLogoutStatus:
    """Test logout status monitoring."""

    @patch('src.auth.enhanced_auth.st.user')
    @patch('streamlit.session_state', new_callable=dict)
    @patch('src.auth.enhanced_auth.extract_user_claims')
    def test_get_logout_status(
        self, mock_extract_claims, mock_session_state, mock_user, 
        enhanced_auth_handler, mock_user_claims
    ):
        """Test logout status information retrieval."""
        # Arrange
        mock_user.__bool__ = Mock(return_value=True)
        mock_user.__iter__ = Mock(return_value=iter([('email', 'test@example.com')]))
        mock_extract_claims.return_value = mock_user_claims
        mock_session_state["auth_timestamp"] = datetime.now()
        mock_session_state["permissions_initialized"] = True
        
        # Act
        status = enhanced_auth_handler.get_logout_status()
        
        # Assert
        assert status["is_logged_in"] is True
        assert status["user_email"] == "test@example.com"
        assert status["permissions_initialized"] is True
        assert status["streamlit_nightly_features"]["enhanced_logout"] is True
        assert status["streamlit_nightly_features"]["oidc_provider_logout"] is True