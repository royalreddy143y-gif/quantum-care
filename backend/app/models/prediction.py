from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, TYPE_CHECKING
from sqlalchemy import Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.session import Base

if TYPE_CHECKING:
    from app.models.analysis import Analysis


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    analysis_id: Mapped[int] = mapped_column(Integer, ForeignKey("analyses.id", ondelete="CASCADE"), unique=True, nullable=False)
    prediction_label: Mapped[str] = mapped_column(String(100), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)  # e.g., 0.87
    risk_category: Mapped[str] = mapped_column(String(50), nullable=False)  # Low, Moderate, High
    classical_features: Mapped[Optional[List[float]]] = mapped_column(JSON, nullable=True)   # Reduced 4D vector from Swin
    quantum_features: Mapped[Optional[List[float]]] = mapped_column(JSON, nullable=True)     # PauliZ expectation measurements
    fusion_weights: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)       # Modal weights
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    processing_time_ms: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    analysis: Mapped["Analysis"] = relationship("Analysis", back_populates="prediction")
