import uuid
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field

ChannelType = Literal["chatbot", "ivrs", "sms", "app", "web"]


class InteractionCreate(BaseModel):
    case_id: uuid.UUID = Field(..., description="ID of the monitored case")
    channel: ChannelType = Field(default="chatbot", description="Communication channel used for the check-in")
    response_text: Optional[str] = Field(None, description="Check-in response text or transcribed audio")
    response_latency_sec: Optional[int] = Field(None, ge=0, description="Response latency in seconds")
    was_skipped: bool = Field(default=False, description="Whether check-in was skipped by victim")


class InteractionResponse(BaseModel):
    id: uuid.UUID
    occurred_at: datetime

    model_config = {"from_attributes": True}
