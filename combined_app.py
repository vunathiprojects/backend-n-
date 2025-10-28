from fastapi import FastAPI
from ai_backend.app import app as ai_app
from django.core.wsgi import get_wsgi_application
from starlette.middleware.wsgi import WSGIMiddleware
import os

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_n.settings')

# Initialize Django app
django_app = get_wsgi_application()

# Create FastAPI main app
main_app = FastAPI(title="Combined FastAPI + Django App")

# Mount FastAPI AI backend
main_app.mount("/ai", ai_app)

# Mount Django under /django
main_app.mount("/django", WSGIMiddleware(django_app))

