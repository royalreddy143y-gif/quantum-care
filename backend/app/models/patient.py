from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, TYPE_CHECKING
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.session import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.medical_image import MedicalImage
    from app.models.analysis import Analysis


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    patient_id: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    symptoms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    medical_history: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    biomarkers: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # e.g., {"ca125": 35.2, "psa": 2.1, "cea": 4.0}
    genomics: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)    # e.g., {"brca1_mutation": false, "egfr": "wild_type"}
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    creator: Mapped["User"] = relationship("User", back_populates="patients")
    images: Mapped[List["MedicalImage"]] = relationship("MedicalImage", back_populates="patient", cascade="all, delete-orphan")
    analyses: Mapped[List["Analysis"]] = relationship("Analysis", back_populates="patient", cascade="all, delete-orphan")
