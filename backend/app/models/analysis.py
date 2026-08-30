from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.session import Base

if TYPE_CHECKING:
    from app.models.patient import Patient
    from app.models.medical_image import MedicalImage
    from app.models.user import User
    from app.models.prediction import Prediction
    from app.models.report import Report


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    analysis_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    image_id: Mapped[int] = mapped_column(Integer, ForeignKey("medical_images.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="COMPLETED")  # PENDING, PROCESSING, COMPLETED, FAILED
    model_mode: Mapped[str] = mapped_column(String(20), default="demo")   # demo or research
    target_condition: Mapped[str] = mapped_column(String(100), default="General Cellular & Tissue Anomaly")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    patient: Mapped["Patient"] = relationship("Patient", back_populates="analyses")
    image: Mapped["MedicalImage"] = relationship("MedicalImage", back_populates="analyses")
    user: Mapped["User"] = relationship("User", back_populates="analyses")
    prediction: Mapped[Optional["Prediction"]] = relationship("Prediction", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
    report: Mapped[Optional["Report"]] = relationship("Report", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
