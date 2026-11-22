import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Text, Index
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


def utcnow() -> datetime:
    """Naive UTC (works identically on SQLite and PostgreSQL)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def new_id() -> str:
    return str(uuid.uuid4())


class SyncMixin:
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, index=True)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)


class School(Base):
    __tablename__ = "schools"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String(200))
    state: Mapped[Optional[str]] = mapped_column(String(100))
    board: Mapped[str] = mapped_column(String(50), default="NCERT")  # NCERT / State Board
    api_key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    is_pilot: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class Student(Base):
    __tablename__ = "students"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    school_id: Mapped[str] = mapped_column(ForeignKey("schools.id"), index=True)
    display_name: Mapped[str] = mapped_column(String(100))  # keep PII minimal (children's data)
    grade: Mapped[int] = mapped_column(Integer)             # 1-6
    language: Mapped[str] = mapped_column(String(10), default="en")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class Experiment(Base):
    """Virtual-lab catalog (100+ experiments)."""
    __tablename__ = "experiments"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    title: Mapped[str] = mapped_column(String(200))
    grade: Mapped[int] = mapped_column(Integer)
    subject: Mapped[str] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class MissionProgress(Base, SyncMixin):
    """Inquiry mission, Kolb cycle: 0 none, 1 Do, 2 Reflect, 3 Think, 4 Apply."""
    __tablename__ = "mission_progress"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)  # client-generated UUID
    student_id: Mapped[str] = mapped_column(ForeignKey("students.id"), index=True)
    experiment_id: Mapped[str] = mapped_column(ForeignKey("experiments.id"), index=True)
    stage_completed: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[Optional[float]] = mapped_column(Float)


class AssessmentResult(Base, SyncMixin):
    __tablename__ = "assessment_results"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    student_id: Mapped[str] = mapped_column(ForeignKey("students.id"), index=True)
    experiment_id: Mapped[Optional[str]] = mapped_column(ForeignKey("experiments.id"), index=True)
    skill: Mapped[str] = mapped_column(String(30), index=True)  # reading | math | problem_solving
    score: Mapped[float] = mapped_column(Float)
    max_score: Mapped[float] = mapped_column(Float, default=100.0)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    taken_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, index=True)


class ActivityEvent(Base, SyncMixin):
    """Append-only analytics log."""
    __tablename__ = "activity_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    student_id: Mapped[str] = mapped_column(ForeignKey("students.id"), index=True)
    experiment_id: Mapped[Optional[str]] = mapped_column(ForeignKey("experiments.id"))
    event_type: Mapped[str] = mapped_column(String(40), index=True)  # session_start, experiment_open, hint_used, ai_tutor_query, group_project...
    duration_sec: Mapped[int] = mapped_column(Integer, default=0)
    payload: Mapped[Optional[dict]] = mapped_column(JSON)
    device_id: Mapped[Optional[str]] = mapped_column(String(64))
    occurred_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, index=True)


class SyncChange(Base):
    """Server-side change log; clients pull with `seq` as a cursor."""
    __tablename__ = "sync_changes"
    seq: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    school_id: Mapped[Optional[str]] = mapped_column(String(36), index=True)  # NULL = global (catalog)
    entity: Mapped[str] = mapped_column(String(40))
    entity_id: Mapped[str] = mapped_column(String(36))
    op: Mapped[str] = mapped_column(String(10))
    device_id: Mapped[Optional[str]] = mapped_column(String(64))
    payload: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class Lead(Base):
    """'Partner with Be Scientific' form: schools, CSR/NGO, early adopters."""
    __tablename__ = "leads"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    kind: Mapped[str] = mapped_column(String(20))  # school | csr_ngo | early_adopter
    org_name: Mapped[str] = mapped_column(String(200))
    contact_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200))
    message: Mapped[Optional[str]] = mapped_column(Text)
    demo_requested: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
