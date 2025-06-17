#!/bin/bash

echo "Starting build process for Render..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Verify gunicorn is installed
echo "Verifying gunicorn installation..."
gunicorn --version || {
    echo "ERROR: gunicorn not found. Installing..."
    pip install gunicorn==21.2.0
}

# Run Django migrations
echo "Running Django migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Verify the Django app can start
echo "Testing Django application..."
python manage.py check --deploy

# Create superuser if needed (optional)
# echo "Creating superuser..."
# python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

echo "Build completed successfully!"
