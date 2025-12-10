from streamlit.testing.v1 import AppTest


def test_login_page_loads():
    """Test that the app loads and shows the login page by default."""
    at = AppTest.from_file("streamlit_main.py").run()
    assert not at.exception

    # Check if there are any errors
    if at.error:
        print(f"Streamlit Errors: {[e.value for e in at.error]}")

    # The title "FinOps AI" is now in an animated header (HTML/Markdown)
    # Check for presence in Markdown values
    assert any("FinOps AI" in md.value for md in at.markdown)

    # Should have a button for Microsoft Login with updated label
    # We look for the primary button "Sign in with Microsoft"
    buttons = [b for b in at.button if "Sign in with Microsoft" in b.label]
    assert len(buttons) > 0


def test_chat_interface_structure():
    """Test that the chat interface structure exists."""
    # This test currently just checks importability which is fine
    from src.ui.chat import render_chat

    assert callable(render_chat)
