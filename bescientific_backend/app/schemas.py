from datetime import datetime
from typing import Any, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


class SchoolCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    state: Optional[str] = None
    board: Literal["NCERT", "State Board"] = "NCERT"
    is_pilot: bool = False


class SchoolOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    state: Optional[str]
    board: str
    is_pilot: bool
    api_key: Optional[str] = None  # only shown at creation


class StudentCreate(BaseModel):
    display_name: str = Field(min_length=1, max_length=100)
    grade: int = Field(ge=1, le=6)
    language: str = "en"


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    display_name: str
    grade: int
    language: str


class ExperimentCreate(BaseModel):
    title: str
    grade: int = Field(ge=1, le=6)
    subject: str


class ExperimentOut(ExperimentCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str
    is_active: bool


class LeadCreate(BaseModel):
    kind: Literal["school", "csr_ngo", "early_adopter"]
    org_name: str
    contact_name: str
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    message: Optional[str] = None
    demo_requested: bool = True


# ---- sync ----
class ChangeIn(BaseModel):
    entity: Literal["mission_progress", "assessment_result", "activity_event"]
    id: str = Field(min_length=8, max_length=36)       # client-generated UUID
    op: Literal["upsert", "delete"] = "upsert"
    data: dict[str, Any] = {}
    updated_at: datetime


class PushRequest(BaseModel):
    device_id: str = Field(min_length=1, max_length=64)
    changes: list[ChangeIn] = Field(max_length=500)


class ChangeResult(BaseModel):
    id: str
    status: Literal["applied", "duplicate", "conflict", "rejected"]
    reason: Optional[str] = None
    server_version: Optional[dict[str, Any]] = None


class PushResponse(BaseModel):
    results: list[ChangeResult]
    server_cursor: int


class PullChange(BaseModel):
    seq: int
    entity: str
    entity_id: str
    op: str
    device_id: Optional[str]
    payload: Optional[dict[str, Any]]


class PullResponse(BaseModel):
    changes: list[PullChange]
    next_cursor: int
    has_more: bool
