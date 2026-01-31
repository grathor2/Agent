#!/bin/bash
# Script to start the Collaborative Agent System server

cd /Users/gauravr/Downloads/artifacts

# Activate virtual environment
source venv/bin/activate

# Start server
echo "Starting Collaborative Agent System..."
echo "Server will be available at: http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

python run.py
