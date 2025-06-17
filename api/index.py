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

def handler(request, context):
    """
    Vercel serverless function handler for Django
    """
    try:
        # Create a simple WSGI environment
        environ = {
            'REQUEST_METHOD': request.get('method', 'GET'),
            'SCRIPT_NAME': '',
            'PATH_INFO': request.get('path', '/'),
            'QUERY_STRING': request.get('query', ''),
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': None,
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': True,
        }
        
        # Add headers
        headers = request.get('headers', {})
        for key, value in headers.items():
            environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
        
        # Call Django application
        def start_response(status, headers, exc_info=None):
            return status, headers
        
        response = application(environ, start_response)
        
        # Convert response to Vercel format
        status_code = int(response[0].split()[0])
        response_headers = dict(response[1])
        body = b''.join(response[2]).decode('utf-8')
        
        return {
            'statusCode': status_code,
            'body': body,
            'headers': response_headers
        }
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error in handler: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'body': f'Internal Server Error: {str(e)}',
            'headers': {'Content-Type': 'text/plain'}
        }

# Export the handler for Vercel
app = handler
