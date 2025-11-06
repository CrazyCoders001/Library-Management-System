#!/bin/bash

echo "======================================"
echo "Library Management System - Startup"
echo "======================================"
echo ""

cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting Flask server..."
echo "Server will run at: http://localhost:5000"
echo ""
echo "To access the application:"
echo "Open index.html in your browser or visit http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py

