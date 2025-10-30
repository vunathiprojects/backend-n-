#!/bin/bash
echo "🚀 Starting FastAPI on Azure..."
/home/site/wwwroot/antenv/bin/gunicorn -k uvicorn.workers.UvicornWorker app:app \
    -b 0.0.0.0:${PORT:-8000} --timeout 600 --workers 2
