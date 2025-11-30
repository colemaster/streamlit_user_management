# Project Roadmap

This document outlines upcoming features in Streamlit and how they will impact the **Streamlit User Management System**.

## Upcoming Streamlit Features

### 1. `st.auth_fragment` (PR #12696)
*Note: This feature appears to be related to `st.fragment` but specifically optimized for authentication flows or partial reruns during auth.*

**Impact on Project:**
-   **Smoother Login Flows**: Currently, the entire app reruns upon login/logout. `st.auth_fragment` (or using `st.fragment` for auth components) could allow the login form or sidebar user profile to update without reloading the entire page.
-   **Performance**: Reducing full page reruns will improve the user experience, especially on the dashboard page which might load heavy data.

**Implementation Plan:**
-   Wrap the `render_login_page` and sidebar user profile in `@st.fragment`.
-   Test if session state updates within the fragment correctly propagate to the rest of the app upon successful login.

### 2. Enhanced `st.login` and `st.logout` (PR #12044)
*Streamlit is continuously improving its native auth commands.*

**Impact on Project:**
-   **Simplified AuthGuard**: As `st.login` becomes more robust, we might be able to simplify our `AuthGuard` class.

### 3. Expose OIDC Tokens & `st.user.refresh()`
*Upcoming features to provide more control over the auth session.*

**Impact on Project:**
-   **Backend API Access**: If Streamlit exposes the raw **Access Token** (JWT) via `st.user` (or similar), we can stop using `msal` for the "Optional MSAL" flow and rely entirely on native Streamlit auth while still being able to call our protected backend APIs.
-   **Session Management**: `st.user.refresh()` would allow us to programmatically refresh the user's session (and potentially the tokens) without forcing a full redirect/re-login flow, improving the user experience when tokens expire.

**Implementation Plan:**
-   Monitor Streamlit updates for token exposure in `st.user`.
-   Once available, refactor `AuthGuard` to use the native token for Graph API calls instead of acquiring a separate one via `httpx` or `msal`.
-   Implement `st.user.refresh()` in the `AuthGuard.require_auth` check to handle near-expiry tokens gracefully.

## Future Auth Enhancements

Based on the roadmap and current architecture, here are potential enhancements:

### 1. Multi-Factor Authentication (MFA) Enforcement
-   **Current**: Relies on Entra ID's default policy.
-   **Future**: Check for `amr` (Authentication Methods References) claim in the token to ensure MFA was used. If not, prompt the user or deny access to sensitive admin features.

### 2. Session Timeout Handling
-   **Current**: Relies on token expiration check in `AuthGuard`.
-   **Future**: Implement a client-side warning (using `st.empty` or a custom component) when the session is about to expire, prompting the user to refresh their token.

### 3. Role Management UI
-   **Current**: Roles are defined in `secrets.toml` (static).
-   **Future**:
    -   Create a "Roles" tab in the Admin Dashboard.
    -   Allow Admins to view all available Entra ID groups and map them to roles dynamically (stored in SQLite instead of `secrets.toml`).
    -   *Requires*: Database schema update to store `GroupMapping` table.

### 4. Backend API Proxy
-   **Current**: Frontend calls Graph API directly.
-   **Future**: Create a dedicated backend API (FastAPI) that handles all Graph API calls. Streamlit would pass the user's token to this backend. This improves security by keeping client secrets strictly server-side (though Streamlit secrets are already server-side, a separate API decouples the UI from the logic).

### 5. Audit Log Export
-   **Current**: Logs are in-memory (last 1000).
-   **Future**: Add a "Download Logs" button in the Admin Dashboard to export logs as CSV/JSON for compliance.
