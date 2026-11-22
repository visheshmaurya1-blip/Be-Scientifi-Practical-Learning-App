"""Analytics that back the dashboard ideas in the deck (engagement, mastery, Kolb funnel, retention, pilot)."""
from collections import defaultdict
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, true
from sqlalchemy.orm import Session
from .database import get_db
from .deps import analytics_scope, require_admin
from .models import (Student, School, Experiment, MissionProgress, AssessmentResult,
                     ActivityEvent, Lead, utcnow)

router = APIRouter(prefix="/analytics", tags=["analytics"])
KOLB = ["do", "reflect", "think", "apply"]
PILOT_TARGET = {"schools": 5, "students": 500, "months": 6}


def _mine(col, sid: Optional[str]):
    return col.in_(select(Student.id).where(Student.school_id == sid)) if sid else true()


def _pct(score_col, max_col):
    return score_col * 100.0 / max_col


@router.get("/overview")
def overview(sid: Optional[str] = Depends(analytics_scope), db: Session = Depends(get_db)):
    since7 = utcnow() - timedelta(days=7)
    students = db.scalar(select(func.count()).select_from(Student).where(
        Student.school_id == sid if sid else true()))
    active7 = db.scalar(select(func.count(func.distinct(ActivityEvent.student_id))).where(
        _mine(ActivityEvent.student_id, sid), ActivityEvent.occurred_at >= since7,
        ActivityEvent.deleted.is_(False)))
    minutes = db.scalar(select(func.coalesce(func.sum(ActivityEvent.duration_sec), 0)).where(
        _mine(ActivityEvent.student_id, sid), ActivityEvent.deleted.is_(False))) / 60
    missions = db.scalar(select(func.count()).select_from(MissionProgress).where(
        _mine(MissionProgress.student_id, sid), MissionProgress.deleted.is_(False)))
    done = db.scalar(select(func.count()).select_from(MissionProgress).where(
        _mine(MissionProgress.student_id, sid), MissionProgress.deleted.is_(False),
        MissionProgress.stage_completed >= 4))
    avg = db.scalar(select(func.avg(_pct(AssessmentResult.score, AssessmentResult.max_score))).where(
        _mine(AssessmentResult.student_id, sid), AssessmentResult.deleted.is_(False)))
    return {
        "students": students,
        "active_students_7d": active7,
        "active_rate_7d_pct": round(active7 * 100 / students, 1) if students else 0,
        "total_learning_minutes": round(minutes, 1),
        "missions_started": missions,
        "mission_completion_pct": round(done * 100 / missions, 1) if missions else 0,
        "avg_assessment_pct": round(avg, 1) if avg is not None else None,
    }


@router.get("/engagement")
def engagement(days: int = Query(30, ge=1, le=365), sid: Optional[str] = Depends(analytics_scope),
               db: Session = Depends(get_db)):
    since = utcnow() - timedelta(days=days)
    day = func.date(ActivityEvent.occurred_at).label("day")
    rows = db.execute(
        select(day, func.count(func.distinct(ActivityEvent.student_id)),
               func.coalesce(func.sum(ActivityEvent.duration_sec), 0), func.count())
        .where(_mine(ActivityEvent.student_id, sid), ActivityEvent.occurred_at >= since,
               ActivityEvent.deleted.is_(False))
        .group_by(day).order_by(day)).all()
    return [{"date": str(d), "active_students": a, "minutes": round(s / 60, 1), "events": n}
            for d, a, s, n in rows]


@router.get("/mastery")
def mastery(sid: Optional[str] = Depends(analytics_scope), db: Session = Depends(get_db)):
    """Average % by skill: reading comprehension / math / problem solving."""
    rows = db.execute(
        select(AssessmentResult.skill, func.avg(_pct(AssessmentResult.score, AssessmentResult.max_score)),
               func.count(), func.avg(AssessmentResult.hints_used))
        .where(_mine(AssessmentResult.student_id, sid), AssessmentResult.deleted.is_(False))
        .group_by(AssessmentResult.skill)).all()
    return [{"skill": s, "avg_pct": round(a, 1), "attempts": n, "avg_hints": round(h or 0, 2)}
            for s, a, n, h in rows]


@router.get("/kolb-funnel")
def kolb_funnel(sid: Optional[str] = Depends(analytics_scope), db: Session = Depends(get_db)):
    """How many missions reach each Do -> Reflect -> Think -> Apply stage."""
    out, base = [], None
    for i, name in enumerate(KOLB, start=1):
        n = db.scalar(select(func.count()).select_from(MissionProgress).where(
            _mine(MissionProgress.student_id, sid), MissionProgress.deleted.is_(False),
            MissionProgress.stage_completed >= i))
        base = base if base is not None else n
        out.append({"stage": name, "missions": n, "pct_of_first_stage": round(n * 100 / base, 1) if base else 0})
    return out


@router.get("/experiments")
def top_experiments(limit: int = Query(10, ge=1, le=100), sid: Optional[str] = Depends(analytics_scope),
                    db: Session = Depends(get_db)):
    rows = db.execute(
        select(Experiment.id, Experiment.title, Experiment.grade, func.count(MissionProgress.id),
               func.avg(MissionProgress.score))
        .join(MissionProgress, MissionProgress.experiment_id == Experiment.id)
        .where(_mine(MissionProgress.student_id, sid), MissionProgress.deleted.is_(False))
        .group_by(Experiment.id, Experiment.title, Experiment.grade)
        .order_by(func.count(MissionProgress.id).desc()).limit(limit)).all()
    return [{"experiment_id": i, "title": t, "grade": g, "attempts": n,
             "avg_score": round(a, 1) if a is not None else None} for i, t, g, n, a in rows]


@router.get("/retention")
def retention(min_gap_days: int = Query(14, ge=1), sid: Optional[str] = Depends(analytics_scope),
              db: Session = Depends(get_db)):
    """Measured retention: for each student+experiment, compare the first score with a later re-test
    taken at least `min_gap_days` later. Compute this from real data before quoting retention claims."""
    rows = db.execute(
        select(AssessmentResult.student_id, AssessmentResult.experiment_id, AssessmentResult.taken_at,
               _pct(AssessmentResult.score, AssessmentResult.max_score))
        .where(_mine(AssessmentResult.student_id, sid), AssessmentResult.deleted.is_(False),
               AssessmentResult.experiment_id.is_not(None))
        .order_by(AssessmentResult.taken_at)).all()
    groups = defaultdict(list)
    for st, ex, ts, pct in rows:
        groups[(st, ex)].append((ts, pct))
    ratios = []
    for attempts in groups.values():
        first_ts, first_pct = attempts[0]
        later = [p for t, p in attempts[1:] if t - first_ts >= timedelta(days=min_gap_days)]
        if later and first_pct > 0:
            ratios.append(later[-1] / first_pct)
    if not ratios:
        return {"pairs_measured": 0, "avg_retention_ratio": None, "retained_80pct_share": None}
    return {"pairs_measured": len(ratios),
            "avg_retention_ratio": round(sum(ratios) / len(ratios), 3),
            "retained_80pct_share": round(sum(r >= 0.8 for r in ratios) * 100 / len(ratios), 1)}


@router.get("/pilot", dependencies=[Depends(require_admin)])
def pilot(db: Session = Depends(get_db)):
    """Pilot programme tracker (deck: 5 schools, 500 students, 6 months) + partner pipeline."""
    schools = db.scalar(select(func.count()).select_from(School).where(School.is_pilot.is_(True)))
    students = db.scalar(select(func.count()).select_from(Student).join(School).where(School.is_pilot.is_(True)))
    leads = dict(db.execute(select(Lead.kind, func.count()).group_by(Lead.kind)).all())
    return {
        "schools": {"enrolled": schools, "target": PILOT_TARGET["schools"]},
        "students": {"enrolled": students, "target": PILOT_TARGET["students"]},
        "duration_months": PILOT_TARGET["months"],
        "leads_by_type": leads,
    }
