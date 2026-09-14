from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class PartyStatus(str, Enum):
    waiting = "waiting"
    notified = "notified"
    seated = "seated"
    cancelled = "cancelled"


class PartyBase(BaseModel):
    name: str = Field(..., min_length=1)
    party_size: int = Field(..., ge=1)
    phone: Optional[str] = None
    notes: Optional[str] = None


class PartyCreate(PartyBase):
    pass


class PartyUpdate(BaseModel):
    status: Optional[PartyStatus] = None
    notes: Optional[str] = None
    party_size: Optional[int] = Field(None, ge=1)


class Party(PartyBase):
    id: int
    status: PartyStatus
    created_at: datetime
    updated_at: datetime
