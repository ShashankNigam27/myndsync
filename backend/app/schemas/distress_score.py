import uuid
from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

RiskBandType = Literal["low", "moderate", "high", "critical"]


class DistressScoreResponse(BaseModel):
    id: uuid.UUID
    case_id: uuid.UUID
    assessment_id: uuid.UUID
    current_score: float = Field(..., ge=0.0, le=100.0, description="DDS score from 0.0 to 100.0")
    baseline_score: float = Field(..., ge=0.0, le=100.0, description="Initial baseline DDS score")
    trend_slope: float = Field(..., description="Calculated trend slope across recent check-ins")
    risk_band: RiskBandType = Field(..., description="Categorized risk band (low, moderate, high, critical)")
    computed_at: datetime

    model_config = {"from_attributes": True}


class CaseDistressHistoryResponse(BaseModel):
    case_id: uuid.UUID
    total_checkins: int
    current_score: Optional[float] = None
    current_risk_band: Optional[str] = None
    baseline_score: Optional[float] = None
    trend_slope: Optional[float] = None
    history: List[DistressScoreResponse]
