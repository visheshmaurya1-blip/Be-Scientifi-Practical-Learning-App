"""KivyMD 2 application: wires Database, sync, labs, quizzes and the platform backend."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import NoTransition

ROOT = Path(__file__).resolve().parent.parent
PKG = ROOT / "be_scientific"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

from bescientific.content import SUBJECTS, pick_quiz
from bescientific.db import Database
from bescientific.game import QUESTIONS_PER_RUN, QuizSession
from bescientific.i18n import DEFAULT_LANG, t
from bescientific.sync import SyncClient, SyncWorker
from bescientific.ui.theme import register_fonts
from navigation.routes import HOME, LAB, QUIZ, SCIENCE, STUDY, TUTOR, WELCOME
from .scenery import LOGO_IMAGE
from .screens import SCREENS


class BeScientificApp(MDApp):
    """Unified client. Optional env:

        BESCIENTIFIC_API_URL       FastAPI tutor/sync (be_scientific/server)
        BESCIENTIFIC_PLATFORM_URL  school platform (bescientific_backend)
        BESCIENTIFIC_API_KEY       shared secret
    """

    def __init__(self, db_path: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self._db_path = db_path
        self.lang = DEFAULT_LANG
        self.student_id: str | None = None
        self.current_experiment: str | None = None
        self.current_subject: str | None = None
        self.current_study_lesson: str | None = None
        self.current_tutor_course: str | None = None
        self.current_tutor_lesson: str | None = None
        self.quiz_session = None
        self.api_url: str | None = None
        self.api_key: str | None = None
        self.platform_url: str | None = None
        self.sync_worker: SyncWorker | None = None
        self.sync_enabled = False

    def build(self):
        self.title = "Be Scientific"
        if LOGO_IMAGE:
            self.icon = LOGO_IMAGE
        Window.clearcolor = (0.82, 0.90, 0.88, 1)
        self.theme_cls.theme_style_switch_animation = False
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        register_fonts(self.theme_cls)
        self.db = Database(self._db_path or os.path.join(self.user_data_dir, "bescientific.db"))
        self._load_settings()
        sm = MDScreenManager(size_hint=(1, 1), transition=NoTransition())
        for name, cls in SCREENS:
            sm.add_widget(cls(name=name))
        sm.current = WELCOME
        self._setup_sync()
        return sm

    def on_start(self):
        def refresh_initial_screen(_dt):
            if not self.root:
                return
            welcome = self.root.get_screen(WELCOME)
            self.root.current = WELCOME
            welcome.on_pre_enter()

        Clock.schedule_once(refresh_initial_screen, 0)

    def _load_settings(self):
        cfg = {}
        path = os.path.join(self.user_data_dir, "settings.json")
        if os.path.exists(path):
            try:
                with open(path, encoding="utf8") as fh:
                    cfg = json.load(fh)
            except (OSError, ValueError):
                cfg = {}
        self.api_url = os.getenv("BESCIENTIFIC_API_URL") or cfg.get("api_url") or None
        self.api_key = os.getenv("BESCIENTIFIC_API_KEY") or cfg.get("api_key") or None
        self.platform_url = (os.getenv("BESCIENTIFIC_PLATFORM_URL") or cfg.get("platform_url")
                             or self.api_url)

    def _setup_sync(self):
        self.sync_enabled = bool(self.api_url)
        if not self.sync_enabled:
            return
        client = SyncClient(self.db, self.api_url, self.api_key)
        self.sync_worker = SyncWorker(client, interval=60.0, on_result=self._on_sync_result)
        self.sync_worker.start()

    def on_stop(self):
        if self.sync_worker:
            self.sync_worker.stop()
        self.db.close()

    def tr(self, key: str, **fmt) -> str:
        return t(key, self.lang, **fmt)

    def go(self, screen: str, direction: str = "left"):
        self.root.transition.direction = direction
        self.root.current = screen

    def set_lang(self, code: str, persist: bool = False):
        self.lang = code
        if persist and self.student_id:
            self.db.set_student_lang(self.student_id, code)
            self.request_sync()

    def login(self, student_id: str):
        self.student_id = student_id
        self.lang = self.db.get_student(student_id)["lang"]
        self.go(HOME)

    def logout(self):
        self.student_id = None
        self.go(WELCOME, "right")

    def open_experiment(self, experiment_id: str):
        self.current_experiment = experiment_id
        self.go(LAB)

    def open_subject(self, subject_id: str):
        self.current_subject = subject_id
        if subject_id == "science":
            self.go(SCIENCE)
        else:
            self.start_quiz(subject_id)

    def open_study_material(self, subject_id: str):
        self.current_subject = subject_id
        self.current_study_lesson = None
        self.go(STUDY)

    def open_tutor(self, course_id: str | None = None, lesson_id: str | None = None):
        self.current_tutor_course = course_id
        self.current_tutor_lesson = lesson_id
        self.go(TUTOR)

    def start_quiz(self, subject_id: str):
        student = self.db.get_student(self.student_id)
        skill_id = SUBJECTS[subject_id].skill_id
        questions = pick_quiz(subject_id, student["class_level"], QUESTIONS_PER_RUN)
        self.current_subject = subject_id
        self.quiz_session = QuizSession(questions, skill_id=skill_id, subject_id=subject_id)
        self.go(QUIZ)

    def request_sync(self, manual: bool = False):
        if self.sync_worker:
            self.sync_worker.trigger()
        elif manual:
            self._on_sync_result(None)

    def _on_sync_result(self, result):
        def ui(_dt):
            home = self.root.get_screen(HOME) if self.root else None
            if home is None or not hasattr(home, "refresh_sync_label"):
                return
            if result is None:
                msg = None
            elif result.ok and result.sent:
                msg = self.tr("sync_ok_n", n=result.sent)
            elif result.ok:
                msg = None
            else:
                msg = self.tr("sync_offline")
            home.refresh_sync_label(msg)
        Clock.schedule_once(ui)
