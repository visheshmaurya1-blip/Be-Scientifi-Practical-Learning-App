"""Offline-first local store (SQLite).

All learning data is written here first. Rows carry a `synced` flag; the sync
client uploads unsynced rows later and marks them. Event ids are UUIDs so the
server can accept the same event twice without double counting.
"""
from __future__ import annotations

import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

import json

from . import bkt
from .content import SKILLS
from .game import new_badges

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS students (
    id TEXT PRIMARY KEY, name TEXT NOT NULL, class_level INTEGER NOT NULL,
    lang TEXT NOT NULL DEFAULT 'en', created_at TEXT NOT NULL, synced INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY, student_id TEXT NOT NULL REFERENCES students(id),
    experiment_id TEXT NOT NULL, skill_id TEXT NOT NULL, question_id TEXT NOT NULL,
    correct INTEGER NOT NULL, hint_used INTEGER NOT NULL DEFAULT 0,
    p_before REAL NOT NULL, p_after REAL NOT NULL, ts TEXT NOT NULL,
    synced INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS mastery (
    student_id TEXT NOT NULL REFERENCES students(id), skill_id TEXT NOT NULL,
    p_known REAL NOT NULL, attempts INTEGER NOT NULL DEFAULT 0, updated_at TEXT NOT NULL,
    synced INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (student_id, skill_id));
CREATE INDEX IF NOT EXISTS idx_events_unsynced ON events(synced);
CREATE TABLE IF NOT EXISTS student_stats (
    student_id TEXT PRIMARY KEY REFERENCES students(id),
    xp INTEGER NOT NULL DEFAULT 0,
    coins INTEGER NOT NULL DEFAULT 0,
    streak INTEGER NOT NULL DEFAULT 0,
    best_streak INTEGER NOT NULL DEFAULT 0,
    badges TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL,
    synced INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS hindi_study_courses (
    class_level INTEGER NOT NULL,
    course_id TEXT NOT NULL,
    title_hi TEXT NOT NULL,
    book_hi TEXT NOT NULL,
    source_url_hi TEXT,
    PRIMARY KEY (class_level, course_id));
CREATE TABLE IF NOT EXISTS hindi_study_lessons (
    class_level INTEGER NOT NULL,
    course_id TEXT NOT NULL,
    lesson_id TEXT NOT NULL,
    chapter_hi TEXT NOT NULL,
    focus_hi TEXT NOT NULL,
    learn_hi TEXT NOT NULL,
    activity_hi TEXT NOT NULL,
    check_hi TEXT NOT NULL,
    answer_hi TEXT NOT NULL,
    PRIMARY KEY (class_level, course_id, lesson_id),
    FOREIGN KEY (class_level, course_id)
        REFERENCES hindi_study_courses(class_level, course_id));
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Database:
    def __init__(self, path: str | Path = ":memory:"):
        self.path = str(path)
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        with self._tx():
            self._conn.executescript(SCHEMA)
            self._ensure_stats_table()
            self._seed_hindi_study_content()

    @contextmanager
    def _tx(self):
        try:
            yield self._conn
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise

    def close(self) -> None:
        self._conn.close()

    def _ensure_stats_table(self) -> None:
        # SCHEMA already creates it on fresh DBs; this is a no-op safety net.
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS student_stats ("
            "student_id TEXT PRIMARY KEY REFERENCES students(id), "
            "xp INTEGER NOT NULL DEFAULT 0, coins INTEGER NOT NULL DEFAULT 0, "
            "streak INTEGER NOT NULL DEFAULT 0, best_streak INTEGER NOT NULL DEFAULT 0, "
            "badges TEXT NOT NULL DEFAULT '[]', updated_at TEXT NOT NULL, "
            "synced INTEGER NOT NULL DEFAULT 0)")

    def _study_course_catalogs(self) -> dict:
        from .study_materials import CLASS_1_STUDY_COURSES
        from .study_materials_class2 import CLASS_2_STUDY_COURSES
        from .study_materials_class3 import CLASS_3_STUDY_COURSES
        from .study_materials_class4 import CLASS_4_STUDY_COURSES
        from .study_materials_class5 import CLASS_5_STUDY_COURSES
        from .study_materials_class6 import CLASS_6_STUDY_COURSES

        return {
            1: CLASS_1_STUDY_COURSES,
            2: CLASS_2_STUDY_COURSES,
            3: CLASS_3_STUDY_COURSES,
            4: CLASS_4_STUDY_COURSES,
            5: CLASS_5_STUDY_COURSES,
            6: CLASS_6_STUDY_COURSES,
        }

    def _seed_hindi_study_content(self) -> None:
        self._conn.execute("DELETE FROM hindi_study_lessons")
        self._conn.execute("DELETE FROM hindi_study_courses")
        for class_level, courses in self._study_course_catalogs().items():
            for course in courses.values():
                self._conn.execute(
                    "INSERT INTO hindi_study_courses "
                    "(class_level, course_id, title_hi, book_hi, source_url_hi) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (class_level, course.id, course.title_hi, course.book_hi,
                     course.source_url_hi),
                )
                self._conn.executemany(
                    "INSERT INTO hindi_study_lessons "
                    "(class_level, course_id, lesson_id, chapter_hi, focus_hi, "
                    "learn_hi, activity_hi, check_hi, answer_hi) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        (class_level, course.id, lesson.id, lesson.chapter_hi,
                         lesson.hi.focus, lesson.hi.learn, lesson.hi.activity,
                         lesson.hi.check, lesson.hi.answer)
                        for lesson in course.lessons
                    ),
                )

    def hindi_study_courses(self, class_level: int) -> dict:
        from .study_materials import LessonText, StudyCourse, StudyLesson

        source_courses = self._study_course_catalogs().get(class_level, {})
        course_rows = self._conn.execute(
            "SELECT course_id, title_hi, book_hi, source_url_hi "
            "FROM hindi_study_courses WHERE class_level = ? ORDER BY course_id",
            (class_level,),
        ).fetchall()
        localized_courses = {}
        for course_row in course_rows:
            source = source_courses[course_row["course_id"]]
            lesson_rows = self._conn.execute(
                "SELECT lesson_id, chapter_hi, focus_hi, learn_hi, activity_hi, "
                "check_hi, answer_hi FROM hindi_study_lessons "
                "WHERE class_level = ? AND course_id = ? ORDER BY rowid",
                (class_level, course_row["course_id"]),
            ).fetchall()
            source_lessons = {lesson.id: lesson for lesson in source.lessons}
            lessons = tuple(
                StudyLesson(
                    lesson_row["lesson_id"],
                    source_lessons[lesson_row["lesson_id"]].chapter_en,
                    lesson_row["chapter_hi"],
                    source_lessons[lesson_row["lesson_id"]].en,
                    LessonText(
                        lesson_row["focus_hi"], lesson_row["learn_hi"],
                        lesson_row["activity_hi"], lesson_row["check_hi"],
                        lesson_row["answer_hi"],
                    ),
                )
                for lesson_row in lesson_rows
            )
            localized_courses[course_row["course_id"]] = StudyCourse(
                source.id, source.title_en, course_row["title_hi"],
                source.book_en, course_row["book_hi"], source.source_url,
                lessons, course_row["source_url_hi"],
            )
        return localized_courses

    # ---------------------------------------------------------------- device
    def device_id(self) -> str:
        row = self._conn.execute("SELECT value FROM meta WHERE key='device_id'").fetchone()
        if row:
            return row["value"]
        did = str(uuid.uuid4())
        with self._tx() as c:
            c.execute("INSERT INTO meta(key,value) VALUES('device_id',?)", (did,))
        return did

    # -------------------------------------------------------------- students
    def create_student(self, name: str, class_level: int, lang: str = "en") -> str:
        name = name.strip()
        if not name:
            raise ValueError("name required")
        if not 1 <= int(class_level) <= 6:
            raise ValueError("class_level must be 1-6")
        sid = str(uuid.uuid4())
        with self._tx() as c:
            c.execute("INSERT INTO students(id,name,class_level,lang,created_at) VALUES(?,?,?,?,?)",
                      (sid, name, int(class_level), lang, _now()))
            c.execute("INSERT INTO student_stats(student_id,xp,coins,streak,best_streak,badges,updated_at) "
                      "VALUES(?,0,0,0,0,'[]',?)", (sid, _now()))
        return sid

    def get_student(self, student_id: str) -> dict | None:
        row = self._conn.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
        return dict(row) if row else None

    def list_students(self) -> list[dict]:
        return [dict(r) for r in self._conn.execute("SELECT * FROM students ORDER BY name")]

    def set_student_lang(self, student_id: str, lang: str) -> None:
        with self._tx() as c:
            c.execute("UPDATE students SET lang=?, synced=0 WHERE id=?", (lang, student_id))

    # -------------------------------------------------------------- mastery
    def get_mastery(self, student_id: str, skill_id: str) -> tuple[float, int]:
        """Return (p_known, attempts); the skill's prior if there are no attempts yet."""
        row = self._conn.execute("SELECT p_known, attempts FROM mastery WHERE student_id=? AND skill_id=?",
                                 (student_id, skill_id)).fetchone()
        if row:
            return row["p_known"], row["attempts"]
        return SKILLS[skill_id].params.p_init, 0

    def all_mastery(self, student_id: str) -> dict[str, tuple[float, int]]:
        return {sk: self.get_mastery(student_id, sk) for sk in SKILLS}

    def record_attempt(self, student_id: str, experiment_id: str, skill_id: str, question_id: str,
                       correct: bool, hint_used: bool = False) -> dict:
        """Log one answered question and update BKT atomically. Returns the outcome."""
        params = SKILLS[skill_id].params
        p_before, attempts = self.get_mastery(student_id, skill_id)
        p_after = bkt.update(p_before, correct, params)
        now = _now()
        with self._tx() as c:
            c.execute("INSERT INTO events(id,student_id,experiment_id,skill_id,question_id,correct,hint_used,"
                      "p_before,p_after,ts) VALUES(?,?,?,?,?,?,?,?,?,?)",
                      (str(uuid.uuid4()), student_id, experiment_id, skill_id, question_id,
                       int(correct), int(hint_used), p_before, p_after, now))
            c.execute("INSERT INTO mastery(student_id,skill_id,p_known,attempts,updated_at,synced) "
                      "VALUES(?,?,?,?,?,0) ON CONFLICT(student_id,skill_id) DO UPDATE SET "
                      "p_known=excluded.p_known, attempts=excluded.attempts, "
                      "updated_at=excluded.updated_at, synced=0",
                      (student_id, skill_id, p_after, attempts + 1, now))
        return {"p_before": p_before, "p_after": p_after, "attempts": attempts + 1,
                "action": bkt.next_action(p_after, attempts + 1)}

    # -------------------------------------------------------------- gamification
    def get_stats(self, student_id: str) -> dict:
        row = self._conn.execute("SELECT * FROM student_stats WHERE student_id=?", (student_id,)).fetchone()
        if not row:
            now = _now()
            with self._tx() as c:
                c.execute("INSERT INTO student_stats(student_id,xp,coins,streak,best_streak,badges,updated_at) "
                          "VALUES(?,0,0,0,0,'[]',?)", (student_id, now))
            return {"student_id": student_id, "xp": 0, "coins": 0, "streak": 0,
                    "best_streak": 0, "badges": [], "updated_at": now, "synced": 0}
        d = dict(row)
        try:
            d["badges"] = json.loads(d["badges"] or "[]")
        except ValueError:
            d["badges"] = []
        return d

    def apply_session_rewards(self, student_id: str, session) -> dict:
        """Fold a finished (or in-progress) quiz session into persistent XP/streak/badges."""
        stats = self.get_stats(student_id)
        last = session.history[-1] if session.history else None
        streak = last.streak if last else 0
        best = max(stats["best_streak"], session.best_streak, streak)
        badges = list(stats["badges"])
        earned = new_badges(badges, stats["xp"], session)
        badges.extend(earned)
        xp = stats["xp"] + (last.xp_gain if last else 0)
        coins = stats["coins"] + (last.coins_gain if last else 0)
        # persist running streak across questions in the same and later sessions
        now = _now()
        with self._tx() as c:
            c.execute("UPDATE student_stats SET xp=?, coins=?, streak=?, best_streak=?, badges=?, "
                      "updated_at=?, synced=0 WHERE student_id=?",
                      (xp, coins, streak, best, json.dumps(badges), now, student_id))
        out = self.get_stats(student_id)
        out["new_badges"] = earned
        return out

    # ----------------------------------------------------------------- sync
    def pending_counts(self) -> int:
        q = self._conn.execute
        return (q("SELECT COUNT(*) FROM events WHERE synced=0").fetchone()[0]
                + q("SELECT COUNT(*) FROM mastery WHERE synced=0").fetchone()[0]
                + q("SELECT COUNT(*) FROM students WHERE synced=0").fetchone()[0])

    def unsynced_batch(self, limit: int = 500) -> dict:
        c = self._conn
        return {
            "students": [dict(r) for r in c.execute(
                "SELECT id,name,class_level,lang,created_at FROM students WHERE synced=0 LIMIT ?", (limit,))],
            "events": [dict(r) for r in c.execute(
                "SELECT id,student_id,experiment_id,skill_id,question_id,correct,hint_used,p_before,p_after,ts "
                "FROM events WHERE synced=0 ORDER BY ts LIMIT ?", (limit,))],
            "mastery": [dict(r) for r in c.execute(
                "SELECT student_id,skill_id,p_known,attempts,updated_at FROM mastery WHERE synced=0 LIMIT ?",
                (limit,))],
        }

    def mark_synced(self, batch: dict) -> None:
        with self._tx() as c:
            c.executemany("UPDATE students SET synced=1 WHERE id=?", [(s["id"],) for s in batch["students"]])
            c.executemany("UPDATE events SET synced=1 WHERE id=?", [(e["id"],) for e in batch["events"]])
            # Only mark mastery rows that have not changed since they were read.
            c.executemany("UPDATE mastery SET synced=1 WHERE student_id=? AND skill_id=? AND updated_at=?",
                          [(m["student_id"], m["skill_id"], m["updated_at"]) for m in batch["mastery"]])

    # -------------------------------------------------------------- teacher
    def class_summary(self) -> list[dict]:
        """Per-student average mastery and weakest skill, computed locally (no network)."""
        out = []
        for s in self.list_students():
            m = self.all_mastery(s["id"])
            attempted = {k: v for k, v in m.items() if v[1] > 0}
            avg = sum(p for p, _ in attempted.values()) / len(attempted) if attempted else None
            weakest = min(attempted, key=lambda k: attempted[k][0]) if attempted else None
            out.append({"id": s["id"], "name": s["name"], "class_level": s["class_level"],
                        "avg": avg, "weakest": weakest,
                        "attempts": sum(a for _, a in m.values())})
        return out
