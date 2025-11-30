# Requirements Document

## Introduction

This document specifies the requirements for implementing Microsoft Entra ID (Azure AD) authentication in the FinOps AI Dashboard Streamlit application. The feature will leverage Streamlit's native authentication features (`st.login`, `st.logout`, `st.user`) introduced in version 1.42+, combined with Entra ID group-based permission mapping using Object IDs (OIDs) for role-based access control.

## Glossary

- **Entra ID**: Microsoft's cloud-based identity and access management service (formerly Azure Active Directory)
- **st.login**: Streamlit's native function that redirects users to an identity provider for authentication
- **st.logout**: Streamlit's native function that removes the identity cookie and logs out the user
- **st.user**: Streamlit's dict-like object containing user information from the identity provider, including `is_logged_in` attribute
- **JWT**: JSON Web Token - a compact, URL-safe means of representing claims between two parties
- **OID**: Object Identifier - a unique identifier assigned to each object (user, group, application) in Entra ID
- **OIDC**: OpenID Connect - an authentication protocol built on top of OAuth 2.0
- **ID Token**: A JWT containing user identity claims returned by Entra ID
- **Group Claim**: A claim in the JWT containing the OIDs of groups the user belongs to
- **Permission Level**: An application-defined access level (e.g., admin, analyst, viewer)
- **secrets.toml**: Streamlit's configuration file for storing sensitive authentication settings

## Requirements

### Requirement 1

**User Story:** As a system administrator, I want to configure Entra ID authentication using Streamlit's secrets management, so that the application can authenticate users against our organization's identity provider.

#### Acceptance Criteria

1. WHEN the application starts THEN the Entra_ID_Auth_System SHALL load authentication configuration from `.streamlit/secrets.toml` including client_id, client_secret, redirect_uri, cookie_secret, and server_metadata_url
2. WHEN any required Entra ID configuration value is missing from secrets.toml THEN the Entra_ID_Auth_System SHALL display a descriptive error message to the administrator
3. WHEN the server_metadata_url is configured THEN the Entra_ID_Auth_System SHALL use the format `https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration`
4. WHEN group-to-permission mappings are configured THEN the Entra_ID_Auth_System SHALL store mappings between Entra ID group OIDs and application permission levels in the application configuration

### Requirement 2

**User Story:** As a user, I want to authenticate using my organization's Entra ID credentials via Streamlit's native login, so that I can access the application with single sign-on.

#### Acceptance Criteria

1. WHEN an unauthenticated user accesses the application THEN the Entra_ID_Auth_System SHALL check `st.user.is_logged_in` and display a login interface if false
2. WHEN a user clicks the login button THEN the Entra_ID_Auth_System SHALL call `st.login()` to initiate the Entra ID OAuth flow
3. WHEN authentication completes successfully THEN the Entra_ID_Auth_System SHALL have access to user claims via `st.user` including name, email, oid, and tid (tenant ID)
4. WHEN a user is authenticated THEN the Entra_ID_Auth_System SHALL redirect the user to the dashboard view
5. WHEN a user clicks logout THEN the Entra_ID_Auth_System SHALL call `st.logout()` to clear the identity cookie and end the session

### Requirement 3

**User Story:** As a security engineer, I want the application to properly handle Entra ID tokens, so that user identity information is correctly processed.

#### Acceptance Criteria

1. WHEN a user authenticates THEN the Entra_ID_Auth_System SHALL extract user claims from `st.user` including oid (user object ID), email, name, and preferred_username
2. WHEN accessing user information THEN the Entra_ID_Auth_System SHALL verify `st.user.is_logged_in` is true before accessing other claims
3. WHEN the identity cookie expires (after 30 days) THEN the Entra_ID_Auth_System SHALL require the user to re-authenticate
4. WHEN token expiration information is available in `st.user.exp` THEN the Entra_ID_Auth_System SHALL check expiration and call `st.logout()` if the token has expired
5. WHEN serializing user permission data for session storage THEN the Entra_ID_Auth_System SHALL encode the data properly
6. WHEN deserializing user permission data from session storage THEN the Entra_ID_Auth_System SHALL decode and restore the original permission data

### Requirement 4

**User Story:** As a system administrator, I want to map Entra ID groups to application permissions using OIDs, so that I can control access based on organizational group membership.

#### Acceptance Criteria

1. WHEN a user authenticates THEN the Entra_ID_Auth_System SHALL retrieve group membership by calling the Microsoft Graph API using the user's OID
2. WHEN group OIDs are retrieved THEN the Entra_ID_Auth_System SHALL map each OID to the corresponding application permission level using the configured mappings
3. WHEN a user belongs to multiple groups with different permission levels THEN the Entra_ID_Auth_System SHALL assign the highest permission level
4. WHEN a user belongs to no mapped groups THEN the Entra_ID_Auth_System SHALL assign a default viewer permission level
5. WHEN permission mappings are updated in configuration THEN the Entra_ID_Auth_System SHALL apply new mappings on the next user authentication

### Requirement 5

**User Story:** As a user, I want my authentication session to persist appropriately using Streamlit's native session management, so that I don't have to re-authenticate unnecessarily.

#### Acceptance Criteria

1. WHEN a user successfully authenticates via `st.login()` THEN the Entra_ID_Auth_System SHALL have Streamlit automatically store the identity cookie
2. WHEN a user returns to the application with a valid identity cookie THEN the Entra_ID_Auth_System SHALL restore the session via `st.user.is_logged_in` without requiring re-authentication
3. WHEN a user opens the application in a new tab while logged in THEN the Entra_ID_Auth_System SHALL automatically recognize the user as logged in
4. WHEN a user calls `st.logout()` THEN the Entra_ID_Auth_System SHALL remove the identity cookie and start a new session
5. WHEN the user's permission level is determined THEN the Entra_ID_Auth_System SHALL cache the permission level in `st.session_state` for the duration of the session

### Requirement 6

**User Story:** As a developer, I want to check user permissions in the application code, so that I can enforce access control on features and data.

#### Acceptance Criteria

1. WHEN application code requests the current user's permissions THEN the Entra_ID_Auth_System SHALL return the mapped permission level from session state
2. WHEN application code checks if a user has a specific permission THEN the Entra_ID_Auth_System SHALL return a boolean indicating authorization status
3. WHEN an unauthorized user attempts to access a protected feature THEN the Entra_ID_Auth_System SHALL display an access denied message
4. WHEN permission checks are performed THEN the Entra_ID_Auth_System SHALL use the cached permission level from session state

### Requirement 7

**User Story:** As a security engineer, I want authentication events to be logged, so that I can audit access to the application.

#### Acceptance Criteria

1. WHEN a user successfully authenticates THEN the Entra_ID_Auth_System SHALL log the event with user email, OID, timestamp, and assigned permissions
2. WHEN authentication fails or a user is not logged in THEN the Entra_ID_Auth_System SHALL log the access attempt without exposing sensitive details
3. WHEN a user logs out THEN the Entra_ID_Auth_System SHALL log the logout event with user email and timestamp
4. WHEN a permission check denies access THEN the Entra_ID_Auth_System SHALL log the denied access attempt with user OID and requested resource
