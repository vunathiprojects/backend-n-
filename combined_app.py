from fastapi import FastAPI
from ai_backend.app import app as ai_app
from django.core.wsgi import get_wsgi_application
from starlette.middleware.wsgi import WSGIMiddleware
import os

# ✅ Correct Django settings path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# ✅ Initialize Django WSGI app
django_app = get_wsgi_application()

# ✅ Create FastAPI main app
main_app = FastAPI()

# ✅ Mount FastAPI AI backend
main_app.mount("/ai", ai_app)

# ✅ Mount Django app
main_app.mount("/", WSGIMiddleware(django_app))
