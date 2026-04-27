"""End-to-end API tests covering the high-value paths."""


def test_health_endpoint_works_without_auth(client):
    """The health endpoint should be open and return ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_protected_endpoint_rejects_missing_api_key(client):
    """Endpoints without an API key header should return 401."""
    response = client.get("/loads/search")
    assert response.status_code == 401


def test_loads_search_filters_by_origin(client, auth_headers):
    """Searching by origin should return only matching loads."""
    response = client.get("/loads/search?origin=Atlanta", headers=auth_headers)
    assert response.status_code == 200
    loads = response.json()
    assert len(loads) == 1
    assert loads[0]["load_id"] == "L-1002"
    assert loads[0]["origin"] == "Atlanta, GA"


def test_post_call_persists_and_marks_load_booked(client, auth_headers):
    """A successful call POST should save the call and update load status."""
    payload = {
        "call_id": "test-call-001",
        "mc_number": "123456",
        "load_id": "L-1002",
        "loadboard_rate": 2400,
        "final_agreed_rate": 2625,
        "negotiation_rounds": 2,
        "deal_agreed": True,
        "outcome": "booked",
        "sentiment": "neutral",
    }
    response = client.post("/calls", json=payload, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["deal_agreed"] is True

    # Confirm the load got marked as booked
    load_resp = client.get("/loads/L-1002", headers=auth_headers)
    assert load_resp.json()["status"] == "booked"


def test_post_call_is_idempotent_on_duplicate_id(client, auth_headers):
    """Posting the same call_id twice should return the existing record, not error."""
    payload = {
        "call_id": "test-duplicate-001",
        "mc_number": "999",
        "deal_agreed": False,
        "outcome": "negotiation_failed",
    }
    first = client.post("/calls", json=payload, headers=auth_headers)
    second = client.post("/calls", json=payload, headers=auth_headers)

    assert first.status_code == 201
    # Idempotent: second post returns the same record, not an error
    assert second.status_code in (200, 201)
    assert first.json()["call_id"] == second.json()["call_id"]


def test_metrics_computes_booking_rate_and_breakdowns(client, auth_headers):
    """Metrics should aggregate calls correctly across outcomes."""
    # Post 1 booked + 1 failed call
    client.post("/calls", json={
        "call_id": "m1",
        "load_id": "L-1001",
        "loadboard_rate": 1800,
        "final_agreed_rate": 1900,
        "deal_agreed": True,
        "outcome": "booked",
        "sentiment": "positive",
    }, headers=auth_headers)
    client.post("/calls", json={
        "call_id": "m2",
        "deal_agreed": False,
        "outcome": "negotiation_failed",
        "sentiment": "negative",
    }, headers=auth_headers)

    response = client.get("/metrics", headers=auth_headers)
    assert response.status_code == 200
    metrics = response.json()
    assert metrics["total_calls"] == 2
    assert metrics["booked_calls"] == 1
    assert metrics["booking_rate"] == 0.5
    assert metrics["outcome_breakdown"]["booked"] == 1
    assert metrics["outcome_breakdown"]["negotiation_failed"] == 1
    assert metrics["sentiment_breakdown"]["positive"] == 1
    assert metrics["sentiment_breakdown"]["negative"] == 1
