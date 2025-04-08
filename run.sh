#!/bin/bash

# Check for required commands
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "Error: $1 is not installed. Please install it first."
        exit 1
    fi
}

# Check dependencies
check_command python3
check_command pip
check_command redis-cli

# Load environment variables
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

# Add project root to PYTHONPATH
export PYTHONPATH=$(pwd):$PYTHONPATH

# Start Redis server if not running
if ! redis-cli ping > /dev/null 2>&1; then
    echo "Starting Redis server..."
    redis-server --daemonize yes
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt --break-system-packages

# Set up directories
python3 backend/setup_directories.py

# Start Celery worker in background
echo "Starting Celery worker..."
celery -A backend.celery_config.celery_app worker --loglevel=info --hostname=worker1@%%h &

# Start Flask application
echo "Starting Flask application..."
export FLASK_APP=backend/app.py
export FLASK_ENV=development
flask --app backend/app.py run --host=0.0.0.0 --port=${PORT:-5000}

# Cleanup on exit
trap "pkill -f 'celery worker'; pkill -f 'flask run'" EXIT
