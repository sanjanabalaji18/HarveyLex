# Harvey Lex - Integrated Deployment

This project is configured to run as a single integrated product using Docker.

## Architecture

- **Frontend**: React/Vite app served by Nginx.
- **Backend**: FastAPI app running on Uvicorn.
- **Integration**: Nginx acts as a reverse proxy.
  - Static files are served from `/`.
  - API requests to `/api/*` are proxied to the backend.

## Running the Application

Use the provided deployment script:

```bash
./deploy.sh
```

## Accessing the Application

Once running, you only need to access the Frontend URL:

- **Application URL**: [http://localhost:5173](http://localhost:5173)

The frontend will automatically communicate with the backend through this same URL (e.g., `http://localhost:5173/api/...`).

## Troubleshooting

- **Logs**: `docker compose logs -f`
- **Stop**: `docker compose down`
