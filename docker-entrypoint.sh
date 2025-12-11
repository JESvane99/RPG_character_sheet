#!/bin/bash
set -e

# Function to handle shutdown signals
cleanup() {
    echo "Received shutdown signal, stopping application gracefully..."
    if [ ! -z "$SERVER_PID" ]; then
        echo "Stopping server process $SERVER_PID"
        kill -TERM "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Set default Flask environment if not provided
export FLASK_ENV="${FLASK_ENV:-production}"

# Function to wait for database to be ready (if using external DB)
wait_for_db() {
    echo "Waiting for database to be ready..."
    # Add database connection check here if using external database
    sleep 2
}

# Function to run database migrations
run_migrations() {
    echo "Running database migrations..."
    uv run alembic upgrade head
}

# Main command handling
case "$1" in
    "serve")
        echo "Starting application server in $FLASK_ENV mode..."
        wait_for_db
        run_migrations
        
        # Check if we should run in development mode
        if [ "$FLASK_ENV" = "development" ]; then
            echo "Running in development mode"
            uv run flask --app src.main run --host 0.0.0.0 --port 5000 --debug &
            SERVER_PID=$!
            wait $SERVER_PID
        else
            echo "Running in production mode"
            uv run waitress-serve --host 0.0.0.0 --port 5000 src.main:app &
            SERVER_PID=$!
            wait $SERVER_PID
        fi
        ;;
    "migrate")
        echo "Running migrations only..."
        wait_for_db
        run_migrations
        ;;
    "alembic")
        echo "Running alembic command..."
        shift
        exec uv run alembic "$@"
        ;;
    "bash")
        exec /bin/bash
        ;;
    *)
        echo "Available commands:"
        echo "  serve     - Start the application (default)"
        echo "  migrate   - Run database migrations only"
        echo "  alembic   - Run alembic commands"
        echo "  bash      - Open bash shell"
        exec "$@"
        ;;
esac
