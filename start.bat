@echo off
echo ========================================
echo Starting Django Backend (LMS) on Port 8001
echo ========================================
echo.
echo Make sure you have:
echo 1. Configured database in config/settings.py
echo 2. Run migrations: python manage.py migrate
echo 3. Installed requirements: pip install -r requirements.txt
echo.
python manage.py runserver 8001

