#!/bin/bash
echo "🚀 Starting FastAPI + Django services..."

# Exit if any command fails
set -e

# === Kill old Django process (port 8181) if exists ===
echo "🧹 Checking for process on port 8181..."
PID=$(lsof -t -i:8181 || true)
if [ -n "$PID" ]; then
  echo "Killing old Django process ($PID)..."
  kill -9 $PID || true
fi

# === Kill old FastAPI process (port 8002) if exists ===
echo "🧹 Checking for process on port 8002..."
PID=$(lsof -t -i:8002 || true)
if [ -n "$PID" ]; then
  echo "Killing old FastAPI process ($PID)..."
  kill -9 $PID || true
fi

# === Start FastAPI Backend ===
echo "⚡ Starting FastAPI backend on port 8002..."
cd ai_backend
nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 8002 > ../fastapi.log 2>&1 &
cd ..

sleep 3

# === Start Django Backend ===
echo "🌐 Starting Django backend on port 8181..."
cd django_backend
nohup gunicorn config.wsgi:application --bind 0.0.0.0:8181 > ../django.log 2>&1 &
cd ..

sleep 3

# === Done ===
echo "✅ Both FastAPI and Django are running!"
echo "📜 Logs:"
echo "   • FastAPI → fastapi.log"
echo "   • Django  → django.log"
