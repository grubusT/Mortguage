# Deploying to Vercel - Step by Step Guide

## 1. Prepare Your Database

### Option A: Use Vercel Postgres (Recommended)
1. Go to your Vercel dashboard
2. Navigate to Storage → Create Database → Postgres
3. Copy the connection string

### Option B: Use External Database (Neon, PlanetScale, etc.)
1. Create a database on your preferred provider
2. Get the connection string

## 2. Set Environment Variables in Vercel

Go to your Vercel project settings and add these environment variables:

\`\`\`
DATABASE_URL=your_database_connection_string
DJANGO_SECRET_KEY=your_secret_key_here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app.vercel.app
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
\`\`\`

## 3. Deploy Backend to Vercel

### Method 1: Using Vercel CLI
\`\`\`bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from your project root
vercel --prod
\`\`\`

### Method 2: Using Git Integration
1. Push your code to GitHub
2. Connect your GitHub repo to Vercel
3. Vercel will automatically deploy

## 4. Run Database Migrations

After deployment, you need to run migrations:

### Option A: Using Vercel CLI
\`\`\`bash
vercel exec -- python manage.py migrate
\`\`\`

### Option B: Create a migration endpoint (temporary)
Add this to your Django views for one-time setup:

```python
from django.http import JsonResponse
from django.core.management import call_command

def migrate_db(request):
    if request.method == 'POST':
        call_command('migrate')
        return JsonResponse({'status': 'Migrations completed'})
    return JsonResponse({'error': 'POST method required'})
