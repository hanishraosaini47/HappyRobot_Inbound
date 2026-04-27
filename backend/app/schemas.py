"""Pydantic schemas for API request and response shapes."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ----------- Loads ----------- #


class LoadOut(BaseModel):
    """Load data returned to the agent and dashboard."""

    model_config = ConfigDict(from_attributes=True)

    load_id: str
    origin: str
    destination: str
    pickup_datetime: datetime
    delivery_datetime: datetime
    equipment_type: str
    loadboard_rate: float
    notes: str | None = None
    weight: int
    commodity_type: str
    num_of_pieces: int
    miles: int
    dimensions: str
    status: str


# ----------- Calls ----------- #


class CallIn(BaseModel):
    """Payload posted by HappyRobot after each call ends.

    Defensive: tolerates HappyRobot's quirks where the platform sometimes
    sends 'null' (string) instead of null, numbers as strings, etc.
    """

    call_id: str
    timestamp: datetime | None = None
    duration_seconds: int | None = None

    mc_number: str | int | None = None
    company_name: str | None = None
    carrier_eligible: bool | None = None

    load_id: str | None = None
    loadboard_rate: float | None = None
    final_agreed_rate: float | None = None
    first_counter_offer: float | None = None
    negotiation_rounds: int = 0
    deal_agreed: bool = False
    transfer_initiated: bool = False

    requested_origin: str | None = None
    requested_destination: str | None = None
    requested_equipment_type: str | None = None

    outcome: str | None = None
    sentiment: str | None = None

    transcript: str | list | None = None

    @field_validator(
        "duration_seconds",
        "loadboard_rate",
        "final_agreed_rate",
        "first_counter_offer",
        "negotiation_rounds",
        "carrier_eligible",
        "deal_agreed",
        "transfer_initiated",
        "load_id",
        "company_name",
        "requested_origin",
        "requested_destination",
        "requested_equipment_type",
        "outcome",
        "sentiment",
        "mc_number",
        mode="before",
    )
    @classmethod
    def empty_string_to_none(cls, v: Any) -> Any:
        """Coerce 'null', 'None', and empty strings to actual None.

        HappyRobot's webhook sometimes sends string 'null' instead of JSON null.
        """
        if isinstance(v, str) and v.strip().lower() in ("null", "none", ""):
            return None
        return v


class CallOut(BaseModel):
    """Call data returned to the dashboard."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    call_id: str
    timestamp: datetime
    duration_seconds: int | None = None
    mc_number: str | None = None
    company_name: str | None = None
    carrier_eligible: bool | None = None
    load_id: str | None = None
    loadboard_rate: float | None = None
    final_agreed_rate: float | None = None
    first_counter_offer: float | None = None
    negotiation_rounds: int
    deal_agreed: bool
    transfer_initiated: bool
    requested_origin: str | None = None
    requested_destination: str | None = None
    requested_equipment_type: str | None = None
    outcome: str | None = None
    sentiment: str | None = None
    transcript: str | None = None


# ----------- Metrics ----------- #


class LaneCount(BaseModel):
    """A requested lane and how many times carriers asked for it."""

    origin: str
    destination: str
    count: int


class MetricsOut(BaseModel):
    """Aggregated metrics for the dashboard."""

    total_calls: int
    booked_calls: int
    booking_rate: float = Field(description="0.0 to 1.0")
    avg_negotiated_rate: float | None = None
    avg_negotiation_rounds: float | None = None
    avg_rate_uplift_pct: float | None = Field(
        default=None,
        description="Average % above loadboard rate for booked deals",
    )
    avg_first_counter_offer_pct: float | None = Field(
        default=None,
        description="Average carrier first counter-offer as % above loadboard rate",
    )

    total_loads: int
    available_loads: int
    booked_loads: int

    outcome_breakdown: dict[str, int]
    sentiment_breakdown: dict[str, int]

    top_requested_lanes: list[LaneCount]
    top_requested_equipment: dict[str, int]
