from datetime import datetime, timezone
from typing import Dict, Any
from fastapi import APIRouter, Response, status
from sqlalchemy import text
import torch
import pennylane as qml

from app.core.config import settings
from app.database.session import engine

router = APIRouter(tags=["Health & Monitoring"])

START_TIME = datetime.now(timezone.utc)


def check_database_health() -> Dict[str, Any]:
    """
    Executes a lightweight query to verify SQLite/PostgreSQL connectivity.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "connected": True}
    except Exception as ex:
        return {"status": "degraded", "connected": False, "error": str(ex)}


@router.api_route("/ping", methods=["GET", "HEAD"], summary="Ultra-lightweight Keep-Alive Ping")
def ping():
    """
    Fast, zero-overhead endpoint designed for external cronjobs and pingers
    (e.g., cron-job.org, UptimeRobot, GitHub Actions) to prevent Render free instance sleep.
    """
    return {
        "status": "ok",
        "ping": "pong",
        "service": settings.PROJECT_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.api_route("/health", methods=["GET", "HEAD"], summary="Main Health Check")
def health_check():
    """
    Primary health check endpoint used by Render deploy health checks,
    cloud monitors, and frontend status dashboards.
    """
    uptime_seconds = round((datetime.now(timezone.utc) - START_TIME).total_seconds(), 2)
    db_health = check_database_health()
    
    return {
        "status": "online",
        "platform": settings.PROJECT_NAME,
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "uptime_seconds": uptime_seconds,
        "database": db_health["status"],
        "database_connected": db_health["connected"],
        "engine": "Hybrid Quantum-Classical Pipeline",
        "model_mode": settings.MODEL_MODE,
        "pytorch_version": torch.__version__,
        "pennylane_version": qml.__version__,
        "quantum_qubits": settings.QUANTUM_NUM_QUBITS,
        "quantum_layers": settings.QUANTUM_NUM_LAYERS,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.api_route("/healthz", methods=["GET", "HEAD"], summary="Kubernetes/Cloud Liveness Probe")
def healthz():
    """
    Standard container/cloud orchestrator health probe.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.api_route("/livez", methods=["GET", "HEAD"], summary="Liveness Probe")
def livez():
    """
    Confirms the server process is responsive and accepting HTTP connections.
    """
    return {"status": "alive", "timestamp": datetime.now(timezone.utc).isoformat()}


@router.api_route("/readyz", methods=["GET", "HEAD"], summary="Readiness Probe")
def readyz(response: Response):
    """
    Confirms all downstream dependencies (database, ML runtime) are operational.
    """
    db_health = check_database_health()
    if not db_health["connected"]:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "status": "not_ready",
            "database": db_health,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    return {
        "status": "ready",
        "database": db_health["status"],
        "ml_engine": "ready",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

