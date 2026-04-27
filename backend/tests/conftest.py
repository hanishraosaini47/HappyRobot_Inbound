"""Shared pytest fixtures: test client + fresh in-memory database per test."""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Load


@pytest.fixture
def client():
    """FastAPI TestClient backed by a shared in-memory SQLite DB."""
    # StaticPool ensures all sessions share the SAME in-memory database
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine)

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Seed two sample loads for tests that need them
    db = TestingSessionLocal()
    db.add(Load(
        load_id="L-1001",
        origin="Dallas, TX",
        destination="Phoenix, AZ",
        pickup_datetime=datetime(2026, 4, 28, 8, 0, 0),
        delivery_datetime=datetime(2026, 4, 30, 17, 0, 0),
        equipment_type="dry_van",
        loadboard_rate=1800,
        weight=22000,
        commodity_type="general_freight",
        num_of_pieces=12,
        miles=887,
        dimensions="53ft trailer",
        status="available",
    ))
    db.add(Load(
        load_id="L-1002",
        origin="Atlanta, GA",
        destination="Chicago, IL",
        pickup_datetime=datetime(2026, 4, 29, 12, 0, 0),
        delivery_datetime=datetime(2026, 5, 1, 9, 0, 0),
        equipment_type="reefer",
        loadboard_rate=2400,
        weight=38000,
        commodity_type="produce",
        num_of_pieces=24,
        miles=717,
        dimensions="53ft reefer",
        status="available",
    ))
    db.commit()
    db.close()

    # Override the get_db dependency to use the test database
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers():
    """Headers with the valid API key for protected endpoints."""
    return {"X-API-Key": "dev_secret_change_me"}
