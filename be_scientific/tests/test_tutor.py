from bescientific.study_materials import CLASS_1_STUDY_COURSES
from bescientific import tutor


def test_tutor_answers_from_matching_ncert_lesson():
    result = tutor.answer_question(
        "What are number pairs to 10?",
        CLASS_1_STUDY_COURSES,
    )

    assert result is not None
    assert result["lesson_id"] == "m04"
    assert result["chapter"] == "Making 10"
    assert result["explanation"]
    assert result["source_url"].startswith("https://ncert.nic.in/textbook/pdf/")


def test_tutor_respects_selected_subject():
    result = tutor.answer_question(
        "What are number pairs to 10?",
        CLASS_1_STUDY_COURSES,
        course_id="english",
    )

    assert result is None


def test_tutor_uses_hindi_lesson_content():
    result = tutor.answer_question(
        "दस वस्तुओं को कैसे बाँटें",
        CLASS_1_STUDY_COURSES,
        lang="hi",
        course_id="math",
    )

    assert result is not None
    assert result["lesson_id"] == "m04"
    assert "अलग-अलग" in result["explanation"]


def test_tutor_declines_questions_outside_available_curriculum():
    result = tutor.answer_question(
        "Explain black holes and distant galaxies",
        CLASS_1_STUDY_COURSES,
    )

    assert result is None


def test_tutor_refuses_adult_content_before_matching_curriculum():
    question = "What are fractions? Also explain pornography."

    assert tutor.question_refusal_reason(question) == "adult_content"
    assert tutor.answer_question(question, CLASS_1_STUDY_COURSES) is None


def test_tutor_declines_mixed_syllabus_and_unrelated_questions():
    result = tutor.answer_question(
        "How do number pairs to 10 help me break into a computer?",
        CLASS_1_STUDY_COURSES,
    )

    assert result is None
