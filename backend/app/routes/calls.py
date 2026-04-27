"""Calls endpoints — POST from the agent, GET for the dashboard."""

import json
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database import get_db
from app.models import Call, Load
from app.schemas import CallIn, CallOut

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.post("", response_model=CallOut, status_code=201)
def create_call(payload: CallIn, db: Session = Depends(get_db)) -> Call:
    """Receive a completed call from HappyRobot and persist it.

    - Idempotent: duplicate call_id returns the existing record instead of erroring.
    - Marks the associated load as 'booked' if a deal was agreed.
    """
    # Idempotency: if this call_id already exists, return it
    existing = db.query(Call).filter(Call.call_id == payload.call_id).first()
    if existing:
        return existing

    # Normalize mc_number to string
    mc_number = str(payload.mc_number) if payload.mc_number is not None else None

    # Normalize transcript: if it's a structured list, JSON-encode it
    transcript = payload.transcript
    if isinstance(transcript, list):
        transcript = json.dumps(transcript, ensure_ascii=False)

    # Optional warning: deal closed but no final rate captured
    if payload.deal_agreed and payload.final_agreed_rate is None:
        print(f"⚠️  Call {payload.call_id} marked as booked but no final rate captured")

    call = Call(
        call_id=payload.call_id,
        timestamp=payload.timestamp or datetime.utcnow(),
        duration_seconds=payload.duration_seconds,
        mc_number=mc_number,
        company_name=payload.company_name,
        carrier_eligible=payload.carrier_eligible,
        load_id=payload.load_id,
        loadboard_rate=payload.loadboard_rate,
        final_agreed_rate=payload.final_agreed_rate,
        first_counter_offer=payload.first_counter_offer,
        negotiation_rounds=payload.negotiation_rounds,
        deal_agreed=payload.deal_agreed,
        transfer_initiated=payload.transfer_initiated,
        requested_origin=payload.requested_origin,
        requested_destination=payload.requested_destination,
        requested_equipment_type=payload.requested_equipment_type,
        outcome=payload.outcome,
        sentiment=payload.sentiment,
        transcript=transcript,
    )
    db.add(call)

    # Mark the load as booked if a deal was agreed
    if payload.deal_agreed and payload.load_id:
        load = db.query(Load).filter(Load.load_id == payload.load_id).first()
        if load and load.status == "available":
            load.status = "booked"

    # Race-condition safety: another concurrent request might have inserted
    # the same call_id between our check and commit. Catch and return existing.
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.query(Call).filter(Call.call_id == payload.call_id).first()
        if existing:
            return existing
        raise

    db.refresh(call)
    return call


@router.get("", response_model=list[CallOut])
def list_calls(
    limit: int = Query(default=20, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[Call]:
    """Return the most recent calls for the dashboard table."""
    return db.query(Call).order_by(Call.timestamp.desc()).limit(limit).all()
