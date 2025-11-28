from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes_ingestion import router as ingestion_router
from backend.api.routes_analysis import router as analysis_router
from backend.api.routes_drafting import router as drafting_router
from backend.api.routes_health import router as health_router

app = FastAPI(
    title="Legal Compliance AI",
    description="AI-powered legal document compliance analysis and drafting",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingestion_router, prefix="/api", tags=["ingestion"])
app.include_router(analysis_router, prefix="/api", tags=["analysis"])
app.include_router(drafting_router, prefix="/api", tags=["drafting"])
app.include_router(health_router, prefix="/api", tags=["health"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
