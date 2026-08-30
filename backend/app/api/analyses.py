from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.analysis import Analysis
from app.models.patient import Patient
from app.models.medical_image import MedicalImage
from app.models.user import User
from app.schemas.analysis import AnalysisCreate, AnalysisOut
from app.api.deps import get_current_user
from app.core.config import settings

router = APIRouter(prefix="/analyses", tags=["Analyses"])


@router.post("", response_model=AnalysisOut, status_code=status.HTTP_201_CREATED)
def create_analysis(
    analysis_in: AnalysisCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Initialize a new analysis entry."""
    patient = db.query(Patient).filter(Patient.id == analysis_in.patient_id, Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    image = db.query(MedicalImage).filter(MedicalImage.id == analysis_in.image_id, MedicalImage.patient_id == patient.id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical scan not found for this patient")

    code = f"QC-AN-{uuid.uuid4().hex[:8].upper()}"
    analysis = Analysis(
        analysis_code=code,
        patient_id=patient.id,
        image_id=image.id,
        user_id=current_user.id,
        status="PENDING",
        model_mode=settings.MODEL_MODE,
        target_condition=analysis_in.target_condition or "General Cellular & Tissue Anomaly"
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


@router.get("", response_model=List[AnalysisOut])
def list_analyses(
    patient_id: Optional[int] = Query(None),
    status_filter: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve history of analyses performed by the user."""
    query = db.query(Analysis).filter(Analysis.user_id == current_user.id)
    if patient_id:
        query = query.filter(Analysis.patient_id == patient_id)
    if status_filter:
        query = query.filter(Analysis.status == status_filter)

    results = query.order_by(Analysis.created_at.desc()).offset(skip).limit(limit).all()
    return results


@router.get("/{analysis_id}", response_model=AnalysisOut)
def get_analysis_detail(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve full analysis report including hybrid prediction breakdown."""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis record not found")
    return analysis
