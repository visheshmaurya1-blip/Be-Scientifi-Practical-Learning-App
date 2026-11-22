import os
import secrets
from typing import Optional
from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import get_db
from .models import School

ADMIN_KEY = os.getenv("ADMIN_KEY", "change-me-admin")


def _is_admin(key: Optional[str]) -> bool:
    return bool(key) and secrets.compare_digest(key, ADMIN_KEY)


def require_admin(x_admin_key: Optional[str] = Header(None)):
    if not _is_admin(x_admin_key):
        raise HTTPException(401, "Invalid admin key")


def get_school(x_api_key: Optional[str] = Header(None), db: Session = Depends(get_db)) -> School:
    if x_api_key:
        school = db.scalar(select(School).where(School.api_key == x_api_key))
        if school:
            return school
    raise HTTPException(401, "Invalid or missing X-API-Key")


def analytics_scope(
    x_api_key: Optional[str] = Header(None),
    x_admin_key: Optional[str] = Header(None),
    school_id: Optional[str] = None,
    db: Session = Depends(get_db),
) -> Optional[str]:
    """School key -> that school only. Admin key -> all schools (or ?school_id=...)."""
    if _is_admin(x_admin_key):
        return school_id
    if x_api_key:
        school = db.scalar(select(School).where(School.api_key == x_api_key))
        if school:
            return school.id
    raise HTTPException(401, "Provide X-API-Key (school) or X-Admin-Key")
