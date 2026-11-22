from __future__ import annotations

from pydantic import BaseModel, Field


class StudentIn(BaseModel):
    id: str = Field(min_length=1, max_length=36)
    name: str = Field(min_length=1, max_length=120)
    class_level: int = Field(ge=1, le=6)
    lang: str = "en"
    created_at: str


class EventIn(BaseModel):
    id: str = Field(min_length=1, max_length=36)
    student_id: str
    experiment_id: str
    skill_id: str
    question_id: str
    correct: bool
    hint_used: bool = False
    p_before: float = Field(ge=0, le=1)
    p_after: float = Field(ge=0, le=1)
    ts: str


class MasteryIn(BaseModel):
    student_id: str
    skill_id: str
    p_known: float = Field(ge=0, le=1)
    attempts: int = Field(ge=0)
    updated_at: str


class SyncIn(BaseModel):
    device_id: str = Field(min_length=1, max_length=36)
    students: list[StudentIn] = []
    events: list[EventIn] = []
    mastery: list[MasteryIn] = []


class SyncOut(BaseModel):
    accepted_events: int
    duplicate_events: int
    students: int
    mastery: int


class HintIn(BaseModel):
    skill_id: str
    question_id: str = ""
    lang: str = "en"
    attempt: int = 1


class HintOut(BaseModel):
    hint: str
    source: str   # "llm" or "static"
