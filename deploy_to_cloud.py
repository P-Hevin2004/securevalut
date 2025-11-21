#!/usr/bin/env python3
"""
Script to help deploy the file sharing system to cloud platforms
"""
import os

def show_deployment_options():
    print("☁️  Cloud Deployment Options for File Sharing")
    print("=" * 60)
    print()
    print("🚀 Option 1: Railway (Recommended - Free)")
    print("   1. Go to: https://railway.app")
    print("   2. Sign up with GitHub")
    print("   3. Create new project from GitHub repo")
    print("   4. Add environment variables:")
    print("      - SECRET_KEY: your-secret-key")
    print("      - DEBUG: False")
    print("   5. Deploy automatically!")
    print()
    print("🚀 Option 2: Heroku (Free tier available)")
    print("   1. Install Heroku CLI")
    print("   2. Create Procfile: web: python manage.py runserver 0.0.0.0:$PORT")
    print("   3. Deploy: heroku create your-app-name")
    print("   4. Push: git push heroku main")
    print()
    print("🚀 Option 3: PythonAnywhere (Free)")
    print("   1. Go to: https://pythonanywhere.com")
    print("   2. Create free account")
    print("   3. Upload your project files")
    print("   4. Configure web app")
    print()
    print("🚀 Option 4: Render (Free)")
    print("   1. Go to: https://render.com")
    print("   2. Connect your GitHub repo")
    print("   3. Deploy as web service")
    print()
    print("💡 After deployment:")
    print("   - Your files will be accessible worldwide")
    print("   - QR codes will work from any device")
    print("   - No network configuration needed")
    print("=" * 60)

def create_production_settings():
    """Create production settings file"""
    prod_settings = '''
# Production settings for cloud deployment
import os

# Use environment variables for security
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
DEBUG = False
ALLOWED_HOSTS = ['*']  # Configure with your domain

# Database (use PostgreSQL for production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
'''
    
    with open('production_settings.py', 'w') as f:
        f.write(prod_settings)
    print("✅ Created production_settings.py")

def create_requirements():
    """Create production requirements"""
    requirements = '''Django==5.0.7
Pillow==10.0.0
qrcode[pil]==8.2
gunicorn==21.2.0
psycopg2-binary==2.9.7
'''
    
    with open('requirements_production.txt', 'w') as f:
        f.write(requirements)
    print("✅ Created requirements_production.txt")

def create_procfile():
    """Create Procfile for Heroku/Railway"""
    procfile = '''web: python manage.py runserver 0.0.0.0:$PORT
'''
    
    with open('Procfile', 'w') as f:
        f.write(procfile)
    print("✅ Created Procfile")

if __name__ == "__main__":
    show_deployment_options()
    print("\n🔧 Creating deployment files...")
    create_production_settings()
    create_requirements()
    create_procfile()
    print("\n✅ Deployment files created!")
    print("📁 Files created:")
    print("   - production_settings.py")
    print("   - requirements_production.txt") 
    print("   - Procfile")
