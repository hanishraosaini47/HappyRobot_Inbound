"""Loads endpoints — used by the voice agent during a call."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database import get_db
from app.models import Load
from app.schemas import LoadOut

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get("/search", response_model=list[LoadOut])
def search_loads(
    origin: str | None = Query(default=None, description="Substring match on origin"),
    destination: str | None = Query(default=None, description="Substring match on destination"),
    equipment_type: str | None = Query(default=None, description="Exact equipment type"),
    only_available: bool = Query(default=True, description="Only return available loads"),
    limit: int = Query(default=5, ge=1, le=50),
    db: Session = Depends(get_db),
) -> list[Load]:
    """Search loads by origin / destination / equipment type."""
    query = db.query(Load)

    if only_available:
        query = query.filter(Load.status == "available")
    if origin:
        query = query.filter(Load.origin.ilike(f"%{origin}%"))
    if destination:
        query = query.filter(Load.destination.ilike(f"%{destination}%"))
    if equipment_type:
        query = query.filter(Load.equipment_type.ilike(equipment_type))

    return query.limit(limit).all()


@router.get("/{load_id}", response_model=LoadOut)
def get_load(load_id: str, db: Session = Depends(get_db)) -> Load:
    """Fetch a single load by its load_id."""
    load = db.query(Load).filter(Load.load_id == load_id).first()
    if not load:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Load {load_id} not found",
        )
    return load
