"""
Property-based tests for the authentication configuration module.

**Feature: entraid-authentication**
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from src.auth.config import (
    PermissionLevel,
    AuthConfig,
    ConfigurationError,
    build_metadata_url,
)


# Strategies for generating test data
uuid_strategy = st.uuids().map(str)
non_empty_string = st.text(min_size=1, max_size=100).filter(lambda x: x.strip())
permission_level_strategy = st.sampled_from([PermissionLevel.VIEWER, PermissionLevel.ANALYST, PermissionLevel.ADMIN])
permission_string_strategy = st.sampled_from(["viewer", "analyst", "admin", "VIEWER", "ANALYST", "ADMIN"])


def make_valid_secrets(
    client_id: str,
    client_secret: str,
    tenant_id: str,
    redirect_uri: str,
    cookie_secret: str,
    server_metadata_url: str,
    group_mappings: dict = None,
) -> dict:
    """Helper to create a valid secrets dict."""
    secrets = {
        "auth": {
            "client_id": client_id,
            "client_secret": client_secret,
            "tenant_id": tenant_id,
            "redirect_uri": redirect_uri,
            "cookie_secret": cookie_secret,
            "server_metadata_url": server_metadata_url,
        }
    }
    if group_mappings:
        secrets["auth"]["group_mappings"] = group_mappings
    return secrets


class TestProperty1ConfigurationLoadingCompleteness:
    """
    **Feature: entraid-authentication, Property 1: Configuration Loading Completeness**
    
    *For any* valid secrets.toml configuration containing all required fields 
    (client_id, client_secret, redirect_uri, cookie_secret, server_metadata_url), 
    loading the configuration SHALL produce an AuthConfig object with all fields 
    populated correctly.
    
    **Validates: Requirements 1.1**
    """

    @settings(max_examples=100)
    @given(
        client_id=non_empty_string,
        client_secret=non_empty_string,
        tenant_id=uuid_strategy,
        redirect_uri=non_empty_string,
        cookie_secret=non_empty_string,
        server_metadata_url=non_empty_string,
    )
    def test_valid_config_loads_all_fields(
        self,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        redirect_uri: str,
        cookie_secret: str,
        server_metadata_url: str,
    ):
        """All required fields should be populated correctly when loading valid config."""
        secrets = make_valid_secrets(
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id,
            redirect_uri=redirect_uri,
            cookie_secret=cookie_secret,
            server_metadata_url=server_metadata_url,
        )
        
        config = AuthConfig.from_secrets(secrets)
        
        assert config.client_id == client_id
        assert config.client_secret == client_secret
        assert config.tenant_id == tenant_id
        assert config.redirect_uri == redirect_uri
        assert config.cookie_secret == cookie_secret
        assert config.server_metadata_url == server_metadata_url
        
        # Should not raise on validation
        config.validate()


class TestProperty2MissingConfigurationDetection:
    """
    **Feature: entraid-authentication, Property 2: Missing Configuration Detection**
    
    *For any* secrets.toml configuration missing one or more required fields, 
    the configuration validation SHALL raise a descriptive error identifying 
    the missing field(s).
    
    **Validates: Requirements 1.2**
    """

    @settings(max_examples=100)
    @given(
        client_id=st.one_of(st.just(""), st.just(None)),
        client_secret=non_empty_string,
        tenant_id=uuid_strategy,
        redirect_uri=non_empty_string,
        cookie_secret=non_empty_string,
        server_metadata_url=non_empty_string,
    )
    def test_missing_client_id_raises_error(
        self,
        client_id,
        client_secret: str,
        tenant_id: str,
        redirect_uri: str,
        cookie_secret: str,
        server_metadata_url: str,
    ):
        """Missing client_id should raise ConfigurationError mentioning client_id."""
        secrets = make_valid_secrets(
            client_id=client_id or "",
            client_secret=client_secret,
            tenant_id=tenant_id,
            redirect_uri=redirect_uri,
            cookie_secret=cookie_secret,
            server_metadata_url=server_metadata_url,
        )
        
        config = AuthConfig.from_secrets(secrets)
        
        with pytest.raises(ConfigurationError) as exc_info:
            config.validate()
        
        assert "client_id" in str(exc_info.value)

    @settings(max_examples=100)
    @given(
        fields_to_remove=st.lists(
            st.sampled_from(["client_id", "client_secret", "tenant_id", "redirect_uri", "cookie_secret", "server_metadata_url"]),
            min_size=1,
            max_size=6,
            unique=True,
        ),
        client_id=non_empty_string,
        client_secret=non_empty_string,
        tenant_id=uuid_strategy,
        redirect_uri=non_empty_string,
        cookie_secret=non_empty_string,
        server_metadata_url=non_empty_string,
    )
    def test_any_missing_field_raises_descriptive_error(
        self,
        fields_to_remove: list,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        redirect_uri: str,
        cookie_secret: str,
        server_metadata_url: str,
    ):
        """Any missing required field should raise ConfigurationError identifying it."""
        secrets = make_valid_secrets(
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id,
            redirect_uri=redirect_uri,
            cookie_secret=cookie_secret,
            server_metadata_url=server_metadata_url,
        )
        
        # Remove specified fields
        for field in fields_to_remove:
            secrets["auth"][field] = ""
        
        config = AuthConfig.from_secrets(secrets)
        
        with pytest.raises(ConfigurationError) as exc_info:
            config.validate()
        
        error_message = str(exc_info.value)
        for field in fields_to_remove:
            assert field in error_message, f"Error should mention missing field: {field}"


class TestProperty3MetadataURLFormat:
    """
    **Feature: entraid-authentication, Property 3: Metadata URL Format**
    
    *For any* valid tenant ID (GUID format), the `build_metadata_url` function 
    SHALL produce a URL matching the pattern 
    `https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration`.
    
    **Validates: Requirements 1.3**
    """

    @settings(max_examples=100)
    @given(tenant_id=uuid_strategy)
    def test_metadata_url_format(self, tenant_id: str):
        """Metadata URL should follow the expected pattern."""
        url = build_metadata_url(tenant_id)
        
        expected_prefix = "https://login.microsoftonline.com/"
        expected_suffix = "/v2.0/.well-known/openid-configuration"
        
        assert url.startswith(expected_prefix)
        assert url.endswith(expected_suffix)
        assert tenant_id in url
        assert url == f"{expected_prefix}{tenant_id}{expected_suffix}"


class TestProperty4GroupMappingStorage:
    """
    **Feature: entraid-authentication, Property 4: Group Mapping Storage**
    
    *For any* group-to-permission mapping configuration, the loaded AuthConfig 
    SHALL contain a `group_mappings` dict where each key is a group OID string 
    and each value is a valid PermissionLevel.
    
    **Validates: Requirements 1.4**
    """

    @settings(max_examples=100)
    @given(
        group_oids=st.lists(uuid_strategy, min_size=0, max_size=10, unique=True),
        permission_strings=st.lists(permission_string_strategy, min_size=0, max_size=10),
        client_id=non_empty_string,
        client_secret=non_empty_string,
        tenant_id=uuid_strategy,
        redirect_uri=non_empty_string,
        cookie_secret=non_empty_string,
        server_metadata_url=non_empty_string,
    )
    def test_group_mappings_stored_correctly(
        self,
        group_oids: list,
        permission_strings: list,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        redirect_uri: str,
        cookie_secret: str,
        server_metadata_url: str,
    ):
        """Group mappings should be stored with OID keys and PermissionLevel values."""
        # Create mappings from generated data
        group_mappings = {}
        for i, oid in enumerate(group_oids):
            if i < len(permission_strings):
                group_mappings[oid] = permission_strings[i]
        
        secrets = make_valid_secrets(
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id,
            redirect_uri=redirect_uri,
            cookie_secret=cookie_secret,
            server_metadata_url=server_metadata_url,
            group_mappings=group_mappings,
        )
        
        config = AuthConfig.from_secrets(secrets)
        
        # Verify all keys are strings (OIDs)
        for key in config.group_mappings.keys():
            assert isinstance(key, str)
        
        # Verify all values are valid PermissionLevel
        for value in config.group_mappings.values():
            assert isinstance(value, PermissionLevel)
            assert value in [PermissionLevel.VIEWER, PermissionLevel.ANALYST, PermissionLevel.ADMIN]
        
        # Verify the count matches (only valid mappings should be stored)
        permission_map = {"viewer", "analyst", "admin"}
        expected_count = sum(
            1 for oid in group_oids 
            if oid in group_mappings and group_mappings[oid].lower() in permission_map
        )
        assert len(config.group_mappings) == expected_count
