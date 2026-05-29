import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path(__file__).parent / "events.json"


def _load() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open() as f:
        return json.load(f)


def _save(events: list[dict]) -> None:
    with DATA_FILE.open("w") as f:
        json.dump(events, f, indent=2)


def get_events(category: str | None = None) -> list[dict]:
    events = _load()
    if category:
        events = [e for e in events if e.get("category") == category]
    return sorted(events, key=lambda e: e["date"])


def get_categories() -> list[str]:
    events = _load()
    return sorted({e["category"] for e in events if e.get("category")})


def add_event(date: str, title: str, description: str, category: str) -> dict:
    events = _load()
    event = {
        "id": str(uuid.uuid4()),
        "date": date,
        "title": title,
        "description": description,
        "category": category,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    events.append(event)
    _save(events)
    return event


def delete_event(event_id: str) -> bool:
    events = _load()
    filtered = [e for e in events if e["id"] != event_id]
    if len(filtered) == len(events):
        return False
    _save(filtered)
    return True
