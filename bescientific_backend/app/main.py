import secrets
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session
from . import analytics, sync
from .database import Base, engine, get_db
from .deps import get_school, require_admin
from .models import School, Student, Experiment, Lead
from .schemas import (SchoolCreate, SchoolOut, StudentCreate, StudentOut,
                      ExperimentCreate, ExperimentOut, LeadCreate)
from .sync import log_change


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)  # use Alembic migrations in production
    yield


app = FastAPI(title="Be Scientific API", version="1.0.0", lifespan=lifespan,
              description="Backend for the Be Scientific learning platform (Class 1-6, NCERT aligned).")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])  # restrict in prod
app.include_router(sync.router)
app.include_router(analytics.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/curriculum")
def curriculum():
    """Class 1-6 subjects used by the tablet/desktop client (offline copy lives in content.py)."""
    return {
        "classes": [{"id": n, "label": f"Class {n}"} for n in range(1, 7)],
        "subjects": [
            {"id": "science", "name_key": "subject_science", "modes": ["lab", "quiz"]},
            {"id": "math", "name_key": "subject_math", "modes": ["quiz"]},
            {"id": "reasoning", "name_key": "subject_reasoning", "modes": ["quiz"]},
        ],
        "skills": ["math", "science", "reasoning", "problem_solving"],
    }


# ---------- admin ----------
@app.post("/admin/schools", response_model=SchoolOut, dependencies=[Depends(require_admin)])
def create_school(body: SchoolCreate, db: Session = Depends(get_db)):
    school = School(**body.model_dump(), api_key=secrets.token_urlsafe(32))
    db.add(school)
    db.commit()
    return school  # includes api_key once


@app.get("/admin/schools", response_model=list[SchoolOut], dependencies=[Depends(require_admin)])
def list_schools(db: Session = Depends(get_db)):
    schools = db.scalars(select(School)).all()
    return [SchoolOut.model_validate(s).model_copy(update={"api_key": None}) for s in schools]


@app.post("/admin/experiments", response_model=ExperimentOut, dependencies=[Depends(require_admin)])
def create_experiment(body: ExperimentCreate, db: Session = Depends(get_db)):
    exp = Experiment(**body.model_dump())
    db.add(exp)
    db.flush()
    log_change(db, None, "experiment", exp)  # pushed to every school's devices on next pull
    db.commit()
    return exp


@app.get("/admin/leads", dependencies=[Depends(require_admin)])
def list_leads(db: Session = Depends(get_db)):
    return db.scalars(select(Lead).order_by(Lead.created_at.desc())).all()


# ---------- school-facing ----------
@app.get("/experiments", response_model=list[ExperimentOut])
def experiments(grade: Optional[int] = None, school: School = Depends(get_school), db: Session = Depends(get_db)):
    q = select(Experiment).where(Experiment.is_active.is_(True))
    if grade:
        q = q.where(Experiment.grade == grade)
    return db.scalars(q).all()


@app.post("/students", response_model=StudentOut)
def create_student(body: StudentCreate, school: School = Depends(get_school), db: Session = Depends(get_db)):
    student = Student(school_id=school.id, **body.model_dump())
    db.add(student)
    db.flush()
    log_change(db, school.id, "student", student)
    db.commit()
    return student


@app.get("/students", response_model=list[StudentOut])
def list_students(school: School = Depends(get_school), db: Session = Depends(get_db)):
    return db.scalars(select(Student).where(Student.school_id == school.id)).all()


# ---------- public: "Partner with Be Scientific" form ----------
@app.post("/leads", status_code=201)
def create_lead(body: LeadCreate, db: Session = Depends(get_db)):
    lead = Lead(**body.model_dump())
    db.add(lead)
    db.commit()
    return {"id": lead.id, "message": "Thanks! We'll contact you to schedule a demo."}
