FROM python:3.11-slim

WORKDIR /app

# Install minimal build tools (faiss or other wheels may need them)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
 && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./backend

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
