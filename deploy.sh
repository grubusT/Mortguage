#!/bin/bash

echo "🚀 Starting Vercel Deployment Process..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Login to Vercel (if not already logged in)
echo "🔐 Logging into Vercel..."
vercel login

# Deploy to production
echo "🚀 Deploying to production..."
vercel --prod

echo "✅ Deployment complete!"
echo "🔗 Your API will be available at: https://your-app.vercel.app"
echo "📋 Next steps:"
echo "   1. Run database migrations"
echo "   2. Test your API endpoints"
echo "   3. Update frontend environment variables"
