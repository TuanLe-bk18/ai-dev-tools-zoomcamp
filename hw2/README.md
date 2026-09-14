# SeatFlow (Restaurant Waitlist Manager)

A real-time restaurant waitlist management app built using an AI-native, spec-driven full-stack workflow for **AI Dev Tools Zoomcamp 2026 (Module 2)**.

## Overview
SeatFlow replaces manual pen-and-paper clipboards at restaurant host stands. It provides a single-screen queue view to register incoming parties, track wait times, and update seating status.

## Development Workflow
Following the course methodology:
1. **Spec-first:** Outlined user stories, data models, and non-goals in `_docs/specs.md`.
2. **Contract-first:** Defined the REST API interface in `openapi.yaml`.
3. **Frontend Prototype:** Built an interactive React UI using centralized mock API calls.
4. **Backend Implementation:** Built a FastAPI backend managed with `uv`, initially backed by in-memory storage.
5. **Database Persistence:** Replaced mock storage with SQLite via SQLAlchemy ORM without touching the frontend.
6. **Automated Testing:** 100% test coverage for endpoint CRUD operations using isolated in-memory SQLite.

## Tech Stack
- **Frontend:** React 19, Vite 6, Native CSS with responsive flexbox/grid layout.
- **Backend:** Python 3.11+, FastAPI, Uvicorn, managed with `uv`.
- **Database:** SQLite with SQLAlchemy ORM (database-agnostic).
- **Testing:** Pytest with FastAPI TestClient and SQLite `:memory:` isolation.
- **Contract:** OpenAPI 3.0 specification (`openapi.yaml`).

## Project Layout
```text
hw2/
├── _docs/
│   └── specs.md            # Product & technical requirements
├── frontend/               # React client app
│   ├── src/
│   │   ├── api.js          # Centralized API client (fetch)
│   │   ├── App.jsx         # Waitlist UI & state management
│   │   ├── index.css       # App styling
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── backend/                # FastAPI backend app
│   ├── app/
│   │   ├── database.py     # SQLAlchemy engine & session factory
│   │   ├── models.py       # Party SQLAlchemy ORM model
│   │   ├── schemas.py      # Pydantic request/response models
│   │   └── main.py         # FastAPI routes and lifecycle
│   ├── tests/
│   │   └── test_parties.py # Pytest test suite
│   └── pyproject.toml      # uv package configuration
├── openapi.yaml            # OpenAPI 3.0 API schema
├── AGENTS.md               # AI agent instructions & conventions
└── README.md
```

## Running Locally

### 1. Backend
```bash
cd backend
uv sync
uv run pytest
uv run uvicorn app.main:app --reload --port 8000
```
- API Docs (Swagger): `http://localhost:8000/docs`
- Health check: `http://localhost:8000/healthz`

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```
- Web Application: `http://localhost:5173` (or `http://localhost:5174`)

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/parties?status={active\|seated\|all}` | List waitlist parties filtered by status |
| `POST` | `/api/parties` | Add new guest party to queue |
| `PATCH` | `/api/parties/{id}` | Update party status (`notified`, `seated`, `cancelled`) or details |
| `DELETE` | `/api/parties/{id}` | Remove party from waitlist |
| `GET` | `/healthz` | Health check endpoint |
