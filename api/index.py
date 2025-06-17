import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mortgauge_project.settings')

# Import Django and configure
import django
from django.conf import settings

# Configure Django
django.setup()

# Import the WSGI application
from mortgauge_project.wsgi import application

# Vercel serverless function handler
def handler(request, context):
    """
    Vercel serverless function handler
    """
    try:
        return application(request, lambda status, headers: None)
    except Exception as e:
        # Log the error for debugging
        print(f"Error in handler: {e}")
        return {
            'statusCode': 500,
            'body': 'Internal Server Error',
            'headers': {'Content-Type': 'text/plain'}
        }

# Export the handler for Vercel
app = handler
