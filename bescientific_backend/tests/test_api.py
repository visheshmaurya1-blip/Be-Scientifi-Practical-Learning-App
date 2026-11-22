import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["ADMIN_KEY"] = "adm"
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app

A = {"X-Admin-Key": "adm"}


def iso(days_ago=0):
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()


def test_flow():
    with TestClient(app) as c:
        s = c.post("/admin/schools", json={"name": "Pilot School 1", "is_pilot": True}, headers=A).json()
        H = {"X-API-Key": s["api_key"]}
        exp = c.post("/admin/experiments", json={"title": "Plant Growth", "grade": 3, "subject": "EVS"}, headers=A).json()
        st = c.post("/students", json={"display_name": "Asha", "grade": 3}, headers=H).json()

        mp, ev = str(uuid4()), str(uuid4())
        changes = [
            {"entity": "mission_progress", "id": mp, "updated_at": iso(),
             "data": {"student_id": st["id"], "experiment_id": exp["id"], "stage_completed": 4, "score": 80}},
            {"entity": "activity_event", "id": ev, "updated_at": iso(),
             "data": {"student_id": st["id"], "event_type": "session_start", "duration_sec": 600, "occurred_at": iso()}},
            {"entity": "assessment_result", "id": str(uuid4()), "updated_at": iso(20),
             "data": {"student_id": st["id"], "experiment_id": exp["id"], "skill": "math", "score": 50, "taken_at": iso(20)}},
            {"entity": "assessment_result", "id": str(uuid4()), "updated_at": iso(),
             "data": {"student_id": st["id"], "experiment_id": exp["id"], "skill": "math", "score": 45, "taken_at": iso()}},
            {"entity": "activity_event", "id": str(uuid4()), "updated_at": iso(),
             "data": {"student_id": "bogus", "event_type": "x"}},
        ]
        r = c.post("/sync/push", json={"device_id": "tab1", "changes": changes}, headers=H).json()
        assert [x["status"] for x in r["results"]] == ["applied"] * 4 + ["rejected"]

        # idempotent re-send + stale-write conflict
        again = c.post("/sync/push", json={"device_id": "tab1", "changes": [changes[1]]}, headers=H).json()
        assert again["results"][0]["status"] == "duplicate"
        old = dict(changes[0], updated_at=iso(5), data={**changes[0]["data"], "stage_completed": 1})
        assert c.post("/sync/push", json={"device_id": "t", "changes": [old]}, headers=H).json()["results"][0]["status"] == "conflict"

        p = c.get("/sync/pull?since=0", headers=H).json()
        assert {x["entity"] for x in p["changes"]} >= {"experiment", "student", "mission_progress"}

        o = c.get("/analytics/overview", headers=H).json()
        assert o["students"] == 1 and o["mission_completion_pct"] == 100.0
        assert c.get("/analytics/mastery", headers=H).json()[0]["skill"] == "math"
        assert c.get("/analytics/kolb-funnel", headers=H).json()[3]["missions"] == 1
        assert c.get("/analytics/retention", headers=H).json()["pairs_measured"] == 1
        assert len(c.get("/analytics/engagement", headers=H).json()) == 1
        assert c.get("/analytics/pilot", headers=A).json()["schools"]["enrolled"] == 1
        assert c.post("/leads", json={"kind": "school", "org_name": "X", "contact_name": "Y", "email": "a@b.co"}).status_code == 201
        assert c.get("/students").status_code == 401
        cur = c.get("/curriculum").json()
        assert {s["id"] for s in cur["subjects"]} == {"science", "math", "reasoning"}
        assert len(cur["classes"]) == 6
