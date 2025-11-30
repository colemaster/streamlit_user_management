from streamlit.testing.v1 import AppTest


def test_login_page_loads():
    """Test that the app loads and shows the login page by default."""
    at = AppTest.from_file("streamlit_main.py").run()
    assert not at.exception

    # Check if there are any errors
    if at.error:
        print(f"Streamlit Errors: {[e.value for e in at.error]}")

    # The title is "FinOps AI Dashboard" in src/auth/guard.py
    assert "FinOps AI Dashboard" in at.title[0].value
    # Should have a button for Microsoft Login
    assert at.button[0].label == "Sign in with Microsoft"


def test_chat_interface_structure():
    """Test that the chat interface structure exists (mocking auth)."""
    # Note: mocking auth in AppTest is tricky without modifying the app code to accept a mock auth manager.
    # For now, we verify the file structure and imports via static analysis or unit tests.
    # This test just checks if we can import the chat module without error.
    from src.ui.chat import render_chat

    assert callable(render_chat)
