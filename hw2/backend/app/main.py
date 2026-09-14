from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import Party, PartyCreate, PartyUpdate
from app.mock_db import db

app = FastAPI(
    title="SeatFlow API",
    description="Restaurant Waitlist Manager Backend",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/parties", response_model=List[Party])
def get_parties(status: Optional[str] = Query(default="active")):
    return db.list_parties(status_filter=status)


@app.post("/api/parties", response_model=Party, status_code=status.HTTP_201_CREATED)
def create_party(payload: PartyCreate):
    return db.create_party(payload)


@app.patch("/api/parties/{party_id}", response_model=Party)
def update_party(party_id: int, payload: PartyUpdate):
    party = db.update_party(party_id, payload)
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return party


@app.delete("/api/parties/{party_id}")
def delete_party(party_id: int):
    deleted = db.delete_party(party_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Party not found")
    return {"message": "Party deleted"}


@app.get("/healthz")
def health_check():
    return {"status": "ok", "app": "SeatFlow"}
