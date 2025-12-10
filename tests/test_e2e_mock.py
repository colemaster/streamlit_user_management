import pytest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from src.auth.config import PermissionLevel
from src.auth.claims import UserClaims
from src.auth.permissions import UserPermission

# Mock User Data
MOCK_VIEWER = UserClaims(
    oid="viewer-oid",
    email="viewer@example.com",
    name="Viewer User",
    preferred_username="viewer",
    tenant_id="tenant-id",
    exp=9999999999,
)

MOCK_ANALYST = UserClaims(
    oid="analyst-oid",
    email="analyst@example.com",
    name="Analyst User",
    preferred_username="analyst",
    tenant_id="tenant-id",
    exp=9999999999,
)

MOCK_ADMIN = UserClaims(
    oid="admin-oid",
    email="admin@example.com",
    name="Admin User",
    preferred_username="admin",
    tenant_id="tenant-id",
    exp=9999999999,
)

MOCK_EXPIRED_USER = UserClaims(
    oid="expired-oid",
    email="expired@example.com",
    name="Expired User",
    preferred_username="expired",
    tenant_id="tenant-id",
    exp=0,  # Expired
)


@pytest.fixture
def mock_auth_guard():
    """Mock the AuthGuard to bypass Graph API calls."""
    with patch("src.auth.guard.AuthGuard.initialize_user_permission") as mock_init:
        yield mock_init


def test_unauthenticated_access():
    """Test that unauthenticated users are shown the login page."""
    # Patch check_login_status in src.auth.guard where it is used
    with patch("src.auth.guard.check_login_status", return_value=False):
        at = AppTest.from_file("streamlit_main.py").run()

        assert not at.exception
        # Only check if the animated header text is present in the markdown elements
        # Since animated_header uses HTML inside markdown, we check for presence in markdown values
        assert any("FinOps AI" in md.value for md in at.markdown)

        # Check for the updated button label
        assert at.button[0].label == "🔐 Sign in with Microsoft"


def test_viewer_access(mock_auth_guard):
    """Test VIEWER access: Chat access, no Admin Console."""
    # Mock logged in status and claims in all places they are used
    with (
        patch("src.auth.guard.check_login_status", return_value=True),
        patch("src.auth.guard.extract_user_claims", return_value=MOCK_VIEWER),
        patch("src.ui.pages.extract_user_claims", return_value=MOCK_VIEWER),
        patch(
            "src.auth.permissions.get_current_permission",
            return_value=PermissionLevel.VIEWER,
        ),
        patch(
            "src.ui.pages.get_current_permission", return_value=PermissionLevel.VIEWER
        ),
        patch(
            "src.ui.chat.get_current_permission", return_value=PermissionLevel.VIEWER
        ),
        patch("src.ui.chat.has_permission", return_value=True),
    ):
        # Mock permission initialization to return VIEWER permission
        mock_auth_guard.return_value = UserPermission(
            user_oid=MOCK_VIEWER.oid,
            permission_level=PermissionLevel.VIEWER,
            group_oids=["viewer-group"],
        )

        at = AppTest.from_file("streamlit_main.py").run()

        assert not at.exception

        # Should see Chat/Assistant title
        # render_chat calls animated_header("FinOps Assistant", ...)
        assert any("FinOps Assistant" in md.value for md in at.markdown)

        # Sidebar should NOT have navigation to Admin Console
        if at.sidebar.radio:
            assert "Admin Console" not in at.sidebar.radio[0].options


def test_admin_access(mock_auth_guard):
    """Test ADMIN access: Access to Admin Console."""
    # Mock logged in status and claims in all places they are used
    with (
        patch("src.auth.guard.check_login_status", return_value=True),
        patch("src.auth.guard.extract_user_claims", return_value=MOCK_ADMIN),
        patch("src.ui.pages.extract_user_claims", return_value=MOCK_ADMIN),
        patch("src.ui.admin.extract_user_claims", return_value=MOCK_ADMIN),
        patch("src.ui.chat.get_current_permission", return_value=PermissionLevel.ADMIN),
        patch("src.ui.chat.has_permission", return_value=True),
        patch(
            "src.auth.permissions.get_current_permission",
            return_value=PermissionLevel.ADMIN,
        ),
        patch(
            "src.ui.pages.get_current_permission", return_value=PermissionLevel.ADMIN
        ),
    ):
        # Mock permission initialization to return ADMIN permission
        mock_auth_guard.return_value = UserPermission(
            user_oid=MOCK_ADMIN.oid,
            permission_level=PermissionLevel.ADMIN,
            group_oids=["admin-group"],
        )

        at = AppTest.from_file("streamlit_main.py").run()

        assert not at.exception

        # Should see Assistant title initially (default page)
        assert any("FinOps Assistant" in md.value for md in at.markdown)

        # Sidebar SHOULD have navigation
        assert at.sidebar.radio
        assert "Admin Console" in at.sidebar.radio[0].options

        # Navigate to Admin Console
        at.sidebar.radio[0].set_value("Admin Console").run()

        # Should see Admin Console title
        assert any("Admin Console" in md.value for md in at.markdown)


def test_expired_session():
    """Test that expired session redirects to login."""
    # Mock logged in status but expired claims
    with (
        patch("src.auth.guard.check_login_status", return_value=True),
        patch("src.auth.guard.extract_user_claims", return_value=MOCK_EXPIRED_USER),
    ):
        at = AppTest.from_file("streamlit_main.py").run()

        # Should be redirected to login page (AuthGuard.require_auth returns False)
        # Check for presence of Login page elements
        assert any("FinOps AI" in md.value for md in at.markdown)
        assert at.button[0].label == "🔐 Sign in with Microsoft"
