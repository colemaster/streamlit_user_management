# Streamlit User Management & FinOps Dashboard Context

## Project Overview
This project is a **Streamlit-based User Management System** tailored for **FinOps** use cases. It features a modern UI with BHP branding, an intelligent FinOps chatbot, and enterprise-grade authentication using **Microsoft Entra ID (Azure AD)**.

## Tech Stack
- **Frontend/App Framework:** Streamlit (with `uvloop` for performance)
- **Language:** Python 3.x
- **Dependency Management:** uv
- **Authentication:** 
  - Microsoft Entra ID (via `httpx` & Microsoft Graph API)
  - OAuth2, MSAL (Optional)
  - Custom Auth Service (JWT, hashing) managed via `AuthManager`
- **Database:** SQLite (SQLAlchemy ORM)
- **Data/Viz:** Pandas, Plotly
- **Testing:** Pytest, Hypothesis, Playwright (browser testing)
- **Styling:** Custom CSS (BHP Theme)
- **Key Libraries:** 
  - `streamlit-cookies-controller`: Cookie management for auth persistence.
  - `python-jose[cryptography]`: JWT handling.
  - `orjson`: Fast JSON processing.
  - `watchdog`: Filesystem monitoring.

## Project Structure

### Core Entry Points
- `streamlit_main.py`: **Primary Entry Point**. Handles DB initialization, Authentication (AuthGuard), and main page rendering. Use this to run the full app.
- `main.py`: Likely a dev/demo entry point focusing on the dashboard layout without the full auth flow.

### Source Code (`src/`)

#### `src/auth/` - Authentication & Security
- `guard.py`: `AuthGuard` class. Manages the authentication state, login flow, and permission initialization.
- `msal_guard.py`: `MSALAuthGuard` class. Optional MSAL-based authentication implementation.
- `config.py`: Configuration loader for Entra ID credentials (from `.streamlit/secrets.toml`).
- `graph_client.py`: Client for interacting with Microsoft Graph API (fetching user groups).
- `claims.py`: Token claim parsing and validation.
- `permissions.py`: Logic for mapping AD groups to application roles (VIEWER, ANALYST, ADMIN).
- `logging.py`: Auth logging with memory buffer for Admin Dashboard.
- `external.py`: Helpers for making authenticated requests to downstream APIs using the current user's credentials.

#### `src/database/` - Data Layer
- `database.py`: SQLAlchemy engine and session setup (SQLite).
- `models.py`: Database models (e.g., `User`, `AuditLog`).

#### `src/ui/` - User Interface
- `pages.py`: Main routing logic for Streamlit pages (Login, Dashboard, Admin).
- `admin.py`: Admin Dashboard component (User Info, Metrics, Logs).
- `chat.py`: FinOps Chatbot UI component.
- `dashboard.py`: Main analytics dashboard renderer.
- `styles.py`: CSS injection for the custom theme.
- `components.py`: Reusable UI widgets.
- `managers.py`: `AuthManager` class. Mediates between UI and services, handling cookie persistence and session state.
- `services.py`: `AuthService` class. Business logic for user authentication, registration, password hashing, and token generation.

#### `src/finops/` - Business Logic
- `engine.py`: Logic for the FinOps chatbot (AI responses).
- `data.py`: Data sources or mock data for the FinOps engine.

#### Configuration
- `pyproject.toml`: Project configuration and dependencies (managed by uv).
- `uv.lock`: Locked dependencies (managed by uv).
- `src/settings.py`: Application-wide settings and constants.
- `src/example.env`: Template for environment variables.
- `.streamlit/secrets.toml`: (Not committed) Contains sensitive auth credentials and group mappings.
- `AUTH.md`: Detailed authentication documentation.
- `JWT.md`: JWT token flow and backend integration guide.
- `ROADMAP.md`: Project roadmap and upcoming features.

## Development Guidelines

### Running the App
Always prefer running via `streamlit_main.py` to ensure the full context (Auth + DB) is loaded:
```bash
uv run streamlit run streamlit_main.py
```

### Authentication Workflow
1. **App Start**: `AuthGuard` checks `st.session_state` for a valid token/user.
2. **No Auth**: Redirects to Microsoft Login (OAuth2 flow) OR Custom Login (if configured).
3. **Persistence**: `AuthManager` checks cookies to restore sessions if `st.session_state` is empty.
4. **Callback (Entra ID)**: Microsoft redirects back to `/oauth2callback`.
5. **Token Exchange**: Code is exchanged for an Access Token.
6. **Permission Sync**: `AuthGuard` fetches user groups from MS Graph and maps them to roles defined in `secrets.toml`.

### Testing
- **End-to-End**: `uv run pytest tests/` (Includes Playwright tests for UI interactions).
- **Unit**: `uv run pytest` can also run unit tests for logic in `src/`.

## Key Context for AI Assistant
- **State Management**: Heavily relies on `st.session_state` and `streamlit-cookies-controller`. Be careful when clearing or modifying state keys like `messages`, `user`, `token`, `page` or `permissions_initialized`.
- **Async**: Some auth operations (like Graph API calls) are async (`asyncio.run` is used in sync contexts like Streamlit).
- **Secrets**: Auth config is in `secrets.toml`. Do not hardcode credentials in code.

---

## AI Assistant Environment Context
- **Current Date:** Thursday, January 8, 2026
- **Operating System:** linux
- **Project Temporary Directory:** /home/sean/.gemini/tmp/bd966495fc76a517dfc4826915106347657066774fff26c008d5ad4475f0dde4
- **Current Working Directory:** /home/sean/code/streamlit_user_management