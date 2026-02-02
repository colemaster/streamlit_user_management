"""Database setup using SQLAlchemy with enhanced session-scoped caching"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import streamlit as st
from src.settings import DatabaseConfig


@st.cache_resource(scope="session", show_spinner="Initializing database connection...")
def get_db_engine():
    """
    Get database engine with session-scoped resource caching.
    
    Uses Streamlit nightly 2026 session-scoped caching to maintain
    database connections per user session for better performance.
    """
    return create_engine(
        DatabaseConfig.get_connection_url(),
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=3600,   # Recycle connections after 1 hour
        echo=False           # Set to True for SQL debugging
    )


@st.cache_resource(scope="session")
def get_session_maker():
    """Get SQLAlchemy session maker with session-scoped caching."""
    engine = get_db_engine()
    return sessionmaker(bind=engine)


# Initialize with session-scoped caching
engine = get_db_engine()
SessionLocal = get_session_maker()
Base = declarative_base()


# Database utility functions with session-scoped caching
@st.cache_data(scope="session", ttl=1800, show_spinner="Loading user data...")
def get_cached_user_data(user_id: str):
    """
    Get user data with session-scoped caching.
    
    Args:
        user_id: User identifier
        
    Returns:
        User data dictionary
    """
    # This would typically query the database
    # For now, return mock data
    return {
        "user_id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com",
        "preferences": {
            "theme": "dark",
            "notifications": True,
            "dashboard_layout": "default"
        },
        "last_login": "2026-01-31T10:30:00Z"
    }


@st.cache_data(scope="session", ttl=3600, show_spinner="Loading application settings...")
def get_cached_app_settings():
    """
    Get application settings with session-scoped caching.
    
    Returns:
        Application settings dictionary
    """
    # This would typically query the database
    # For now, return mock settings
    return {
        "app_name": "FinOps AI Dashboard",
        "version": "2.0.0",
        "features": {
            "enhanced_metrics": True,
            "session_caching": True,
            "advanced_dialogs": True,
            "sparklines": True
        },
        "limits": {
            "max_cache_size": "100MB",
            "session_timeout": 28800,  # 8 hours
            "max_concurrent_users": 1000
        }
    }


def clear_database_cache():
    """Clear all database-related caches."""
    get_cached_user_data.clear()
    get_cached_app_settings.clear()


def refresh_database_connections():
    """Refresh database connections and clear resource cache."""
    get_db_engine.clear()
    get_session_maker.clear()
