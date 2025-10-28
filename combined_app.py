from fastapi import FastAPI
from ai_backend.app import app as ai_app
from django.core.wsgi import get_wsgi_application
from starlette.middleware.wsgi import WSGIMiddleware
import os

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend-n.settings')
django_app = get_wsgi_application()

# Create main FastAPI app
main_app = FastAPI()

# Mount FastAPI AI backend
main_app.mount("/ai", ai_app)

# Mount Django app under /django
main_app.mount("/django", WSGIMiddleware(django_app))
