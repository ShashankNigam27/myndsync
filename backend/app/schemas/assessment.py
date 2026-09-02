import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AssessmentResponse(BaseModel):
    id: uuid.UUID
    interaction_id: uuid.UUID
    sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="Sentiment polarity from -1.0 (severe distress) to +1.0 (positive)")
    emotion_label: Optional[str] = Field(None, description="Classified emotion (e.g., fear, sadness, anger, hopelessness, neutral)")
    voice_stress_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Acoustic voice stress score when audio is analyzed")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score from 0.0 to 1.0")
    processed_at: datetime

    model_config = {"from_attributes": True}
