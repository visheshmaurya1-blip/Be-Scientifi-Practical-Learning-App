import random
from bescientific.content import CLASS_LEVELS, SUBJECTS, pick_quiz, questions_for
from bescientific.db import Database
from bescientific.game import (BADGE_FIRST_WIN, BADGE_QUIZ_ACE, QuizSession,
                               level_for_xp, new_badges)
from bescientific.i18n import STRINGS, t
from navigation.access import can_open
from navigation.routes import HOME, QUIZ


def test_every_class_has_quiz_banks():
    for level in CLASS_LEVELS:
        for sid in SUBJECTS:
            pool = questions_for(sid, level)
            assert len(pool) >= 5, (sid, level, len(pool))
            quiz = pick_quiz(sid, level, 5, rng=random.Random(0))
            assert len(quiz) == 5


def test_quiz_session_xp_streak_and_lives():
    qs = pick_quiz("math", 4, 5, rng=random.Random(1))
    session = QuizSession(qs, skill_id="math_quiz", subject_id="math")
    first = session.current
    session.answer(first.correct)
    assert session.xp == 10 and session.streak == 1 and session.lives == 3
    session.answer((session.current.correct + 1) % len(session.current.option_keys))
    assert session.streak == 0 and session.lives == 2
    while not session.finished:
        q = session.current
        session.answer(q.correct)
    assert session.percent >= 0
    assert level_for_xp(0) == 1 and level_for_xp(100) == 2


def test_perfect_run_awards_ace_badge():
    qs = pick_quiz("reasoning", 6, 5, rng=random.Random(2))
    session = QuizSession(qs, skill_id="reasoning_quiz", subject_id="reasoning")
    while not session.finished:
        session.answer(session.current.correct)
    earned = new_badges([], 0, session)
    assert BADGE_FIRST_WIN in earned and BADGE_QUIZ_ACE in earned


def test_facing_north_and_turning_right_twice_is_south():
    question = next(q for q in pick_quiz("reasoning", 6, 6)
                    if q.id == "r56_6")
    assert question.option_keys[question.correct] == "a_south"


def test_db_records_quiz_and_xp():
    db = Database(":memory:")
    sid = db.create_student("Asha", 3)
    qs = pick_quiz("science", 3, 5, rng=random.Random(3))
    session = QuizSession(qs, skill_id="science_quiz", subject_id="science")
    q = session.current
    result = session.answer(q.correct)
    db.record_attempt(sid, "quiz_science", "science_quiz", q.id, result.correct)
    stats = db.apply_session_rewards(sid, session)
    assert stats["xp"] >= 10
    assert "first_win" in stats["badges"]
    db.close()


def test_quiz_strings_exist():
    qs = pick_quiz("math", 1, 5, rng=random.Random(4))
    for q in qs:
        assert t(q.text_key, "en") != q.text_key
        assert STRINGS[q.text_key].get("hi")
    assert t("continue_quiz", "en") == "Continue"
    assert t("continue_quiz", "hi") != "continue_quiz"


def test_navigation_student_can_open_quiz():
    assert can_open(QUIZ, "student")
    assert can_open(HOME, "student")
