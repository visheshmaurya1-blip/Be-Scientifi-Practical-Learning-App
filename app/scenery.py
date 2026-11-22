"""Classroom photo background with a calm offline fallback."""
from __future__ import annotations

from pathlib import Path

from kivy.graphics import Color, Ellipse, Rectangle
from kivy.resources import resource_add_path, resource_find
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout

ROOT = Path(__file__).resolve().parent.parent
GRAPHICS = ROOT / "Graphics"
resource_add_path(str(GRAPHICS))
BACKGROUND_IMAGE = resource_find("background.jpg")
LOGO_IMAGE = resource_find("logo.png")


class ScenicBackground(FloatLayout):
    """Display the classroom photo over a calm fallback that remains visible if loading fails."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.82, 0.90, 0.88, 1)
            self._sky = Rectangle()
            Color(0.74, 0.84, 0.78, 1)
            self._distant_hills = [Ellipse(), Ellipse()]
            Color(0.60, 0.76, 0.66, 1)
            self._near_hills = [Ellipse(), Ellipse()]
            Color(0.47, 0.66, 0.53, 1)
            self._foreground = Rectangle()
        self.bind(pos=self._layout_fallback, size=self._layout_fallback)
        self._layout_fallback()

        self._photo = None
        if BACKGROUND_IMAGE:
            self._photo = Image(
                source=BACKGROUND_IMAGE, fit_mode="cover",
                size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
            self.add_widget(self._photo)

    def _layout_fallback(self, *_):
        if not hasattr(self, "_sky") or self.width <= 0 or self.height <= 0:
            return
        x, y = self.pos
        width, height = self.size
        ground = height * 0.14
        self._sky.pos = self.pos
        self._sky.size = self.size
        self._distant_hills[0].pos = (x - width * 0.20, y + ground * 0.40)
        self._distant_hills[0].size = (width * 0.90, height * 0.30)
        self._distant_hills[1].pos = (x + width * 0.34, y + ground * 0.30)
        self._distant_hills[1].size = (width * 0.92, height * 0.35)
        self._near_hills[0].pos = (x - width * 0.25, y + ground * 0.18)
        self._near_hills[0].size = (width * 0.88, height * 0.25)
        self._near_hills[1].pos = (x + width * 0.36, y + ground * 0.10)
        self._near_hills[1].size = (width * 0.92, height * 0.27)
        self._foreground.pos = (x, y)
        self._foreground.size = (width, ground)

    def start(self):
        """Kept for compatibility with the screen lifecycle."""

    def stop(self):
        """Kept for compatibility with the screen lifecycle."""
