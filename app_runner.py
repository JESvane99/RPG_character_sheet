import sys
import os


if __name__ == '__main__':
    
    if "dev" in sys.argv:
        print("Running in development mode")
        serve_cmd = "uv run flask --app src/main run --debug"
    else:
        print("Running in production mode")
        serve_cmd = "uv run waitress-serve --host 127.0.0.1 --port 5000 src:app"
    if "migrate" in sys.argv:
        print("Migrating database")
        os.system("uv run alembic upgrade head")
    if "quiet" in sys.argv:
        serve_cmd += " &"
    
    if "db_init" in sys.argv:
        from src.main import init_db
        print("Initializing database")
        init_db()
        print("Database initialized. Run command again without 'db_init' arg to start the server.")
        exit(0)
    
    os.system(serve_cmd)
    