#!/bin/bash

echo "Starting FastAPI application..."

# Activate virtual environment (if you're using one)
if [ -f "/home/site/wwwroot/antenv/bin/activate" ]; then
    source /home/site/wwwroot/antenv/bin/activate
fi

# Start the FastAPI app with uvicorn
# Adjust the path to your main FastAPI app file
cd ai_backend
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 4
