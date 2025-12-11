import sys
import os
import signal
import subprocess


if __name__ == '__main__':
    
    if "dev" in sys.argv:
        print("Running in development mode")
        serve_cmd = "uv run flask --app src.main run --debug --host 0.0.0.0 --port 5000"
    else:
        print("Running in production mode")
        serve_cmd = "uv run waitress-serve --host 0.0.0.0 --port 5000 src.main:app"
    if "migrate" in sys.argv:
        print("Migrating database")
        try:
            result = subprocess.run("uv run alembic upgrade head", shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Migration failed with error code: {e.returncode}")
            sys.exit(e.returncode)
    
    if "quiet" in sys.argv:
        # Run in background with proper process management
        process = subprocess.Popen(serve_cmd, shell=True, preexec_fn=os.setsid)
        print(f"Server started with PID: {process.pid}")
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\nStopping server...")
            try:
                # Send SIGTERM to the process group
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Force killing server...")
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                process.wait()
            except ProcessLookupError:
                # Process already terminated
                pass
    else:
        # Use subprocess.Popen for better signal handling in both dev and prod
        try:
            process = subprocess.Popen(serve_cmd, shell=True, preexec_fn=os.setsid)
            process.wait()
        except KeyboardInterrupt:
            print("\nStopping server...")
            try:
                # Send SIGTERM to the process group
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Force killing server...")
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                process.wait()
            except ProcessLookupError:
                # Process already terminated
                pass
        except Exception as e:
            print(f"Server exited with error: {e}")
            sys.exit(1)

    