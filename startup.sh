#!/bin/bash
echo "Starting FastAPI (AI Backend)..."

# Kill any process using port 8181 (Django port)
echo "Checking and killing any process using port 8181..."
python3 - <<'EOF'
import os, socket, subprocess
try:
    s = socket.socket()
    s.bind(("0.0.0.0", 8181))
    s.close()
except OSError:
    print("Port 8181 is in use — trying to kill process...")
    try:
        out = subprocess.check_output("ps aux | grep gunicorn | grep 8181 | awk '{print $2}'", shell=True)
        for pid in out.decode().split():
            os.system(f"kill -9 {pid}")
            print(f"Killed PID {pid}")
    except Exception as e:
        print(f"Could not kill old process: {e}")
EOF

# Start FastAPI (port 8002)
( cd ai_backend && nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 8002 & )

# Start Django (port 8181)
echo "Starting Django Backend..."
( nohup gunicorn config.wsgi:application --bind 0.0.0.0:8181 & )

echo "Both backends started!"


