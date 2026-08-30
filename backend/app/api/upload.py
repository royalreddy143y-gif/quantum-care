import os
import uuid
from PIL import Image
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.session import get_db
from app.models.medical_image import MedicalImage
from app.models.patient import Patient
from app.models.user import User
from app.schemas.analysis import MedicalImageOut
from app.api.deps import get_current_user

router = APIRouter(prefix="/upload", tags=["Image Upload"])

ALLOWED_MIME_TYPES = {"image/jpeg", "image/jpg", "image/png"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


@router.post("", response_model=MedicalImageOut, status_code=status.HTTP_201_CREATED)
async def upload_medical_image(
    patient_id: int = Form(...),
    image_type: str = Form("medical_scan"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Securely uploads, validates, and stores a patient medical scan image.
    Validates MIME type, extension, size limit, and PIL image integrity.
    """
    # 1. Verify Patient ownership
    patient = db.query(Patient).filter(Patient.id == patient_id, Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target patient record not found")

    content_type = file.content_type or ""
    # 2. Validate MIME type
    if content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Only JPEG and PNG medical scans are accepted."
        )

    # 3. Validate file extension
    filename = file.filename or "upload.jpg"
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file extension: '{ext}'. Allowed: .jpg, .jpeg, .png"
        )

    # 4. Read contents and check file size
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE // (1024 * 1024)}MB."
        )
    if len(contents) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty."
        )

    # 5. Verify image integrity with PIL (guards against disguised malware/executables)
    import io
    try:
        with Image.open(io.BytesIO(contents)) as test_img:
            test_img.verify()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is corrupted or not a valid raster medical image."
        )

    # 6. Save sanitized file to disk
    sanitized_filename = f"{uuid.uuid4().hex[:12]}_{os.path.basename(filename)}"
    destination_path = os.path.join(settings.UPLOAD_DIR, sanitized_filename)

    with open(destination_path, "wb") as buffer:
        buffer.write(contents)

    # 7. Create database record
    medical_image = MedicalImage(
        patient_id=patient.id,
        file_path=destination_path,
        filename=filename,
        mime_type=content_type,
        file_size=len(contents),
        image_type=image_type
    )
    db.add(medical_image)
    db.commit()
    db.refresh(medical_image)

    return medical_image
