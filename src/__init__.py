from flask import Flask
from pathlib import Path

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI= "sqlite:///CharSheet_test.db",
        SECRET_KEY = "your_secret_key"
    )
    
    # Ensure the instance folder exists and by extension the database
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    
    