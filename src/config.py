"""
Application configuration module.
Loads settings from environment variables with sensible defaults for development.
"""

import os


class Config:
    """Base configuration - shared settings for all environments."""

    # Secret key for session/CSRF protection - MUST be set in production
    SECRET_KEY = os.getenv(
        "FLASK_SECRET_KEY",
        os.getenv("SECRET_KEY", "dev-key-change-in-production")
    )

    # Database URI - supports both SQLite and other databases
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///CharSheet.db"
    )

    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(Config):
    """Development-specific configuration."""

    DEBUG = True
    SQLALCHEMY_ECHO = True
    TESTING = False


class ProductionConfig(Config):
    """Production-specific configuration."""

    DEBUG = False
    SQLALCHEMY_ECHO = False
    TESTING = False


class TestingConfig(Config):
    """Testing-specific configuration."""

    DEBUG = True
    SQLALCHEMY_ECHO = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


def get_config():
    """Get the appropriate configuration based on FLASK_ENV environment variable."""
    env = os.getenv("FLASK_ENV", "development").lower()

    config_map = {
        "production": ProductionConfig,
        "prod": ProductionConfig,
        "development": DevelopmentConfig,
        "dev": DevelopmentConfig,
        "testing": TestingConfig,
        "test": TestingConfig,
    }

    return config_map.get(env, DevelopmentConfig)
