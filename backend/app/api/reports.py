import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.analysis import Analysis
from app.models.report import Report
from app.models.user import User
from app.api.deps import get_current_user
from app.reports.pdf_generator import generate_pdf_report
from app.core.config import settings

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/{analysis_id}/pdf")
def download_or_view_pdf_report(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generates and returns the official QuantumCare PDF analysis report.
    Displays patient findings and quantum circuit metrics.
    """
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    if not analysis.prediction:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Analysis does not yet have a prediction result")

    # Check if a generated PDF already exists and is on disk
    report = db.query(Report).filter(Report.analysis_id == analysis.id).first()
    if report and report.pdf_path:
        existing_pdf_path = str(report.pdf_path)
        if os.path.exists(existing_pdf_path):
            return FileResponse(
                existing_pdf_path,
                media_type="application/pdf",
                filename=f"QuantumCare_Report_{analysis.analysis_code}.pdf"
            )

    # Generate PDF
    report_code = f"QC-REP-{uuid.uuid4().hex[:8].upper()}"
    output_filename = f"QuantumCare_{analysis.analysis_code}.pdf"
    pdf_dest = os.path.join(settings.REPORTS_DIR, output_filename)

    analysis_data = {
        "analysis_code": analysis.analysis_code,
        "model_mode": analysis.model_mode,
        "target_condition": analysis.target_condition,
        "created_at": analysis.created_at.isoformat() if analysis.created_at else ""
    }

    patient_data = {
        "patient_id": analysis.patient.patient_id,
        "name": analysis.patient.name,
        "age": analysis.patient.age,
        "gender": analysis.patient.gender,
        "symptoms": analysis.patient.symptoms,
        "medical_history": analysis.patient.medical_history
    }

    prediction_data = {
        "prediction_label": analysis.prediction.prediction_label,
        "confidence_score": analysis.prediction.confidence_score,
        "risk_category": analysis.prediction.risk_category,
        "classical_features": analysis.prediction.classical_features,
        "quantum_features": analysis.prediction.quantum_features,
        "explanation": analysis.prediction.explanation,
        "processing_time_ms": analysis.prediction.processing_time_ms
    }

    image_path = str(analysis.image.file_path) if (analysis.image and analysis.image.file_path and os.path.exists(str(analysis.image.file_path))) else None

    generated_path = generate_pdf_report(
        analysis_data=analysis_data,
        patient_data=patient_data,
        prediction_data=prediction_data,
        image_path=image_path,
        output_path=pdf_dest
    )

    # Save to database
    if not report:
        report = Report(
            analysis_id=analysis.id,
            report_code=report_code,
            pdf_path=generated_path
        )
        db.add(report)
    else:
        report.pdf_path = generated_path
    db.commit()

    return FileResponse(
        generated_path,
        media_type="application/pdf",
        filename=f"QuantumCare_Report_{analysis.analysis_code}.pdf"
    )
