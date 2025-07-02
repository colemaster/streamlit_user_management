"""Manager layer to mediate between UI and services"""

import streamlit as st
from src.database.database import SessionLocal
from src.ui.services import AuthService
from streamlit_cookies_controller import CookieController

controller = CookieController()

class AuthManager:
    def __init__(self):
        self.db = SessionLocal()
        self.auth_service = AuthService(self.db)
        self.cookie_manager = controller
        self._initialize_auth_state()

    def _initialize_auth_state(self):
        """Initialize authentication state from cookies on page load"""
        try:
            self.cookie_manager.getAll()

            session_token = st.session_state.get("token")
            cookie_token = self.cookie_manager.get("auth_token")
            cookie_page = self.cookie_manager.get("page")

            if cookie_token:
                if self._is_token_valid(cookie_token):
                    st.session_state["token"] = cookie_token
                    if cookie_page:
                        st.session_state["page"] = cookie_page
                    else:
                        st.session_state["page"] = "dashboard"
                    print(f"Token restored from cookies: {cookie_token[:20]}...")
                else:
                    # Invalid token in cookies, clear everything
                    print("Invalid token in cookies, clearing...")
                    self._clear_invalid_cookies()
                    self._clear_session_state()

            # If no cookie token but session token exists, sync to cookies
            elif session_token and not cookie_token:
                if self._is_token_valid(session_token):
                    # Save to cookies
                    self.cookie_manager.set("auth_token", session_token, max_age=3600)
                    current_page = st.session_state.get("page", "dashboard")
                    self.cookie_manager.set("page", current_page, max_age=3600)
                    print("Session token saved to cookies")
                else:
                    # Invalid session token
                    self._clear_session_state()

        except Exception as e:
            print(f"Error initializing auth state: {e}")
            self._clear_invalid_cookies()

    def _is_token_valid(self, token):
        """Check if a token is valid by decoding it"""
        if not token:
            return False

        try:
            email = self.auth_service.decode_token(token)
            is_valid = email is not None
            print(f"Token validation result: {is_valid}, Email: {email}")
            return is_valid
        except Exception as e:
            print(f"Token validation error: {e}")
            return False

    def _clear_invalid_cookies(self):
        """Clear invalid cookies"""
        try:
            self.cookie_manager.remove("auth_token")
            self.cookie_manager.remove("page")
            print("Invalid cookies cleared")
        except Exception as e:
            print(f"Error clearing cookies: {e}")

    @staticmethod
    def _clear_session_state():
        """Clear authentication session state"""
        keys_to_clear = ["token", "page"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        print("Session state cleared")

    def login(self, email, password):
        """Authenticate user and save token in session and cookies"""
        try:
            user = self.auth_service.authenticate_user(email, password)
            if user:
                token = self.auth_service.create_token(user.email)

                st.session_state["token"] = token
                st.session_state["page"] = "dashboard"

                self.cookie_manager.set("auth_token", token, max_age=86400)  # 24 hours
                self.cookie_manager.set("page", "dashboard", max_age=86400)

                print(f"Login successful for {email}")
                print(f"Token created: {token[:20]}...")

                # just for the cookie refresh
                self.cookie_manager.getAll()

                return True
            else:
                print(f"Login failed for {email}")
                return False
        except Exception as e:
            print(f"Login error: {e}")
            return False

    def register(self, first_name, last_name, email, password):
        """Register a new user"""
        try:
            user = self.auth_service.register_user(first_name, last_name, email, password)
            if user:
                st.success("User registered successfully")
                return True
            else:
                st.error("Email already exists")
                return False
        except Exception as e:
            print(f"Registration error: {e}")
            st.error(f"Registration failed: {str(e)}")
            return False

    def is_authenticated(self):
        """Check if user is authenticated"""
        try:
            session_token = st.session_state.get("token")
            if session_token and self._is_token_valid(session_token):
                print("Authenticated via session token")
                return True

            cookie_token = self.cookie_manager.get("auth_token")
            if cookie_token and self._is_token_valid(cookie_token):
                print("Authenticated via cookie token - restoring session")
                st.session_state["token"] = cookie_token
                cookie_page = self.cookie_manager.get("page")
                if cookie_page:
                    st.session_state["page"] = cookie_page
                return True

            print("Not authenticated - no valid tokens found")
            return False

        except Exception as e:
            print(f"Authentication check error: {e}")
            return False

    def logout(self):
        """Log out user and clear all data"""
        try:
            keys_to_clear = ["token", "page"]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]

            self.cookie_manager.remove("auth_token")
            self.cookie_manager.remove("page")

            st.session_state["page"] = "login"

            print("Logout successful - session and cookies cleared")

        except Exception as e:
            print(f"Logout error: {e}")
            st.session_state["page"] = "login"

    def get_current_user_email(self):
        """Return current authenticated user's email"""
        token = st.session_state.get("token")
        if not token:
            token = self.cookie_manager.get("auth_token")

        if token and self._is_token_valid(token):
            return self.auth_service.decode_token(token)
        return None