from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.session import get_db
from app.models.patient import Patient
from app.models.user import User
from app.schemas.patient import PatientCreate, PatientUpdate, PatientOut
from app.api.deps import get_current_user

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient_in: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new patient record tied to the authenticated researcher/clinician."""
    existing = db.query(Patient).filter(Patient.patient_id == patient_in.patient_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Patient with ID '{patient_in.patient_id}' already exists."
        )

    patient = Patient(
        user_id=current_user.id,
        patient_id=patient_in.patient_id,
        name=patient_in.name,
        age=patient_in.age,
        gender=patient_in.gender,
        symptoms=patient_in.symptoms,
        medical_history=patient_in.medical_history,
        biomarkers=patient_in.biomarkers,
        genomics=patient_in.genomics
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)

    # Sync patient document to MongoDB Atlas
    from app.database.mongodb import mongo_save_patient
    try:
        mongo_save_patient({
            "id": patient.id,
            "patient_id": patient.patient_id,
            "user_id": patient.user_id,
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
            "symptoms": patient.symptoms,
            "medical_history": patient.medical_history,
            "biomarkers": patient.biomarkers,
            "genomics": patient.genomics,
            "created_at": patient.created_at.isoformat() if patient.created_at else None
        })
    except Exception as ex:
        print(f"[*] MongoDB patient sync notice: {ex}")

    return patient


@router.get("", response_model=List[PatientOut])
def list_patients(
    search: Optional[str] = Query(None, description="Search by name or patient ID"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List accessible patient records with optional search filter."""
    query = db.query(Patient).filter(Patient.user_id == current_user.id)
    if search:
        query = query.filter(
            or_(
                Patient.name.ilike(f"%{search}%"),
                Patient.patient_id.ilike(f"%{search}%")
            )
        )
    patients = query.order_by(Patient.created_at.desc()).offset(skip).limit(limit).all()
    return patients


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve details of a specific patient."""
    patient = db.query(Patient).filter(Patient.id == patient_id, Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient record not found")
    return patient


@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(
    patient_id: int,
    patient_in: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update patient demographic, history, or optional biomarker/genomic data."""
    patient = db.query(Patient).filter(Patient.id == patient_id, Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient record not found")

    update_data = patient_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Permanently delete patient record and associated analyses."""
    patient = db.query(Patient).filter(Patient.id == patient_id, Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient record not found")

    db.delete(patient)
    db.commit()
    return None
