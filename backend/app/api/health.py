from datetime import datetime, timezone
from fastapi import APIRouter
import torch
import pennylane as qml
from app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    """
    Returns system status and active ML/QML engine status.
    """
    return {
        "status": "online",
        "platform": settings.PROJECT_NAME,
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "engine": "Hybrid Quantum-Classical Pipeline",
        "pytorch_version": torch.__version__,
        "pennylane_version": qml.__version__,
        "quantum_qubits": settings.QUANTUM_NUM_QUBITS,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
