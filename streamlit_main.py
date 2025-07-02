"""Entry point for the Streamlit application"""


import streamlit as st
from src.ui.pages import render
from src.database.database import Base, engine

Base.metadata.create_all(engine)

if "page" not in st.session_state:
    st.session_state["page"] = "login"

render()
