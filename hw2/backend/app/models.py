from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.database import Base
from app.schemas import PartyStatus


def get_utc_now():
    return datetime.now(timezone.utc)


class PartyModel(Base):
    __tablename__ = "parties"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    party_size = Column(Integer, nullable=False)
    phone = Column(String(20), nullable=True)
    notes = Column(String(255), nullable=True)
    status = Column(
        Enum(PartyStatus, values_callable=lambda obj: [e.value for e in obj]),
        default=PartyStatus.waiting,
        nullable=False,
        index=True,
    )
    created_at = Column(DateTime(timezone=True), default=get_utc_now, nullable=False)
    updated_at = Column(
        DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now, nullable=False
    )
