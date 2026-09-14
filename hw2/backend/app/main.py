from typing import List, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import PartyModel
from app.schemas import Party, PartyCreate, PartyUpdate, PartyStatus


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="SeatFlow API",
    description="Restaurant Waitlist Manager Backend with SQLite/SQLAlchemy",
    version="0.2.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/parties", response_model=List[Party])
def get_parties(
    status_filter: Optional[str] = Query(default="active", alias="status"),
    db: Session = Depends(get_db),
):
    query = db.query(PartyModel)

    if not status_filter or status_filter == "active":
        query = query.filter(
            PartyModel.status.in_([PartyStatus.waiting, PartyStatus.notified])
        )
    elif status_filter != "all":
        query = query.filter(PartyModel.status == status_filter)

    return query.order_by(PartyModel.created_at.asc()).all()


@app.post("/api/parties", response_model=Party, status_code=status.HTTP_201_CREATED)
def create_party(payload: PartyCreate, db: Session = Depends(get_db)):
    party = PartyModel(
        name=payload.name,
        party_size=payload.party_size,
        phone=payload.phone,
        notes=payload.notes,
        status=PartyStatus.waiting,
    )
    db.add(party)
    db.commit()
    db.refresh(party)
    return party


@app.patch("/api/parties/{party_id}", response_model=Party)
def update_party(party_id: int, payload: PartyUpdate, db: Session = Depends(get_db)):
    party = db.query(PartyModel).filter(PartyModel.id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    if payload.status is not None:
        party.status = payload.status
    if payload.notes is not None:
        party.notes = payload.notes
    if payload.party_size is not None:
        party.party_size = payload.party_size

    db.commit()
    db.refresh(party)
    return party


@app.delete("/api/parties/{party_id}")
def delete_party(party_id: int, db: Session = Depends(get_db)):
    party = db.query(PartyModel).filter(PartyModel.id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    db.delete(party)
    db.commit()
    return {"message": "Party deleted"}


@app.get("/healthz")
def health_check():
    return {"status": "ok", "app": "SeatFlow", "storage": "SQLAlchemy"}
