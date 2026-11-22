"""FastAPI backend: receives offline progress, serves dashboards, gives tutor hints.

Run:   uvicorn server.main:app --host 0.0.0.0 --port 8000
Env:   DATABASE_URL (PostgreSQL in production), API_KEY (shared secret; if set,
       clients must send it as the X-API-Key header), LLM_* (see tutor.py).
"""
from __future__ import annotations

import os
from collections import defaultdict

from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import tutor
from .database import Base, make_engine, make_session_factory
from .models import Event, Mastery, Student
from .schemas import HintIn, HintOut, SyncIn, SyncOut


def create_app(database_url: str | None = None) -> FastAPI:
    engine = make_engine(database_url)
    Base.metadata.create_all(engine)
    SessionLocal = make_session_factory(engine)
    app = FastAPI(title="Be Scientific API", version="0.1.0")
    app.state.engine = engine

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def check_key(x_api_key: str | None = Header(default=None)):
        expected = os.getenv("API_KEY")
        if expected and x_api_key != expected:
            raise HTTPException(status_code=401, detail="invalid API key")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/v1/sync", response_model=SyncOut, dependencies=[Depends(check_key)])
    def sync(payload: SyncIn, db: Session = Depends(get_db)):
        """Idempotent upload: safe to retry, events are de-duplicated by client UUID."""
        for s in payload.students:
            row = db.get(Student, s.id)
            if row is None:
                db.add(Student(id=s.id, name=s.name, class_level=s.class_level, lang=s.lang,
                               created_at=s.created_at, device_id=payload.device_id))
            else:
                row.name, row.class_level, row.lang = s.name, s.class_level, s.lang
        db.flush()

        known_students = {r for r in db.scalars(select(Student.id))}
        accepted = dupes = 0
        for e in payload.events:
            if e.student_id not in known_students:
                raise HTTPException(422, f"event {e.id} references unknown student {e.student_id}")
            if db.get(Event, e.id) is not None:
                dupes += 1
                continue
            db.add(Event(**e.model_dump()))
            accepted += 1

        m_count = 0
        for m in payload.mastery:
            if m.student_id not in known_students:
                raise HTTPException(422, f"mastery references unknown student {m.student_id}")
            row = db.get(Mastery, (m.student_id, m.skill_id))
            if row is None:
                db.add(Mastery(**m.model_dump()))
                m_count += 1
            elif m.updated_at >= row.updated_at:       # last-writer-wins by timestamp (ISO-8601 UTC)
                row.p_known, row.attempts, row.updated_at = m.p_known, m.attempts, m.updated_at
                m_count += 1
        db.commit()
        return SyncOut(accepted_events=accepted, duplicate_events=dupes,
                       students=len(payload.students), mastery=m_count)

    @app.get("/v1/students/{student_id}/mastery", dependencies=[Depends(check_key)])
    def student_mastery(student_id: str, db: Session = Depends(get_db)):
        if db.get(Student, student_id) is None:
            raise HTTPException(404, "student not found")
        rows = db.scalars(select(Mastery).where(Mastery.student_id == student_id))
        return {r.skill_id: {"p_known": r.p_known, "attempts": r.attempts} for r in rows}

    @app.get("/v1/dashboard", dependencies=[Depends(check_key)])
    def dashboard(class_level: int | None = None, db: Session = Depends(get_db)):
        """Teacher analytics: per-student average mastery and weakest skill, plus skill averages."""
        q = select(Student)
        if class_level is not None:
            q = q.where(Student.class_level == class_level)
        students = list(db.scalars(q))
        ids = [s.id for s in students]
        by_student: dict[str, list[Mastery]] = defaultdict(list)
        if ids:
            for m in db.scalars(select(Mastery).where(Mastery.student_id.in_(ids), Mastery.attempts > 0)):
                by_student[m.student_id].append(m)
        rows, skill_vals = [], defaultdict(list)
        for s in students:
            ms = by_student.get(s.id, [])
            for m in ms:
                skill_vals[m.skill_id].append(m.p_known)
            rows.append({
                "id": s.id, "name": s.name, "class_level": s.class_level,
                "avg_mastery": sum(m.p_known for m in ms) / len(ms) if ms else None,
                "weakest_skill": min(ms, key=lambda m: m.p_known).skill_id if ms else None,
                "attempts": sum(m.attempts for m in ms)})
        return {"students": rows,
                "skill_average": {k: sum(v) / len(v) for k, v in skill_vals.items()}}

    @app.post("/v1/tutor/hint", response_model=HintOut, dependencies=[Depends(check_key)])
    def hint(body: HintIn):
        res = tutor.get_hint(body.skill_id, body.lang, body.attempt)
        if res is None:
            raise HTTPException(404, "unknown skill")
        return HintOut(hint=res[0], source=res[1])

    return app


app = create_app()
