"""Offline-first client (runs on the tablet/laptop): works with no internet, syncs when online.

    c = OfflineClient("http://localhost:8000", API_KEY, device_id="tab-01")
    c.log_event(student_id, "session_start", duration_sec=600)
    c.sync()      # push outbox, then pull server changes
"""
import json
import sqlite3
import uuid
from datetime import datetime, timezone
import requests


def now_iso():
    return datetime.now(timezone.utc).isoformat()


class OfflineClient:
    def __init__(self, server: str, api_key: str, device_id: str, path: str = "local_store.db"):
        self.server, self.device_id = server.rstrip("/"), device_id
        self.h = {"X-API-Key": api_key}
        self.db = sqlite3.connect(path)
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS outbox(id TEXT PRIMARY KEY, entity TEXT, op TEXT, data TEXT,
                                              updated_at TEXT, synced INTEGER DEFAULT 0);
            CREATE TABLE IF NOT EXISTS replica(entity TEXT, entity_id TEXT, payload TEXT,
                                               PRIMARY KEY(entity, entity_id));
            CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);
        """)

    # ---- local writes (always succeed offline) ----
    def record(self, entity, data, op="upsert", id=None):
        id = id or str(uuid.uuid4())
        self.db.execute("INSERT OR REPLACE INTO outbox(id,entity,op,data,updated_at,synced) VALUES(?,?,?,?,?,0)",
                        (id, entity, op, json.dumps(data), now_iso()))
        self.db.commit()
        return id

    def log_event(self, student_id, event_type, experiment_id=None, duration_sec=0, **payload):
        return self.record("activity_event", {"student_id": student_id, "event_type": event_type,
                                               "experiment_id": experiment_id, "duration_sec": duration_sec,
                                               "payload": payload, "occurred_at": now_iso()})

    def save_progress(self, student_id, experiment_id, stage_completed, score=None, id=None):
        return self.record("mission_progress", {"student_id": student_id, "experiment_id": experiment_id,
                                                 "stage_completed": stage_completed, "score": score}, id=id)

    def save_assessment(self, student_id, skill, score, max_score=100, experiment_id=None, hints_used=0):
        return self.record("assessment_result", {"student_id": student_id, "skill": skill, "score": score,
                                                  "max_score": max_score, "experiment_id": experiment_id,
                                                  "hints_used": hints_used, "taken_at": now_iso()})

    # ---- sync ----
    def push(self):
        rows = self.db.execute("SELECT id,entity,op,data,updated_at FROM outbox WHERE synced=0 "
                               "ORDER BY updated_at LIMIT 500").fetchall()
        if not rows:
            return 0
        body = {"device_id": self.device_id,
                "changes": [{"id": r[0], "entity": r[1], "op": r[2], "data": json.loads(r[3]),
                             "updated_at": r[4]} for r in rows]}
        resp = requests.post(f"{self.server}/sync/push", json=body, headers=self.h, timeout=30)
        resp.raise_for_status()
        for res in resp.json()["results"]:
            # applied/duplicate/conflict(server wins; arrives on pull)/rejected(bad data) -> don't retry forever
            self.db.execute("UPDATE outbox SET synced=1 WHERE id=?", (res["id"],))
            if res["status"] in ("rejected", "conflict"):
                print("sync:", res["status"], res["id"], res.get("reason"))
        self.db.commit()
        return len(rows)

    def pull(self):
        cur = int((self.db.execute("SELECT v FROM meta WHERE k='cursor'").fetchone() or ["0"])[0])
        total = 0
        while True:
            r = requests.get(f"{self.server}/sync/pull", params={"since": cur}, headers=self.h, timeout=30)
            r.raise_for_status()
            data = r.json()
            for ch in data["changes"]:
                self.db.execute("INSERT OR REPLACE INTO replica VALUES(?,?,?)",
                                (ch["entity"], ch["entity_id"], json.dumps(ch["payload"])))
            total += len(data["changes"])
            cur = data["next_cursor"]
            self.db.execute("INSERT OR REPLACE INTO meta VALUES('cursor',?)", (str(cur),))
            self.db.commit()
            if not data["has_more"]:
                return total

    def sync(self):
        try:
            return {"pushed": self.push(), "pulled": self.pull()}
        except requests.RequestException as e:
            return {"offline": True, "error": str(e)}  # keep working; try again later
