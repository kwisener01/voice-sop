#!/bin/bash
# Startup script for Railway
PORT=${PORT:-5000}
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120
