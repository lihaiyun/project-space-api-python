#!/bin/bash
# Production startup script for Linux/Mac
echo "Starting Project Space API in production mode..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "Virtual environment activated"
fi

# Set production environment
export FLASK_ENV=production
export WORKERS=2
export LOG_LEVEL=info

# Start with Gunicorn
echo "Starting Gunicorn server..."
gunicorn -c gunicorn.conf.py src.app:app
