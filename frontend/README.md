# Frontend — Carrier Sales Dashboard

Single-page React dashboard that visualizes call performance for the inbound carrier sales agent.

## Setup (local)

```bash
npm install
cp .env.example .env
npm run dev
```

Dashboard runs at `http://localhost:5173`. Make sure the backend is running on `http://localhost:8000` first.

## Build

```bash
npm run build
```

## Run with Docker

```bash
docker build -t carrier-dashboard .
docker run -p 8080:80 carrier-dashboard
```

Visit `http://localhost:8080`.

## Environment variables

| Var | Default | Purpose |
|---|---|---|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Backend URL |
| `VITE_API_KEY` | `dev_secret_change_me` | Must match backend's `API_KEY` |

Vite env vars are baked in at build time. For production, set them before `npm run build`.
