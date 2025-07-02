"""
Configuration settings module for the user management application.

This module contains all configuration constants and settings used throughout
the application, including database connection parameters, JWT settings,
and application constants.
"""

import os
from dotenv import load_dotenv


load_dotenv()


class DatabaseConfig:
    """Database configuration settings."""

    HOST = os.getenv('DB_HOST', 'localhost')
    PORT = os.getenv('DB_PORT', '3306')
    USERNAME = os.getenv('DB_USERNAME', 'root')
    PASSWORD = os.getenv('DB_PASSWORD', 'Changeme_123')
    DATABASE = os.getenv('DB_DATABASE', 'user_management')

    @classmethod
    def get_connection_url(cls) -> str:
        """
        Generate MySQL connection string for SQLAlchemy.

        Returns:
            str: Complete database connection string
        """
        return f"mysql+mysqlconnector://{cls.USERNAME}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.DATABASE}"


class JWTConfig:
    """JWT token configuration settings."""

    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this-in-production')
    ALGORITHM = 'HS256'
    EXPIRATION_SECONDS = 3600


class AppConfig:
    """General application configuration."""

    APP_NAME = "User Management System"
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    SESSION_TOKEN_KEY = 'auth_token'
    SESSION_USER_KEY = 'current_user'
    SESSION_AUTHENTICATED_KEY = 'is_authenticated'