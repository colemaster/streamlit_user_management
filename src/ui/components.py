"""UI components for user registration and login forms"""

import streamlit as st


class LoginForm:
    @staticmethod
    def render():
        st.subheader("🔐 Login")
        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")
        submit = st.button("Login", use_container_width=True)
        return email, password, submit

class RegisterForm:
    @staticmethod
    def render():
        st.subheader("📝 Register")
        first_name = st.text_input("👤 First Name")
        last_name = st.text_input("👥 Last Name")
        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")
        submit = st.button("Register", use_container_width=True)
        return first_name, last_name, email, password, submit

class Dashboard:
    def __init__(self):
        self.widgets = []

    def add_widget(self, func):
        self.widgets.append(func)

    def render(self):
        st.subheader("📊 User Dashboard")
        for widget in self.widgets:
            widget()