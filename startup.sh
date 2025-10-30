#!/bin/bash
echo "🚀 Starting FastAPI + Django services..."

# Stop if any command fails
set -e

# === Kill old Django (port 8181) ===
echo "🧹 Checking for process on port 8181..."
PID=$(netstat -tuln 2>/dev/null | grep ":8181 " | awk '{print $7}' | cut -d'/' -f1)
if [ -n "$PID" ]; then
  echo "Killing old Django process ($PID)..."
  kill -9 $PID || true
fi

# === Kill old FastAPI (port 8002) ===
echo "🧹 Checking for process on port 8002..."
PID=$(netstat -tuln 2>/dev/null | grep ":8002 " | awk '{print $7}' | cut -d'/' -f1)
if [ -n "$PID" ]; then
  echo "Killing old FastAPI process ($PID)..."
  kill -9 $PID || true
fi

# === Start FastAPI Backend ===
echo "⚡ Starting FastAPI backend on port 8002..."
cd ai_backend || { echo "❌ ai_backend folder not found!"; exit 1; }
nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 8002 > ../fastapi.log 2>&1 &
cd ..

sleep 3

# === Start Django Backend ===
echo "🌐 Starting Django backend on port 8181..."
nohup gunicorn config.wsgi:application --bind 0.0.0.0:8181 > django.log 2>&1 &

sleep 3

echo "✅ Both FastAPI and Django are running!"
echo "📜 Logs:"
echo "   • FastAPI → fastapi.log"
echo "   • Django  → django.log"
