from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.patient import PatientOut


class PredictionOut(BaseModel):
    id: int
    analysis_id: int
    prediction_label: str
    confidence_score: float
    risk_category: str
    classical_features: Optional[List[float]] = None
    quantum_features: Optional[List[float]] = None
    fusion_weights: Optional[Dict[str, float]] = None
    explanation: Optional[str] = None
    processing_time_ms: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MedicalImageOut(BaseModel):
    id: int
    filename: str
    file_path: str
    mime_type: str
    file_size: int
    image_type: str
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnalysisCreate(BaseModel):
    patient_id: int
    image_id: int
    target_condition: Optional[str] = "General Cellular & Tissue Anomaly"


class AnalysisOut(BaseModel):
    id: int
    analysis_code: str
    patient_id: int
    image_id: int
    user_id: int
    status: str
    model_mode: str
    target_condition: str
    created_at: datetime
    patient: Optional[PatientOut] = None
    image: Optional[MedicalImageOut] = None
    prediction: Optional[PredictionOut] = None

    model_config = ConfigDict(from_attributes=True)


class PredictRequest(BaseModel):
    patient_id: int
    image_id: int
    target_condition: Optional[str] = "General Cellular & Tissue Anomaly"
    override_mode: Optional[str] = None  # optionally override demo / research
