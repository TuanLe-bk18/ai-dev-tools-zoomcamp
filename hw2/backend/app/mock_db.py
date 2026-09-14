from datetime import datetime, timezone
from typing import List, Optional
from app.schemas import Party, PartyCreate, PartyUpdate, PartyStatus


class MockDatabase:
    def __init__(self):
        self._parties: List[dict] = [
            {
                "id": 1,
                "name": "Sarah Connor",
                "party_size": 4,
                "phone": "555-0199",
                "notes": "Needs high chair",
                "status": PartyStatus.waiting,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
            {
                "id": 2,
                "name": "David Miller",
                "party_size": 2,
                "phone": "555-0142",
                "notes": "Window booth preferred",
                "status": PartyStatus.notified,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
        ]
        self._next_id = 3

    def list_parties(self, status_filter: Optional[str] = None) -> List[Party]:
        parties = self._parties
        if not status_filter or status_filter == "active":
            filtered = [
                p for p in parties if p["status"] in (PartyStatus.waiting, PartyStatus.notified)
            ]
        elif status_filter == "all":
            filtered = parties
        else:
            filtered = [p for p in parties if p["status"] == status_filter]
        return [Party(**p) for p in filtered]

    def create_party(self, payload: PartyCreate) -> Party:
        now = datetime.now(timezone.utc)
        record = {
            "id": self._next_id,
            "name": payload.name,
            "party_size": payload.party_size,
            "phone": payload.phone,
            "notes": payload.notes,
            "status": PartyStatus.waiting,
            "created_at": now,
            "updated_at": now,
        }
        self._next_id += 1
        self._parties.append(record)
        return Party(**record)

    def update_party(self, party_id: int, payload: PartyUpdate) -> Optional[Party]:
        for record in self._parties:
            if record["id"] == party_id:
                if payload.status is not None:
                    record["status"] = payload.status
                if payload.notes is not None:
                    record["notes"] = payload.notes
                if payload.party_size is not None:
                    record["party_size"] = payload.party_size
                record["updated_at"] = datetime.now(timezone.utc)
                return Party(**record)
        return None

    def delete_party(self, party_id: int) -> bool:
        initial_len = len(self._parties)
        self._parties = [p for p in self._parties if p["id"] != party_id]
        return len(self._parties) < initial_len


db = MockDatabase()
