import pytest
from fastapi.testclient import TestClient

from bescientific.db import Database
from bescientific.sync import SyncClient
from bescientific import tutor as client_tutor
from server.main import create_app


@pytest.fixture
def api(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    return TestClient(create_app("sqlite:///:memory:"))


@pytest.fixture
def db():
    d = Database(":memory:")
    yield d
    d.close()


def _post_via(client):
    # TestClient.post(url, json=..., headers=...) mirrors requests.post; `timeout` is not accepted.
    return lambda url, json=None, headers=None, timeout=None: client.post(url.replace("http://test", ""),
                                                                           json=json, headers=headers)


def _seed(db):
    sid = db.create_student("Asha", 4)
    db.record_attempt(sid, "gravity", "gravity_equal_fall", "gravity_q1", True)
    db.record_attempt(sid, "friction", "friction", "friction_q1", False)
    return sid


def test_full_offline_to_server_round_trip(api, db):
    sid = _seed(db)
    sc = SyncClient(db, "http://test", post=_post_via(api))
    r = sc.sync_all()
    assert r.ok and r.sent == 5 and db.pending_counts() == 0       # 1 student + 2 events + 2 mastery
    mastery = api.get(f"/v1/students/{sid}/mastery").json()
    assert set(mastery) == {"gravity_equal_fall", "friction"}
    dash = api.get("/v1/dashboard").json()
    assert dash["students"][0]["name"] == "Asha" and dash["students"][0]["attempts"] == 2


def test_retrying_the_same_upload_is_idempotent(api, db):
    _seed(db)
    batch = db.unsynced_batch()
    payload = {"device_id": db.device_id(), **batch}
    first = api.post("/v1/sync", json=payload).json()
    second = api.post("/v1/sync", json=payload).json()
    assert first["accepted_events"] == 2 and second["accepted_events"] == 0 and second["duplicate_events"] == 2


def test_failed_sync_keeps_data_queued(db):
    _seed(db)
    def offline(*a, **k):
        raise ConnectionError("no network")
    r = SyncClient(db, "http://test", post=offline).sync_once()
    assert not r.ok and "ConnectionError" in r.error and db.pending_counts() == 5


def test_server_error_status_keeps_data_queued(db):
    _seed(db)
    class R: status_code = 503
    r = SyncClient(db, "http://test", post=lambda *a, **k: R()).sync_once()
    assert not r.ok and r.error == "HTTP 503" and db.pending_counts() == 5


def test_api_key_is_enforced_when_configured(monkeypatch, db):
    monkeypatch.setenv("API_KEY", "s3cret")
    api = TestClient(create_app("sqlite:///:memory:"))
    _seed(db)
    bad = SyncClient(db, "http://test", api_key="wrong", post=_post_via(api)).sync_once()
    assert not bad.ok and bad.error == "HTTP 401"
    good = SyncClient(db, "http://test", api_key="s3cret", post=_post_via(api)).sync_once()
    assert good.ok


def test_event_for_unknown_student_is_rejected(api, db):
    sid = _seed(db)
    batch = db.unsynced_batch()
    batch["students"] = []                           # student never uploaded
    r = api.post("/v1/sync", json={"device_id": "d", **batch})
    assert r.status_code == 422


def test_validation_rejects_bad_probabilities(api, db):
    _seed(db)
    batch = db.unsynced_batch()
    batch["events"][0]["p_after"] = 1.7
    assert api.post("/v1/sync", json={"device_id": "d", **batch}).status_code == 422


def test_tutor_endpoint_falls_back_to_static_hint(api):
    r = api.post("/v1/tutor/hint", json={"skill_id": "friction", "lang": "hi", "attempt": 2})
    assert r.status_code == 200 and r.json()["source"] == "static" and "घर्षण" in r.json()["hint"]
    assert api.post("/v1/tutor/hint", json={"skill_id": "nope"}).status_code == 404


def test_client_cloud_hint_falls_back_to_none_on_failure():
    def boom(*a, **k):
        raise TimeoutError()
    assert client_tutor.cloud_hint("http://x", "friction", "q", "en", 1, post=boom) is None
    assert client_tutor.local_hint("friction", "en")
