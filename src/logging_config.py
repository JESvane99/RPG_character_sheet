import logging
import logging.handlers
import os


def setup_logging(app):
    """Configure simplified logging for the Flask application."""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Clear any existing handlers to avoid duplicates
    app.logger.handlers.clear()
    
    # Create a simple formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler for application logs
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/app.log', 
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Console handler 
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Add handlers to the Flask app logger only
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    
    # Prevent propagation to root logger to avoid duplicates
    app.logger.propagate = False
    
    # Log startup message
    app.logger.info("Application started")
    
    return app
