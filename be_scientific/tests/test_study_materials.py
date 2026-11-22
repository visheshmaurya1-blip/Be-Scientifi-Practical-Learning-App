from types import SimpleNamespace

from bescientific.study_materials import CLASS_1_STUDY_COURSES
from bescientific.study_materials_class2 import CLASS_2_STUDY_COURSES
from bescientific.study_materials_class3 import CLASS_3_STUDY_COURSES
from bescientific.study_materials_class4 import CLASS_4_STUDY_COURSES
from bescientific.study_materials_class5 import CLASS_5_STUDY_COURSES
from bescientific.study_materials_class6 import CLASS_6_STUDY_COURSES
from bescientific.virtual_activities import (CLASS_1_VIRTUAL_ACTIVITIES,
                                             CLASS_1_VIRTUAL_OBJECTS,
                                             CLASS_2_VIRTUAL_ACTIVITIES,
                                             CLASS_2_VIRTUAL_OBJECTS,
                                             CLASS_3_VIRTUAL_ACTIVITIES,
                                             CLASS_3_VIRTUAL_OBJECTS,
                                             CLASS_4_VIRTUAL_ACTIVITIES,
                                             CLASS_4_VIRTUAL_OBJECTS,
                                             CLASS_5_VIRTUAL_ACTIVITIES,
                                             CLASS_5_VIRTUAL_OBJECTS,
                                             CLASS_6_VIRTUAL_ACTIVITIES,
                                             CLASS_6_VIRTUAL_OBJECTS)
from bescientific.ui.theme import FONT_FILE, FONT_NAME, register_fonts
from navigation.access import can_open
from navigation.routes import STUDY


def test_class_one_ncert_core_courses_cover_all_book_units():
    assert {course_id: len(course.lessons)
            for course_id, course in CLASS_1_STUDY_COURSES.items()} == {
                "math": 13,
                "english": 9,
                "hindi": 19,
            }
    assert all(course.source_url.startswith("https://ncert.nic.in/textbook/pdf/")
               for course in CLASS_1_STUDY_COURSES.values())


def test_every_study_unit_has_bilingual_original_material():
    lesson_ids = []
    for catalog in (
        CLASS_1_STUDY_COURSES,
        CLASS_2_STUDY_COURSES,
        CLASS_3_STUDY_COURSES,
        CLASS_4_STUDY_COURSES,
        CLASS_5_STUDY_COURSES,
        CLASS_6_STUDY_COURSES,
    ):
        for course in catalog.values():
            for lesson in course.lessons:
                lesson_ids.append(lesson.id)
                assert lesson.chapter_en and lesson.chapter_hi
                for text in (lesson.en, lesson.hi):
                    assert all((text.focus, text.learn, text.activity, text.check, text.answer))
    assert len(lesson_ids) == len(set(lesson_ids))


def test_every_class_one_lesson_activity_has_a_valid_virtual_simulation():
    lesson_ids = {
        lesson.id
        for course in CLASS_1_STUDY_COURSES.values()
        for lesson in course.lessons
    }
    assert set(CLASS_1_VIRTUAL_ACTIVITIES) == lesson_ids
    assert set(CLASS_1_VIRTUAL_OBJECTS) == lesson_ids
    for activity in CLASS_1_VIRTUAL_ACTIVITIES.values():
        assert activity.prompt_en and activity.prompt_hi
        assert len(activity.choices) >= 2
        assert all(english and hindi for english, hindi in activity.choices)
        assert 0 <= activity.answer_index < len(activity.choices)
    for lesson_id, objects in CLASS_1_VIRTUAL_OBJECTS.items():
        assert len(objects) == len(CLASS_1_VIRTUAL_ACTIVITIES[lesson_id].choices)
        assert all(objects)


def test_every_class_two_lesson_activity_has_a_valid_virtual_simulation():
    lesson_ids = {
        lesson.id
        for course in CLASS_2_STUDY_COURSES.values()
        for lesson in course.lessons
    }
    assert set(CLASS_2_VIRTUAL_ACTIVITIES) == lesson_ids
    assert set(CLASS_2_VIRTUAL_OBJECTS) == lesson_ids
    for lesson_id, activity in CLASS_2_VIRTUAL_ACTIVITIES.items():
        assert activity.prompt_en and activity.prompt_hi
        assert len(activity.choices) >= 2
        assert all(english and hindi for english, hindi in activity.choices)
        assert 0 <= activity.answer_index < len(activity.choices)
        objects = CLASS_2_VIRTUAL_OBJECTS[lesson_id]
        assert len(objects) == len(activity.choices)
        assert all(objects)


def test_every_class_three_lesson_activity_has_a_valid_virtual_simulation():
    lesson_ids = {
        lesson.id
        for course in CLASS_3_STUDY_COURSES.values()
        for lesson in course.lessons
    }
    assert set(CLASS_3_VIRTUAL_ACTIVITIES) == lesson_ids
    assert set(CLASS_3_VIRTUAL_OBJECTS) == lesson_ids
    for lesson_id, activity in CLASS_3_VIRTUAL_ACTIVITIES.items():
        assert activity.prompt_en and activity.prompt_hi
        assert len(activity.choices) >= 2
        assert all(english and hindi for english, hindi in activity.choices)
        assert 0 <= activity.answer_index < len(activity.choices)
        objects = CLASS_3_VIRTUAL_OBJECTS[lesson_id]
        assert len(objects) == len(activity.choices)
        assert all(objects)


def _assert_class_virtual_catalog(study_courses, activities, object_catalog):
    lesson_ids = {lesson.id for course in study_courses.values()
                  for lesson in course.lessons}
    assert set(activities) == lesson_ids
    assert set(object_catalog) == lesson_ids
    for lesson_id, activity in activities.items():
        assert activity.prompt_en and activity.prompt_hi
        assert len(activity.choices) >= 2
        assert all(english and hindi for english, hindi in activity.choices)
        assert 0 <= activity.answer_index < len(activity.choices)
        assert len(object_catalog[lesson_id]) == len(activity.choices)
        assert all(object_catalog[lesson_id])


def test_every_class_four_lesson_activity_has_a_valid_virtual_simulation():
    _assert_class_virtual_catalog(
        CLASS_4_STUDY_COURSES, CLASS_4_VIRTUAL_ACTIVITIES, CLASS_4_VIRTUAL_OBJECTS)


def test_every_class_five_lesson_activity_has_a_valid_virtual_simulation():
    _assert_class_virtual_catalog(
        CLASS_5_STUDY_COURSES, CLASS_5_VIRTUAL_ACTIVITIES, CLASS_5_VIRTUAL_OBJECTS)


def test_every_class_six_lesson_activity_has_a_valid_virtual_simulation():
    _assert_class_virtual_catalog(
        CLASS_6_STUDY_COURSES, CLASS_6_VIRTUAL_ACTIVITIES, CLASS_6_VIRTUAL_OBJECTS)


def test_class_two_ncert_core_courses_cover_all_book_units():
    assert {course_id: len(course.lessons)
            for course_id, course in CLASS_2_STUDY_COURSES.items()} == {
                "math": 11,
                "english": 13,
                "hindi": 26,
            }
    assert all(course.source_url.startswith("https://ncert.nic.in/textbook/pdf/")
               for course in CLASS_2_STUDY_COURSES.values())


def test_students_can_open_study_material():
    assert can_open(STUDY, "student")


def test_devanagari_font_is_registered_for_kivymd_nested_styles():
    theme = SimpleNamespace(font_styles={
        "Body": {
            "large": {"font-name": "Roboto", "font-size": 20},
            "small": {"font-name": "Roboto", "font-size": 15},
        }
    })
    assert FONT_FILE.is_file()
    assert register_fonts(theme)
    assert all(
        style["font-name"] == FONT_NAME
        for style in theme.font_styles["Body"].values()
    )


def test_class_three_ncert_courses_cover_all_core_book_units():
    assert {course_id: len(course.lessons)
            for course_id, course in CLASS_3_STUDY_COURSES.items()} == {
                "math": 14,
                "english": 12,
                "hindi": 18,
                "world": 12,
            }
    assert all(course.source_url.startswith("https://ncert.nic.in/textbook/pdf/")
               for course in CLASS_3_STUDY_COURSES.values())
    assert CLASS_3_STUDY_COURSES["math"].source_url_hi.endswith("chmm1ps.pdf")
    assert CLASS_3_STUDY_COURSES["hindi"].source_url.endswith("chve1ps.pdf")
    assert CLASS_3_STUDY_COURSES["english"].source_url.endswith("cesa1ps.pdf")
    assert CLASS_3_STUDY_COURSES["world"].source_url_hi.endswith("chev1ps.pdf")


def test_class_four_ncert_courses_cover_all_core_book_units():
    assert {course_id: len(course.lessons)
            for course_id, course in CLASS_4_STUDY_COURSES.items()} == {
                "math": 14,
                "english": 12,
                "hindi": 13,
                "world": 10,
            }
    assert all(course.source_url.startswith("https://ncert.nic.in/textbook/pdf/")
               for course in CLASS_4_STUDY_COURSES.values())
    assert CLASS_4_STUDY_COURSES["math"].source_url.endswith("demm1ps.pdf")
    assert CLASS_4_STUDY_COURSES["math"].source_url_hi.endswith("dhmm1ps.pdf")
    assert CLASS_4_STUDY_COURSES["english"].source_url.endswith("desa1ps.pdf")
    assert CLASS_4_STUDY_COURSES["hindi"].source_url.endswith("dhve1ps.pdf")
    assert CLASS_4_STUDY_COURSES["world"].source_url.endswith("deev1ps.pdf")
    assert CLASS_4_STUDY_COURSES["world"].source_url_hi.endswith("dhev1ps.pdf")


def test_class_five_ncert_courses_cover_all_core_book_units():
    assert {course_id: len(course.lessons)
            for course_id, course in CLASS_5_STUDY_COURSES.items()} == {
                "math": 15,
                "english": 10,
                "hindi": 10,
                "world": 10,
            }
    assert all(course.source_url.startswith("https://ncert.nic.in/textbook/pdf/")
               for course in CLASS_5_STUDY_COURSES.values())
    assert CLASS_5_STUDY_COURSES["math"].source_url.endswith("eemm1ps.pdf")
    assert CLASS_5_STUDY_COURSES["math"].source_url_hi.endswith("ehmm1ps.pdf")
    assert CLASS_5_STUDY_COURSES["english"].source_url.endswith("eesa1ps.pdf")
    assert CLASS_5_STUDY_COURSES["hindi"].source_url.endswith("ehve1ps.pdf")
    assert CLASS_5_STUDY_COURSES["world"].source_url.endswith("eeev1ps.pdf")
    assert CLASS_5_STUDY_COURSES["world"].source_url_hi.endswith("ehev1ps.pdf")


def test_class_six_ncert_courses_cover_all_core_book_units():
    assert {course_id: len(course.lessons)
            for course_id, course in CLASS_6_STUDY_COURSES.items()} == {
                "math": 10,
                "english": 16,
                "hindi": 13,
                "science": 12,
                "social": 14,
                "sanskrit": 16,
            }
    assert all(course.source_url.startswith("https://ncert.nic.in/textbook/pdf/")
               for course in CLASS_6_STUDY_COURSES.values())
    assert CLASS_6_STUDY_COURSES["math"].source_url.endswith("fegp1ps.pdf")
    assert CLASS_6_STUDY_COURSES["math"].source_url_hi.endswith("fhgp1ps.pdf")
    assert CLASS_6_STUDY_COURSES["english"].source_url.endswith("fepr1ps.pdf")
    assert CLASS_6_STUDY_COURSES["hindi"].source_url.endswith("fhml1ps.pdf")
    assert CLASS_6_STUDY_COURSES["science"].source_url.endswith("fecu1ps.pdf")
    assert CLASS_6_STUDY_COURSES["social"].source_url.endswith("fees1ps.pdf")
    assert CLASS_6_STUDY_COURSES["sanskrit"].source_url.endswith("fsde1ps.pdf")
    assert all(
        not any("\u0900" <= character <= "\u097f" for character in lesson.en.learn)
        for lesson in CLASS_6_STUDY_COURSES["hindi"].lessons
    )
