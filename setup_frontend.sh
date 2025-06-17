#!/bin/bash

echo "🎨 Setting up frontend environment..."

# Get the backend URL from user
read -p "Enter your Vercel backend URL (e.g., https://mortguage.vercel.app): " BACKEND_URL

# Create or update .env.local
cat > .env.local << EOF
# Backend API Configuration
NEXT_PUBLIC_API_URL=${BACKEND_URL}

# Optional: Add other environment variables
# NEXT_PUBLIC_APP_NAME=Mortgage Broker Portal
# NEXT_PUBLIC_VERSION=1.0.0
EOF

echo "✅ Frontend environment configured!"
echo "📝 Created .env.local with:"
echo "   NEXT_PUBLIC_API_URL=${BACKEND_URL}"
echo ""
echo "🚀 You can now run your frontend with:"
echo "   npm run dev"
