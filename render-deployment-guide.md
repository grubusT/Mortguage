# Render Deployment Guide for Mortgage Broker Portal

## Prerequisites
- GitHub account with your code repository
- Render account (free at render.com)

## Step 1: Prepare Your Repository

1. **Push your code to GitHub** (already done)
2. **Ensure these files are in your repository**:
   - `render.yaml` (deployment configuration)
   - `requirements.txt` (Python dependencies)
   - `build.sh` (build script)
   - `mortgauge_project/settings.py` (Django settings)

## Step 2: Deploy to Render

### Option A: Using render.yaml (Recommended)

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** → **"Blueprint"**
3. **Connect your GitHub repository**
4. **Select the repository**: `grubusT/Mortguage`
5. **Render will automatically detect the `render.yaml` file**
6. **Click "Apply"** to deploy

### Option B: Manual Deployment

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service**:
   - **Name**: `mortgauge-django-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn mortgauge_project.wsgi:application`
   - **Plan**: Free

5. **Add Environment Variables**:
   ```
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=mortgauge-django-api.onrender.com
   CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
   ```

6. **Create Database**:
   - Click "New +" → "PostgreSQL"
   - Name: `mortgauge-db`
   - Plan: Free
   - Copy the connection string

7. **Link Database to Web Service**:
   - Go back to your web service
   - Add environment variable: `DATABASE_URL` with the connection string

## Step 3: Configure Frontend

Update your Next.js frontend to use the new API URL:

```typescript
// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://mortgauge-django-api.onrender.com';

export const api = {
  baseURL: API_BASE_URL,
  // ... rest of your API configuration
};
```

## Step 4: Environment Variables

### Backend (Render)
```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=mortgauge-django-api.onrender.com
DATABASE_URL=postgres://... (provided by Render)
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
```

### Frontend (Vercel)
```
NEXT_PUBLIC_API_URL=https://mortgauge-django-api.onrender.com
```

## Step 5: Test Your Deployment

1. **Check the API**: Visit `https://mortgauge-django-api.onrender.com/api/`
2. **Check Admin**: Visit `https://mortgauge-django-api.onrender.com/admin/`
3. **Check Swagger**: Visit `https://mortgauge-django-api.onrender.com/swagger/`

## Troubleshooting

### Common Issues:

1. **Build Fails**:
   - Check the build logs in Render dashboard
   - Ensure all dependencies are in `requirements.txt`

2. **Database Connection Issues**:
   - Verify `DATABASE_URL` is set correctly
   - Check if database is created and running

3. **CORS Issues**:
   - Update `CORS_ALLOWED_ORIGINS` with your frontend domain
   - Ensure the domain format is correct (https://...)

4. **Static Files Not Loading**:
   - Check if `collectstatic` ran successfully
   - Verify `STATIC_ROOT` is set correctly

### Useful Commands:

```bash
# Check logs
# Go to Render dashboard → Your service → Logs

# Run migrations manually (if needed)
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Benefits of Render Deployment

✅ **No Cold Starts**: Traditional server deployment
✅ **Database Included**: PostgreSQL with connection pooling
✅ **Automatic HTTPS**: SSL certificates included
✅ **Easy Scaling**: Can upgrade to paid plans
✅ **Better Performance**: Faster than serverless for Django
✅ **Real-time Logs**: Easy debugging and monitoring

## Next Steps

1. **Deploy the backend to Render**
2. **Update your frontend API configuration**
3. **Test all endpoints**
4. **Set up monitoring and alerts**
5. **Configure custom domain (optional)** 