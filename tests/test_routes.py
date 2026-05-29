import pytest
from app import create_app
import app.data as data_mod


@pytest.fixture
def client(tmp_path, monkeypatch):
    fake = tmp_path / "events.json"
    monkeypatch.setattr(data_mod, "DATA_FILE", fake)
    flask_app = create_app()
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


def test_index_empty(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"No events yet" in resp.data


def test_add_get(client):
    resp = client.get("/add")
    assert resp.status_code == 200
    assert b"Add a New Event" in resp.data


def test_add_post_and_redirect(client):
    resp = client.post("/add", data={
        "date": "1066-10-14",
        "title": "Battle of Hastings",
        "description": "Norman conquest",
        "category": "War",
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Battle of Hastings" in resp.data


def test_add_post_missing_fields(client):
    resp = client.post("/add", data={"title": "No date"}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"required" in resp.data


def test_delete_event(client):
    client.post("/add", data={
        "date": "1969-07-20",
        "title": "Moon Landing",
        "description": "",
        "category": "Science",
    })
    events = data_mod.get_events()
    event_id = events[0]["id"]
    resp = client.post(f"/delete/{event_id}", follow_redirects=True)
    assert resp.status_code == 200
    assert b"No events yet" in resp.data
