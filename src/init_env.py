"""
Application initialization module.
Loads environment variables from .env file before the app is created.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file)
