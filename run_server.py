#!/usr/bin/env python3
"""
Startup script for Railway deployment
Handles PORT environment variable and starts gunicorn
"""
import os
import sys
import subprocess

# Get PORT from environment, default to 5000
port = os.environ.get('PORT', '5000')

# Validate port is a number
try:
    port_num = int(port)
    if not (1 <= port_num <= 65535):
        print(f"Error: PORT {port} is out of valid range (1-65535)", file=sys.stderr)
        sys.exit(1)
except ValueError:
    print(f"Error: PORT '{port}' is not a valid port number", file=sys.stderr)
    sys.exit(1)

# Build gunicorn command
cmd = [
    'gunicorn',
    'app:app',
    '--bind', f'0.0.0.0:{port}',
    '--workers', '4',
    '--timeout', '120',
    '--log-level', 'info'
]

print(f"Starting gunicorn on port {port}...")
print(f"Command: {' '.join(cmd)}")

# Execute gunicorn
os.execvp('gunicorn', cmd)
