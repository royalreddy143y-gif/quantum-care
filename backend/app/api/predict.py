import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.analysis import Analysis
from app.models.prediction import Prediction
from app.models.patient import Patient
from app.models.medical_image import MedicalImage
from app.models.user import User
from app.schemas.analysis import PredictRequest, AnalysisOut
from app.api.deps import get_current_user
from app.ml.hybrid_model import run_hybrid_inference
from app.core.config import settings

router = APIRouter(prefix="/predict", tags=["Prediction Pipeline"])


@router.post("", response_model=AnalysisOut, status_code=status.HTTP_200_OK)
def trigger_prediction(
    req: PredictRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Executes the full hybrid pipeline:
    Image Preprocessing -> Swin Transformer -> Feature Reduction -> PennyLane VQC -> Hybrid Classification.
    """
    patient = db.query(Patient).filter(Patient.id == req.patient_id, Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient record not found")

    image = db.query(MedicalImage).filter(MedicalImage.id == req.image_id, MedicalImage.patient_id == patient.id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical image not found")

    # Run hybrid classical-quantum inference
    try:
        inference_result = run_hybrid_inference(
            image_path=image.file_path,
            biomarkers=patient.biomarkers,
            genomics=patient.genomics,
            override_mode=req.override_mode
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference pipeline execution error: {str(e)}"
        )

    # Create or update Analysis
    code = f"QC-AN-{uuid.uuid4().hex[:8].upper()}"
    analysis = Analysis(
        analysis_code=code,
        patient_id=patient.id,
        image_id=image.id,
        user_id=current_user.id,
        status="COMPLETED",
        model_mode=inference_result["model_mode"],
        target_condition=req.target_condition or "General Cellular & Tissue Anomaly"
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # Save Prediction outcome
    prediction = Prediction(
        analysis_id=analysis.id,
        prediction_label=inference_result["prediction_label"],
        confidence_score=inference_result["confidence_score"],
        risk_category=inference_result["risk_category"],
        classical_features=inference_result["classical_features"],
        quantum_features=inference_result["quantum_features"],
        fusion_weights=inference_result["fusion_weights"],
        explanation=inference_result["explanation"],
        processing_time_ms=inference_result["processing_time_ms"]
    )
    db.add(prediction)
    db.commit()
    db.refresh(analysis)

    return analysis
