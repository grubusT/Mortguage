#!/usr/bin/env python
"""
Script to run database migrations after deployment
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def run_migrations():
    """Run Django migrations"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mortgauge_project.settings')
    django.setup()
    
    print("🔄 Running database migrations...")
    
    try:
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully!")
        
        # Create superuser if needed
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(is_superuser=True).exists():
            print("👤 Creating superuser...")
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'  # Change this!
            )
            print("✅ Superuser created! Username: admin, Password: admin123")
            
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_migrations()
