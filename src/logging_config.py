import logging
import logging.handlers
import os
from datetime import datetime


def setup_logging(app):
    """Configure logging for the Flask application with timestamps."""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure the root logger
    logging.basicConfig(level=logging.INFO)
    
    # Create a custom formatter with timestamps
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler for application logs
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/app.log', 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Add handlers to the Flask app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    
    # Configure Werkzeug (Flask's WSGI server) logging
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.addHandler(file_handler)
    werkzeug_logger.setLevel(logging.INFO)
    
    # Configure Waitress logging
    waitress_logger = logging.getLogger('waitress')
    waitress_logger.addHandler(file_handler)
    waitress_logger.setLevel(logging.INFO)
    
    # Log startup message
    app.logger.info("Application started")
    
    return app
