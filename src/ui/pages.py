"""Handles routing and layout rendering with persistent authentication"""

import streamlit as st
from src.ui.components import LoginForm, RegisterForm, Dashboard
from src.ui.managers import AuthManager


def render():
    # Initialize manager (which will automatically check cookies)
    auth = AuthManager()

    # Initialize UI components
    login_ui = LoginForm()
    register_ui = RegisterForm()
    dashboard_ui = Dashboard()

    dashboard_ui.add_widget(lambda: st.info("🔔 Notifications will appear here."))
    dashboard_ui.add_widget(lambda: st.success("✅ You are authenticated!"))

    page = st.session_state.get("page")

    if not page:
        if auth.is_authenticated():
            page = "dashboard"
            st.session_state["page"] = "dashboard"
        else:
            page = "login"
            st.session_state["page"] = "login"

    print(f"Current page: {page}")
    print(f"Is authenticated: {auth.is_authenticated()}")

    if page == "register":
        st.title("🔐 Register")
        first, last, email, password, submit = register_ui.render()

        if submit:
            if auth.register(first, last, email, password):
                st.success("Registration successful! Redirecting to login...")
                st.session_state["page"] = "login"
                st.rerun()

        st.markdown("---")
        if st.button("← Back to Login", type="secondary"):
            st.session_state["page"] = "login"
            st.rerun()

    elif page == "login":
        st.title("🔑 Login")
        email, password, submit = login_ui.render()

        if submit:
            if auth.login(email, password):
                st.success("Login successful! Redirecting...")
                # AuthManager already sets page to dashboard in login()
                st.rerun()
            else:
                st.error("❌ Invalid email or password")

        st.markdown("---")
        if st.button("Create Account", type="secondary"):
            st.session_state["page"] = "register"
            st.rerun()

    elif page == "dashboard":
        # Check authentication again for security
        if auth.is_authenticated():
            st.title("📊 Dashboard")

            # Display current user's email
            user_email = auth.get_current_user_email()
            if user_email:
                st.sidebar.success(f"👋 Welcome, {user_email}")

            # Render dashboard
            dashboard_ui.render()

            # Logout button in sidebar
            st.sidebar.markdown("---")
            if st.sidebar.button("🚪 Logout", type="primary"):
                auth.logout()
                st.rerun()
        else:
            st.error("🔒 Authentication required. Please login.")
            st.session_state["page"] = "login"
            st.rerun()

    else:
        # Fallback for any other situation
        st.session_state["page"] = "login"
        st.rerun()

    # Debug info (you can remove this in production)
    # with st.sidebar:
    #     st.markdown("---")
    #     with st.expander("🔧 Debug Info", expanded=False):
    #         st.write("Current page:", page)
    #         st.write("Is authenticated:", auth.is_authenticated())
    #         st.write("Session token exists:", "token" in st.session_state)
    #         try:
    #             cookies = auth.cookie_manager.getAll()
    #             st.write("Cookies:", cookies)
    #         except:
    #             st.write("Could not read cookies")