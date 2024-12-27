import sys
import os


if __name__ == '__main__':
    
    if "dev" in sys.argv:
        print("Running in development mode")
        serve_cmd = "uv run flask --app src/main run --debug 2>&1 > output.log"
    else:
        print("Running in production mode")
        serve_cmd = "uv run waitress-serve --host 127.0.0.1 --port 5000 src:app 2>&1 > output.log"
    if "migrate" in sys.argv:
        print("Migrating database")
        os.system("uv run alembic upgrade head")
    if "quiet" in sys.argv:
        serve_cmd += " &"
    
    os.system(serve_cmd)