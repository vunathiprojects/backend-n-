#!/bin/bash
echo "🚀 Starting FastAPI + Django (Combined App)..."

# Stop on error
set -e

# Add user/local bin paths
export PATH=$PATH:/home/.local/bin:/home/site/wwwroot/.local/bin

# Confirm Python path
echo "🐍 Python path: $(which python3)"
python3 --version

# Kill any leftover processes
pkill -f "uvicorn" || true
pkill -f "gunicorn" || true

# Start combined app
echo "⚡ Starting combined FastAPI + Django..."
nohup python3 -m uvicorn combined_app:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &

echo "✅ App started!"
echo "📜 Logs: tail -f /home/site/wwwroot/app.log"
