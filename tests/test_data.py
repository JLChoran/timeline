import json
import pytest
from pathlib import Path


@pytest.fixture(autouse=True)
def tmp_data_file(tmp_path, monkeypatch):
    """Point data module at a temp file so tests never touch real data."""
    fake = tmp_path / "events.json"
    import app.data as data_mod
    monkeypatch.setattr(data_mod, "DATA_FILE", fake)
    yield fake


def test_empty_on_start():
    from app.data import get_events
    assert get_events() == []


def test_add_and_retrieve():
    from app.data import add_event, get_events
    add_event("1066-10-14", "Battle of Hastings", "Norman conquest of England", "War")
    events = get_events()
    assert len(events) == 1
    assert events[0]["title"] == "Battle of Hastings"


def test_sorted_by_date():
    from app.data import add_event, get_events
    add_event("1945-09-02", "End of WWII", "", "War")
    add_event("1939-09-01", "Start of WWII", "", "War")
    events = get_events()
    assert events[0]["date"] == "1939-09-01"
    assert events[1]["date"] == "1945-09-02"


def test_filter_by_category():
    from app.data import add_event, get_events
    add_event("1687-01-01", "Principia Mathematica", "", "Science")
    add_event("1066-10-14", "Battle of Hastings", "", "War")
    science = get_events("Science")
    assert len(science) == 1
    assert science[0]["title"] == "Principia Mathematica"


def test_delete_event():
    from app.data import add_event, get_events, delete_event
    event = add_event("1969-07-20", "Moon Landing", "", "Science")
    assert delete_event(event["id"]) is True
    assert get_events() == []


def test_delete_nonexistent():
    from app.data import delete_event
    assert delete_event("fake-id") is False


def test_get_categories():
    from app.data import add_event, get_categories
    add_event("1066-10-14", "Battle of Hastings", "", "War")
    add_event("1687-01-01", "Principia", "", "Science")
    cats = get_categories()
    assert sorted(cats) == ["Science", "War"]
