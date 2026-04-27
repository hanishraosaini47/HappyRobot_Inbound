"""Seed the database with sample loads.

Run from the backend/ directory:
    python -m seed.seed
"""

import json
from datetime import datetime
from pathlib import Path

from app.database import Base, SessionLocal, engine
from app.models import Load


def main() -> None:
    # Make sure tables exist
    Base.metadata.create_all(bind=engine)

    seed_file = Path(__file__).parent / "loads.json"
    with seed_file.open() as f:
        loads_data = json.load(f)

    db = SessionLocal()
    try:
        inserted = 0
        skipped = 0
        for entry in loads_data:
            existing = db.query(Load).filter(Load.load_id == entry["load_id"]).first()
            if existing:
                skipped += 1
                continue

            load = Load(
                load_id=entry["load_id"],
                origin=entry["origin"],
                destination=entry["destination"],
                pickup_datetime=datetime.fromisoformat(entry["pickup_datetime"]),
                delivery_datetime=datetime.fromisoformat(entry["delivery_datetime"]),
                equipment_type=entry["equipment_type"],
                loadboard_rate=entry["loadboard_rate"],
                notes=entry.get("notes"),
                weight=entry["weight"],
                commodity_type=entry["commodity_type"],
                num_of_pieces=entry["num_of_pieces"],
                miles=entry["miles"],
                dimensions=entry["dimensions"],
                status="available",
            )
            db.add(load)
            inserted += 1

        db.commit()
        print(f"✓ Seed complete. Inserted: {inserted}, Skipped (already existed): {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
