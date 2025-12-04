#!/bin/bash

echo "================================================"
echo "Voice SOP Generator - Startup Script"
echo "================================================"
echo ""

# Activate virtual environment
if [ -f venv/bin/activate ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment not found!"
    echo "Please run: python -m venv venv"
    exit 1
fi

echo ""
echo "Virtual environment activated!"
echo ""
echo "Available commands:"
echo "  1. Install dependencies:  pip install -r requirements.txt"
echo "  2. Run setup:             python setup.py"
echo "  3. Start application:     python app.py"
echo "  4. Start with Docker:     docker-compose up"
echo ""
echo "Current environment: $VIRTUAL_ENV"
echo ""

# Start a new shell with the virtual environment activated
$SHELL
