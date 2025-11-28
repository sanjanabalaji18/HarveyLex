#!/bin/bash

# Function to kill processes on exit
cleanup() {
    echo ""
    echo "Stopping services..."
    if [ -n "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ -n "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    exit
}

trap cleanup SIGINT

echo "Starting local development environment..."

# Start Backend
echo "Starting Backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "Installing backend dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "Starting Uvicorn..."
uvicorn main:app --reload --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!
cd ..

# Start Frontend
echo "Starting Frontend..."
cd frontend/app
echo "Installing frontend dependencies..."
npm install > /dev/null 2>&1
echo "Starting Vite..."
npm run dev &
FRONTEND_PID=$!
cd ../..

echo "Services running. Press Ctrl+C to stop."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"

wait
