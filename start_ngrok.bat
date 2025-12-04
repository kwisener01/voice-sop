@echo off
echo ================================================
echo Starting ngrok tunnel for Voice SOP Generator
echo ================================================
echo.
echo This will expose your local server (port 5000) to the internet
echo so VAPI can send webhooks to it.
echo.
echo Press Ctrl+C to stop ngrok
echo.
ngrok http 5000
