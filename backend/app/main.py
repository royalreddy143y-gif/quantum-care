import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.database.session import engine, Base
# Import all models to ensure metadata registration
import app.models
from app.api import auth, patients, upload, analyses, predict, reports, health

# Ensure DB tables exist on startup
Base.metadata.create_all(bind=engine)

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


@app.get("/")
def root():
    return {
        "name": "QuantumCare API",
        "tagline": "Quantum Intelligence for Early Disease Detection",
        "documentation": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }
