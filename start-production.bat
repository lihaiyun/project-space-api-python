@echo off
REM Production startup script for Windows
echo Starting Project Space API in production mode...

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated
)

REM Set production environment
set FLASK_ENV=production
set WORKERS=2
set LOG_LEVEL=info

REM Start with Gunicorn
echo Starting Gunicorn server...
gunicorn -c gunicorn.conf.py src.app:app

pause
