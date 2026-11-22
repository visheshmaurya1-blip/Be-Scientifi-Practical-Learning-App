"""KivyMD 2 screens for the unified desktop app."""
from __future__ import annotations

from kivy.core.window import Window
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDLinearProgressIndicator
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText

from bescientific.study_materials import CLASS_1_STUDY_COURSES
from bescientific import tutor
from bescientific.backend_bridge import fetch_curriculum, platform_health
from bescientific.content import (CLASS_LEVELS, EXPERIMENTS, SKILLS, SUBJECTS,
                                  experiments_for_class, pick_question, subjects_for_class)
from bescientific.game import AnswerResult, QuizSession, level_for_xp
from bescientific.i18n import LANGS
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
from bescientific.labs.models import MODELS
from bescientific.labs.views import LabView
from bescientific.speech import speak
from bescientific.ui.theme import font_for_fields, lang_label
from navigation.routes import (HOME, LAB, PROFILE, PROGRESS, QUIZ, SCIENCE, STUDY,
                               TEACHER, TUTOR, WELCOME)
from .scenery import LOGO_IMAGE, ScenicBackground
from .visuals import LearningSymbol, VirtualObjectIcon

TEXT_COLOR = (0.08, 0.15, 0.13, 1)
STUDY_COURSES_BY_CLASS = {
    1: CLASS_1_STUDY_COURSES,
    2: CLASS_2_STUDY_COURSES,
    3: CLASS_3_STUDY_COURSES,
    4: CLASS_4_STUDY_COURSES,
    5: CLASS_5_STUDY_COURSES,
    6: CLASS_6_STUDY_COURSES,
}


def _app():
    return MDApp.get_running_app()


def _label(text, size="16sp", **kw):
    kw.setdefault("theme_text_color", "Custom")
    kw.setdefault("text_color", TEXT_COLOR)
    kw.setdefault("theme_font_size", "Custom")
    font_name = font_for_fields()
    if font_name:
        kw.setdefault("font_name", font_name)
    requested_size = float(size.removesuffix("sp"))
    readable_size = max(16, requested_size)
    if Window.width and Window.width < dp(360) and readable_size > 20:
        readable_size = 20
    return MDLabel(text=text, adaptive_height=True, font_size=sp(readable_size), **kw)


def _button(text, callback, style="filled"):
    text_kwargs = {}
    font_name = font_for_fields()
    if font_name:
        text_kwargs["font_name"] = font_name
    btn = MDButton(MDButtonText(text=text, **text_kwargs), style=style, size_hint_x=1,
                   size_hint_y=None, height=dp(52))
    btn.bind(on_release=lambda *_: callback())
    return btn


class ResponsiveGrid(GridLayout):
    def __init__(self, compact_columns: int, wide_columns: int, **kwargs):
        self.compact_columns = compact_columns
        self.wide_columns = wide_columns
        super().__init__(cols=compact_columns, size_hint_y=None, **kwargs)
        self.bind(minimum_height=self.setter("height"), width=self._update_columns)

    def _update_columns(self, _instance, width):
        columns = self.wide_columns if width >= dp(600) else self.compact_columns
        if self.cols != columns:
            self.cols = columns


def _scroll_col():
    scroll = ScrollView()
    col = MDBoxLayout(
        orientation="vertical", adaptive_height=True, spacing=dp(12),
        padding=(dp(10), dp(10), dp(10), dp(92)))
    scroll.add_widget(col)
    return scroll, col


class BunnyTutorButton(ButtonBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical", size_hint=(None, None), size=(dp(68), dp(68)),
            pos_hint={"right": 0.97, "y": 0.025}, padding=dp(4), **kwargs)
        with self.canvas.before:
            Color(0.08, 0.31, 0.27, 0.96)
            self._button_background = RoundedRectangle(
                radius=[(dp(34), dp(34))])
        self.bind(pos=self._update_background, size=self._update_background)
        self.add_widget(LearningSymbol(
            kind="bunny", size_hint=(None, None), size=(dp(56), dp(56))))
        self.bind(on_release=lambda *_: _app().open_tutor())

    def _update_background(self, *_):
        self._button_background.pos = self.pos
        self._button_background.size = self.size


class LearningPanel(MDBoxLayout):
    def __init__(self, **kwargs):
        self.fill_color = kwargs.pop("fill_color", (0.98, 0.99, 0.97, 0.96))
        self.border_color = kwargs.pop("border_color", (0.73, 0.82, 0.76, 1))
        super().__init__(**kwargs)
        self.bind(pos=self._draw_panel, size=self._draw_panel)
        self._draw_panel()

    def _draw_panel(self, *_):
        if self.width <= 0 or self.height <= 0:
            return
        self.canvas.before.clear()
        self.canvas.after.clear()
        with self.canvas.before:
            Color(*self.fill_color)
            RoundedRectangle(
                pos=self.pos, size=self.size, radius=[(dp(16), dp(16))])
        with self.canvas.after:
            Color(*self.border_color)
            Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(16)),
                width=dp(1))


class LearningCard(MDCard):
    def __init__(self, **kwargs):
        kwargs.setdefault("style", "elevated")
        super().__init__(**kwargs)


class BaseScreen(MDScreen):
    title = ""
    back_to = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.scenery = ScenicBackground()
        self.scenery.size_hint = (1, 1)
        self.scenery.pos_hint = {"x": 0, "y": 0}
        self.scenery.opacity = 1
        self.add_widget(self.scenery)
        self.layout = MDBoxLayout(
            orientation="vertical", size_hint=(1, 1),
            spacing=dp(4), padding=dp(8))
        self.layout.pos_hint = {"x": 0, "y": 0}
        self.layout.opacity = 1
        self.add_widget(self.layout)

    def on_pre_enter(self, *_):
        self.scenery.start()
        a = _app()
        self.layout.clear_widgets()
        header = LearningPanel(
            orientation="horizontal", adaptive_height=True, size_hint_y=None,
            height=dp(68), spacing=dp(10), padding=dp(10),
            fill_color=(0.98, 0.99, 0.97, 0.98))
        if self.back_to:
            header.add_widget(_button(a.tr("back"), lambda: a.go(self.back_to, "right"), "text"))
        header.add_widget(Image(
            source=str(LOGO_IMAGE), fit_mode="contain",
            size_hint=(None, None), size=(dp(44), dp(44))))
        header.add_widget(_label(self._title(), "22sp", bold=True))
        self.layout.add_widget(header)
        body = LearningPanel(
            orientation="vertical", padding=dp(8), spacing=dp(8),
            fill_color=(0.98, 0.99, 0.97, 0.94))
        self.layout.add_widget(body)
        self.build_content(body)
        if a.student_id and not hasattr(self, "tutor_button"):
            self.tutor_button = BunnyTutorButton()
            self.add_widget(self.tutor_button)

    def on_leave(self, *_):
        self.scenery.stop()

    def _title(self):
        return _app().tr("app_title")

    def build_content(self, box):
        raise NotImplementedError


class WelcomeScreen(BaseScreen):
    def build_content(self, box):
        a = _app()
        scroll, col = _scroll_col()
        box.add_widget(scroll)
        col.add_widget(Image(
            source=str(LOGO_IMAGE), fit_mode="contain",
            size_hint=(1, None), height=dp(170)))
        col.add_widget(_label(a.tr("welcome"), "20sp"))
        row = MDBoxLayout(adaptive_height=True, spacing=dp(8))
        for code in LANGS:
            row.add_widget(_button(lang_label(code), lambda c=code: self._set_lang(c),
                                   "filled" if a.lang == code else "outlined"))
        col.add_widget(row)
        for s in a.db.list_students():
            col.add_widget(_button(f"{s['name']}  (Class {s['class_level']})",
                                   lambda sid=s["id"]: a.login(sid)))
        font_name = font_for_fields()
        hint_kwargs = {"font_name": font_name} if font_name else {}
        field_kwargs = {"font_name": font_name} if font_name else {}
        self.name_field = MDTextField(
            MDTextFieldHintText(text=a.tr("your_name"), **hint_kwargs),
            mode="outlined", **field_kwargs)
        self.class_field = MDTextField(
            MDTextFieldHintText(text=a.tr("class_level"), **hint_kwargs),
            mode="outlined", **field_kwargs)
        col.add_widget(self.name_field)
        chips = ResponsiveGrid(compact_columns=3, wide_columns=6, spacing=dp(6))
        for n in CLASS_LEVELS:
            chips.add_widget(_button(a.tr("class_chip", n=n), lambda n=n: self._pick_class(n), "tonal"))
        col.add_widget(chips)
        col.add_widget(self.class_field)
        self.error = _label("", "14sp")
        col.add_widget(self.error)
        col.add_widget(_button(a.tr("start"), self._create))

    def _pick_class(self, n):
        self.class_field.text = str(n)

    def _set_lang(self, code):
        _app().set_lang(code)
        self.on_pre_enter()

    def _create(self):
        a = _app()
        name = (self.name_field.text or "").strip()
        if not name:
            self.error.text = a.tr("invalid_name")
            return
        try:
            level = int((self.class_field.text or "").strip())
            sid = a.db.create_student(name, level, a.lang)
        except ValueError:
            self.error.text = a.tr("invalid_class")
            return
        a.login(sid)
        a.request_sync()


class HomeScreen(BaseScreen):
    def build_content(self, box):
        a = _app()
        student = a.db.get_student(a.student_id)
        stats = a.db.get_stats(a.student_id)
        scroll, col = _scroll_col()
        box.add_widget(scroll)
        col.add_widget(_label(a.tr("hello", name=student["name"]), "22sp"))
        col.add_widget(_label(a.tr("class_chip", n=student["class_level"]) + "  ·  " +
                              a.tr("xp_label", xp=stats["xp"], level=level_for_xp(stats["xp"]))))
        col.add_widget(_label(a.tr("pick_subject"), "18sp"))
        course_catalog = (
            a.db.hindi_study_courses(student["class_level"])
            if a.lang == "hi"
            else STUDY_COURSES_BY_CLASS.get(student["class_level"])
        )
        if course_catalog is not None:
            for course in course_catalog.values():
                title = course.title_hi if a.lang == "hi" else course.title_en
                book = course.book_hi if a.lang == "hi" else course.book_en
                card = LearningCard(orientation="horizontal", padding=dp(12), spacing=dp(12),
                                    size_hint_y=None, height=dp(108))
                card.add_widget(LearningSymbol(
                    kind=course.id, size_hint=(None, None), size=(dp(52), dp(52))))
                details = MDBoxLayout(orientation="vertical", spacing=dp(4),
                                      adaptive_height=True, pos_hint={"center_y": 0.5})
                details.add_widget(_label(title, "18sp"))
                details.add_widget(_label(
                    f"{book}  ·  {len(course.lessons)} " +
                    ("पाठ" if a.lang == "hi" else "lessons"), "14sp"))
                card.add_widget(details)
                card.bind(on_release=lambda _card, c=course: a.open_study_material(c.id))
                col.add_widget(card)
        else:
            for sub in subjects_for_class(student["class_level"]):
                card = LearningCard(orientation="horizontal", padding=dp(12), spacing=dp(12),
                                    size_hint_y=None, height=dp(112))
                card.add_widget(LearningSymbol(
                    kind=sub.id, size_hint=(None, None), size=(dp(52), dp(52))))
                details = MDBoxLayout(orientation="vertical", spacing=dp(4),
                                      adaptive_height=True, pos_hint={"center_y": 0.5})
                details.add_widget(_label(a.tr(sub.name_key), "18sp"))
                details.add_widget(_label(a.tr(sub.desc_key), "14sp"))
                card.add_widget(details)
                card.bind(on_release=lambda _c, s=sub: a.open_subject(s.id))
                col.add_widget(card)
        col.add_widget(_button(
            "एनसीईआरटी ट्यूटर से पूछें" if a.lang == "hi" else "Ask the NCERT tutor",
            a.open_tutor, "tonal"))
        row = ResponsiveGrid(compact_columns=1, wide_columns=3, spacing=dp(8))
        row.add_widget(_button(a.tr("my_progress"), lambda: a.go(PROGRESS), "tonal"))
        row.add_widget(_button(a.tr("teacher_view"), lambda: a.go(TEACHER), "tonal"))
        row.add_widget(_button(a.tr("profile"), lambda: a.go(PROFILE), "tonal"))
        col.add_widget(row)
        col.add_widget(_button(a.tr("switch_student"), a.logout, "text"))
        self.sync_label = _label("")
        col.add_widget(self.sync_label)
        if a.sync_enabled:
            col.add_widget(_button(a.tr("sync_now"), lambda: a.request_sync(True), "text"))
        self.refresh_sync_label()

    def refresh_sync_label(self, message: str | None = None):
        a = _app()
        if not hasattr(self, "sync_label"):
            return
        if message:
            self.sync_label.text = message
        else:
            n = a.db.pending_counts()
            self.sync_label.text = a.tr("sync_pending", n=n) if n else a.tr("sync_done")


class ScienceScreen(BaseScreen):
    back_to = HOME

    def _title(self):
        return _app().tr("subject_science")

    def build_content(self, box):
        a = _app()
        student = a.db.get_student(a.student_id)
        scroll, col = _scroll_col()
        box.add_widget(scroll)
        col.add_widget(_label(a.tr("labs_title"), "18sp"))
        for exp in experiments_for_class(student["class_level"]):
            card = LearningCard(orientation="vertical", padding=dp(12),
                                size_hint_y=None, height=dp(116))
            card.add_widget(_label(a.tr(exp.title_key), "18sp"))
            card.add_widget(_label(a.tr(exp.desc_key), "14sp"))
            card.bind(on_release=lambda _c, e=exp: a.open_experiment(e.id))
            col.add_widget(card)
        col.add_widget(_button(a.tr("start_quiz"), lambda: a.start_quiz("science")))


class VirtualObjectCard(ButtonBehavior, MDBoxLayout):
    def __init__(self, caption, kind, on_select, **kwargs):
        self.selected = False
        self.correct = None
        self.on_select = on_select
        super().__init__(orientation="vertical", spacing=dp(2), padding=dp(5),
                         size_hint_y=None, height=dp(158), **kwargs)
        self.bind(pos=self._draw_card, size=self._draw_card)
        self.add_widget(VirtualObjectIcon(
            kind, size_hint=(None, None), size=(dp(104), dp(104)),
            pos_hint={"center_x": 0.5}))
        self.add_widget(_label(caption, "13sp", halign="center"))
        self._draw_card()

    def on_release(self):
        self.on_select()

    def _draw_card(self, *_):
        if not hasattr(self, "canvas"):
            return
        self.canvas.before.clear()
        with self.canvas.before:
            if self.correct is True:
                Color(0.78, 0.94, 0.80, 1)
            elif self.correct is False:
                Color(1, 0.84, 0.80, 1)
            elif self.selected:
                Color(0.82, 0.93, 0.98, 1)
            else:
                Color(1, 1, 1, 0.96)
            RoundedRectangle(pos=self.pos, size=self.size,
                             radius=[(dp(12), dp(12))])
            Color(0.12, 0.49, 0.55, 1) if self.selected else Color(
                0.72, 0.78, 0.80, 1)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(12)),
                 width=dp(2) if self.selected else dp(1))


class VirtualActivityLab(MDBoxLayout):
    def __init__(self, activity_id, activity, object_catalog, lang, **kwargs):
        super().__init__(orientation="vertical", adaptive_height=True, spacing=dp(8),
                         padding=dp(12), **kwargs)
        self.activity = activity
        self.lang = lang
        self.selected_index = None
        self.object_cards = []
        self.add_widget(_label(
            "Virtual Try-it Lab" if lang == "en" else "आभासी करके देखें प्रयोगशाला",
            "18sp", bold=True))
        self.add_widget(_label(
            activity.prompt_en if lang == "en" else activity.prompt_hi, "16sp"))
        self.add_widget(_label(
            "Tap a virtual object to use it, then run the activity."
            if lang == "en" else "आभासी वस्तु को छूकर चुनें, फिर गतिविधि चलाएँ।", "14sp"))
        self.object_grid = ResponsiveGrid(
            compact_columns=2, wide_columns=3, spacing=dp(8))
        self.add_widget(self.object_grid)
        self.choice_buttons = []
        object_kinds = object_catalog[activity_id]
        for index, (english, hindi) in enumerate(activity.choices):
            card = VirtualObjectCard(
                english if lang == "en" else hindi,
                object_kinds[index],
                lambda i=index: self._choose(i),
            )
            self.object_cards.append(card)
            self.choice_buttons.append(card)
            self.object_grid.add_widget(card)
        self.feedback = _label("", "14sp")
        self.add_widget(self.feedback)
        self.add_widget(_button(
            "Run simulation" if lang == "en" else "सिमुलेशन चलाएँ",
            self._run, "filled"))

    def _choose(self, index):
        self.selected_index = index
        for i, card in enumerate(self.object_cards):
            card.selected = i == index
            card.correct = None
            card._draw_card()
        self.feedback.text = (
            "Object selected. Run the activity to see what happens."
            if self.lang == "en" else
            "वस्तु चुनी गई। परिणाम देखने के लिए गतिविधि चलाएँ।"
        )

    def _run(self):
        if self.selected_index is None:
            self.feedback.text = (
                "Choose an action first." if self.lang == "en"
                else "पहले कोई काम चुनें।"
            )
            return
        answer = self.activity.choices[self.activity.answer_index][
            0 if self.lang == "en" else 1
        ]
        for i, card in enumerate(self.object_cards):
            card.correct = i == self.activity.answer_index if i == self.selected_index else None
            card._draw_card()
        if self.selected_index == self.activity.answer_index:
            self.feedback.text = (
                f"Great work! Your object completes the activity: {answer}."
                if self.lang == "en" else f"बहुत अच्छा! आपकी वस्तु से गतिविधि पूरी हुई: {answer}।"
            )
        else:
            self.feedback.text = (
                f"Not quite. Try another object. The activity result is: {answer}."
                if self.lang == "en" else f"अभी सही नहीं। दूसरी वस्तु आज़माएँ। गतिविधि का परिणाम है: {answer}।"
            )


class StudyMaterialScreen(BaseScreen):
    back_to = HOME

    def __init__(self, **kw):
        super().__init__(**kw)
        self.virtual_lab_open = False

    def _course_catalog(self):
        a = _app()
        student = a.db.get_student(a.student_id)
        if a.lang == "hi":
            return a.db.hindi_study_courses(student["class_level"])
        return STUDY_COURSES_BY_CLASS.get(student["class_level"], {})

    def _course(self):
        return self._course_catalog().get(_app().current_subject)

    def _title(self):
        course = self._course()
        if course is None:
            return _app().tr("study_material")
        return course.title_hi if _app().lang == "hi" else course.title_en

    def build_content(self, box):
        a = _app()
        course = self._course()
        scroll, col = _scroll_col()
        box.add_widget(scroll)
        if course is None:
            col.add_widget(_label(a.tr("no_data")))
            return

        book = course.book_hi if a.lang == "hi" else course.book_en
        col.add_widget(_label(
            (f"कक्षा {a.db.get_student(a.student_id)['class_level']}  ·  {book}  ·  "
             f"{len(course.lessons)} पाठ" if a.lang == "hi"
             else f"Class {a.db.get_student(a.student_id)['class_level']}  ·  "
             f"{book}  ·  {len(course.lessons)} lessons"), "14sp"))
        col.add_widget(_button(
            "आधिकारिक NCERT पुस्तक खोलें" if a.lang == "hi" else "Open official NCERT textbook",
            lambda: self._open_source(
                course.source_url_hi if a.lang == "hi" and course.source_url_hi
                else course.source_url), "text"))
        self.message = _label("", "14sp")
        col.add_widget(self.message)

        selected = next(
            (lesson for lesson in course.lessons
             if lesson.id == a.current_study_lesson),
            None,
        )
        if selected is None:
            for number, lesson in enumerate(course.lessons, 1):
                text = lesson.hi if a.lang == "hi" else lesson.en
                chapter = lesson.chapter_hi if a.lang == "hi" else lesson.chapter_en
                card = LearningCard(orientation="vertical", padding=dp(12), spacing=dp(4),
                                    size_hint_y=None, height=dp(100))
                card.add_widget(_label(
                    f"{number}. {chapter}", "17sp"))
                card.add_widget(_label(text.focus, "14sp"))
                card.bind(on_release=lambda _card, lid=lesson.id: self._open_lesson(lid))
                col.add_widget(card)
            if course.id == "math":
                col.add_widget(_button(
                    "गणित प्रश्नोत्तरी खेलें" if a.lang == "hi" else "Try the Math quiz",
                    lambda: a.start_quiz("math"), "tonal"))
            return

        text = selected.hi if a.lang == "hi" else selected.en
        chapter = selected.chapter_hi if a.lang == "hi" else selected.chapter_en
        student = a.db.get_student(a.student_id)
        col.add_widget(_button(
            "विषयों पर वापस जाएँ" if a.lang == "hi" else "Back to topics",
            self._back_to_topics, "text"))
        col.add_widget(_label(chapter, "20sp", bold=True))
        col.add_widget(_label(text.focus, "16sp", bold=True))
        col.add_widget(_label("सीखें" if a.lang == "hi" else "Learn", "16sp", bold=True))
        col.add_widget(_label(text.learn))
        col.add_widget(_label("करके देखें" if a.lang == "hi" else "Try it", "16sp", bold=True))
        col.add_widget(_label(text.activity))
        virtual_activities = {
            1: (CLASS_1_VIRTUAL_ACTIVITIES, CLASS_1_VIRTUAL_OBJECTS),
            2: (CLASS_2_VIRTUAL_ACTIVITIES, CLASS_2_VIRTUAL_OBJECTS),
            3: (CLASS_3_VIRTUAL_ACTIVITIES, CLASS_3_VIRTUAL_OBJECTS),
            4: (CLASS_4_VIRTUAL_ACTIVITIES, CLASS_4_VIRTUAL_OBJECTS),
            5: (CLASS_5_VIRTUAL_ACTIVITIES, CLASS_5_VIRTUAL_OBJECTS),
            6: (CLASS_6_VIRTUAL_ACTIVITIES, CLASS_6_VIRTUAL_OBJECTS),
        }.get(student["class_level"])
        virtual_activity = virtual_activities[0].get(selected.id) if virtual_activities else None
        if virtual_activity is not None:
            col.add_widget(_button(
                ("प्रयोगशाला बंद करें" if self.virtual_lab_open else "आभासी करके देखें")
                if a.lang == "hi"
                else ("Close virtual lab" if self.virtual_lab_open else "Try it virtually"),
                self._toggle_virtual_lab, "tonal"))
            if self.virtual_lab_open:
                col.add_widget(VirtualActivityLab(
                    selected.id, virtual_activity, virtual_activities[1], a.lang))
        col.add_widget(_label("जाँचें" if a.lang == "hi" else "Quick check", "16sp", bold=True))
        col.add_widget(_label(text.check))
        col.add_widget(_label(
            ("उत्तर: " if a.lang == "hi" else "Answer: ") + text.answer, "14sp"))
        col.add_widget(_button(
            "इस पाठ के बारे में ट्यूटर से पूछें" if a.lang == "hi"
            else "Ask the tutor about this lesson",
            lambda: a.open_tutor(course.id, selected.id), "tonal"))

    def _open_lesson(self, lesson_id):
        _app().current_study_lesson = lesson_id
        self.virtual_lab_open = False
        self.on_pre_enter()

    def _back_to_topics(self):
        _app().current_study_lesson = None
        self.virtual_lab_open = False
        self.on_pre_enter()

    def _toggle_virtual_lab(self):
        self.virtual_lab_open = not self.virtual_lab_open
        self.on_pre_enter()

    def _open_source(self, url):
        import webbrowser

        if not webbrowser.open(url):
            self.message.text = (
                "आधिकारिक पुस्तक का लिंक नहीं खुला।" if _app().lang == "hi"
                else "Could not open the official textbook link."
            )


class TutorScreen(BaseScreen):
    back_to = HOME

    def __init__(self, **kw):
        super().__init__(**kw)
        self.chat_turns = []
        self._chat_identity = None

    def _title(self):
        return "एनसीईआरटी ट्यूटर" if _app().lang == "hi" else "NCERT tutor"

    def build_content(self, box):
        a = _app()
        student = a.db.get_student(a.student_id)
        identity = (a.student_id, a.lang)
        if identity != self._chat_identity:
            self.chat_turns.clear()
            self._chat_identity = identity
        courses = (
            a.db.hindi_study_courses(student["class_level"])
            if a.lang == "hi"
            else STUDY_COURSES_BY_CLASS.get(student["class_level"], {})
        )
        scroll, col = _scroll_col()
        box.add_widget(scroll)
        col.add_widget(_label(
            "अपने पाठ्यक्रम से प्रश्न पूछें। उत्तर उपलब्ध पाठ-मार्गदर्शिकाओं पर आधारित हैं।"
            if a.lang == "hi"
            else "Ask about your curriculum. Answers are grounded in the available lesson guides.",
            "14sp"))

        selected_course = a.current_tutor_course
        subject_buttons = ResponsiveGrid(compact_columns=1, wide_columns=3, spacing=dp(8))
        subject_buttons.add_widget(_button(
            "सभी विषय" if a.lang == "hi" else "All subjects",
            lambda: self._select_course(None),
            "filled" if selected_course is None else "outlined"))
        for course in courses.values():
            title = course.title_hi if a.lang == "hi" else course.title_en
            subject_buttons.add_widget(_button(
                title, lambda cid=course.id: self._select_course(cid),
                "filled" if selected_course == course.id else "outlined"))
        col.add_widget(subject_buttons)

        font_name = font_for_fields()
        field_kwargs = {"font_name": font_name} if font_name else {}
        hint = "अपना प्रश्न लिखें" if a.lang == "hi" else "Type your question"
        self.question_field = MDTextField(
            MDTextFieldHintText(text=hint, **field_kwargs),
            mode="outlined", multiline=True, size_hint_y=None, height=dp(96), **field_kwargs)
        col.add_widget(self.question_field)
        col.add_widget(_button(
            "उत्तर खोजें" if a.lang == "hi" else "Find an answer",
            self._answer, "filled"))
        self.result_box = MDBoxLayout(
            orientation="vertical", spacing=dp(8), adaptive_height=True)
        col.add_widget(self.result_box)
        self._render_chat()

    def _select_course(self, course_id):
        a = _app()
        a.current_tutor_course = course_id
        a.current_tutor_lesson = None
        self.on_pre_enter()

    def _answer(self):
        a = _app()
        question = self.question_field.text.strip()
        self.result_box.clear_widgets()
        if not question or len(question) > 1000:
            self.result_box.add_widget(_label(
                "कृपया 1 से 1000 अक्षरों का प्रश्न लिखें।" if a.lang == "hi"
                else "Enter a question between 1 and 1,000 characters.", "14sp"))
            return

        student = a.db.get_student(a.student_id)
        courses = (
            a.db.hindi_study_courses(student["class_level"])
            if a.lang == "hi"
            else STUDY_COURSES_BY_CLASS.get(student["class_level"], {})
        )
        refusal = tutor.question_refusal_reason(question)
        result = tutor.answer_question(
            question,
            courses,
            lang=a.lang,
            course_id=a.current_tutor_course,
            preferred_lesson_id=a.current_tutor_lesson,
        )
        self.chat_turns.append((question, result, refusal))
        self.question_field.text = ""
        self._render_chat()

    def _render_chat(self):
        a = _app()
        self.result_box.clear_widgets()
        student = a.db.get_student(a.student_id)
        for question, result, refusal in self.chat_turns:
            self.result_box.add_widget(_label(
                ("आप: " if a.lang == "hi" else "You: ") + question, "15sp", bold=True))
            if refusal:
                reply = (
                    "मैं वयस्क या अश्लील विषयों में मदद नहीं कर सकता। कृपया स्कूल के पाठों के बारे में पूछें।"
                    if a.lang == "hi"
                    else "I can't help with adult or explicit topics. Please ask about a school lesson."
                )
                self.result_box.add_widget(_label(
                    ("बन्नी ट्यूटर: " if a.lang == "hi" else "Bunny tutor: ") + reply,
                    "14sp"))
            elif result is None:
                reply = (
                    "इस कक्षा के उपलब्ध पाठ्यक्रम में इससे जुड़ा पाठ नहीं मिला। किसी अध्याय या विषय के बारे में पूछें।"
                    if a.lang == "hi"
                    else "That topic isn't in this class's available curriculum. Try asking about one of its subjects or chapters."
                )
                self.result_box.add_widget(_label(
                    ("बन्नी ट्यूटर: " if a.lang == "hi" else "Bunny tutor: ") + reply,
                    "14sp"))
            else:
                self.result_box.add_widget(_label(
                    ("बन्नी ट्यूटर · कक्षा " if a.lang == "hi" else "Bunny tutor · Class ")
                    + str(student["class_level"]) + " · " + result["course_title"]
                    + " · " + result["chapter"], "15sp", bold=True))
                self.result_box.add_widget(_label(
                    ("समझें: " if a.lang == "hi" else "Explanation: ")
                    + result["explanation"], "15sp"))
                self.result_box.add_widget(_label(
                    ("करके देखें: " if a.lang == "hi" else "Try this: ")
                    + result["activity"], "14sp"))
                self.result_box.add_widget(_label(
                    ("पाठ की जाँच: " if a.lang == "hi" else "Lesson check: ")
                    + result["check"] + "  "
                    + ("उत्तर: " if a.lang == "hi" else "Answer: ")
                    + result["answer"], "14sp"))
                self.result_box.add_widget(_button(
                    "आधिकारिक एनसीईआरटी पुस्तक खोलें" if a.lang == "hi"
                    else "Open the official NCERT book",
                    lambda url=result["source_url"]: self._open_source(url), "text"))

    def _open_source(self, url):
        import webbrowser

        if not webbrowser.open(url):
            self.result_box.add_widget(_label(
                "आधिकारिक पुस्तक का लिंक नहीं खुला।" if _app().lang == "hi"
                else "Could not open the official textbook link.", "14sp"))


class QuizScreen(BaseScreen):
    back_to = HOME

    def __init__(self, **kw):
        super().__init__(**kw)
        self._session: QuizSession | None = None
        self.feedback: AnswerResult | None = None

    def _title(self):
        a = _app()
        session = a.quiz_session
        if session and session.subject_id in SUBJECTS:
            return a.tr(SUBJECTS[session.subject_id].name_key)
        return a.tr("start_quiz")

    def build_content(self, box):
        a = _app()
        session = a.quiz_session
        scroll, col = _scroll_col()
        box.add_widget(scroll)
        if session is None:
            col.add_widget(_label(a.tr("no_data")))
            return
        if session is not self._session:
            self._session = session
            self.feedback = None
        col.add_widget(_label(a.tr("lives_label", n=session.lives) + "   " +
                              a.tr("streak_label", n=session.streak) + "   " +
                              a.tr("plus_xp", n=session.xp), "14sp"))
        bar = MDLinearProgressIndicator(size_hint_y=None, height=dp(8))
        bar.value = session.progress * 100
        col.add_widget(bar)
        if self.feedback is not None and self.feedback.question is not None:
            result = self.feedback
            if result.correct:
                col.add_widget(_label(a.tr("correct"), "18sp"))
                detail = tutor.explanation(session.skill_id, a.lang)
            else:
                answer = a.tr(result.question.option_keys[result.question.correct])
                col.add_widget(_label(a.tr("wrong_short", answer=answer), "18sp"))
                detail = tutor.local_hint(session.skill_id, a.lang)
            col.add_widget(_label(detail, "16sp"))
            rewards = []
            if result.xp_gain:
                rewards.append(a.tr("plus_xp", n=result.xp_gain))
            if result.coins_gain:
                rewards.append(a.tr("coins_label", n=result.coins_gain))
            if rewards:
                col.add_widget(_label("  ·  ".join(rewards), "14sp"))
            col.add_widget(_button(a.tr("continue_quiz"), self._continue))
            return
        if session.finished or session.current is None:
            col.add_widget(_label(a.tr("quiz_over"), "22sp"))
            col.add_widget(_label(a.tr("quiz_score", score=session.percent, xp=session.xp)))
            stats = a.db.get_stats(a.student_id)
            for bid in stats["badges"]:
                col.add_widget(_label(a.tr(f"badge_{bid}")))
            col.add_widget(_button(a.tr("play_again"), lambda: a.start_quiz(session.subject_id)))
            col.add_widget(_button(a.tr("back"), lambda: a.go(HOME, "right"), "text"))
            return
        q = session.current
        col.add_widget(_label(a.tr("question_n", n=session.index + 1, total=session.total), "14sp"))
        question_panel = MDBoxLayout(orientation="vertical", padding=dp(12), adaptive_height=True)
        question_panel.add_widget(_label(a.tr(q.text_key), "22sp", bold=True))
        col.add_widget(question_panel)
        for i, key in enumerate(q.option_keys):
            col.add_widget(_button(a.tr(key), lambda i=i: self._answer(i)))

    def _answer(self, idx):
        a = _app()
        session = a.quiz_session
        q = session.current
        result = session.answer(idx)
        a.db.record_attempt(a.student_id, f"quiz_{session.subject_id}", session.skill_id, q.id,
                            result.correct, False)
        a.db.apply_session_rewards(a.student_id, session)
        self.feedback = result
        speak(a.tr("correct") if result.correct else a.tr("not_quite"))
        a.request_sync()
        self.on_pre_enter()

    def _continue(self):
        self.feedback = None
        self.on_pre_enter()


class LabScreen(BaseScreen):
    back_to = SCIENCE

    def on_pre_enter(self, *_):
        self.view = None
        self.ran = False
        super().on_pre_enter()

    def on_leave(self, *_):
        if getattr(self, "view", None):
            self.view.stop_loop()
        super().on_leave()

    def _title(self):
        a = _app()
        if a.current_experiment:
            return a.tr(EXPERIMENTS[a.current_experiment].title_key)
        return a.tr("app_title")

    def build_content(self, box):
        a = _app()
        self.exp = EXPERIMENTS[a.current_experiment]
        scroll, col = _scroll_col()
        box.add_widget(scroll)
        col.add_widget(_label(a.tr("lab_do"), "16sp"))
        self.view = LabView(MODELS[self.exp.lab](), on_finished=self._on_finished,
                            size_hint_y=None, height=dp(260))
        col.add_widget(self.view)
        self.result_label = _label("")
        col.add_widget(self.result_label)
        self.controls = ResponsiveGrid(compact_columns=1, wide_columns=3, spacing=dp(8),
                                       padding=dp(8))
        self._build_controls()
        col.add_widget(self.controls)
        col.add_widget(_button(a.tr("answer_question"), self._ask))
        self.view.start_loop()

    def _slider(self, label_key, key, lo, hi, value, step):
        a = _app()
        wrap = MDBoxLayout(orientation="vertical", adaptive_height=True, size_hint_x=1)
        wrap.add_widget(_label(a.tr(label_key), "14sp"))
        s = Slider(min=lo, max=hi, value=value, step=step, size_hint_y=None, height=dp(40))
        s.bind(value=lambda _w, v: self._param(key, v))
        wrap.add_widget(s)
        self.controls.add_widget(wrap)

    def _build_controls(self):
        a, lab = _app(), self.exp.lab
        if lab == "gravity":
            self._slider("height", "height", 50, 300, 300, 10)
        elif lab == "bounce":
            self._slider("bounciness", "elasticity", 0.0, 1.0, 0.7, 0.05)
        elif lab == "friction":
            for key in ("ice", "wood", "rough"):
                self.controls.add_widget(_button(a.tr(f"surf_{key}"),
                                                 lambda k=key: self._param("surface", k), "tonal"))
        go_key = "release" if lab == "friction" else "drop"
        self.controls.add_widget(_button(a.tr(go_key), self._go))
        self.controls.add_widget(_button(a.tr("reset"), self._reset, "text"))

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

    def _ask(self):
        a = _app()
        if not self.ran:
            self.result_label.text = a.tr("run_first")
            return
        _, attempts = a.db.get_mastery(a.student_id, self.exp.skill_id)
        q = pick_question(self.exp, attempts)
        self._quiz_q = q
        self.result_label.text = a.tr(q.text_key)
        self.controls.clear_widgets()
        for i, key in enumerate(q.option_keys):
            self.controls.add_widget(_button(a.tr(key), lambda i=i: self._answer(i)))

    def _answer(self, idx):
        a = _app()
        q = self._quiz_q
        correct = idx == q.correct
        out = a.db.record_attempt(a.student_id, self.exp.id, self.exp.skill_id, q.id, correct, False)
        lines = [a.tr("correct") if correct else a.tr("not_quite")]
        lines.append(tutor.explanation(self.exp.skill_id, a.lang) if correct
                     else f"{a.tr('hint')}: {tutor.local_hint(self.exp.skill_id, a.lang)}")
        lines.append(a.tr("mastery_now", pct=round(out["p_after"] * 100)))
        self.result_label.text = "\n".join(lines)
        speak(lines[0])
        a.request_sync()
        self.controls.clear_widgets()
        self._build_controls()


class ProgressScreen(BaseScreen):
    back_to = HOME

    def _title(self):
        return _app().tr("my_progress")

    def build_content(self, box):
        a = _app()
        scroll, col = _scroll_col()
        box.add_widget(scroll)
        stats = a.db.get_stats(a.student_id)
        col.add_widget(_label(a.tr("xp_label", xp=stats["xp"], level=level_for_xp(stats["xp"])), "18sp"))
        mastery = a.db.all_mastery(a.student_id)
        if not any(n for _, n in mastery.values()):
            col.add_widget(_label(a.tr("no_data")))
        for sid, (p, n) in mastery.items():
            if n == 0:
                continue
            col.add_widget(_label(f"{a.tr(SKILLS[sid].name_key)}  —  {round(p * 100)}%  ({a.tr('attempts', n=n)})"))
            bar = MDLinearProgressIndicator(size_hint_y=None, height=dp(8))
            bar.value = p * 100
            col.add_widget(bar)


class TeacherScreen(BaseScreen):
    back_to = HOME

    def _title(self):
        return _app().tr("teacher_view")

    def build_content(self, box):
        a = _app()
        scroll, col = _scroll_col()
        box.add_widget(scroll)
        rows = a.db.class_summary()
        if not rows:
            col.add_widget(_label(a.tr("no_data")))
        for r in sorted(rows, key=lambda r: (r["avg"] is None, r["avg"] if r["avg"] is not None else 0)):
            avg = "-" if r["avg"] is None else f"{round(r['avg'] * 100)}%"
            col.add_widget(_label(f"{r['name']} (Class {r['class_level']})  —  {a.tr('avg_mastery')}: {avg}"))
            col.add_widget(_label(a.tr("attempts", n=r["attempts"]), "14sp"))


class ProfileScreen(BaseScreen):
    back_to = HOME

    def _title(self):
        return _app().tr("profile")

    def build_content(self, box):
        a = _app()
        student = a.db.get_student(a.student_id)
        stats = a.db.get_stats(a.student_id)
        scroll, col = _scroll_col()
        box.add_widget(scroll)
        col.add_widget(_label(student["name"], "22sp"))
        col.add_widget(_label(a.tr("class_chip", n=student["class_level"])))
        col.add_widget(_label(a.tr("xp_label", xp=stats["xp"], level=level_for_xp(stats["xp"]))))
        col.add_widget(_label(a.tr("streak_label", n=stats["streak"]) + "  ·  " +
                              a.tr("coins_label", n=stats["coins"])))
        col.add_widget(_label(a.tr("badges"), "18sp"))
        if stats["badges"]:
            for bid in stats["badges"]:
                col.add_widget(_label(a.tr(f"badge_{bid}")))
        else:
            col.add_widget(_label(a.tr("no_badges")))
        url = a.platform_url
        if url and platform_health(url):
            col.add_widget(_label(a.tr("backend_ok")))
            cur = fetch_curriculum(url, api_key=a.api_key)
            if cur and cur.get("subjects"):
                col.add_widget(_label(", ".join(s.get("id", "") for s in cur["subjects"]), "14sp"))
        else:
            col.add_widget(_label(a.tr("backend_off")))
        row = MDBoxLayout(adaptive_height=True, spacing=dp(8))
        for code in LANGS:
            row.add_widget(_button(lang_label(code), lambda c=code: self._lang(c), "outlined"))
        col.add_widget(row)

    def _lang(self, code):
        _app().set_lang(code, persist=True)
        self.on_pre_enter()


SCREENS = (
    (WELCOME, WelcomeScreen),
    (HOME, HomeScreen),
    (STUDY, StudyMaterialScreen),
    (TUTOR, TutorScreen),
    (SCIENCE, ScienceScreen),
    (QUIZ, QuizScreen),
    (LAB, LabScreen),
    (PROGRESS, ProgressScreen),
    (TEACHER, TeacherScreen),
    (PROFILE, ProfileScreen),
)
