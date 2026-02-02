"""
Test authentication dependencies after SDK updates.

Tests MSAL, authlib, and python-jose functionality to ensure
compatibility with updated versions.
"""

import pytest
import msal
from jose import jwt
from authlib.jose import JsonWebSignature, JsonWebToken
from authlib.common.security import generate_token
from datetime import datetime, timedelta
import json


class TestMSALDependency:
    """Test MSAL functionality with updated version."""
    
    def test_msal_import_and_version(self):
        """Test that MSAL imports correctly and has expected version."""
        assert hasattr(msal, '__version__')
        # Ensure we have at least version 1.34.0
        version_parts = msal.__version__.split('.')
        major, minor = int(version_parts[0]), int(version_parts[1])
        assert major >= 1
        if major == 1:
            assert minor >= 34
    
    def test_msal_public_client_creation(self):
        """Test creating a PublicClientApplication."""
        app = msal.PublicClientApplication(
            client_id="test-client-id",
            authority="https://login.microsoftonline.com/common"
        )
        assert app is not None
        assert hasattr(app, 'get_accounts')
        assert hasattr(app, 'acquire_token_silent')
    
    def test_msal_confidential_client_creation(self):
        """Test creating a ConfidentialClientApplication."""
        app = msal.ConfidentialClientApplication(
            client_id="test-client-id",
            client_credential="test-secret",
            authority="https://login.microsoftonline.com/common"
        )
        assert app is not None
        assert hasattr(app, 'get_authorization_request_url')
        assert hasattr(app, 'acquire_token_by_authorization_code')
    
    def test_msal_token_cache(self):
        """Test MSAL token cache functionality."""
        cache = msal.SerializableTokenCache()
        assert cache is not None
        assert hasattr(cache, 'serialize')
        assert hasattr(cache, 'deserialize')
        
        # Test serialization
        serialized = cache.serialize()
        assert isinstance(serialized, (str, type(None)))


class TestAuthlibDependency:
    """Test authlib functionality with updated version."""
    
    def test_authlib_import_and_version(self):
        """Test that authlib imports correctly."""
        import authlib
        assert hasattr(authlib, '__version__')
        # Ensure we have at least version 1.6.6
        version_parts = authlib.__version__.split('.')
        major, minor, patch = int(version_parts[0]), int(version_parts[1]), int(version_parts[2])
        assert major >= 1
        if major == 1:
            assert minor >= 6
            if minor == 6:
                assert patch >= 6
    
    def test_authlib_jwt_creation(self):
        """Test JWT creation with authlib."""
        jwt_handler = JsonWebToken(['HS256'])
        
        header = {'alg': 'HS256'}
        payload = {
            'sub': 'test-user',
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow()
        }
        secret = 'test-secret-key'
        
        token = jwt_handler.encode(header, payload, secret)
        assert isinstance(token, bytes)
        
        # Decode and verify
        decoded = jwt_handler.decode(token, secret)
        assert decoded['sub'] == 'test-user'
    
    def test_authlib_jws_functionality(self):
        """Test JSON Web Signature functionality."""
        jws = JsonWebSignature()
        
        header = {'alg': 'HS256'}
        payload = b'test-payload'
        secret = 'test-secret'
        
        token = jws.serialize_compact(header, payload, secret)
        assert isinstance(token, bytes)
        
        # Verify signature
        data = jws.deserialize_compact(token, secret)
        assert data['payload'] == payload
    
    def test_authlib_token_generation(self):
        """Test secure token generation."""
        token = generate_token(32)
        assert isinstance(token, str)
        assert len(token) == 32  # generate_token returns string of specified length
        
        # Generate multiple tokens to ensure randomness
        tokens = [generate_token(16) for _ in range(10)]
        assert len(set(tokens)) == 10  # All should be unique


class TestPythonJoseDependency:
    """Test python-jose functionality with updated version."""
    
    def test_jose_import_and_version(self):
        """Test that python-jose imports correctly."""
        from jose import __version__
        assert __version__ is not None
        # Ensure we have at least version 3.5.0
        version_parts = __version__.split('.')
        major, minor = int(version_parts[0]), int(version_parts[1])
        assert major >= 3
        if major == 3:
            assert minor >= 5
    
    def test_jose_jwt_encode_decode(self):
        """Test JWT encoding and decoding with python-jose."""
        payload = {
            'sub': 'test-user',
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow(),
            'email': 'test@example.com'
        }
        secret = 'test-secret-key'
        
        # Encode
        token = jwt.encode(payload, secret, algorithm='HS256')
        assert isinstance(token, str)
        
        # Decode
        decoded = jwt.decode(token, secret, algorithms=['HS256'])
        assert decoded['sub'] == 'test-user'
        assert decoded['email'] == 'test@example.com'
    
    def test_jose_jwt_with_expiration(self):
        """Test JWT with expiration handling."""
        # Create expired token
        expired_payload = {
            'sub': 'test-user',
            'exp': datetime.utcnow() - timedelta(hours=1)  # Expired
        }
        secret = 'test-secret-key'
        
        token = jwt.encode(expired_payload, secret, algorithm='HS256')
        
        # Should raise exception when decoding expired token
        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(token, secret, algorithms=['HS256'])
    
    def test_jose_jwt_invalid_signature(self):
        """Test JWT with invalid signature."""
        payload = {'sub': 'test-user'}
        secret = 'test-secret-key'
        wrong_secret = 'wrong-secret-key'
        
        token = jwt.encode(payload, secret, algorithm='HS256')
        
        # Should raise exception with wrong secret
        with pytest.raises(jwt.JWTError):
            jwt.decode(token, wrong_secret, algorithms=['HS256'])


class TestAuthenticationIntegration:
    """Test integration between authentication dependencies."""
    
    def test_msal_with_jose_token_validation(self):
        """Test using python-jose to validate tokens in MSAL flow."""
        # Simulate a scenario where we validate ID tokens from MSAL using jose
        payload = {
            'aud': 'test-client-id',
            'iss': 'https://login.microsoftonline.com/test-tenant/v2.0',
            'sub': 'test-user-oid',
            'preferred_username': 'test@example.com',
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow()
        }
        
        # In real scenario, this would be the tenant's signing key
        secret = 'test-signing-key'
        
        # Create token (simulating what MSAL would return)
        token = jwt.encode(payload, secret, algorithm='HS256')
        
        # Validate token (what our app would do) - specify audience
        decoded = jwt.decode(token, secret, algorithms=['HS256'], audience='test-client-id')
        assert decoded['preferred_username'] == 'test@example.com'
        assert decoded['aud'] == 'test-client-id'
    
    def test_authlib_oauth_client_simulation(self):
        """Test authlib OAuth client functionality."""
        from authlib.integrations.requests_client import OAuth2Session
        
        # Create OAuth2 session (simulating what we might use with MSAL)
        client = OAuth2Session(
            client_id='test-client-id',
            redirect_uri='http://localhost:8501/callback'
        )
        
        assert client.client_id == 'test-client-id'
        assert client.redirect_uri == 'http://localhost:8501/callback'
        
        # Test authorization URL generation
        auth_url, state = client.create_authorization_url(
            'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
        )
        
        assert 'client_id=test-client-id' in auth_url
        assert 'redirect_uri=' in auth_url
        assert state is not None


class TestCompatibilityWithExistingCode:
    """Test that updated dependencies work with existing authentication code."""
    
    def test_msal_guard_compatibility(self):
        """Test that MSALAuthGuard can be instantiated with updated MSAL."""
        # Import the actual MSALAuthGuard class
        from src.auth.msal_guard import MSALAuthGuard
        from src.auth.config import AuthConfig
        from unittest.mock import patch
        
        # Create a test config with all required fields
        config = AuthConfig(
            client_id="test-client-id",
            client_secret="test-secret",
            tenant_id="common",  # Use 'common' to avoid tenant validation
            redirect_uri="http://localhost:8501/callback",
            cookie_secret="test-cookie-secret",
            server_metadata_url="https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration"
        )
        
        # Mock the MSAL app creation to avoid network calls
        with patch('msal.ConfidentialClientApplication') as mock_msal:
            mock_app = mock_msal.return_value
            mock_app.get_authorization_request_url.return_value = "https://test-auth-url"
            
            # This should work with updated MSAL
            guard = MSALAuthGuard(config)
            assert guard.msal_app is not None
            assert hasattr(guard.msal_app, 'get_authorization_request_url')
    
    def test_auth_service_compatibility(self):
        """Test that AuthService works with updated python-jose."""
        from src.ui.services import AuthService
        
        # Test token creation and decoding
        token = AuthService.create_token("test@example.com")
        assert isinstance(token, str)
        
        # Test token decoding
        decoded_email = AuthService.decode_token(token)
        assert decoded_email == "test@example.com"
    
    def test_external_auth_headers(self):
        """Test that external auth functionality works."""
        # This test would require a mock session state
        # For now, just test that the module imports correctly
        from src.auth.external import get_auth_headers_safe
        
        # Should return empty dict when no user is logged in
        headers = get_auth_headers_safe()
        assert isinstance(headers, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])