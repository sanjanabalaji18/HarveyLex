#!/bin/bash
set -e

echo "Starting deployment with Docker..."

# Check if docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker is not running or not installed."
  exit 1
fi

echo "Building Backend (using host network to avoid DNS issues)..."
docker build --network=host -t harvey-backend:latest -f backend/Dockerfile .

echo "Building Frontend (using host network to avoid DNS issues)..."
docker build --network=host -t harvey-frontend:latest -f frontend/app/Dockerfile .

echo "Starting services..."
docker compose up -d

echo "Deployment successful!"
echo "Backend is running at: http://localhost:8000"
echo "Frontend is running at: http://localhost:5173"
echo ""
echo "To view backend logs: docker compose logs -f backend"
echo "To stop services: docker compose down"
