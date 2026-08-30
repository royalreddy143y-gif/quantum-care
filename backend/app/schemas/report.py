from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ReportOut(BaseModel):
    id: int
    analysis_id: int
    report_code: str
    pdf_path: Optional[str] = None
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)
