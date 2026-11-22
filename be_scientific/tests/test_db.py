import pytest
from bescientific.db import Database
from bescientific.content import EXPERIMENTS, QUIZ_QUESTIONS, SKILLS, SUBJECTS, pick_question
from bescientific.i18n import STRINGS, t


@pytest.fixture
def db():
    d = Database(":memory:")
    yield d
    d.close()


def test_student_validation(db):
    with pytest.raises(ValueError):
        db.create_student("  ", 3)
    with pytest.raises(ValueError):
        db.create_student("Asha", 9)
    sid = db.create_student("Asha", 4, "hi")
    assert db.get_student(sid)["lang"] == "hi"


def test_record_attempt_updates_bkt_and_counts(db):
    sid = db.create_student("Ravi", 5)
    p0, n0 = db.get_mastery(sid, "friction")
    assert n0 == 0 and p0 == SKILLS["friction"].params.p_init
    out = db.record_attempt(sid, "friction", "friction", "friction_q1", True)
    assert out["p_after"] > p0 and out["attempts"] == 1
    out2 = db.record_attempt(sid, "friction", "friction", "friction_q2", False)
    assert out2["p_after"] < out["p_after"] and out2["attempts"] == 2
    assert db.get_mastery(sid, "friction") == (pytest.approx(out2["p_after"]), 2)


def test_repeated_wrong_answers_trigger_remediation(db):
    sid = db.create_student("Meena", 3)
    last = None
    for _ in range(4):
        last = db.record_attempt(sid, "bounce", "elasticity", "bounce_q1", False)
    assert last["action"] == "remediate"


def test_unsynced_queue_and_mark_synced(db):
    sid = db.create_student("Ravi", 5)
    db.record_attempt(sid, "gravity", "gravity_equal_fall", "gravity_q1", True)
    assert db.pending_counts() == 3          # student + event + mastery
    batch = db.unsynced_batch()
    assert len(batch["events"]) == 1 and len(batch["mastery"]) == 1
    db.mark_synced(batch)
    assert db.pending_counts() == 0


def test_mastery_changed_after_read_stays_unsynced(db):
    sid = db.create_student("Ravi", 5)
    db.record_attempt(sid, "gravity", "gravity_equal_fall", "gravity_q1", True)
    batch = db.unsynced_batch()
    db._conn.execute("UPDATE mastery SET updated_at='2099-01-01T00:00:00+00:00'")  # simulate a newer attempt
    db.mark_synced(batch)
    assert db.pending_counts() == 1          # the newer mastery row is still waiting


def test_class_summary(db):
    a = db.create_student("A", 4)
    b = db.create_student("B", 4)
    for _ in range(3):
        db.record_attempt(a, "gravity", "gravity_equal_fall", "gravity_q1", True)
        db.record_attempt(b, "gravity", "gravity_equal_fall", "gravity_q1", False)
    s = {r["name"]: r for r in db.class_summary()}
    assert s["A"]["avg"] > s["B"]["avg"] and s["B"]["weakest"] == "gravity_equal_fall"


def test_device_id_is_stable(db):
    assert db.device_id() == db.device_id()


def test_hindi_study_content_is_available_for_every_class(db):
    from bescientific.study_materials import CLASS_1_STUDY_COURSES
    from bescientific.study_materials_class2 import CLASS_2_STUDY_COURSES
    from bescientific.study_materials_class3 import CLASS_3_STUDY_COURSES
    from bescientific.study_materials_class4 import CLASS_4_STUDY_COURSES
    from bescientific.study_materials_class5 import CLASS_5_STUDY_COURSES
    from bescientific.study_materials_class6 import CLASS_6_STUDY_COURSES

    source_catalogs = (
        CLASS_1_STUDY_COURSES, CLASS_2_STUDY_COURSES, CLASS_3_STUDY_COURSES,
        CLASS_4_STUDY_COURSES, CLASS_5_STUDY_COURSES, CLASS_6_STUDY_COURSES,
    )
    for class_level, source_courses in enumerate(source_catalogs, start=1):
        localized_courses = db.hindi_study_courses(class_level)
        assert set(localized_courses) == set(source_courses)
        for course_id, source_course in source_courses.items():
            localized_course = localized_courses[course_id]
            assert localized_course.title_hi == source_course.title_hi
            assert localized_course.book_hi == source_course.book_hi
            assert len(localized_course.lessons) == len(source_course.lessons)
            for localized, source in zip(localized_course.lessons, source_course.lessons):
                assert localized.id == source.id
                assert localized.chapter_hi == source.chapter_hi
                assert localized.hi == source.hi


def test_hindi_study_content_persists_in_sqlite(tmp_path):
    path = tmp_path / "hindi-study.db"
    db = Database(path)
    original = db.hindi_study_courses(6)["science"].lessons[0].hi
    db.close()

    reopened = Database(path)
    assert reopened.hindi_study_courses(6)["science"].lessons[0].hi == original
    assert reopened._conn.execute(
        "SELECT COUNT(*) FROM hindi_study_lessons").fetchone()[0] == 322
    reopened.close()


def test_every_catalogue_string_exists_in_both_languages():
    keys = set()
    for sk in SKILLS.values():
        keys |= {sk.name_key, sk.hint_key, sk.explain_key}
    for sub in SUBJECTS.values():
        keys |= {sub.name_key, sub.desc_key}
    for e in EXPERIMENTS.values():
        keys |= {e.module_key, e.title_key, e.desc_key}
        for q in e.questions:
            keys |= {q.text_key, *q.option_keys}
            assert 0 <= q.correct < len(q.option_keys)
    for q in QUIZ_QUESTIONS:
        keys |= {q.text_key, *q.option_keys}
        assert 0 <= q.correct < len(q.option_keys)
        assert q.skill_id in SKILLS
    for k in keys:
        assert k in STRINGS, k
        assert STRINGS[k].get("en") and STRINGS[k].get("hi"), k
    assert pick_question(EXPERIMENTS["gravity"], 4).id == "gravity_q2"      # rotation wraps
    assert t("hello", "hi", name="Asha").startswith("नमस्ते")
    assert t("missing_key") == "missing_key"
