"""Database setup using SQLAlchemy"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import streamlit as st
from src.settings import DatabaseConfig


@st.cache_resource
def get_db_engine():
    return create_engine(DatabaseConfig.get_connection_url())


engine = get_db_engine()
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
