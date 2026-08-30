from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class PatientBase(BaseModel):
    patient_id: str = Field(..., description="Unique clinical code e.g. QC-2025-001")
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=0, le=130)
    gender: str = Field(..., description="Male, Female, Other")
    symptoms: Optional[str] = None
    medical_history: Optional[str] = None
    biomarkers: Optional[Dict[str, Any]] = None  # e.g., {"ca125": 24.5, "psa": 1.8}
    genomics: Optional[Dict[str, Any]] = None    # e.g., {"brca1_mutation": False}


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    symptoms: Optional[str] = None
    medical_history: Optional[str] = None
    biomarkers: Optional[Dict[str, Any]] = None
    genomics: Optional[Dict[str, Any]] = None


class PatientOut(PatientBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
