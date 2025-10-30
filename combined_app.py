# combined_app.py
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from config.wsgi import application as django_app

# Create FastAPI app
app = FastAPI()

# Mount Django under /django (you can change this path)
app.mount("/django", WSGIMiddleware(django_app))

@app.get("/")
def home():
    return {"message": "Combined Django + FastAPI is running!"}
