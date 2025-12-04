@echo off
echo ================================================
echo Voice SOP Generator - Startup Script
echo ================================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

echo.
echo Virtual environment activated!
echo.
echo Available commands:
echo   1. Install dependencies:  pip install -r requirements.txt
echo   2. Run setup:             python setup.py
echo   3. Start application:     python app.py
echo   4. Start with Docker:     docker-compose up
echo.
echo Current environment: %VIRTUAL_ENV%
echo.

cmd /k
