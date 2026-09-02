import uuid
from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

ChannelType = Literal["chatbot", "ivrs", "sms", "app", "web"]
ConsentStatusType = Literal["active", "revoked", "pending"]


class VictimCreate(BaseModel):
    case_ref_id: str = Field(..., min_length=1, max_length=100, description="Legal case reference identifier")
    preferred_language: str = Field(default="hi", max_length=10, description="Preferred language code (e.g. hi, en)")
    preferred_channel: ChannelType = Field(default="sms", description="Preferred contact channel")


class VictimResponse(BaseModel):
    id: uuid.UUID
    case_ref_id: str
    enrolled_at: datetime

    model_config = {"from_attributes": True}


class ConsentCreate(BaseModel):
    victim_id: uuid.UUID
    consented: bool = Field(..., description="Whether victim consents to periodic monitoring")
    channels: List[ChannelType] = Field(default=["sms", "chatbot"], description="Channels victim consents to")


class ConsentResponse(BaseModel):
    id: uuid.UUID
    victim_id: uuid.UUID
    status: ConsentStatusType

    model_config = {"from_attributes": True}
