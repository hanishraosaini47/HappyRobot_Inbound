"""Metrics endpoint — aggregated stats for the dashboard."""

from collections import Counter

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database import get_db
from app.models import Call, Load
from app.schemas import LaneCount, MetricsOut

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get("", response_model=MetricsOut)
def get_metrics(db: Session = Depends(get_db)) -> MetricsOut:
    """Compute dashboard metrics from the calls and loads tables."""
    calls = db.query(Call).all()
    loads = db.query(Load).all()

    total_calls = len(calls)
    booked_calls = sum(1 for c in calls if c.deal_agreed)
    booking_rate = (booked_calls / total_calls) if total_calls else 0.0

    booked = [c for c in calls if c.deal_agreed and c.final_agreed_rate is not None]
    avg_rate = (
        sum(c.final_agreed_rate for c in booked) / len(booked) if booked else None
    )

    uplift_values = [
        ((c.final_agreed_rate - c.loadboard_rate) / c.loadboard_rate) * 100
        for c in booked
        if c.loadboard_rate
    ]
    avg_uplift = sum(uplift_values) / len(uplift_values) if uplift_values else None

    # Average first counter offer as % over loadboard rate
    counter_pct_values = [
        ((c.first_counter_offer - c.loadboard_rate) / c.loadboard_rate) * 100
        for c in calls
        if c.first_counter_offer is not None and c.loadboard_rate
    ]
    avg_counter_pct = (
        sum(counter_pct_values) / len(counter_pct_values) if counter_pct_values else None
    )

    avg_rounds = (
        sum(c.negotiation_rounds for c in calls) / total_calls if total_calls else None
    )

    outcome_breakdown = Counter(c.outcome for c in calls if c.outcome)
    sentiment_breakdown = Counter(c.sentiment for c in calls if c.sentiment)

    total_loads = len(loads)
    available_loads = sum(1 for ld in loads if ld.status == "available")
    booked_loads = sum(1 for ld in loads if ld.status == "booked")

    # Top requested lanes — what carriers were asking for
    lane_counter: Counter[tuple[str, str]] = Counter()
    for c in calls:
        if c.requested_origin and c.requested_destination:
            lane_counter[(c.requested_origin, c.requested_destination)] += 1
    top_lanes = [
        LaneCount(origin=o, destination=d, count=count)
        for (o, d), count in lane_counter.most_common(5)
    ]

    # Top requested equipment types
    equipment_counter: Counter[str] = Counter(
        c.requested_equipment_type for c in calls if c.requested_equipment_type
    )

    return MetricsOut(
        total_calls=total_calls,
        booked_calls=booked_calls,
        booking_rate=round(booking_rate, 4),
        avg_negotiated_rate=round(avg_rate, 2) if avg_rate is not None else None,
        avg_negotiation_rounds=round(avg_rounds, 2) if avg_rounds is not None else None,
        avg_rate_uplift_pct=round(avg_uplift, 2) if avg_uplift is not None else None,
        avg_first_counter_offer_pct=round(avg_counter_pct, 2)
        if avg_counter_pct is not None
        else None,
        total_loads=total_loads,
        available_loads=available_loads,
        booked_loads=booked_loads,
        outcome_breakdown=dict(outcome_breakdown),
        sentiment_breakdown=dict(sentiment_breakdown),
        top_requested_lanes=top_lanes,
        top_requested_equipment=dict(equipment_counter),
    )
