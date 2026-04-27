"""SQLAlchemy ORM models for loads and calls."""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Load(Base):
    """A freight load available for booking."""

    __tablename__ = "loads"

    load_id: Mapped[str] = mapped_column(String, primary_key=True)
    origin: Mapped[str] = mapped_column(String, index=True)
    destination: Mapped[str] = mapped_column(String, index=True)
    pickup_datetime: Mapped[datetime] = mapped_column(DateTime)
    delivery_datetime: Mapped[datetime] = mapped_column(DateTime)
    equipment_type: Mapped[str] = mapped_column(String, index=True)
    loadboard_rate: Mapped[float] = mapped_column(Float)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    weight: Mapped[int] = mapped_column(Integer)
    commodity_type: Mapped[str] = mapped_column(String)
    num_of_pieces: Mapped[int] = mapped_column(Integer)
    miles: Mapped[int] = mapped_column(Integer)
    dimensions: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="available", index=True)


class Call(Base):
    """A completed inbound carrier call captured from the agent."""

    __tablename__ = "calls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    call_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)

    mc_number: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    company_name: Mapped[str | None] = mapped_column(String, nullable=True)
    carrier_eligible: Mapped[bool | None] = mapped_column(nullable=True)

    load_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("loads.load_id"), nullable=True, index=True
    )
    loadboard_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    final_agreed_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    first_counter_offer: Mapped[float | None] = mapped_column(Float, nullable=True)
    negotiation_rounds: Mapped[int] = mapped_column(Integer, default=0)
    deal_agreed: Mapped[bool] = mapped_column(default=False)
    transfer_initiated: Mapped[bool] = mapped_column(default=False)

    requested_origin: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    requested_destination: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    requested_equipment_type: Mapped[str | None] = mapped_column(String, nullable=True)

    outcome: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    sentiment: Mapped[str | None] = mapped_column(String, nullable=True, index=True)

    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
