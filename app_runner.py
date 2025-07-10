import sys
import os
import signal
import subprocess

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    print(f"\nReceived signal {sig}, shutting down gracefully...")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == '__main__':
    
    if "dev" in sys.argv:
        print("Running in development mode")
        serve_cmd = "uv run flask --app src.main run --debug --host 0.0.0.0 --port 5000"
    else:
        print("Running in production mode")
        serve_cmd = "uv run waitress-serve --host 0.0.0.0 --port 5000 src.main:app"
    if "migrate" in sys.argv:
        print("Migrating database")
        os.system("uv run alembic upgrade head")
    
    if "db_init" in sys.argv:
        from src.main import init_db
        print("Initializing database")
        init_db()
        print("Database initialized. Run command again without 'db_init' arg to start the server.")
        exit(0)
    
    if "quiet" in sys.argv:
        serve_cmd += " &"
        # Run in background and capture PID for graceful shutdown
        process = subprocess.Popen(serve_cmd, shell=True)
        print(f"Server started with PID: {process.pid}")
        try:
            process.wait()
        except KeyboardInterrupt:
            print("Stopping server...")
            process.terminate()
            process.wait()
    else:
        os.system(serve_cmd)
    