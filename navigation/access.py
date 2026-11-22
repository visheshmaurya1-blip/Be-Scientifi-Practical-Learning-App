"""Who can open which screen. Students stay in learning screens; teacher view is a summary."""

from .routes import HOME, LAB, PROFILE, PROGRESS, QUIZ, SCIENCE, STUDY, TEACHER, WELCOME

STUDENT_SCREENS = {WELCOME, HOME, SCIENCE, QUIZ, LAB, PROGRESS, PROFILE, STUDY}
TEACHER_SCREENS = STUDENT_SCREENS | {TEACHER}


def can_open(screen: str, role: str = "student") -> bool:
    allowed = TEACHER_SCREENS if role == "teacher" else STUDENT_SCREENS
    return screen in allowed
