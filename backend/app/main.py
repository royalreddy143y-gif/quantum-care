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

# Ensure DB tables exist and demo data is seeded on startup
Base.metadata.create_all(bind=engine)
try:
    seed_demo_data()
except Exception as e:
    print(f"[*] Seed data initialization notice: {e}")

app = FastAPI(
    title="QuantumCare API",
    description="Hybrid Quantum Machine Learning Platform for Early Disease Detection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits localhost dev ports seamlessly
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving for medical scans
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Mount API Routers
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(patients.router, prefix=settings.API_V1_STR)
app.include_router(upload.router, prefix=settings.API_V1_STR)
app.include_router(analyses.router, prefix=settings.API_V1_STR)
app.include_router(predict.router, prefix=settings.API_V1_STR)
app.include_router(reports.router, prefix=settings.API_V1_STR)


from fastapi.responses import FileResponse

# Check for frontend build directory (Single-Service Full-Stack Deployment)
FRONTEND_DIST_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")
)

if os.path.exists(FRONTEND_DIST_DIR) and os.path.exists(os.path.join(FRONTEND_DIST_DIR, "index.html")):
    assets_dir = os.path.join(FRONTEND_DIST_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIST_DIR, "index.html"))

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Allow standard API / docs routes to be handled by FastAPI
        if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("redoc") or full_path.startswith("openapi.json"):
            from fastapi import HTTPException
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
            "health": f"{settings.API_V1_STR}/health"
        }

