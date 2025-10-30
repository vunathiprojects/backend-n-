#!/bin/bash
export PATH=$PATH:/home/.local/bin
echo "🚀 Starting Combined Django + FastAPI app on port 8000..."

# Stop if any command fails
set -e

# === Kill any old process using port 8000 ===
echo "🧹 Checking for process on port 8000..."
PID=$(netstat -tuln 2>/dev/null | grep ":8000 " | awk '{print $7}' | cut -d'/' -f1)
if [ -n "$PID" ]; then
  echo "Killing old process ($PID)..."
  kill -9 $PID || true
fi

# === Start Combined App (Django + FastAPI) ===
echo "⚡ Launching Uvicorn (combined_app.py) on port 8000..."
nohup python3 -m uvicorn combined_app:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &

sleep 3

echo "✅ Combined app started successfully!"
echo "📜 Logs: app.log"
