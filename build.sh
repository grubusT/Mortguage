#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Add backend directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend

# Run migrations
cd backend
python manage.py migrate 