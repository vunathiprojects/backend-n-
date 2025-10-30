
#!/bin/bash
echo "🚀 Starting FastAPI + Django services (Azure-compatible)..."

# -------------------------------------------------------
# Detect Python & Gunicorn paths dynamically
# -------------------------------------------------------
PYTHON_PATH=$(which python3)
GUNICORN_PATH=$(which gunicorn)

echo "🐍 Using Python at: $PYTHON_PATH"
echo "🔫 Using Gunicorn at: $GUNICORN_PATH"

if [ -z "$PYTHON_PATH" ]; then
  echo "❌ Python3 not found!"
  exit 1
fi

if [ -z "$GUNICORN_PATH" ]; then
  echo "⚠️ Gunicorn not found — installing..."
  pip install gunicorn
  GUNICORN_PATH=$(which gunicorn)
fi

# -------------------------------------------------------
# Read Azure port
# -------------------------------------------------------
export PORT=${PORT:-8000}
echo "🔌 Azure expects app to listen on port: $PORT"

# -------------------------------------------------------
# Cleanup section
# -------------------------------------------------------
echo "🧹 Checking for old processes..."
pkill -f gunicorn || true
pkill -f uvicorn || true
pkill -f python || true
sleep 3

# -------------------------------------------------------
# Start Django backend (internal use)
# -------------------------------------------------------
echo "🌐 Starting Django backend on port 8183..."
nohup $GUNICORN_PATH config.wsgi:application --bind 0.0.0.0:8183 > django.log 2>&1 &

# -------------------------------------------------------
# Start FastAPI backend (public-facing)
# -------------------------------------------------------
echo "⚡ Starting FastAPI backend on Azure port $PORT..."
nohup $PYTHON_PATH -m uvicorn ai_backend.app:app --host 0.0.0.0 --port $PORT > fastapi.log 2>&1 &

echo "✅ Both FastAPI (on $PORT) and Django (on 8183) are running!"
echo "📜 Logs:"
echo "   • FastAPI → fastapi.log"
echo "   • Django  → django.log"

# Keep container alive
tail -f fastapi.log django.log
