@echo off
echo ==========================================
echo   LEARNOVA - Quick Start Script
echo ==========================================
echo.

cd /d "c:\Users\sirid\OneDrive\Desktop\Learnova"

echo [1/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/4] Running migrations...
python manage.py migrate

echo [3/4] Starting server...
echo.
echo  Open your browser and go to:
echo  http://127.0.0.1:8000
echo.
echo  Press CTRL+C to stop the server.
echo ==========================================
python manage.py runserver
