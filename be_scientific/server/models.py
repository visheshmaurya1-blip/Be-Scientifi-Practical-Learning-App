from __future__ import annotations

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Student(Base):
    __tablename__ = "students"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    class_level: Mapped[int] = mapped_column(Integer)
    lang: Mapped[str] = mapped_column(String(8), default="en")
    created_at: Mapped[str] = mapped_column(String(40))
    device_id: Mapped[str] = mapped_column(String(36), index=True)


class Event(Base):
    __tablename__ = "events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)          # client UUID => idempotent upload
    student_id: Mapped[str] = mapped_column(ForeignKey("students.id"), index=True)
    experiment_id: Mapped[str] = mapped_column(String(64))
    skill_id: Mapped[str] = mapped_column(String(64), index=True)
    question_id: Mapped[str] = mapped_column(String(64))
    correct: Mapped[bool] = mapped_column(Boolean)
    hint_used: Mapped[bool] = mapped_column(Boolean, default=False)
    p_before: Mapped[float] = mapped_column(Float)
    p_after: Mapped[float] = mapped_column(Float)
    ts: Mapped[str] = mapped_column(String(40))


class Mastery(Base):
    __tablename__ = "mastery"
    student_id: Mapped[str] = mapped_column(ForeignKey("students.id"), primary_key=True)
    skill_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    p_known: Mapped[float] = mapped_column(Float)
    attempts: Mapped[int] = mapped_column(Integer)
    updated_at: Mapped[str] = mapped_column(String(40))
