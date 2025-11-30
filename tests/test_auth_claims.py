"""
Property-based tests for the user claims extraction module.

**Feature: entraid-authentication**
"""

import pytest
from hypothesis import given, strategies as st, settings, assume
from datetime import datetime
from unittest.mock import patch, MagicMock

from src.auth.claims import (
    UserClaims,
    check_login_status,
    extract_user_claims,
)


# Strategies for generating test data
uuid_strategy = st.uuids().map(str)
non_empty_string = st.text(min_size=1, max_size=100).filter(lambda x: x.strip())
email_strategy = st.emails()
timestamp_strategy = st.integers(min_value=0, max_value=2147483647)


def make_st_user_dict(
    oid: str,
    email: str,
    name: str,
    preferred_username: str,
    tid: str,
    exp: int = None,
    is_logged_in: bool = True,
) -> dict:
    """Helper to create a st.user-like dict."""
    user_dict = {
        "oid": oid,
        "email": email,
        "name": name,
        "preferred_username": preferred_username,
        "tid": tid,
        "is_logged_in": is_logged_in,
    }
    if exp is not None:
        user_dict["exp"] = exp
    return user_dict


class TestProperty5UserClaimsExtraction:
    """
    **Feature: entraid-authentication, Property 5: User Claims Extraction**
    
    *For any* st.user dict containing oid, email, name, preferred_username, and tid fields,
    the `UserClaims.from_st_user` function SHALL extract all fields into a UserClaims 
    object with matching values.
    
    **Validates: Requirements 2.3, 3.1**
    """

    @settings(max_examples=100)
    @given(
        oid=uuid_strategy,
        email=email_strategy,
        name=non_empty_string,
        preferred_username=email_strategy,
        tid=uuid_strategy,
        exp=st.one_of(st.none(), timestamp_strategy),
    )
    def test_claims_extraction_preserves_all_fields(
        self,
        oid: str,
        email: str,
        name: str,
        preferred_username: str,
        tid: str,
        exp,
    ):
        """All fields from st.user should be correctly extracted into UserClaims."""
        st_user = make_st_user_dict(
            oid=oid,
            email=email,
            name=name,
            preferred_username=preferred_username,
            tid=tid,
            exp=exp,
        )
        
        claims = UserClaims.from_st_user(st_user)
        
        assert claims.oid == oid
        assert claims.email == email
        assert claims.name == name
        assert claims.preferred_username == preferred_username
        assert claims.tenant_id == tid
        assert claims.exp == exp


class TestProperty6LoginStatusVerification:
    """
    **Feature: entraid-authentication, Property 6: Login Status Verification**
    
    *For any* st.user dict where `is_logged_in` is False, calling `extract_user_claims` 
    SHALL return None without attempting to access other claims.
    
    **Validates: Requirements 3.2**
    """

    @settings(max_examples=100)
    @given(
        oid=uuid_strategy,
        email=email_strategy,
        name=non_empty_string,
        preferred_username=email_strategy,
        tid=uuid_strategy,
    )
    def test_not_logged_in_returns_none(
        self,
        oid: str,
        email: str,
        name: str,
        preferred_username: str,
        tid: str,
    ):
        """When is_logged_in is False, extract_user_claims should return None."""
        import sys
        
        # Create a mock streamlit module
        mock_streamlit = MagicMock()
        mock_user = MagicMock()
        mock_user.is_logged_in = False
        mock_streamlit.user = mock_user
        
        with patch.dict(sys.modules, {'streamlit': mock_streamlit}):
            result = extract_user_claims()
            assert result is None

    @settings(max_examples=100)
    @given(
        oid=uuid_strategy,
        email=email_strategy,
        name=non_empty_string,
        preferred_username=email_strategy,
        tid=uuid_strategy,
        exp=st.one_of(st.none(), timestamp_strategy),
    )
    def test_logged_in_returns_claims(
        self,
        oid: str,
        email: str,
        name: str,
        preferred_username: str,
        tid: str,
        exp,
    ):
        """When is_logged_in is True, extract_user_claims should return UserClaims."""
        import sys
        
        st_user_dict = make_st_user_dict(
            oid=oid,
            email=email,
            name=name,
            preferred_username=preferred_username,
            tid=tid,
            exp=exp,
            is_logged_in=True,
        )
        
        # Create a mock streamlit module with a dict-like user object
        mock_streamlit = MagicMock()
        
        # Create a mock user that behaves like a dict when converted
        class MockUser:
            is_logged_in = True
            
            def __iter__(self):
                return iter(st_user_dict.keys())
            
            def keys(self):
                return st_user_dict.keys()
            
            def values(self):
                return st_user_dict.values()
            
            def items(self):
                return st_user_dict.items()
            
            def __getitem__(self, key):
                return st_user_dict[key]
            
            def get(self, key, default=None):
                return st_user_dict.get(key, default)
        
        mock_streamlit.user = MockUser()
        
        with patch.dict(sys.modules, {'streamlit': mock_streamlit}):
            result = extract_user_claims()
            
            assert result is not None
            assert isinstance(result, UserClaims)
            assert result.oid == oid
            assert result.email == email
            assert result.name == name
            assert result.preferred_username == preferred_username
            assert result.tenant_id == tid


class TestProperty7TokenExpirationCheck:
    """
    **Feature: entraid-authentication, Property 7: Token Expiration Check**
    
    *For any* UserClaims object with an `exp` timestamp, the `is_expired` method 
    SHALL return True if the current time is greater than or equal to `exp`, 
    and False otherwise.
    
    **Validates: Requirements 3.4**
    """

    @settings(max_examples=100)
    @given(
        oid=uuid_strategy,
        email=email_strategy,
        name=non_empty_string,
        preferred_username=email_strategy,
        tid=uuid_strategy,
        seconds_offset=st.integers(min_value=1, max_value=86400 * 365),  # 1 second to 1 year
    )
    def test_future_expiration_not_expired(
        self,
        oid: str,
        email: str,
        name: str,
        preferred_username: str,
        tid: str,
        seconds_offset: int,
    ):
        """Token with future expiration should not be expired."""
        future_exp = int(datetime.now().timestamp()) + seconds_offset
        
        claims = UserClaims(
            oid=oid,
            email=email,
            name=name,
            preferred_username=preferred_username,
            tenant_id=tid,
            exp=future_exp,
        )
        
        assert claims.is_expired() is False

    @settings(max_examples=100)
    @given(
        oid=uuid_strategy,
        email=email_strategy,
        name=non_empty_string,
        preferred_username=email_strategy,
        tid=uuid_strategy,
        seconds_offset=st.integers(min_value=1, max_value=86400 * 365),  # 1 second to 1 year
    )
    def test_past_expiration_is_expired(
        self,
        oid: str,
        email: str,
        name: str,
        preferred_username: str,
        tid: str,
        seconds_offset: int,
    ):
        """Token with past expiration should be expired."""
        past_exp = int(datetime.now().timestamp()) - seconds_offset
        
        claims = UserClaims(
            oid=oid,
            email=email,
            name=name,
            preferred_username=preferred_username,
            tenant_id=tid,
            exp=past_exp,
        )
        
        assert claims.is_expired() is True

    @settings(max_examples=100)
    @given(
        oid=uuid_strategy,
        email=email_strategy,
        name=non_empty_string,
        preferred_username=email_strategy,
        tid=uuid_strategy,
    )
    def test_no_expiration_not_expired(
        self,
        oid: str,
        email: str,
        name: str,
        preferred_username: str,
        tid: str,
    ):
        """Token with no expiration (None) should not be expired."""
        claims = UserClaims(
            oid=oid,
            email=email,
            name=name,
            preferred_username=preferred_username,
            tenant_id=tid,
            exp=None,
        )
        
        assert claims.is_expired() is False
