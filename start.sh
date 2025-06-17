#!/bin/bash

echo "Starting Django application..."

# Check if gunicorn is available
if command -v gunicorn &> /dev/null; then
    echo "Using gunicorn to start the application..."
    exec gunicorn mortgauge_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
else
    echo "WARNING: gunicorn not found, trying to install..."
    pip install gunicorn==21.2.0
    
    if command -v gunicorn &> /dev/null; then
        echo "Gunicorn installed successfully, starting application..."
        exec gunicorn mortgauge_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
    else
        echo "ERROR: Could not install gunicorn, falling back to Django development server..."
        echo "WARNING: This is not recommended for production!"
        exec python manage.py runserver 0.0.0.0:$PORT
    fi
fi 