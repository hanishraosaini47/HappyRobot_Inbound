"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routes import calls, loads, metrics

app = FastAPI(
    title="Inbound Carrier Sales API",
    description="Backend for the HappyRobot voice agent + dashboard",
    version="0.1.0",
)

# CORS — allow the dashboard to call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Create tables if they don't exist (simple — no migrations)."""
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Public health check — no auth required."""
    return {"status": "ok"}


# Routes
app.include_router(loads.router, prefix="/loads", tags=["loads"])
app.include_router(calls.router, prefix="/calls", tags=["calls"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
