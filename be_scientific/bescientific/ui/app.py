"""Application object: wiring of database, language, screens and background sync."""
from __future__ import annotations

import json
import os
import threading

from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from ..db import Database
from ..i18n import DEFAULT_LANG, t
from ..sync import SyncClient, SyncWorker
from .screens import (
    HomeScreen, LabScreen, ProfileScreen, ProgressScreen, QuizScreen,
    ScienceScreen, TeacherScreen, WelcomeScreen,
)
from .theme import register_fonts


class BeScientificApp(MDApp):
    """Settings (all optional) come from env vars or <user_data_dir>/settings.json:

        BESCIENTIFIC_API_URL  e.g. https://api.example.org     (omit => fully offline)
        BESCIENTIFIC_API_KEY  shared secret expected by the backend's API_KEY
    """

    def __init__(self, db_path: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self._db_path = db_path
        self.lang = DEFAULT_LANG
        self.student_id: str | None = None
        self.current_experiment: str | None = None
        self.current_subject: str | None = None
        self.quiz_session = None
        self.platform_url: str | None = None
        self.api_url: str | None = None
        self.api_key: str | None = None
        self.sync_worker: SyncWorker | None = None
        self.sync_enabled = False

    # ----------------------------------------------------------------- build
    def build(self):
        self.title = "Be Scientific"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        register_fonts(self.theme_cls)
        self.db = Database(self._db_path or os.path.join(self.user_data_dir, "bescientific.db"))
        self._load_settings()
        sm = MDScreenManager()
        for name, cls in (("welcome", WelcomeScreen), ("home", HomeScreen), ("science", ScienceScreen),
                          ("quiz", QuizScreen), ("lab", LabScreen), ("progress", ProgressScreen),
                          ("teacher", TeacherScreen), ("profile", ProfileScreen)):
            sm.add_widget(cls(name=name))
        sm.current = "welcome"
        self._setup_sync()
        return sm

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

    # ------------------------------------------------------------- helpers
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
        self.go("home")

    def logout(self):
        self.student_id = None
        self.go("welcome", "right")

    def open_experiment(self, experiment_id: str):
        self.current_experiment = experiment_id
        self.go("lab")

    def open_subject(self, subject_id: str):
        self.current_subject = subject_id
        if subject_id == "science":
            self.go("science")
        else:
            self.start_quiz(subject_id)

    def start_quiz(self, subject_id: str):
        from ..content import SUBJECTS, pick_quiz
        from ..game import QUESTIONS_PER_RUN, QuizSession
        student = self.db.get_student(self.student_id)
        skill_id = SUBJECTS[subject_id].skill_id
        questions = pick_quiz(subject_id, student["class_level"], QUESTIONS_PER_RUN)
        self.current_subject = subject_id
        self.quiz_session = QuizSession(questions, skill_id=skill_id, subject_id=subject_id)
        self.go("quiz")

    # ---------------------------------------------------------------- sync
    def request_sync(self, manual: bool = False):
        """Nudge the background worker (non-blocking). Safe to call when offline-only."""
        if self.sync_worker:
            self.sync_worker.trigger()
        elif manual:
            self._on_sync_result(None)

    def _on_sync_result(self, result):
        """Called from the worker thread - hop to the UI thread before touching widgets."""
        def ui(_dt):
            home = self.root.get_screen("home") if self.root else None
            if home is None:
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
