import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.database.session import engine, Base
# Import all models to ensure metadata registration
import app.models
from app.api import auth, patients, upload, analyses, predict, reports, health
from app.utils.seed_data import seed_demo_data
from app.database.mongodb import init_mongo_indexes

# Ensure DB tables exist and demo data is seeded on startup if configured
Base.metadata.create_all(bind=engine)
if settings.SEED_DEMO_DATA:
    try:
        seed_demo_data()
    except Exception as e:
        print(f"[*] Seed data initialization notice: {e}")

# Initialize MongoDB Atlas indexes if configured
try:
    init_mongo_indexes()
except Exception as e:
    print(f"[*] MongoDB Atlas initialization notice: {e}")

app = FastAPI(
    title="QuantumCare API",
    description="Hybrid Quantum Machine Learning Platform for Early Disease Detection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration (supports separate frontend deployment and local development)
cors_origins = settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Static file serving for medical scans
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Mount Health Routers at root (for Render healthCheckPath /health, /ping, /healthz) and under /api
app.include_router(health.router)
app.include_router(health.router, prefix=settings.API_V1_STR)

# Mount Application Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(patients.router, prefix=settings.API_V1_STR)
app.include_router(upload.router, prefix=settings.API_V1_STR)
app.include_router(analyses.router, prefix=settings.API_V1_STR)
app.include_router(predict.router, prefix=settings.API_V1_STR)
app.include_router(reports.router, prefix=settings.API_V1_STR)


from fastapi.responses import FileResponse
from fastapi import HTTPException

# Check for frontend build directory (Single-Service Full-Stack Deployment)
FRONTEND_DIST_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")
)

HEALTH_PATHS = {"health", "healthz", "ping", "livez", "readyz"}

if os.path.exists(FRONTEND_DIST_DIR) and os.path.exists(os.path.join(FRONTEND_DIST_DIR, "index.html")):
    assets_dir = os.path.join(FRONTEND_DIST_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIST_DIR, "index.html"))

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Allow standard API / docs / health routes to be handled by FastAPI
        clean_path = full_path.strip("/")
        if (
            clean_path.startswith("api")
            or clean_path.startswith("docs")
            or clean_path.startswith("redoc")
            or clean_path.startswith("openapi.json")
            or clean_path in HEALTH_PATHS
            or any(clean_path.startswith(f"{hp}/") for hp in HEALTH_PATHS)
        ):
            raise HTTPException(status_code=404, detail="Not Found")
        file_path = os.path.join(FRONTEND_DIST_DIR, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIST_DIR, "index.html"))
else:
    @app.get("/")
    def root():
        return {
            "name": "QuantumCare API",
            "tagline": "Quantum Intelligence for Early Disease Detection",
            "documentation": "/docs",
            "health": "/health",
            "ping": "/ping",
            "api_health": f"{settings.API_V1_STR}/health"
        }


