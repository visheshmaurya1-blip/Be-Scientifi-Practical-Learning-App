"""Offline-first sync: clients push local changes, then pull server changes by cursor.

Rules
- IDs are client-generated UUIDs, so records can be created offline without collisions.
- Last-write-wins on `updated_at` for mission_progress / assessment_result.
- activity_event is append-only and idempotent (re-sending the same id is a no-op).
- Every accepted change is written to `sync_changes`; that table is the pull feed.
"""
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, or_, DateTime
from sqlalchemy.orm import Session
from .database import get_db
from .deps import get_school
from .models import (School, Student, Experiment, MissionProgress, AssessmentResult,
                     ActivityEvent, SyncChange)
from .schemas import PushRequest, PushResponse, ChangeResult, PullResponse, PullChange

router = APIRouter(prefix="/sync", tags=["sync"])

ENTITIES = {
    "mission_progress": MissionProgress,
    "assessment_result": AssessmentResult,
    "activity_event": ActivityEvent,
}
APPEND_ONLY = {"activity_event"}
REQUIRED = {
    "mission_progress": ["student_id", "experiment_id"],
    "assessment_result": ["student_id", "skill", "score"],
    "activity_event": ["student_id", "event_type"],
}


def to_naive_utc(dt: datetime) -> datetime:
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def serialize(row) -> dict:
    out = {}
    for c in row.__table__.columns:
        v = getattr(row, c.name)
        out[c.name] = v.isoformat() if isinstance(v, datetime) else v
    return out


def _clean(model, data: dict) -> dict:
    out = {}
    for c in model.__table__.columns:
        if c.name in ("id", "updated_at", "deleted") or c.name not in data:
            continue
        v = data[c.name]
        if isinstance(c.type, DateTime) and isinstance(v, str):
            v = to_naive_utc(datetime.fromisoformat(v.replace("Z", "+00:00")))
        out[c.name] = v
    return out


def log_change(db: Session, school_id: Optional[str], entity: str, row, op="upsert", device_id=None):
    db.add(SyncChange(school_id=school_id, entity=entity, entity_id=row.id, op=op,
                      device_id=device_id, payload=serialize(row)))


def apply_change(db, school, device_id, ch, student_ids, exp_ids) -> ChangeResult:
    model = ENTITIES[ch.entity]
    ts = to_naive_utc(ch.updated_at)
    row = db.get(model, ch.id)

    if row is not None and row.student_id not in student_ids:
        return ChangeResult(id=ch.id, status="rejected", reason="id belongs to another school")

    if ch.op == "delete":
        if row is None:
            return ChangeResult(id=ch.id, status="rejected", reason="not found")
        if ch.entity in APPEND_ONLY:
            return ChangeResult(id=ch.id, status="rejected", reason="append-only entity")
        if row.updated_at > ts:
            return ChangeResult(id=ch.id, status="conflict", server_version=serialize(row))
        row.deleted, row.updated_at = True, ts
        log_change(db, school.id, ch.entity, row, "delete", device_id)
        return ChangeResult(id=ch.id, status="applied")

    data = _clean(model, ch.data)
    if ch.entity == "activity_event":
        data["device_id"] = device_id

    if row is None:
        missing = [f for f in REQUIRED[ch.entity] if data.get(f) is None]
        if missing:
            return ChangeResult(id=ch.id, status="rejected", reason=f"missing fields: {missing}")
        if data["student_id"] not in student_ids:
            return ChangeResult(id=ch.id, status="rejected", reason="unknown student for this school")
        if data.get("experiment_id") and data["experiment_id"] not in exp_ids:
            return ChangeResult(id=ch.id, status="rejected", reason="unknown experiment")
        row = model(id=ch.id, updated_at=ts, deleted=False, **data)
        db.add(row)
    else:
        if ch.entity in APPEND_ONLY:
            return ChangeResult(id=ch.id, status="duplicate")
        if row.updated_at > ts:
            return ChangeResult(id=ch.id, status="conflict", server_version=serialize(row))
        data.pop("student_id", None)  # ownership can't change
        if data.get("experiment_id") and data["experiment_id"] not in exp_ids:
            return ChangeResult(id=ch.id, status="rejected", reason="unknown experiment")
        for k, v in data.items():
            setattr(row, k, v)
        row.updated_at, row.deleted = ts, False

    db.flush()
    log_change(db, school.id, ch.entity, row, "upsert", device_id)
    return ChangeResult(id=ch.id, status="applied")


@router.post("/push", response_model=PushResponse)
def push(req: PushRequest, school: School = Depends(get_school), db: Session = Depends(get_db)):
    student_ids = set(db.scalars(select(Student.id).where(Student.school_id == school.id)))
    exp_ids = set(db.scalars(select(Experiment.id)))
    results = []
    for ch in req.changes:
        try:
            with db.begin_nested():  # savepoint: one bad record never poisons the batch
                results.append(apply_change(db, school, req.device_id, ch, student_ids, exp_ids))
        except Exception as e:  # noqa
            results.append(ChangeResult(id=ch.id, status="rejected", reason=f"error: {type(e).__name__}"))
    db.commit()
    cursor = db.scalar(select(SyncChange.seq).order_by(SyncChange.seq.desc()).limit(1)) or 0
    return PushResponse(results=results, server_cursor=cursor)


@router.get("/pull", response_model=PullResponse)
def pull(since: int = Query(0, ge=0), limit: int = Query(500, ge=1, le=1000),
         school: School = Depends(get_school), db: Session = Depends(get_db)):
    rows = db.scalars(
        select(SyncChange)
        .where(SyncChange.seq > since, or_(SyncChange.school_id == school.id, SyncChange.school_id.is_(None)))
        .order_by(SyncChange.seq).limit(limit + 1)
    ).all()
    has_more = len(rows) > limit
    rows = rows[:limit]
    next_cursor = rows[-1].seq if rows else since
    return PullResponse(
        changes=[PullChange(seq=r.seq, entity=r.entity, entity_id=r.entity_id, op=r.op,
                            device_id=r.device_id, payload=r.payload) for r in rows],
        next_cursor=next_cursor, has_more=has_more)
