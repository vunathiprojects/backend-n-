#!/bin/bash
echo "Starting FastAPI (AI Backend)..."
uvicorn ai_backend.app:app --host 0.0.0.0 --port 8001 &

echo "Starting Django Backend..."
gunicorn --bind=0.0.0.0:$PORT config.wsgi

