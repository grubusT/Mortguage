# Vercel Deployment Configuration

## Required Environment Variables

Add these to your Vercel project settings:

### Django Settings
```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app.vercel.app
```

### Database Configuration (Neon/Postgres)
```
PGDATABASE=your-database-name
PGUSER=your-database-user
PGPASSWORD=your-database-password
PGHOST=your-database-host
PGPORT=5432
```

### CORS Settings
```
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

## Build Command
```bash
chmod +x build.sh && ./build.sh
```

## Output Directory
```
.next
```

## Install Command
```bash
npm install && pip install -r requirements.txt
``` 