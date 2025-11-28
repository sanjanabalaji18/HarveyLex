**Deploying Locally with Docker (Backend + Frontend)**

- Build and run both services with Docker Compose from repository root:

```bash
docker compose build --pull
docker compose up -d
```

- Backend will be exposed at `http://localhost:8000` and frontend at `http://localhost:5173` (nginx serves the built frontend).

- To view backend logs:

```bash
docker compose logs -f backend
```

- To stop and remove the containers:

```bash
docker compose down
```

Local (non-Docker) quick start:

1. Backend (recommended inside virtualenv):

```bash
cd backend
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

2. Frontend:

```bash
cd frontend/app
npm ci
npm run dev
```

Notes:
- The `backend/Dockerfile` uses Python 3.11 slim. Some native dependencies (e.g., `faiss-cpu`) can increase image build time or require extra system libraries.
- The frontend image builds the Vite app and serves the static `dist` with `nginx`.
