#!/bin/bash
echo "Starting FastAPI (AI Backend)..."
uvicorn ai_backend.main:app --host 0.0.0.0 --port 8001 &

echo "Starting Django Backend..."
gunicorn --bind=0.0.0.0:${PORT:-8000} config.wsgi
