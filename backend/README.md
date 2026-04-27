# Backend — Inbound Carrier Sales API

FastAPI service that serves loads to the HappyRobot voice agent during calls and stores call results for the dashboard.

## Setup (local)

```bash
# 1. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env

# 4. Seed the database with sample loads
python -m seed.seed

# 5. Run the server
uvicorn app.main:app --reload --port 8000
```

The API is now at `http://localhost:8000`. Swagger docs at `http://localhost:8000/docs`.

## Endpoints

All endpoints (except `/health`) require an `X-API-Key` header matching the value in `.env`.

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Health check (no auth) |
| GET | `/loads/search?origin=&destination=&equipment_type=` | Search loads (called by the agent) |
| GET | `/loads/{load_id}` | Fetch one load |
| POST | `/calls` | Receive a completed call (called by the agent) |
| GET | `/calls?limit=20` | List recent calls (called by the dashboard) |
| GET | `/metrics` | Aggregated metrics (called by the dashboard) |

## Tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

6 integration tests covering auth, load search, call persistence with side effects, idempotency, and metrics aggregation. Suite runs against an in-memory SQLite DB in under 2 seconds.

## Run with Docker

```bash
docker build -t carrier-api .
docker run -p 8000:8000 --env-file .env carrier-api
```
