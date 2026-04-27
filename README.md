# Inbound Carrier Sales — HappyRobot FDE Challenge

A complete proof-of-concept for automating inbound carrier calls at a freight brokerage. A HappyRobot voice agent answers calls from carriers, verifies them against FMCSA, pitches matching loads from a custom API, negotiates pricing, and posts call results to a dashboard.

## What's in this repo

```
inbound-carrier-sales/
├── backend/          FastAPI service — loads search, calls store, metrics
├── frontend/         React dashboard — call performance visualization
├── docs/             Deliverables (Acme doc, email draft, etc.)
├── docker-compose.yml
└── README.md
```

## Architecture

```
Carrier → HappyRobot (voice agent)
              ├─ verify_carrier  → FMCSA API (direct webhook)
              ├─ find_loads      → Backend /loads/search
              └─ POST /calls     → Backend (after call, with extracted data)
                                       ↓
                                  PostgreSQL / SQLite
                                       ↓
                                  React Dashboard ← /metrics, /calls
```

Each system owns one concern. HappyRobot handles conversation and external integrations (FMCSA). The backend owns app data (loads, calls). The dashboard visualizes.

## Tech stack

| Layer | Choice |
|---|---|
| Voice agent | HappyRobot platform (web call trigger, GPT-4.1) |
| Backend | FastAPI + SQLAlchemy + SQLite (Postgres-ready) |
| Frontend | Vite + React + TypeScript + Tailwind + Recharts |
| Auth | API key in `X-API-Key` header (constant-time comparison) |
| Deploy | Docker + Fly.io |

## Quickstart

### Option A: Docker Compose (one command)

```bash
docker compose up --build
```

- Backend: http://localhost:8000 (Swagger at `/docs`)
- Dashboard: http://localhost:8080

### Option B: Run services separately

```bash
# Terminal 1 — backend
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m seed.seed
uvicorn app.main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Tests

```bash
cd backend
pip install -r requirements-dev.txt
pytest -v
```

6 integration tests covering authentication enforcement, load search, call persistence with side effects (load marked booked), webhook idempotency, and metrics aggregation. Suite runs in under 2 seconds against an in-memory SQLite database — no external services required.

## Connecting the HappyRobot agent

The agent (configured in HappyRobot's web UI) needs to call this backend during and after each call. Two URLs to point it at:

1. **`find_loads` Tool node** → `GET <backend>/loads/search?origin=...&equipment_type=...`
2. **Final webhook node** → `POST <backend>/calls` with the JSON body shape defined in `backend/app/schemas.py::CallIn`

Both must include the header `X-API-Key: <your API_KEY>`.

For local development, expose your backend to HappyRobot's cloud with a tunnel (e.g., Cloudflare Tunnel):

```bash
cloudflared tunnel --url http://localhost:8000
```

Use the generated HTTPS URL in the Tool/Webhook node configuration.

## Backend endpoints

All endpoints (except `/health`) require `X-API-Key` header.

| Method | Path | Caller | Purpose |
|---|---|---|---|
| GET | `/health` | anyone | Liveness check |
| GET | `/loads/search` | agent | Find available loads |
| GET | `/loads/{load_id}` | agent | Fetch one load |
| POST | `/calls` | agent | Store completed call data |
| GET | `/calls?limit=20` | dashboard | List recent calls |
| GET | `/metrics` | dashboard | Aggregated stats |

## Security

- **HTTPS:** All endpoints served over HTTPS in production (Fly.io with Let's Encrypt). Locally HTTP for development.
- **Authentication:** API key authentication via `X-API-Key` header on all endpoints except `/health`. Keys validated using constant-time comparison (`secrets.compare_digest`) to prevent timing attacks.
- **Secrets management:** API keys and database URLs stored as environment variables, never committed to git.
- **CORS:** Restricted to known origins (the dashboard URL) — configured per environment.

## Design decisions

- **FMCSA verification lives in HappyRobot, not the backend.** The voice agent's `verify_carrier` tool calls FMCSA directly via a webhook node. Keeps the backend focused on application data, leverages the platform's native capabilities, shortens the development loop.
- **SQLite for dev, Postgres for prod.** Swap via `DATABASE_URL` env var. No code changes needed.
- **No migrations framework.** `Base.metadata.create_all()` runs on startup. For a 3-day demo, Alembic would be overkill.
- **Single-page dashboard, no router.** One page is the spec.
- **Defensive Pydantic validation.** Schema tolerates HappyRobot's webhook quirks (string "null" instead of null, numbers as strings, structured array transcripts).
- **Idempotent POST /calls.** Duplicate `call_id` returns existing record instead of erroring — handles webhook retries cleanly.

## Repository links

- Repo: <fill in after pushing to GitHub>
- Backend deployed: <fill in after Fly deploy>
- Dashboard deployed: <fill in after Fly deploy>
- HappyRobot workflow: <fill in with platform link>
- Demo video: <fill in with Loom link>
