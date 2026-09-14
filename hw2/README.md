# SeatFlow (Restaurant Waitlist Manager)

Full-stack application for managing restaurant guest queues in real-time, built with AI-assisted workflows for AI Dev Tools Zoomcamp 2026 (Module 2).

## Tech Stack
- **Frontend:** React + Vite, Tailwind CSS / clean component UI.
- **Backend:** Python FastAPI, managed with `uv`.
- **Database:** SQLite with SQLAlchemy ORM.
- **Contract:** OpenAPI 3.0 specification.

## Directory Layout
```text
hw2/
├── _docs/
│   └── specs.md       # Product and technical specifications
├── frontend/          # React client application
├── backend/           # FastAPI application
├── openapi.yaml       # API contract schema
├── AGENTS.md          # Agent workflow and guidelines
└── README.md
```

## Getting Started

### 1. Backend Setup
```bash
cd backend
uv sync
uv run pytest
uv run uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
