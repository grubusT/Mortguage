# Mortgage Broking Operations Assistant - Project Notes

## Project Overview
Full-stack application for mortgage broking operations using:
- Frontend: React
- Backend: Django
- Database: MySQL
- Real-time updates: WebSocket

## Project Structure
\`\`\`
Mortguage/
├── broker_operations/     # Main Django application
├── frontend/             # React frontend
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── Procfile            # Deployment configuration
├── build.sh            # Build script
└── wsgi.py             # WSGI configuration
\`\`\`

## Key Components

### Backend API Endpoints
1. Authentication
   - POST /auth/login
   - POST /auth/register
   - POST /auth/logout
   - GET /auth/me

2. Client Management
   - GET /clients
   - POST /clients
   - GET /clients/:id
   - PUT /clients/:id
   - DELETE /clients/:id
   - GET /clients/search?q=query

3. Document Handling
   - GET /documents
   - POST /clients/:id/documents
   - GET /clients/:id/documents
   - PUT /documents/:id
   - DELETE /documents/:id

4. Application Processing
   - GET /applications
   - POST /applications
   - GET /clients/:id/applications
   - PUT /applications/:id
   - PATCH /applications/:id/status

5. Dashboard
   - GET /dashboard/summary
   - GET /dashboard/activity
   - GET /dashboard/reminders
   - GET /dashboard/tasks

6. WebSocket
   - /ws (for real-time updates)

### Data Models
1. Client
   - Personal information
   - Contact details
   - Application history

2. Document
   - File information
   - Client association
   - Upload metadata

3. Application
   - Status tracking
   - Client association
   - Processing details

4. Task
   - Priority levels
   - Due dates
   - Assignment

5. Reminder
   - Client association
   - Application association
   - Notification settings

## Recent Changes and Fixes
1. Project Structure
   - Moved from nested backend structure to root-level Django project
   - Updated import paths and configurations
   - Consolidated settings and configurations

2. Dependencies
   - Added django-filter==24.1
   - Updated requirements.txt
   - Configured CORS settings

3. Deployment Configuration
   - Updated Procfile for correct WSGI application
   - Modified build.sh for proper static file handling
   - Configured environment variables

## Environment Variables
Required environment variables:
- DJANGO_SECRET_KEY
- DJANGO_DEBUG
- DJANGO_ALLOWED_HOSTS
- DATABASE_URL
- REDIS_URL

## CORS Configuration
Allowed origins:
- https://mortguage.onrender.com
- https://v0.dev
- https://v0.dev/chat/mortgage-broker-portal-VnsfF8iSSOS
- http://localhost:3000
- http://127.0.0.1:3000

## Next Steps
1. Complete API endpoint implementation
2. Set up WebSocket connections
3. Implement frontend components
4. Configure production database
5. Set up CI/CD pipeline

## Known Issues
1. Port binding issues (resolved with updated wsgi.py)
2. Module import errors (resolved with project structure changes)
3. Static file serving (resolved with build.sh updates)
