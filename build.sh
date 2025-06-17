#!/bin/bash

echo "Starting build process for Render..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run Django migrations
echo "Running Django migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if needed (optional)
# echo "Creating superuser..."
# python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

echo "Build completed successfully!"
