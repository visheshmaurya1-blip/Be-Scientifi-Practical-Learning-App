"""KivyMD screens. Each screen rebuilds its widgets in on_pre_enter so language
changes and fresh data always show up without extra wiring."""
from __future__ import annotations

import threading

from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.screen import MDScreen
from kivymd.uix.slider import MDSlider
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar

from .. import tutor
from ..backend_bridge import fetch_curriculum, platform_health
from ..content import (CLASS_LEVELS, EXPERIMENTS, SKILLS, SUBJECTS, experiments_for_class,
                       pick_question, subjects_for_class)
from ..game import level_for_xp
from ..i18n import LANGS
from ..labs.models import MODELS
from ..labs.views import LabView
from ..speech import speak
from .theme import font_for_fields, lang_label


def _app():
    return MDApp.get_running_app()


def _label(text: str, style: str = "Body1", **kw) -> MDLabel:
    return MDLabel(text=text, font_style=style, adaptive_height=True, **kw)


def _scroll_column(spacing=dp(10), padding=dp(12)):
    scroll = MDScrollView()
    col = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=spacing, padding=padding)
    scroll.add_widget(col)
    return scroll, col


class BaseScreen(MDScreen):
    """Toolbar + content area; subclasses implement build_content(box)."""
    title_key = "app_title"
    back_to: str | None = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = MDBoxLayout(orientation="vertical")
        self.add_widget(self.layout)

    def on_pre_enter(self, *_):
        a = _app()
        self.layout.clear_widgets()
        bar = MDTopAppBar(title=a.tr(self.title_key), elevation=2)
        if self.back_to:
            bar.left_action_items = [["arrow-left", lambda *_: a.go(self.back_to, "right")]]
        self.layout.add_widget(bar)
        body = MDBoxLayout(orientation="vertical")
        self.layout.add_widget(body)
        self.build_content(body)

    def on_leave(self, *_):
        pass

    def build_content(self, box):  # pragma: no cover
        raise NotImplementedError


# ------------------------------------------------------------------ welcome
class WelcomeScreen(BaseScreen):
    title_key = "app_title"

    def build_content(self, box):
        a = _app()
        scroll, col = _scroll_column()
        box.add_widget(scroll)
        col.add_widget(_label(a.tr("welcome"), "H6"))

        # language switch
        row = MDBoxLayout(adaptive_height=True, spacing=dp(8))
        for code in LANGS:
            row.add_widget(MDRaisedButton(
                text=lang_label(code), md_bg_color=a.theme_cls.primary_color if a.lang == code else (0.6, 0.6, 0.6, 1),
                on_release=lambda _b, c=code: self._set_lang(c)))
        col.add_widget(row)

        # returning students
        for s in a.db.list_students():
            col.add_widget(MDRaisedButton(
                text=f"{s['name']}  (Class {s['class_level']})", size_hint=(1, None),
                on_release=lambda _b, sid=s["id"]: a.login(sid)))

        # new student
        font = font_for_fields()
        self.name_field = MDTextField(hint_text=a.tr("your_name"), mode="rectangle")
        self.class_field = MDTextField(hint_text=a.tr("class_level"), mode="rectangle", input_filter="int",
                                       max_text_length=1)
        if font:
            self.name_field.font_name = font
            self.class_field.font_name = font
        col.add_widget(self.name_field)
        chips = MDBoxLayout(adaptive_height=True, spacing=dp(6))
        for n in CLASS_LEVELS:
            chips.add_widget(MDFlatButton(
                text=a.tr("class_chip", n=n),
                on_release=lambda _b, n=n: self._pick_class(n)))
        col.add_widget(chips)
        col.add_widget(self.class_field)
        self.error = _label("", "Caption", theme_text_color="Error")
        col.add_widget(self.error)
        col.add_widget(MDRaisedButton(text=a.tr("start"), size_hint=(1, None), on_release=lambda *_: self._create()))

    def _pick_class(self, n: int):
        self.class_field.text = str(n)

    def _set_lang(self, code):
        _app().set_lang(code)
        self.on_pre_enter()

    def _create(self):
        a = _app()
        name = self.name_field.text.strip()
        if not name:
            self.error.text = a.tr("invalid_name")
            return
        try:
            level = int(self.class_field.text)
            sid = a.db.create_student(name, level, a.lang)
        except ValueError:
            self.error.text = a.tr("invalid_class")
            return
        a.login(sid)
        a.request_sync()


# --------------------------------------------------------------------- home
class HomeScreen(BaseScreen):
    title_key = "app_title"

    def build_content(self, box):
        a = _app()
        student = a.db.get_student(a.student_id)
        scroll, col = _scroll_column()
        box.add_widget(scroll)
        col.add_widget(_label(a.tr("hello", name=student["name"]), "H5"))
        stats = a.db.get_stats(a.student_id)
        col.add_widget(_label(a.tr("class_chip", n=student["class_level"]) + "  ·  " +
                              a.tr("xp_label", xp=stats["xp"], level=level_for_xp(stats["xp"])), "Caption"))
        col.add_widget(_label(a.tr("pick_subject"), "Subtitle1"))
        for sub in subjects_for_class(student["class_level"]):
            card = MDCard(orientation="vertical", padding=dp(12), size_hint_y=None, height=dp(96),
                          ripple_behavior=True, radius=[dp(12)], elevation=1,
                          on_release=lambda _c, s=sub: a.open_subject(s.id))
            card.add_widget(_label(a.tr(sub.name_key), "H6"))
            card.add_widget(_label(a.tr(sub.desc_key), "Caption"))
            col.add_widget(card)
        row = MDBoxLayout(adaptive_height=True, spacing=dp(8))
        row.add_widget(MDRaisedButton(text=a.tr("my_progress"), on_release=lambda *_: a.go("progress")))
        row.add_widget(MDRaisedButton(text=a.tr("teacher_view"), on_release=lambda *_: a.go("teacher")))
        row.add_widget(MDRaisedButton(text=a.tr("profile"), on_release=lambda *_: a.go("profile")))
        col.add_widget(row)
        row2 = MDBoxLayout(adaptive_height=True, spacing=dp(8))
        row2.add_widget(MDFlatButton(text=a.tr("switch_student"), on_release=lambda *_: a.logout()))
        for code in LANGS:
            row2.add_widget(MDFlatButton(text=lang_label(code), on_release=lambda _b, c=code: self._lang(c)))
        col.add_widget(row2)
        # sync status
        self.sync_label = _label("", "Caption")
        col.add_widget(self.sync_label)
        if a.sync_enabled:
            col.add_widget(MDFlatButton(text=a.tr("sync_now"), on_release=lambda *_: a.request_sync(True)))
        self.refresh_sync_label()

    def _lang(self, code):
        _app().set_lang(code, persist=True)
        self.on_pre_enter()

    def refresh_sync_label(self, message: str | None = None):
        a = _app()
        if not hasattr(self, "sync_label"):
            return
        if message:
            self.sync_label.text = message
        else:
            n = a.db.pending_counts()
            self.sync_label.text = a.tr("sync_pending", n=n) if n else a.tr("sync_done")


# ---------------------------------------------------------------- science hub
class ScienceScreen(BaseScreen):
    title_key = "subject_science"
    back_to = "home"

    def build_content(self, box):
        a = _app()
        student = a.db.get_student(a.student_id)
        scroll, col = _scroll_column()
        box.add_widget(scroll)
        col.add_widget(_label(a.tr("labs_title"), "Subtitle1"))
        for exp in experiments_for_class(student["class_level"]):
            card = MDCard(orientation="vertical", padding=dp(12), size_hint_y=None, height=dp(96),
                          ripple_behavior=True, radius=[dp(12)], elevation=1,
                          on_release=lambda _c, e=exp: a.open_experiment(e.id))
            card.add_widget(_label(a.tr(exp.title_key), "H6"))
            card.add_widget(_label(a.tr(exp.desc_key), "Caption"))
            col.add_widget(card)
        col.add_widget(MDRaisedButton(text=a.tr("start_quiz"), size_hint=(1, None),
                                      on_release=lambda *_: a.start_quiz("science")))


# ----------------------------------------------------------------------- quiz
class QuizScreen(BaseScreen):
    title_key = "start_quiz"
    back_to = "home"

    def build_content(self, box):
        a = _app()
        session = a.quiz_session
        if session is None:
            box.add_widget(_label(a.tr("no_data"), "Body1"))
            return
        sub = SUBJECTS.get(session.subject_id)
        self.layout.children[-1].title = a.tr(sub.name_key) if sub else a.tr("start_quiz")
        scroll, col = _scroll_column()
        box.add_widget(scroll)
        col.add_widget(_label(a.tr("lives_label", n=session.lives) + "   " +
                              a.tr("streak_label", n=session.streak) + "   " +
                              a.tr("plus_xp", n=session.xp), "Caption"))
        col.add_widget(MDProgressBar(value=session.progress * 100, size_hint_y=None, height=dp(8)))
        if session.finished or session.current is None:
            col.add_widget(_label(a.tr("quiz_over"), "H5"))
            col.add_widget(_label(a.tr("quiz_score", score=session.percent, xp=session.xp), "Body1"))
            stats = a.db.get_stats(a.student_id)
            if stats["badges"]:
                col.add_widget(_label(a.tr("badges"), "Subtitle1"))
                for bid in stats["badges"]:
                    col.add_widget(_label(a.tr(f"badge_{bid}"), "Caption"))
            col.add_widget(MDRaisedButton(text=a.tr("play_again"), size_hint=(1, None),
                                          on_release=lambda *_: a.start_quiz(session.subject_id)))
            col.add_widget(MDFlatButton(text=a.tr("back"), on_release=lambda *_: a.go("home", "right")))
            return
        q = session.current
        col.add_widget(_label(a.tr("question_n", n=session.index + 1, total=session.total), "Caption"))
        col.add_widget(_label(a.tr(q.text_key), "H6"))
        for i, key in enumerate(q.option_keys):
            col.add_widget(MDRaisedButton(text=a.tr(key), size_hint=(1, None),
                                          on_release=lambda _b, i=i: self._answer(i)))
        self.feedback = _label("", "Caption")
        col.add_widget(self.feedback)

    def _answer(self, idx: int):
        a = _app()
        session = a.quiz_session
        q = session.current
        result = session.answer(idx)
        a.db.record_attempt(a.student_id, f"quiz_{session.subject_id}", session.skill_id, q.id,
                            result.correct, False)
        stats = a.db.apply_session_rewards(a.student_id, session)
        result.new_badges = tuple(stats.get("new_badges") or ())
        speak(a.tr("correct") if result.correct else a.tr("not_quite"))
        a.request_sync()
        self.on_pre_enter()


# ------------------------------------------------------------------- profile
class ProfileScreen(BaseScreen):
    title_key = "profile"
    back_to = "home"

    def build_content(self, box):
        a = _app()
        student = a.db.get_student(a.student_id)
        stats = a.db.get_stats(a.student_id)
        scroll, col = _scroll_column()
        box.add_widget(scroll)
        col.add_widget(_label(student["name"], "H5"))
        col.add_widget(_label(a.tr("class_chip", n=student["class_level"]), "Subtitle1"))
        col.add_widget(_label(a.tr("xp_label", xp=stats["xp"], level=level_for_xp(stats["xp"])), "Body1"))
        col.add_widget(_label(a.tr("streak_label", n=stats["streak"]) + "  ·  " +
                              a.tr("coins_label", n=stats["coins"]), "Caption"))
        col.add_widget(_label(a.tr("badges"), "Subtitle1"))
        if stats["badges"]:
            for bid in stats["badges"]:
                col.add_widget(_label(a.tr(f"badge_{bid}"), "Body1"))
        else:
            col.add_widget(_label(a.tr("no_badges"), "Caption"))
        url = a.platform_url
        if url and platform_health(url):
            col.add_widget(_label(a.tr("backend_ok"), "Caption"))
            cur = fetch_curriculum(url, api_key=a.api_key)
            if cur and cur.get("subjects"):
                col.add_widget(_label(", ".join(s.get("id", "") for s in cur["subjects"]), "Caption"))
        else:
            col.add_widget(_label(a.tr("backend_off"), "Caption"))


# ---------------------------------------------------------------------- lab
class LabScreen(BaseScreen):
    title_key = "app_title"
    back_to = "home"

    def on_pre_enter(self, *_):
        self.view = None
        self.ran = False
        self._dialog = None
        super().on_pre_enter()

    def on_leave(self, *_):
        if getattr(self, "view", None):
            self.view.stop_loop()
        if self._dialog:
            self._dialog.dismiss()

    def build_content(self, box):
        a = _app()
        self.exp = EXPERIMENTS[a.current_experiment]
        self.layout.children[-1].title = a.tr(self.exp.title_key)      # toolbar title
        box.add_widget(_label(a.tr("lab_do"), "Subtitle1", padding=(dp(12), dp(6))))
        self.view = LabView(MODELS[self.exp.lab](), on_finished=self._on_finished, size_hint_y=0.5)
        box.add_widget(self.view)
        self.result_label = _label("", "Body1", padding=(dp(12), dp(4)))
        box.add_widget(self.result_label)
        self.controls = MDBoxLayout(adaptive_height=True, spacing=dp(8), padding=dp(8))
        self._build_controls()
        box.add_widget(self.controls)
        box.add_widget(MDRaisedButton(text=a.tr("answer_question"), size_hint=(1, None),
                                      on_release=lambda *_: self._ask()))
        self.view.start_loop()

    # --- controls (kept data-driven: one block per lab type)
    def _slider(self, label_key, key, lo, hi, value, step):
        a = _app()
        box = MDBoxLayout(orientation="vertical", adaptive_height=True)
        box.add_widget(_label(a.tr(label_key), "Caption"))
        s = MDSlider(min=lo, max=hi, value=value, step=step, hint=False, size_hint_y=None, height=dp(40))
        s.bind(value=lambda _w, v: self._param(key, v))
        box.add_widget(s)
        box.size_hint_x = 0.6
        self.controls.add_widget(box)

    def _build_controls(self):
        a, lab = _app(), self.exp.lab
        if lab == "gravity":
            self._slider("height", "height", 50, 300, 300, 10)
        elif lab == "bounce":
            self._slider("bounciness", "elasticity", 0.0, 1.0, 0.7, 0.05)
        elif lab == "friction":
            for key in ("ice", "wood", "rough"):
                self.controls.add_widget(MDFlatButton(text=a.tr(f"surf_{key}"),
                                                      on_release=lambda _b, k=key: self._param("surface", k)))
        go_key = "release" if lab == "friction" else "drop"
        self.controls.add_widget(MDRaisedButton(text=a.tr(go_key), on_release=lambda *_: self._go()))
        self.controls.add_widget(MDFlatButton(text=a.tr("reset"), on_release=lambda *_: self._reset()))

    def _param(self, key, value):
        self.view.model.set_param(key, value)
        self.view.redraw()

    def _go(self):
        if self.view.model.finished:
            self.view.reset()
        self.view.model.start()

    def _reset(self):
        self.view.reset()
        self.result_label.text = ""

    def _on_finished(self, res):
        a, lab = _app(), self.exp.lab
        self.ran = True
        if lab == "gravity":
            self.result_label.text = a.tr("result_gravity", a=res["heavy"] or 0.0, b=res["light"] or 0.0)
        elif lab == "friction":
            self.result_label.text = a.tr("result_friction", d=res["distance"])
        else:
            self.result_label.text = a.tr("result_bounce", h=res["bounce_height"])

    # --- question flow
    def _ask(self):
        a = _app()
        if not self.ran:
            self._show(a.tr("app_title"), a.tr("run_first"))
            return
        _, attempts = a.db.get_mastery(a.student_id, self.exp.skill_id)
        q = pick_question(self.exp, attempts)
        self._hint_used = False
        content = MDBoxLayout(orientation="vertical", spacing=dp(8), adaptive_height=True)
        for i, key in enumerate(q.option_keys):
            content.add_widget(MDRaisedButton(text=a.tr(key), size_hint=(1, None),
                                              on_release=lambda _b, i=i: self._answer(q, i)))
        self.hint_label = _label("", "Caption")
        content.add_widget(self.hint_label)
        content.add_widget(MDFlatButton(text=a.tr("hint"), on_release=lambda *_: self._show_hint()))
        self._close_dialog()
        self._dialog = MDDialog(title=a.tr(q.text_key), type="custom", content_cls=content)
        self._dialog.open()

    def _show_hint(self):
        self._hint_used = True
        self.hint_label.text = tutor.local_hint(self.exp.skill_id, _app().lang)

    def _answer(self, q, idx):
        a = _app()
        correct = idx == q.correct
        self._close_dialog()
        out = a.db.record_attempt(a.student_id, self.exp.id, self.exp.skill_id, q.id, correct, self._hint_used)
        lines = [a.tr("correct") if correct else a.tr("not_quite")]
        lines.append(tutor.explanation(self.exp.skill_id, a.lang) if correct
                     else f"{a.tr('hint')}: {tutor.local_hint(self.exp.skill_id, a.lang)}")
        lines.append(a.tr("mastery_now", pct=round(out["p_after"] * 100)))
        lines.append(a.tr(f"act_{out['action']}"))
        self._show(lines[0], "\n".join(lines[1:]))
        speak(lines[0])
        a.request_sync()
        if not correct:
            self._upgrade_hint_in_background(q, out["attempts"])

    def _upgrade_hint_in_background(self, q, attempt):
        """If a backend is configured, fetch an LLM hint; otherwise the cached hint stays."""
        a = _app()
        if not a.api_url:
            return

        def work():
            hint = tutor.cloud_hint(a.api_url, self.exp.skill_id, q.id, a.lang, attempt, a.api_key)
            if hint:
                Clock.schedule_once(lambda _dt: self._append_to_dialog(hint))
        threading.Thread(target=work, daemon=True).start()

    def _append_to_dialog(self, hint):
        if self._dialog and getattr(self._dialog, "text", None) is not None:
            self._dialog.text = f"{self._dialog.text}\n\n{_app().tr('hint')}: {hint}"

    def _show(self, title, text):
        a = _app()
        self._close_dialog()
        self._dialog = MDDialog(title=title, text=text,
                                buttons=[MDFlatButton(text=a.tr("ok"), on_release=lambda *_: self._close_dialog())])
        self._dialog.open()

    def _close_dialog(self):
        if self._dialog:
            self._dialog.dismiss()
            self._dialog = None


# ----------------------------------------------------------------- progress
class ProgressScreen(BaseScreen):
    title_key = "my_progress"
    back_to = "home"

    def build_content(self, box):
        a = _app()
        scroll, col = _scroll_column(spacing=dp(14))
        box.add_widget(scroll)
        stats = a.db.get_stats(a.student_id)
        col.add_widget(_label(a.tr("xp_label", xp=stats["xp"], level=level_for_xp(stats["xp"])), "Subtitle1"))
        mastery = a.db.all_mastery(a.student_id)
        if not any(n for _, n in mastery.values()):
            col.add_widget(_label(a.tr("no_data"), "Body1"))
        for sid, (p, n) in mastery.items():
            col.add_widget(_label(f"{a.tr(SKILLS[sid].name_key)}  -  {round(p * 100)}%  ({a.tr('attempts', n=n)})",
                                  "Subtitle1"))
            col.add_widget(MDProgressBar(value=p * 100, size_hint_y=None, height=dp(8)))


# ------------------------------------------------------------------ teacher
class TeacherScreen(BaseScreen):
    title_key = "teacher_view"
    back_to = "home"

    def build_content(self, box):
        a = _app()
        scroll, col = _scroll_column(spacing=dp(8))
        box.add_widget(scroll)
        rows = a.db.class_summary()
        if not rows:
            col.add_widget(_label(a.tr("no_data"), "Body1"))
        for r in sorted(rows, key=lambda r: (r["avg"] is None, r["avg"] if r["avg"] is not None else 0)):
            card = MDCard(orientation="vertical", padding=dp(10), size_hint_y=None, height=dp(92),
                          radius=[dp(10)], elevation=1)
            avg = "-" if r["avg"] is None else f"{round(r['avg'] * 100)}%"
            card.add_widget(_label(f"{r['name']} (Class {r['class_level']})  -  {a.tr('avg_mastery')}: {avg}",
                                   "Subtitle1"))
            if r["weakest"] and r["avg"] is not None and r["avg"] < 0.6:
                card.add_widget(_label(a.tr("needs_help", skill=a.tr(SKILLS[r["weakest"]].name_key)), "Caption"))
            elif r["avg"] is not None:
                card.add_widget(_label(a.tr("on_track"), "Caption"))
            card.add_widget(_label(a.tr("attempts", n=r["attempts"]), "Caption"))
            col.add_widget(card)
