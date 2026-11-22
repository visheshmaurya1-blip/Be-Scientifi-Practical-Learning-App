"""Small scalable vector symbols used by the app shell."""
from __future__ import annotations

from math import cos, radians, sin
import re

from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.graphics import (
    Color,
    Ellipse,
    Line,
    PopMatrix,
    PushMatrix,
    Rectangle,
    Rotate,
    RoundedRectangle,
    Triangle,
)


class LearningSymbol(Widget):
    """Draw a compact app or subject symbol without external image assets."""

    def __init__(self, kind: str = "brand", **kwargs):
        self.kind = kind
        super().__init__(**kwargs)
        self.bind(pos=self._draw, size=self._draw)
        self._draw()

    def _draw(self, *_):
        self.canvas.clear()
        side = min(self.width, self.height)
        if side <= 0:
            return
        x = self.center_x - side / 2
        y = self.center_y - side / 2
        cx, cy = self.center
        radius = side * 0.46
        stroke = max(dp(1.4), side * 0.055)

        with self.canvas:
            if self.kind == "brand":
                Color(0.10, 0.39, 0.31, 1)
            elif self.kind == "bunny":
                Color(0.10, 0.39, 0.31, 1)
            elif self.kind == "science":
                Color(0.12, 0.48, 0.52, 1)
            elif self.kind == "math":
                Color(0.45, 0.34, 0.66, 1)
            else:
                Color(0.84, 0.48, 0.19, 1)
            Ellipse(pos=(x, y), size=(side, side))

            if self.kind == "science":
                Color(0.90, 0.98, 0.95, 1)
                for angle in (0, 60, -60):
                    PushMatrix()
                    Rotate(angle=angle, origin=(cx, cy))
                    Line(ellipse=(cx - radius * 0.68, cy - radius * 0.28,
                                  radius * 1.36, radius * 0.56), width=stroke)
                    PopMatrix()
                Ellipse(pos=(cx - side * 0.07, cy - side * 0.07),
                        size=(side * 0.14, side * 0.14))
            elif self.kind == "bunny":
                Color(0.98, 0.98, 0.94, 1)
                ear_w, ear_h = side * 0.16, side * 0.40
                for ear_x in (cx - side * 0.24, cx + side * 0.08):
                    RoundedRectangle(
                        pos=(ear_x, cy + side * 0.02), size=(ear_w, ear_h),
                        radius=[(ear_w / 2, ear_w / 2)])
                Ellipse(pos=(cx - side * 0.30, cy - side * 0.27),
                        size=(side * 0.60, side * 0.56))
                Color(0.94, 0.60, 0.67, 1)
                for ear_x in (cx - side * 0.19, cx + side * 0.13):
                    RoundedRectangle(
                        pos=(ear_x, cy + side * 0.09), size=(side * 0.06, side * 0.25),
                        radius=[(side * 0.03, side * 0.03)])
                Color(0.12, 0.18, 0.18, 1)
                for eye_x in (cx - side * 0.13, cx + side * 0.09):
                    Ellipse(pos=(eye_x, cy - side * 0.05),
                            size=(side * 0.055, side * 0.055))
                Color(0.82, 0.40, 0.48, 1)
                Ellipse(pos=(cx - side * 0.04, cy - side * 0.17),
                        size=(side * 0.08, side * 0.06))
            elif self.kind == "math":
                Color(0.97, 0.94, 1, 1)
                pad = side * 0.25
                RoundedRectangle(pos=(cx - pad, cy - pad), size=(pad * 2, pad * 2),
                                 radius=[(side * 0.06, side * 0.06)])
                Line(points=(cx - side * 0.13, cy, cx + side * 0.13, cy), width=stroke)
                Line(points=(cx, cy - side * 0.13, cx, cy + side * 0.13), width=stroke)
            elif self.kind in ("english", "hindi"):
                Color(0.97, 0.94, 0.82, 1)
                Line(points=(cx, cy - side * 0.24,
                             cx - side * 0.30, cy - side * 0.14,
                             cx - side * 0.30, cy + side * 0.22,
                             cx, cy + side * 0.14,
                             cx + side * 0.30, cy + side * 0.22,
                             cx + side * 0.30, cy - side * 0.14,
                             cx, cy - side * 0.24),
                     close=True, width=stroke, joint="round")
                Line(points=(cx, cy - side * 0.22, cx, cy + side * 0.15),
                     width=stroke)
                Line(points=(cx - side * 0.22, cy + side * 0.10,
                             cx - side * 0.07, cy + side * 0.14),
                     width=stroke * 0.8)
                Line(points=(cx + side * 0.07, cy + side * 0.14,
                             cx + side * 0.22, cy + side * 0.10),
                     width=stroke * 0.8)
            elif self.kind == "world":
                Color(0.95, 0.97, 0.86, 1)
                Ellipse(pos=(cx - side * 0.31, cy - side * 0.31),
                        size=(side * 0.62, side * 0.62))
                Color(0.84, 0.48, 0.19, 1)
                Line(ellipse=(cx - side * 0.18, cy - side * 0.31,
                              side * 0.36, side * 0.62), width=stroke)
                Line(points=(cx - side * 0.29, cy,
                             cx + side * 0.29, cy), width=stroke)
                Line(ellipse=(cx - side * 0.27, cy - side * 0.13,
                              side * 0.54, side * 0.26), width=stroke * 0.8)
                Line(points=(cx - side * 0.24, cy - side * 0.14,
                             cx + side * 0.24, cy - side * 0.14),
                     width=stroke * 0.8)
                Line(points=(cx - side * 0.24, cy + side * 0.14,
                             cx + side * 0.24, cy + side * 0.14),
                     width=stroke * 0.8)
            elif self.kind == "reasoning":
                Color(1, 0.96, 0.88, 1)
                Ellipse(pos=(cx - side * 0.22, cy - side * 0.20),
                        size=(side * 0.40, side * 0.40),
                        angle_start=25, angle_end=315)
                Line(points=(cx + side * 0.12, cy - side * 0.12,
                             cx + side * 0.29, cy - side * 0.29),
                     width=stroke * 1.5, cap="round")
                Line(points=(cx - side * 0.05, cy + side * 0.04,
                             cx + side * 0.03, cy + side * 0.12,
                             cx + side * 0.12, cy + side * 0.02),
                     width=stroke, joint="round")
            else:
                Color(0.89, 0.96, 0.76, 1)
                Line(points=(cx - side * 0.25, cy - side * 0.22,
                             cx - side * 0.12, cy + side * 0.18,
                             cx + side * 0.02, cy + side * 0.34,
                             cx + side * 0.28, cy + side * 0.30,
                             cx + side * 0.38, cy + side * 0.05,
                             cx + side * 0.18, cy - side * 0.18),
                     close=True, width=stroke)
                Color(0.97, 1, 0.91, 1)
                Line(points=(cx - side * 0.22, cy - side * 0.17,
                             cx + side * 0.12, cy + side * 0.20),
                     width=stroke * 0.8)


class VirtualObjectIcon(Widget):
    """A small, scalable vector illustration for an interactive lab object."""

    def __init__(self, kind: str, **kwargs):
        self.kind = kind
        super().__init__(**kwargs)
        self.bind(pos=self._draw, size=self._draw)
        self._draw()

    def _draw(self, *_):
        self.canvas.clear()
        side = min(self.width, self.height)
        if side <= 0:
            return
        cx, cy = self.center
        s = side / 100
        green = (0.24, 0.61, 0.35, 1)
        blue = (0.24, 0.52, 0.83, 1)
        yellow = (0.97, 0.72, 0.20, 1)
        red = (0.86, 0.31, 0.29, 1)
        brown = (0.52, 0.34, 0.22, 1)
        dark = (0.20, 0.25, 0.30, 1)
        kinds = self.kind

        with self.canvas:
            if kinds.startswith("scene_"):
                parts = kinds.split("_", 2)
                subject = parts[1] if len(parts) > 1 else "math"
                scene = parts[2] if len(parts) > 2 else "mismatch"
                if scene == "mismatch":
                    Color((0.91, 0.94, 0.96, 1))
                    RoundedRectangle(pos=(cx - 32 * s, cy - 25 * s),
                                     size=(64 * s, 50 * s), radius=[(5 * s, 5 * s)])
                    Color(red)
                    Line(points=(cx - 28 * s, cy - 29 * s, cx + 28 * s, cy + 29 * s),
                         width=5 * s)
                    Line(points=(cx - 28 * s, cy + 29 * s, cx + 28 * s, cy - 29 * s),
                         width=5 * s)
                elif scene in ("fraction", "geometry", "pattern"):
                    if scene == "fraction":
                        for index in range(4):
                            Color(yellow if index < 2 else (0.94, 0.95, 0.96, 1))
                            Rectangle(pos=(cx - 32 * s + index * 16 * s,
                                            cy - 17 * s), size=(16 * s, 34 * s))
                        Color(dark)
                        for index in range(5):
                            Line(points=(cx - 32 * s + index * 16 * s, cy - 18 * s,
                                         cx - 32 * s + index * 16 * s, cy + 18 * s),
                                 width=1.5 * s)
                    elif scene == "geometry":
                        Color(blue)
                        Triangle(points=(cx - 29 * s, cy - 22 * s,
                                         cx - 13 * s, cy + 24 * s,
                                         cx + 3 * s, cy - 22 * s))
                        Color(green)
                        Rectangle(pos=(cx + 8 * s, cy - 21 * s),
                                  size=(27 * s, 42 * s))
                        Color(red)
                        Line(points=(cx - 36 * s, cy - 29 * s, cx + 36 * s, cy + 29 * s),
                             width=2 * s)
                    else:
                        for index, color in enumerate((red, blue, blue, red, blue, blue)):
                            Color(color)
                            Rectangle(pos=(cx - 33 * s + index * 13 * s,
                                            cy - 12 * s), size=(11 * s, 24 * s))
                elif scene in ("number", "groups"):
                    group_count = 3 if scene == "groups" else 3
                    for group in range(group_count):
                        x = cx - 26 * s + group * 26 * s
                        Color((0.87, 0.91, 0.95, 1))
                        RoundedRectangle(pos=(x - 9 * s, cy - 20 * s),
                                         size=(18 * s, 40 * s), radius=[(3 * s, 3 * s)])
                        Color((blue, yellow, green)[group])
                        for item in range(group + 2):
                            Ellipse(pos=(x - 3 * s, cy - 15 * s + item * 9 * s),
                                    size=(6 * s, 6 * s))
                elif scene in ("measure", "temperature"):
                    Color((0.93, 0.91, 0.83, 1))
                    RoundedRectangle(pos=(cx - 31 * s, cy - 12 * s),
                                     size=(62 * s, 24 * s), radius=[(3 * s, 3 * s)])
                    Color(red if scene == "temperature" else dark)
                    for index in range(11):
                        x = cx - 28 * s + index * 5.6 * s
                        Line(points=(x, cy + 11 * s, x,
                                     cy + (2 if index % 5 else -4) * s),
                             width=1.5 * s)
                    if scene == "temperature":
                        Color(red)
                        Line(points=(cx, cy - 5 * s, cx, cy - 26 * s), width=5 * s)
                        Ellipse(pos=(cx - 6 * s, cy - 31 * s), size=(12 * s, 12 * s))
                elif scene == "graph":
                    Color(dark)
                    Line(points=(cx - 32 * s, cy - 25 * s, cx + 32 * s, cy - 25 * s,
                                 cx - 32 * s, cy - 25 * s, cx - 32 * s, cy + 27 * s),
                         width=2 * s)
                    for index, (height, color) in enumerate(
                        ((22, blue), (37, yellow), (29, green))
                    ):
                        Color(color)
                        Rectangle(pos=(cx - 22 * s + index * 20 * s, cy - 24 * s),
                                  size=(13 * s, height * s))
                elif scene == "clock":
                    Color((0.94, 0.96, 0.98, 1))
                    Ellipse(pos=(cx - 29 * s, cy - 29 * s), size=(58 * s, 58 * s))
                    Color(dark)
                    Line(circle=(cx, cy, 28 * s), width=2 * s)
                    Line(points=(cx, cy, cx, cy + 17 * s), width=3 * s)
                    Line(points=(cx, cy, cx + 18 * s, cy), width=2 * s)
                    Ellipse(pos=(cx - 3 * s, cy - 3 * s), size=(6 * s, 6 * s))
                elif scene in ("map", "community"):
                    Color((0.74, 0.87, 0.68, 1))
                    Rectangle(pos=(cx - 36 * s, cy - 29 * s), size=(72 * s, 58 * s))
                    Color((0.93, 0.83, 0.59, 1))
                    Line(points=(cx - 32 * s, cy - 18 * s, cx - 8 * s, cy - 3 * s,
                                 cx + 9 * s, cy + 5 * s, cx + 31 * s, cy + 22 * s),
                         width=6 * s)
                    for x, y, color in ((-23, 15, blue), (14, -14, red), (20, 16, yellow)):
                        Color(color)
                        Rectangle(pos=(cx + x * s - 6 * s, cy + y * s - 6 * s),
                                  size=(12 * s, 12 * s))
                elif scene in ("animal", "nature", "plant", "food"):
                    Color((0.55, 0.37, 0.23, 1))
                    Rectangle(pos=(cx - 4 * s, cy - 30 * s), size=(8 * s, 31 * s))
                    Color(green)
                    for x, y in ((-18, 8), (0, 23), (18, 8), (0, -4)):
                        Ellipse(pos=(cx + (x - 15) * s, cy + (y - 10) * s),
                                size=(30 * s, 24 * s))
                    if scene == "animal":
                        Color(yellow)
                        Ellipse(pos=(cx + 15 * s, cy - 21 * s), size=(18 * s, 16 * s))
                        Color(dark)
                        Ellipse(pos=(cx + 27 * s, cy - 13 * s), size=(3 * s, 3 * s))
                    elif scene == "food":
                        Color(red)
                        Ellipse(pos=(cx - 23 * s, cy - 27 * s), size=(17 * s, 17 * s))
                        Color(yellow)
                        Ellipse(pos=(cx + 8 * s, cy - 27 * s), size=(17 * s, 17 * s))
                elif scene == "magnet":
                    Color(red)
                    Line(points=(cx - 20 * s, cy + 24 * s, cx - 20 * s, cy - 5 * s,
                                 cx - 13 * s, cy - 22 * s, cx, cy - 28 * s,
                                 cx + 13 * s, cy - 22 * s, cx + 20 * s, cy - 5 * s,
                                 cx + 20 * s, cy + 24 * s), width=10 * s, joint="round")
                    Color(blue)
                    Line(points=(cx - 20 * s, cy + 24 * s, cx - 20 * s, cy + 10 * s),
                         width=10 * s)
                    Line(points=(cx + 20 * s, cy + 24 * s, cx + 20 * s, cy + 10 * s),
                         width=10 * s)
                elif scene in ("water",):
                    Color(blue)
                    Line(points=(cx - 24 * s, cy + 24 * s, cx + 24 * s, cy + 24 * s,
                                 cx + 18 * s, cy - 22 * s, cx - 18 * s, cy - 22 * s,
                                 cx - 24 * s, cy + 24 * s), width=3 * s)
                    for x in (-11, 0, 11):
                        Ellipse(pos=(cx + x * s - 4 * s, cy - 10 * s), size=(8 * s, 8 * s))
                elif scene in ("space",):
                    Color((0.12, 0.19, 0.42, 1))
                    Ellipse(pos=(cx - 31 * s, cy - 31 * s), size=(62 * s, 62 * s))
                    Color(yellow)
                    for x, y in ((-15, 15), (18, 21), (21, -12), (-18, -17)):
                        Ellipse(pos=(cx + x * s, cy + y * s), size=(5 * s, 5 * s))
                    Color((0.84, 0.86, 0.90, 1))
                    Triangle(points=(cx - 6 * s, cy - 24 * s, cx, cy + 25 * s,
                                     cx + 7 * s, cy - 24 * s))
                elif scene in ("timeline",):
                    Color(dark)
                    Line(points=(cx - 33 * s, cy - 8 * s, cx + 33 * s, cy - 8 * s),
                         width=3 * s)
                    for index, color in enumerate((blue, yellow, red)):
                        x = cx - 25 * s + index * 25 * s
                        Color(color)
                        Ellipse(pos=(x - 7 * s, cy + 7 * s), size=(14 * s, 14 * s))
                        Color(dark)
                        Line(points=(x, cy - 9 * s, x, cy - 24 * s), width=2 * s)
                else:
                    Color((0.96, 0.91, 0.72, 1))
                    RoundedRectangle(pos=(cx - 30 * s, cy - 24 * s),
                                     size=(60 * s, 48 * s), radius=[(4 * s, 4 * s)])
                    Color(blue if subject != "sanskrit" else green)
                    Line(points=(cx - 23 * s, cy + 14 * s, cx + 22 * s, cy + 14 * s,
                                 cx - 23 * s, cy + 3 * s, cx + 12 * s, cy + 3 * s,
                                 cx - 23 * s, cy - 8 * s, cx + 22 * s, cy - 8 * s,
                                 cx - 23 * s, cy - 18 * s, cx + 8 * s, cy - 18 * s),
                         width=2 * s)
            elif kinds.startswith("placevalue_"):
                number = int(kinds.split("_", 1)[1])
                hundreds, remainder = divmod(number, 100)
                tens, ones = divmod(remainder, 10)
                for column, (count, color) in enumerate(
                    ((hundreds, blue), (tens, yellow), (ones, green))
                ):
                    x = cx - 31 * s + column * 31 * s
                    Color(color)
                    for index in range(count):
                        y = cy - 30 * s + index * 7 * s
                        if column < 2:
                            Rectangle(pos=(x - 5 * s, y), size=(10 * s, 5 * s))
                        else:
                            Ellipse(pos=(x - 3 * s, y), size=(6 * s, 6 * s))
                    Color(dark)
                    Line(points=(x - 10 * s, cy - 33 * s, x + 10 * s, cy - 33 * s),
                         width=1.5 * s)
            elif kinds.startswith(("blocks_", "color_")):
                for index, color in enumerate((red, blue, yellow)):
                    x = cx - 31 * s + index * 23 * s
                    if kinds == "color_blue":
                        color = blue
                    elif kinds.endswith("mismatch"):
                        color = (red, red, blue)[index]
                    Color(color)
                    RoundedRectangle(pos=(x, cy - 12 * s), size=(19 * s, 24 * s),
                                     radius=[(3 * s, 3 * s)])
                    if kinds.startswith("blocks_") and index < 2:
                        Color(dark)
                        Line(points=(x + 19 * s, cy, x + 23 * s, cy), width=1.5 * s)
            elif kinds in ("food_sources", "food_tools"):
                for index, color in enumerate((green, yellow, red)):
                    x = cx - 27 * s + index * 25 * s
                    Color(color if kinds == "food_sources" else dark)
                    Ellipse(pos=(x - 9 * s, cy - 11 * s), size=(18 * s, 22 * s))
                if kinds == "food_tools":
                    Color(red)
                    Line(points=(cx - 31 * s, cy - 30 * s, cx + 31 * s, cy + 30 * s),
                         width=4 * s)
            elif kinds.startswith("snacks_") or kinds.startswith("food_"):
                suffix = kinds.rsplit("_", 1)[1]
                amount = int(suffix) if suffix.isdigit() else 4
                Color((0.78, 0.60, 0.37, 1))
                RoundedRectangle(pos=(cx - 34 * s, cy - 28 * s), size=(68 * s, 13 * s),
                                 radius=[(4 * s, 4 * s)])
                if kinds.startswith("snacks_"):
                    hundreds, remainder = divmod(amount, 100)
                    tens, ones = divmod(remainder, 10)
                    Color(blue)
                    for index in range(hundreds):
                        RoundedRectangle(pos=(cx - 28 * s + index * 18 * s,
                                              cy + 5 * s), size=(15 * s, 25 * s),
                                         radius=[(3 * s, 3 * s)])
                    Color(yellow)
                    for index in range(tens):
                        Rectangle(pos=(cx - 29 * s + index * 7 * s,
                                       cy - 10 * s), size=(5 * s, 15 * s))
                    Color(red)
                    for index in range(ones):
                        Ellipse(pos=(cx - 29 * s + index * 7 * s,
                                     cy - 22 * s), size=(5 * s, 5 * s))
                else:
                    Color(yellow)
                    for index in range(amount):
                        row, column = divmod(index, 4)
                        Ellipse(pos=(cx - 25 * s + column * 16 * s,
                                     cy - 10 * s + row * 12 * s), size=(9 * s, 8 * s))
            elif kinds.startswith("shape_"):
                Color(blue)
                if kinds.endswith("triangle"):
                    Triangle(points=(cx, cy + 32 * s, cx - 33 * s, cy - 27 * s,
                                     cx + 33 * s, cy - 27 * s))
                elif kinds.endswith("rectangle"):
                    Rectangle(pos=(cx - 34 * s, cy - 23 * s), size=(68 * s, 46 * s))
                else:
                    Ellipse(pos=(cx - 29 * s, cy - 29 * s), size=(58 * s, 58 * s))
                Color(dark)
                Line(circle=(cx, cy, 2 * s), width=1 * s)
            elif kinds.startswith(("groups_", "share_", "party_")):
                number = int(kinds.rsplit("_", 1)[1])
                group_count = 4 if kinds.startswith("groups_") else 5 if kinds.startswith("share_") else 4
                per_group = (max(1, number // 4) if kinds.startswith("groups_")
                             else number if kinds.startswith("share_")
                             else max(1, number // 4))
                for group in range(group_count):
                    x = cx - 33 * s + group * (66 * s / max(group_count - 1, 1))
                    Color((0.88, 0.91, 0.95, 1))
                    Ellipse(pos=(x - 8 * s, cy - 20 * s), size=(16 * s, 9 * s))
                    Color(blue)
                    for index in range(min(per_group, 6)):
                        Ellipse(pos=(x - 7 * s + (index % 3) * 5 * s,
                                     cy - 8 * s + (index // 3) * 8 * s),
                                size=(5 * s, 5 * s))
            elif kinds.startswith("cup_"):
                capacity = int(kinds.rsplit("_", 1)[1])
                Color((0.72, 0.84, 0.91, 1))
                Line(points=(cx - 21 * s, cy + 25 * s, cx - 16 * s, cy - 25 * s,
                             cx + 16 * s, cy - 25 * s, cx + 21 * s, cy + 25 * s),
                     width=3 * s)
                Color(blue)
                Rectangle(pos=(cx - 14 * s, cy - 23 * s), size=(28 * s, capacity * 7 * s))
                for index in range(1, 7):
                    Line(points=(cx + 10 * s, cy - 23 * s + index * 7 * s,
                                 cx + 16 * s, cy - 23 * s + index * 7 * s), width=1 * s)
            elif kinds.startswith("timeline_"):
                Color(dark)
                Line(points=(cx - 35 * s, cy - 10 * s, cx + 34 * s, cy - 10 * s),
                     width=3 * s)
                colors = (yellow, blue, (0.27, 0.32, 0.57, 1))
                if kinds.endswith("reverse"):
                    colors = tuple(reversed(colors))
                for index, color in enumerate(colors):
                    x = cx - 29 * s + index * 29 * s
                    Color(color)
                    Ellipse(pos=(x - 8 * s, cy + 3 * s), size=(16 * s, 16 * s))
                    Color(dark)
                    Line(points=(x, cy - 10 * s, x, cy - 23 * s), width=2 * s)
            elif kinds.startswith("money_"):
                amount = int(kinds.rsplit("_", 1)[1])
                Color((0.40, 0.67, 0.43, 1))
                for index in range(min(amount // 10, 8)):
                    Rectangle(pos=(cx - 31 * s + (index % 4) * 15 * s,
                                   cy + 8 * s + (index // 4) * 12 * s),
                              size=(12 * s, 8 * s))
                Color(dark)
                for index in range(min(amount % 10, 7)):
                    Ellipse(pos=(cx + 15 * s + (index % 3) * 7 * s,
                                 cy - 27 * s + (index // 3) * 7 * s),
                            size=(6 * s, 6 * s))
            elif kinds == "animal_touch":
                Color(brown)
                Ellipse(pos=(cx - 22 * s, cy - 14 * s), size=(40 * s, 28 * s))
                Ellipse(pos=(cx + 7 * s, cy + 2 * s), size=(20 * s, 20 * s))
                Color(red)
                Line(points=(cx - 31 * s, cy - 31 * s, cx + 31 * s, cy + 31 * s),
                     width=4 * s)
            elif kinds.startswith("animal_"):
                if kinds.endswith("fish"):
                    Color(blue)
                    Ellipse(pos=(cx - 25 * s, cy - 13 * s), size=(43 * s, 26 * s))
                    Triangle(points=(cx + 16 * s, cy, cx + 34 * s, cy + 14 * s,
                                     cx + 34 * s, cy - 14 * s))
                    Color(1, 1, 1, 1)
                    Ellipse(pos=(cx - 13 * s, cy + 3 * s), size=(6 * s, 6 * s))
                elif kinds.endswith("bird"):
                    Color(yellow)
                    Ellipse(pos=(cx - 23 * s, cy - 11 * s), size=(43 * s, 28 * s))
                    Triangle(points=(cx + 18 * s, cy + 2 * s, cx + 32 * s,
                                     cy - 3 * s, cx + 18 * s, cy - 7 * s))
                    Color(dark)
                    Ellipse(pos=(cx + 7 * s, cy + 5 * s), size=(4 * s, 4 * s))
                    Line(points=(cx - 9 * s, cy - 10 * s, cx - 9 * s, cy - 24 * s,
                                 cx + 9 * s, cy - 24 * s), width=2 * s)
                else:
                    Color(brown if kinds.endswith("jackal") else (0.73, 0.51, 0.37, 1))
                    Ellipse(pos=(cx - 24 * s, cy - 16 * s), size=(45 * s, 29 * s))
                    Ellipse(pos=(cx + 9 * s, cy + 1 * s), size=(24 * s, 23 * s))
                    Triangle(points=(cx + 12 * s, cy + 18 * s, cx + 13 * s,
                                     cy + 34 * s, cx + 24 * s, cy + 19 * s))
                    Color(dark)
                    for x in (-15, -2, 12, 22):
                        Line(points=(cx + x * s, cy - 12 * s, cx + x * s, cy - 25 * s),
                             width=3 * s)
                    Line(points=(cx - 21 * s, cy - 8 * s, cx - 33 * s, cy - 1 * s,
                                 cx - 35 * s, cy + 9 * s), width=3 * s)
            elif kinds.startswith(("friend_", "friends_")):
                for index, shirt in enumerate((blue, green)):
                    x = cx - 20 * s + index * 40 * s
                    Color((0.82, 0.55, 0.37, 1))
                    Ellipse(pos=(x - 9 * s, cy + 10 * s), size=(18 * s, 19 * s))
                    Color(shirt)
                    RoundedRectangle(pos=(x - 14 * s, cy - 23 * s),
                                     size=(28 * s, 31 * s), radius=[(7 * s, 7 * s)])
                    Color(dark)
                    Ellipse(pos=(x - 4 * s, cy + 18 * s), size=(2.5 * s, 2.5 * s))
                    Ellipse(pos=(x + 3 * s, cy + 18 * s), size=(2.5 * s, 2.5 * s))
                if kinds.endswith(("grab", "push")):
                    Color(red)
                    Line(points=(cx - 30 * s, cy - 30 * s, cx + 30 * s, cy + 30 * s),
                         width=4 * s)
            elif kinds.startswith(("plant_animals", "animal_distance")):
                Color(green)
                Rectangle(pos=(cx - 4 * s, cy - 24 * s), size=(8 * s, 33 * s))
                for x, y in ((-15, 9), (0, 20), (15, 9)):
                    Ellipse(pos=(cx + (x - 12) * s, cy + (y - 9) * s),
                            size=(24 * s, 20 * s))
                Color(yellow)
                Ellipse(pos=(cx + 11 * s, cy - 23 * s), size=(17 * s, 17 * s))
                if kinds.startswith("plant_animals"):
                    Color(blue)
                    Ellipse(pos=(cx - 31 * s, cy + 10 * s), size=(18 * s, 12 * s))
                    Triangle(points=(cx - 15 * s, cy + 16 * s, cx - 7 * s,
                                     cy + 22 * s, cx - 15 * s, cy + 8 * s))
                    Color(red)
                    Ellipse(pos=(cx + 19 * s, cy + 10 * s), size=(9 * s, 8 * s))
                    Ellipse(pos=(cx + 29 * s, cy + 10 * s), size=(9 * s, 8 * s))
                else:
                    Color(brown)
                    Ellipse(pos=(cx + 15 * s, cy - 17 * s), size=(25 * s, 18 * s))
                    Ellipse(pos=(cx + 30 * s, cy - 8 * s), size=(13 * s, 13 * s))
                    Line(points=(cx + 20 * s, cy - 17 * s, cx + 20 * s, cy - 28 * s,
                                 cx + 25 * s, cy - 28 * s), width=3 * s)
                    Color(red)
                    Line(points=(cx - 15 * s, cy - 12 * s, cx - 15 * s, cy - 24 * s,
                                 cx + 12 * s, cy - 24 * s, cx + 12 * s, cy - 12 * s),
                         width=2 * s)
                if kinds.endswith("touch"):
                    Color(red)
                    Line(points=(cx - 30 * s, cy - 30 * s, cx + 30 * s, cy + 30 * s),
                         width=4 * s)
            elif kinds.startswith(("plant_", "tree_")):
                Color(brown)
                Rectangle(pos=(cx - 5 * s, cy - 32 * s), size=(10 * s, 35 * s))
                Color(green)
                for x, y in ((-17, 9), (0, 22), (17, 9), (0, -2)):
                    Ellipse(pos=(cx + (x - 15) * s, cy + (y - 12) * s),
                            size=(30 * s, 26 * s))
                Color((0.53, 0.73, 0.36, 1))
                Ellipse(pos=(cx - 25 * s, cy - 18 * s), size=(15 * s, 9 * s))
                if kinds.endswith(("wrong", "pull")):
                    Color(red)
                    Line(points=(cx - 31 * s, cy - 31 * s, cx + 31 * s, cy + 31 * s),
                         width=4 * s)
                elif kinds.endswith(("leaf", "water")):
                    Color(blue)
                    for dx in (-12, 0, 12):
                        Ellipse(pos=(cx + dx * s, cy - 32 * s), size=(5 * s, 9 * s))
            elif kinds.startswith(("toy_", "boat_")):
                if kinds.startswith("boat_"):
                    Color(blue)
                    Line(points=(cx - 34 * s, cy - 14 * s, cx - 24 * s, cy - 28 * s,
                                 cx + 25 * s, cy - 28 * s, cx + 35 * s, cy - 14 * s,
                                 cx - 34 * s, cy - 14 * s), width=4 * s)
                    Color((0.95, 0.88, 0.68, 1))
                    Triangle(points=(cx, cy - 8 * s, cx, cy + 31 * s,
                                     cx + 24 * s, cy - 8 * s))
                    Line(points=(cx - 3 * s, cy - 10 * s, cx - 3 * s, cy + 35 * s),
                         width=2 * s)
                    if kinds.endswith("flat"):
                        Color(red)
                        Line(points=(cx - 31 * s, cy + 29 * s, cx + 31 * s, cy - 29 * s),
                             width=4 * s)
                else:
                    Color((0.72, 0.45, 0.32, 1))
                    Ellipse(pos=(cx - 24 * s, cy - 18 * s), size=(48 * s, 47 * s))
                    Ellipse(pos=(cx - 25 * s, cy + 17 * s), size=(17 * s, 16 * s))
                    Ellipse(pos=(cx + 8 * s, cy + 17 * s), size=(17 * s, 16 * s))
                    Color(blue)
                    RoundedRectangle(pos=(cx - 18 * s, cy - 22 * s),
                                     size=(36 * s, 29 * s), radius=[(8 * s, 8 * s)])
                    if kinds.endswith("broken"):
                        Color(red)
                        Line(points=(cx - 31 * s, cy - 31 * s, cx + 31 * s, cy + 31 * s),
                             width=4 * s)
            elif kinds.startswith(("community_", "map_", "fair_")):
                Color((0.43, 0.72, 0.46, 1))
                Rectangle(pos=(cx - 38 * s, cy - 32 * s), size=(76 * s, 64 * s))
                Color((0.88, 0.80, 0.65, 1))
                Line(points=(cx - 35 * s, cy - 8 * s, cx + 35 * s, cy - 8 * s),
                     width=8 * s)
                buildings = ((-23, blue), (5, yellow))
                if kinds == "map_homes":
                    buildings = ((-23, blue), (3, red), (22, yellow))
                for x, color in buildings:
                    Color(color)
                    Rectangle(pos=(cx + x * s, cy + 1 * s), size=(14 * s, 17 * s))
                    Triangle(points=(cx + (x - 3) * s, cy + 18 * s,
                                     cx + (x + 17) * s, cy + 18 * s,
                                     cx + (x + 7) * s, cy + 28 * s))
                if kinds.endswith(("litter", "alone")):
                    Color(red)
                    Line(points=(cx - 31 * s, cy - 29 * s, cx + 31 * s, cy + 29 * s),
                         width=4 * s)
                elif kinds.endswith("help"):
                    Color(red)
                    RoundedRectangle(pos=(cx + 16 * s, cy - 29 * s),
                                     size=(17 * s, 17 * s), radius=[(4 * s, 4 * s)])
                    Color(1, 1, 1, 1)
                    Line(points=(cx + 24 * s, cy - 26 * s, cx + 24 * s, cy - 15 * s),
                         width=2 * s)
            elif kinds.startswith(("night_", "stars_")):
                Color((0.13, 0.20, 0.42, 1))
                Rectangle(pos=(cx - 38 * s, cy - 32 * s), size=(76 * s, 64 * s))
                if kinds.endswith("fish"):
                    Color(blue)
                    Ellipse(pos=(cx - 18 * s, cy - 13 * s), size=(38 * s, 25 * s))
                    Triangle(points=(cx + 18 * s, cy, cx + 34 * s, cy + 12 * s,
                                     cx + 34 * s, cy - 12 * s))
                elif kinds.startswith("stars_"):
                    amount = int(kinds.rsplit("_", 1)[1])
                    for index in range(amount):
                        x = cx - 28 * s + (index * 19 % 58) * s
                        y = cy - 22 * s + (index * 13 % 48) * s
                        Color(yellow)
                        Ellipse(pos=(x, y), size=(5 * s, 5 * s))
                else:
                    Color(yellow)
                    Ellipse(pos=(cx + 7 * s, cy + 7 * s), size=(25 * s, 25 * s))
                    Color((0.13, 0.20, 0.42, 1))
                    Ellipse(pos=(cx + 16 * s, cy + 13 * s), size=(24 * s, 24 * s))
                    for x, y in ((-20, 16), (-5, 25), (28, -13)):
                        Color(1, 1, 1, 1)
                        Ellipse(pos=(cx + x * s, cy + y * s), size=(4 * s, 4 * s))
            elif kinds.startswith(("space_", "dialogue_", "moon_map")):
                Color((0.12, 0.20, 0.42, 1))
                Ellipse(pos=(cx + 9 * s, cy + 8 * s), size=(31 * s, 31 * s))
                Color((0.82, 0.84, 0.80, 1))
                Ellipse(pos=(cx + 16 * s, cy + 16 * s), size=(4 * s, 4 * s))
                Ellipse(pos=(cx + 28 * s, cy + 12 * s), size=(5 * s, 5 * s))
                if kinds.endswith("boat"):
                    Color((0.75, 0.43, 0.20, 1))
                    Line(points=(cx - 33 * s, cy - 15 * s, cx - 24 * s, cy - 29 * s,
                                 cx + 25 * s, cy - 29 * s, cx + 34 * s, cy - 15 * s,
                                 cx - 33 * s, cy - 15 * s), width=4 * s)
                    Color(blue)
                    Line(points=(cx - 34 * s, cy - 24 * s, cx + 34 * s, cy - 24 * s),
                         width=2 * s)
                elif kinds.endswith(("rocket", "moon")):
                    Color((0.85, 0.86, 0.91, 1))
                    Triangle(points=(cx - 15 * s, cy - 25 * s, cx - 7 * s,
                                     cy + 20 * s, cx + 1 * s, cy - 25 * s))
                    Color(red)
                    Triangle(points=(cx - 14 * s, cy - 15 * s, cx - 23 * s,
                                     cy - 30 * s, cx - 9 * s, cy - 25 * s))
                    Triangle(points=(cx, cy - 25 * s, cx + 10 * s,
                                     cy - 30 * s, cx - 1 * s, cy - 15 * s))
                elif kinds.endswith("wrong"):
                    Color(red)
                    Line(points=(cx - 31 * s, cy - 31 * s, cx + 31 * s, cy + 31 * s),
                         width=4 * s)
                else:
                    Color(blue)
                    Line(points=(cx - 30 * s, cy - 22 * s, cx - 15 * s, cy - 5 * s),
                         width=3 * s)
                    Line(points=(cx - 30 * s, cy + 22 * s, cx - 15 * s, cy + 5 * s),
                         width=3 * s)
            elif kinds.startswith(("learning_book", "letter_", "magic_")):
                if kinds.startswith("letter_"):
                    Color((0.96, 0.91, 0.72, 1))
                    Rectangle(pos=(cx - 30 * s, cy - 22 * s), size=(60 * s, 44 * s))
                    Color(brown)
                    Line(points=(cx - 29 * s, cy + 21 * s, cx, cy - 2 * s,
                                 cx + 29 * s, cy + 21 * s), width=3 * s)
                    Line(points=(cx - 29 * s, cy - 21 * s, cx - 5 * s, cy + 1 * s,
                                 cx + 5 * s, cy + 1 * s, cx + 29 * s, cy - 21 * s),
                         width=2 * s)
                    if kinds.endswith("torn"):
                        Color(red)
                        Line(points=(cx - 31 * s, cy - 30 * s, cx + 31 * s, cy + 30 * s),
                             width=4 * s)
                else:
                    Color((0.96, 0.91, 0.72, 1))
                    Rectangle(pos=(cx - 29 * s, cy - 24 * s), size=(58 * s, 48 * s))
                    Color(blue if not kinds.endswith("sign") else red)
                    Line(points=(cx, cy - 23 * s, cx, cy + 23 * s,
                                 cx - 26 * s, cy + 20 * s, cx - 26 * s, cy - 21 * s,
                                 cx, cy - 23 * s, cx + 26 * s, cy - 21 * s,
                                 cx + 26 * s, cy + 20 * s, cx, cy + 23 * s), width=2 * s)
                    for row in range(3):
                        Line(points=(cx - 21 * s, cy + 12 * s - row * 10 * s,
                                     cx - 4 * s, cy + 12 * s - row * 10 * s), width=1 * s)
                    if kinds.endswith("sign"):
                        Color(red)
                        Line(points=(cx - 30 * s, cy - 30 * s, cx + 30 * s, cy + 30 * s),
                             width=4 * s)
            elif kinds.startswith(("ant_", "stone")):
                if kinds.endswith(("observe", "poke")):
                    Color(dark)
                    for x in (-10, 0, 10):
                        Ellipse(pos=(cx + x * s - 5 * s, cy - 4 * s), size=(10 * s, 9 * s))
                        Line(points=(cx + x * s, cy, cx + (x - 7) * s, cy - 12 * s),
                             width=2 * s)
                        Line(points=(cx + x * s, cy, cx + (x + 7) * s, cy - 12 * s),
                             width=2 * s)
                    if kinds.endswith("poke"):
                        Color(red)
                        Line(points=(cx - 30 * s, cy + 27 * s, cx - 5 * s, cy + 2 * s),
                             width=4 * s)
                else:
                    Color((0.56, 0.53, 0.48, 1))
                    Ellipse(pos=(cx - 27 * s, cy - 19 * s), size=(54 * s, 36 * s))
            elif kinds.startswith(("bird_", "festival_")) or kinds == "traffic_cone":
                if kinds.endswith("nest"):
                    Color(brown)
                    Line(points=(cx - 29 * s, cy - 8 * s, cx - 20 * s, cy - 19 * s,
                                 cx + 20 * s, cy - 19 * s, cx + 29 * s, cy - 8 * s),
                         width=4 * s)
                    Color(yellow)
                    Ellipse(pos=(cx - 14 * s, cy - 2 * s), size=(28 * s, 19 * s))
                    Color(blue)
                    Ellipse(pos=(cx - 8 * s, cy + 1 * s), size=(16 * s, 14 * s))
                    Color(dark)
                    Ellipse(pos=(cx + 1 * s, cy + 8 * s), size=(3 * s, 3 * s))
                elif kinds.endswith("lamp"):
                    Color(brown)
                    Ellipse(pos=(cx - 25 * s, cy - 20 * s), size=(50 * s, 15 * s))
                    Color(yellow)
                    Triangle(points=(cx - 20 * s, cy - 14 * s, cx + 20 * s,
                                     cy - 14 * s, cx, cy + 10 * s))
                    Ellipse(pos=(cx - 7 * s, cy + 8 * s), size=(14 * s, 18 * s))
                elif kinds == "traffic_cone":
                    Color(red)
                    Triangle(points=(cx, cy + 29 * s, cx - 23 * s, cy - 26 * s,
                                     cx + 23 * s, cy - 26 * s))
                    Color(1, 1, 1, 1)
                    Line(points=(cx - 15 * s, cy - 7 * s, cx + 15 * s, cy - 7 * s),
                         width=5 * s)
                else:
                    Color(green)
                    Line(points=(cx - 30 * s, cy - 20 * s, cx + 30 * s, cy + 19 * s,
                                 cx - 28 * s, cy + 24 * s), width=3 * s)
                    Color(yellow)
                    for x in (-16, 0, 16):
                        Ellipse(pos=(cx + x * s - 8 * s, cy + x * 0.55 * s - 8 * s),
                                size=(16 * s, 16 * s))
            elif kinds.startswith(("solution_", "crop_", "water_", "routine_",
                                   "material_", "object_", "waste_", "food_sources",
                                   "plant_animals", "animal_distance", "worker_",
                                   "india_map", "map_homes", "rope_", "cave_",
                                   "empty_", "fair_")):
                Color((0.88, 0.92, 0.82, 1))
                RoundedRectangle(pos=(cx - 36 * s, cy - 29 * s),
                                 size=(72 * s, 58 * s), radius=[(8 * s, 8 * s)])
                if kinds.startswith("crop_"):
                    Color(brown)
                    Rectangle(pos=(cx - 31 * s, cy - 23 * s), size=(62 * s, 10 * s))
                    Color(yellow)
                    for x in (-20, 0, 20):
                        Line(points=(cx + x * s, cy - 10 * s, cx + x * s, cy + 20 * s),
                             width=3 * s)
                        Ellipse(pos=(cx + (x - 8) * s, cy + 6 * s), size=(15 * s, 8 * s))
                elif kinds.startswith("water_"):
                    Color(blue)
                    Line(points=(cx - 10 * s, cy + 24 * s, cx + 10 * s, cy + 24 * s,
                                 cx + 7 * s, cy + 1 * s, cx + 19 * s, cy - 10 * s,
                                 cx + 18 * s, cy - 24 * s, cx - 18 * s, cy - 24 * s,
                                 cx - 19 * s, cy - 10 * s, cx - 7 * s, cy + 1 * s,
                                 cx - 10 * s, cy + 24 * s), width=3 * s)
                    if kinds.endswith("waste"):
                        Color(red)
                        Line(points=(cx - 30 * s, cy - 30 * s, cx + 30 * s, cy + 30 * s),
                             width=4 * s)
                elif kinds.startswith("material_") or kinds.startswith("object_"):
                    Color(brown if kinds.endswith("wood") or kinds.endswith("paperbook")
                          else (0.62, 0.78, 0.86, 1))
                    Rectangle(pos=(cx - 24 * s, cy - 24 * s), size=(48 * s, 48 * s))
                    Line(points=(cx - 17 * s, cy - 14 * s, cx + 17 * s, cy - 14 * s,
                                 cx + 17 * s, cy + 14 * s), width=2 * s)
                elif kinds.startswith("waste_"):
                    Color(green)
                    for x in (-20, 5):
                        Rectangle(pos=(cx + x * s, cy - 18 * s), size=(19 * s, 29 * s))
                    if kinds.endswith("mixed"):
                        Color(red)
                        Line(points=(cx - 31 * s, cy - 30 * s, cx + 31 * s, cy + 30 * s),
                             width=4 * s)
                elif kinds.startswith("india_map") or kinds == "map_homes":
                    Color(green)
                    Line(points=(cx - 17 * s, cy + 30 * s, cx + 2 * s, cy + 19 * s,
                                 cx + 13 * s, cy + 6 * s, cx + 7 * s, cy - 8 * s,
                                 cx + 18 * s, cy - 20 * s, cx + 7 * s, cy - 34 * s,
                                 cx - 4 * s, cy - 23 * s, cx - 16 * s, cy - 15 * s,
                                 cx - 23 * s, cy + 6 * s, cx - 17 * s, cy + 30 * s),
                         close=True, width=3 * s)
                elif kinds.startswith("rope_"):
                    Color(brown)
                    Line(points=(cx - 34 * s, cy, cx - 18 * s, cy + 4 * s,
                                 cx, cy - 3 * s, cx + 18 * s, cy + 4 * s,
                                 cx + 34 * s, cy), width=5 * s)
                    for x, shirt in ((-25, blue), (25, red)):
                        Color(shirt)
                        Ellipse(pos=(cx + (x - 7) * s, cy + 9 * s), size=(14 * s, 14 * s))
                        Line(points=(cx + x * s, cy + 8 * s,
                                     cx + x * s, cy - 19 * s), width=5 * s)
                elif kinds.startswith("cave_"):
                    Color(dark)
                    Triangle(points=(cx - 36 * s, cy - 24 * s, cx - 20 * s, cy + 30 * s,
                                     cx + 20 * s, cy + 30 * s, cx + 36 * s, cy - 24 * s))
                    if kinds.endswith("friend"):
                        Color(yellow)
                        Ellipse(pos=(cx - 10 * s, cy - 5 * s), size=(20 * s, 20 * s))
                        Triangle(points=(cx - 9 * s, cy + 12 * s, cx - 15 * s,
                                         cy + 22 * s, cx - 3 * s, cy + 14 * s))
                        Triangle(points=(cx + 9 * s, cy + 12 * s, cx + 15 * s,
                                         cy + 22 * s, cx + 3 * s, cy + 14 * s))
                    else:
                        Color(red)
                        Line(points=(cx - 30 * s, cy - 30 * s, cx + 30 * s, cy + 30 * s),
                             width=4 * s)
                elif kinds.startswith("animal_distance") or kinds.startswith("plant_animals"):
                    Color(green)
                    Rectangle(pos=(cx - 4 * s, cy - 24 * s), size=(8 * s, 33 * s))
                    for x, y in ((-15, 9), (0, 20), (15, 9)):
                        Ellipse(pos=(cx + (x - 12) * s, cy + (y - 9) * s),
                                size=(24 * s, 20 * s))
                    Color(yellow)
                    Ellipse(pos=(cx + 11 * s, cy - 23 * s), size=(17 * s, 17 * s))
                    if kinds.endswith("touch"):
                        Color(red)
                        Line(points=(cx - 30 * s, cy - 30 * s, cx + 30 * s, cy + 30 * s),
                             width=4 * s)
                elif kinds.startswith("worker_"):
                    for x, shirt in ((-15, blue), (15, green)):
                        Color((0.82, 0.55, 0.37, 1))
                        Ellipse(pos=(cx + (x - 7) * s, cy + 8 * s), size=(14 * s, 14 * s))
                        Color(shirt)
                        RoundedRectangle(pos=(cx + (x - 10) * s, cy - 21 * s),
                                         size=(20 * s, 27 * s), radius=[(5 * s, 5 * s)])
                elif kinds.startswith("fair_") and kinds.endswith("cone"):
                    Color(red)
                    Triangle(points=(cx, cy + 29 * s, cx - 23 * s, cy - 26 * s,
                                     cx + 23 * s, cy - 26 * s))
                elif kinds == "empty_box":
                    Color(brown)
                    Rectangle(pos=(cx - 25 * s, cy - 19 * s), size=(50 * s, 37 * s))
                    Color((0.75, 0.54, 0.35, 1))
                    Line(points=(cx - 25 * s, cy + 18 * s, cx - 7 * s, cy + 31 * s,
                                 cx + 25 * s, cy + 18 * s, cx + 7 * s, cy + 6 * s,
                                 cx - 25 * s, cy + 18 * s), width=3 * s)
                elif kinds == "empty_chairs":
                    Color(brown)
                    for x in (-18, 18):
                        Line(points=(cx + x * s, cy - 20 * s, cx + x * s, cy + 15 * s,
                                     cx + (x - 10) * s, cy + 15 * s,
                                     cx + (x - 10) * s, cy - 5 * s,
                                     cx + (x + 10) * s, cy - 5 * s,
                                     cx + (x + 10) * s, cy + 15 * s), width=3 * s)
                elif kinds.startswith("routine_"):
                    Color(blue)
                    Ellipse(pos=(cx - 20 * s, cy - 20 * s), size=(40 * s, 40 * s))
                    Color(1, 1, 1, 1)
                    Line(points=(cx, cy, cx, cy + 12 * s, cx + 12 * s, cy + 12 * s),
                         width=3 * s)
                    if kinds.endswith("unhealthy"):
                        Color(red)
                        Line(points=(cx - 31 * s, cy - 30 * s, cx + 31 * s, cy + 30 * s),
                             width=4 * s)
                else:
                    Color(yellow)
                    Ellipse(pos=(cx - 20 * s, cy - 18 * s), size=(40 * s, 36 * s))
                    Color(green)
                    Line(points=(cx - 28 * s, cy - 23 * s, cx - 28 * s, cy + 23 * s),
                         width=3 * s)
            elif kinds.startswith("shells_"):
                number = int(kinds.rsplit("_", 1)[1])
                tens, ones = divmod(number, 10)
                for group in range(tens):
                    gx = cx - 34 * s + group * 36 * s
                    Color((0.93, 0.68, 0.43, 1))
                    RoundedRectangle(pos=(gx - 14 * s, cy - 18 * s),
                                     size=(29 * s, 38 * s), radius=[(8 * s, 8 * s)])
                    Color((0.98, 0.86, 0.68, 1))
                    for row in range(3):
                        Line(points=(gx - 9 * s, cy - 10 * s + row * 10 * s,
                                     gx + 9 * s, cy - 10 * s + row * 10 * s),
                             width=1.3 * s)
                for index in range(ones):
                    Color((0.83, 0.59, 0.37, 1))
                    Ellipse(pos=(cx - 31 * s + index * 12 * s,
                                 cy - 38 * s), size=(8 * s, 8 * s))
            elif kinds in ("sphere", "cuboid", "cylinder"):
                if kinds == "sphere":
                    Color((0.92, 0.28, 0.24, 1))
                    Ellipse(pos=(cx - 29 * s, cy - 29 * s), size=(58 * s, 58 * s))
                    Color((1, 0.76, 0.69, 1))
                    Ellipse(pos=(cx - 14 * s, cy + 8 * s), size=(13 * s, 9 * s))
                    Color((0.65, 0.15, 0.15, 1))
                    Line(ellipse=(cx - 22 * s, cy - 22 * s, 44 * s, 44 * s),
                         width=1.5 * s)
                elif kinds == "cuboid":
                    Color((0.31, 0.55, 0.79, 1))
                    Rectangle(pos=(cx - 30 * s, cy - 22 * s), size=(44 * s, 43 * s))
                    Color((0.43, 0.66, 0.86, 1))
                    Triangle(points=(cx - 30 * s, cy + 21 * s, cx - 15 * s, cy + 34 * s,
                                     cx + 29 * s, cy + 34 * s, cx + 14 * s, cy + 21 * s))
                    Color((0.22, 0.43, 0.66, 1))
                    Triangle(points=(cx + 14 * s, cy - 22 * s, cx + 29 * s, cy - 9 * s,
                                     cx + 29 * s, cy + 34 * s, cx + 14 * s, cy + 21 * s))
                    Line(points=(cx - 30 * s, cy - 22 * s, cx - 15 * s, cy - 9 * s,
                                 cx + 29 * s, cy - 9 * s), width=1.5 * s)
                else:
                    Color((0.84, 0.45, 0.22, 1))
                    Rectangle(pos=(cx - 22 * s, cy - 23 * s), size=(44 * s, 46 * s))
                    Color((0.94, 0.60, 0.35, 1))
                    Ellipse(pos=(cx - 22 * s, cy + 12 * s), size=(44 * s, 17 * s))
                    Color((0.65, 0.32, 0.18, 1))
                    Ellipse(pos=(cx - 22 * s, cy - 28 * s), size=(44 * s, 17 * s))
                    Color((0.96, 0.74, 0.58, 1))
                    Ellipse(pos=(cx - 13 * s, cy + 16 * s), size=(26 * s, 8 * s))
            elif kinds.startswith("shadow_"):
                Color((0.98, 0.82, 0.31, 1))
                Ellipse(pos=(cx - 34 * s, cy + 12 * s), size=(26 * s, 26 * s))
                for ray in range(3):
                    Line(points=(cx - 31 * s + ray * 10 * s, cy + 8 * s,
                                 cx - 37 * s + ray * 10 * s, cy - 3 * s),
                         width=2 * s)
                Color(dark)
                Rectangle(pos=(cx - 2 * s, cy - 22 * s), size=(14 * s, 34 * s))
                Color((0.37, 0.41, 0.49, 1))
                Triangle(points=(cx + 13 * s, cy - 22 * s, cx + 40 * s, cy - 13 * s,
                                 cx + 13 * s, cy + 7 * s))
                if kinds.endswith("sound"):
                    Color(red)
                    Line(circle=(cx - 24 * s, cy - 24 * s, 15 * s), width=3 * s)
                    Line(circle=(cx - 24 * s, cy - 24 * s, 24 * s), width=2 * s)
            elif kinds.startswith("line_"):
                Color(blue)
                if kinds.endswith("slant"):
                    Line(points=(cx - 33 * s, cy - 31 * s, cx + 33 * s, cy + 31 * s),
                         width=7 * s, cap="round")
                elif kinds.endswith("vertical"):
                    Line(points=(cx, cy - 34 * s, cx, cy + 34 * s),
                         width=7 * s, cap="round")
                else:
                    Line(points=(cx - 34 * s, cy, cx + 34 * s, cy),
                         width=7 * s, cap="round")
                Color(red)
                Ellipse(pos=(cx - 5 * s, cy - 5 * s), size=(10 * s, 10 * s))
            elif kinds.startswith("lamps_"):
                amount = int(kinds.rsplit("_", 1)[1])
                for index in range(amount):
                    row, column = divmod(index, 7)
                    lx = cx - 34 * s + column * 11 * s
                    ly = cy - 29 * s + row * 10 * s
                    Color((0.75, 0.30, 0.13, 1))
                    Ellipse(pos=(lx - 4 * s, ly - 4 * s), size=(8 * s, 8 * s))
                    Color((1, 0.78, 0.22, 1))
                    Ellipse(pos=(lx - 2 * s, ly - 2 * s), size=(4 * s, 4 * s))
                    Color(brown)
                    Line(points=(lx - 3 * s, ly + 4 * s, lx + 3 * s, ly + 4 * s),
                         width=1 * s)
            elif kinds.startswith("ribbon_"):
                length = int(kinds.rsplit("_", 1)[1])
                Color((0.80, 0.25, 0.39, 1))
                RoundedRectangle(pos=(cx - length * 4 * s, cy - 8 * s),
                                 size=(length * 8 * s, 16 * s), radius=[(4 * s, 4 * s)])
                Color(dark)
                Line(points=(cx - length * 4 * s, cy - 17 * s,
                             cx + length * 4 * s, cy - 17 * s), width=1.5 * s)
                for tick in range(length + 1):
                    tx = cx - length * 4 * s + tick * 8 * s
                    Line(points=(tx, cy - 16 * s, tx, cy - (23 if tick % 2 == 0 else 19) * s),
                         width=1 * s)
            elif kinds.startswith("plates_"):
                each = int(kinds.rsplit("_", 1)[1])
                for plate in range(3):
                    px = cx - 30 * s + plate * 30 * s
                    Color((0.78, 0.84, 0.92, 1))
                    Ellipse(pos=(px - 13 * s, cy - 17 * s), size=(26 * s, 13 * s))
                    Color((1, 1, 1, 1))
                    Ellipse(pos=(px - 10 * s, cy - 14 * s), size=(20 * s, 7 * s))
                    for sweet in range(each):
                        sx = px - (each - 1) * 4 * s + sweet * 8 * s
                        Color(yellow if sweet % 2 else red)
                        Ellipse(pos=(sx - 3 * s, cy - 4 * s), size=(6 * s, 6 * s))
            elif kinds.startswith("fair_cars_"):
                total = int(kinds.rsplit("_", 1)[1])
                for car in range(3):
                    x0 = cx - 30 * s + car * 30 * s
                    Color(red if car == 0 else blue if car == 1 else green)
                    RoundedRectangle(pos=(x0 - 12 * s, cy - 15 * s),
                                     size=(25 * s, 18 * s), radius=[(4 * s, 4 * s)])
                    Color(dark)
                    for wheel_x in (x0 - 7, x0 + 7):
                        Ellipse(pos=(cx + (car * 30 + wheel_x - cx) * s - 4 * s,
                                     cy - 20 * s), size=(8 * s, 8 * s))
                    passengers = max(0, min(5, total - car * 5))
                    for passenger in range(passengers):
                        Color(yellow)
                        Ellipse(pos=(x0 - 8 * s + passenger * 4 * s,
                                     cy + 7 * s), size=(6 * s, 6 * s))
            elif kinds.startswith("graph_"):
                heights = {"graph_mango": 46, "graph_apple": 30, "graph_banana": 20}
                height = heights.get(kinds, 24)
                for index, (bar_color, bar_height) in enumerate(
                    ((yellow, height), (red, 30 if height != 30 else 46),
                     (green, 20 if height != 20 else 46))
                ):
                    bx = cx - 28 * s + index * 23 * s
                    Color(bar_color)
                    Rectangle(pos=(bx, cy - 28 * s), size=(16 * s, bar_height * s))
                Color(dark)
                Line(points=(cx - 34 * s, cy - 28 * s, cx + 35 * s, cy - 28 * s,
                             cx - 34 * s, cy - 28 * s, cx - 34 * s, cy + 30 * s),
                     width=2 * s)
            elif kinds in ("bicycle", "child_tree", "child"):
                if kinds == "bicycle":
                    Color(dark)
                    for wheel_x in (-24, 24):
                        Line(circle=(cx + wheel_x * s, cy - 15 * s, 18 * s), width=3 * s)
                    Line(points=(cx - 24 * s, cy - 15 * s, cx - 3 * s, cy + 9 * s,
                                 cx + 8 * s, cy - 15 * s, cx - 24 * s, cy - 15 * s,
                                 cx + 24 * s, cy - 15 * s, cx + 9 * s, cy + 12 * s,
                                 cx + 2 * s, cy + 12 * s), width=3 * s)
                    Line(points=(cx - 7 * s, cy + 11 * s, cx + 5 * s, cy + 11 * s),
                         width=4 * s)
                    Line(points=(cx + 8 * s, cy - 15 * s, cx + 15 * s, cy + 10 * s,
                                 cx + 24 * s, cy + 10 * s), width=3 * s)
                    Color(red)
                    Line(points=(cx - 12 * s, cy + 16 * s, cx - 3 * s, cy + 16 * s),
                         width=4 * s)
                elif kinds == "child_tree":
                    Color(green)
                    for dx, dy in ((-18, 10), (0, 21), (18, 10), (0, -2)):
                        Ellipse(pos=(cx + (dx - 14) * s, cy + (dy - 12) * s),
                                size=(28 * s, 25 * s))
                    Color(brown)
                    Rectangle(pos=(cx - 5 * s, cy - 30 * s), size=(10 * s, 30 * s))
                else:
                    Color((0.82, 0.55, 0.37, 1))
                    Ellipse(pos=(cx - 12 * s, cy + 15 * s), size=(24 * s, 25 * s))
                    Color((0.25, 0.54, 0.82, 1))
                    RoundedRectangle(pos=(cx - 17 * s, cy - 21 * s),
                                     size=(34 * s, 38 * s), radius=[(8 * s, 8 * s)])
                    Color(dark)
                    Line(points=(cx - 10 * s, cy - 19 * s, cx - 17 * s, cy - 35 * s),
                         width=5 * s)
                    Line(points=(cx + 10 * s, cy - 19 * s, cx + 17 * s, cy - 35 * s),
                         width=5 * s)
                    Color(1, 1, 1, 1)
                    Ellipse(pos=(cx - 5 * s, cy + 23 * s), size=(3 * s, 3 * s))
                    Ellipse(pos=(cx + 3 * s, cy + 23 * s), size=(3 * s, 3 * s))
            elif kinds in ("apple", "banana"):
                if kinds == "apple":
                    Color(red)
                    Ellipse(pos=(cx - 24 * s, cy - 23 * s), size=(30 * s, 37 * s))
                    Ellipse(pos=(cx - 6 * s, cy - 23 * s), size=(30 * s, 37 * s))
                    Triangle(points=(cx - 24 * s, cy - 3 * s, cx + 24 * s, cy - 3 * s,
                                     cx, cy - 34 * s))
                    Color(green)
                    Ellipse(pos=(cx + 1 * s, cy + 10 * s), size=(19 * s, 9 * s))
                    Color(brown)
                    Line(points=(cx, cy + 11 * s, cx + 1 * s, cy + 20 * s),
                         width=3 * s)
                else:
                    Color(yellow)
                    Line(points=(cx - 23 * s, cy + 24 * s, cx - 14 * s, cy + 2 * s,
                                 cx + 8 * s, cy - 14 * s, cx + 24 * s, cy - 30 * s),
                         width=17 * s, joint="round", cap="round")
                    Color((0.87, 0.76, 0.22, 1))
                    Line(points=(cx - 18 * s, cy + 20 * s, cx - 10 * s, cy + 1 * s,
                                 cx + 10 * s, cy - 14 * s), width=2 * s)
                    Color(green)
                    Ellipse(pos=(cx - 12 * s, cy + 22 * s), size=(19 * s, 8 * s))
            elif kinds.startswith("route_") or kinds.startswith("town_"):
                Color((0.40, 0.70, 0.40, 1))
                Rectangle(pos=(cx - 38 * s, cy - 31 * s), size=(76 * s, 62 * s))
                Color((0.83, 0.78, 0.64, 1))
                Line(points=(cx - 38 * s, cy - 12 * s, cx + 38 * s, cy - 12 * s),
                     width=10 * s)
                Color((0.94, 0.82, 0.54, 1))
                for bx in (-27, 18):
                    Rectangle(pos=(cx + bx * s, cy + 1 * s), size=(19 * s, 20 * s))
                    Triangle(points=(cx + (bx - 3) * s, cy + 21 * s,
                                     cx + (bx + 22) * s, cy + 21 * s,
                                     cx + (bx + 9) * s, cy + 34 * s))
                Color(red if kinds.endswith("unsafe") else blue)
                Ellipse(pos=(cx - 5 * s, cy - 10 * s), size=(10 * s, 10 * s))
            elif kinds in ("library", "bakery", "bus_stop", "school", "cosy_home",
                           "busy_road"):
                Color((0.59, 0.76, 0.84, 1) if kinds != "bakery" else
                      (0.95, 0.69, 0.48, 1))
                Rectangle(pos=(cx - 27 * s, cy - 28 * s), size=(54 * s, 51 * s))
                Color((0.53, 0.32, 0.22, 1))
                Triangle(points=(cx - 34 * s, cy + 22 * s, cx + 34 * s, cy + 22 * s,
                                 cx, cy + 39 * s))
                Color((0.96, 0.91, 0.75, 1))
                Rectangle(pos=(cx - 7 * s, cy - 28 * s), size=(14 * s, 26 * s))
                Color(blue)
                for dx in (-18, 11):
                    Rectangle(pos=(cx + dx * s, cy - 1 * s), size=(11 * s, 12 * s))
                if kinds == "busy_road":
                    Color(dark)
                    Rectangle(pos=(cx - 40 * s, cy - 37 * s), size=(80 * s, 8 * s))
                    Color(yellow)
                    for dx in (-25, -5, 15):
                        Rectangle(pos=(cx + dx * s, cy - 34 * s), size=(12 * s, 2 * s))
            elif kinds == "child_tree":
                Color(brown)
                Rectangle(pos=(cx + 16 * s, cy - 30 * s), size=(9 * s, 43 * s))
                Color(green)
                for dx, dy in ((0, 19), (-14, 7), (14, 8)):
                    Ellipse(pos=(cx + (dx + 20) * s, cy + (dy - 14) * s),
                            size=(28 * s, 25 * s))
                Color((0.82, 0.55, 0.37, 1))
                Ellipse(pos=(cx - 27 * s, cy + 7 * s), size=(18 * s, 19 * s))
                Color(red)
                RoundedRectangle(pos=(cx - 28 * s, cy - 18 * s),
                                 size=(20 * s, 28 * s), radius=[(6 * s, 6 * s)])
                Color(dark)
                Line(points=(cx - 24 * s, cy - 17 * s, cx - 27 * s, cy - 34 * s),
                     width=3 * s)
                Line(points=(cx - 12 * s, cy - 17 * s, cx - 9 * s, cy - 34 * s),
                     width=3 * s)
            elif kinds in ("blue", "soft"):
                if kinds == "blue":
                    Color(0.18, 0.47, 0.88, 1)
                    RoundedRectangle(pos=(cx - 25 * s, cy - 25 * s),
                                     size=(50 * s, 50 * s), radius=[(8 * s, 8 * s)])
                    Color(0.68, 0.83, 0.98, 1)
                    Ellipse(pos=(cx - 15 * s, cy + 4 * s), size=(13 * s, 9 * s))
                else:
                    Color((0.88, 0.67, 0.48, 1))
                    RoundedRectangle(pos=(cx - 28 * s, cy - 22 * s),
                                     size=(56 * s, 42 * s), radius=[(15 * s, 15 * s)])
                    Color(0.98, 0.94, 0.82, 1)
                    Line(points=(cx - 17 * s, cy + 4 * s, cx + 17 * s, cy + 4 * s),
                         width=2 * s)
            elif kinds in ("bell", "anklet_bell"):
                Color(yellow)
                Ellipse(pos=(cx - 18 * s, cy - 13 * s), size=(36 * s, 40 * s))
                Color(brown)
                Rectangle(pos=(cx - 18 * s, cy + 12 * s), size=(36 * s, 5 * s))
                Line(points=(cx, cy - 13 * s, cx, cy - 23 * s), width=3 * s)
                Ellipse(pos=(cx - 4 * s, cy - 28 * s), size=(8 * s, 8 * s))
                if kinds == "anklet_bell":
                    Color((0.83, 0.83, 0.88, 1))
                    Line(circle=(cx, cy - 4 * s, 34 * s), width=5 * s)
                    for angle in (30, 90, 150, 210, 270, 330):
                        theta = radians(angle)
                        Ellipse(pos=(cx + cos(theta) * 34 * s - 4 * s,
                                     cy - 4 * s + sin(theta) * 34 * s - 4 * s),
                                size=(8 * s, 8 * s))
            elif kinds in ("eye", "tongue"):
                if kinds == "eye":
                    Color(1, 1, 1, 1)
                    Ellipse(pos=(cx - 33 * s, cy - 17 * s), size=(66 * s, 34 * s))
                    Color(blue)
                    Ellipse(pos=(cx - 14 * s, cy - 14 * s), size=(28 * s, 28 * s))
                    Color(dark)
                    Ellipse(pos=(cx - 7 * s, cy - 7 * s), size=(14 * s, 14 * s))
                    Color(1, 1, 1, 1)
                    Ellipse(pos=(cx - 4 * s, cy + 2 * s), size=(5 * s, 5 * s))
                else:
                    Color(red)
                    Ellipse(pos=(cx - 20 * s, cy - 20 * s), size=(40 * s, 40 * s))
                    Color((0.93, 0.50, 0.59, 1))
                    Ellipse(pos=(cx - 8 * s, cy - 25 * s), size=(16 * s, 29 * s))
                    Color(1, 1, 1, 1)
                    Line(points=(cx - 20 * s, cy + 4 * s, cx + 20 * s, cy + 4 * s),
                         width=3 * s)
            elif kinds in ("listening", "interrupting", "listen_turn",
                           "thank_you", "unkind_words", "silly_face", "teasing",
                           "sharing_blocks", "grabbing_blocks", "pattern_red_blue",
                           "pattern_mixed", "purple_jojo", "green_jojo",
                           "orange_jojo", "mouse_help", "mouse_ignore", "game_fair",
                           "game_unfair", "trusted_adult", "online_stranger"):
                if kinds in ("pattern_red_blue", "pattern_mixed"):
                    colors = (red, blue, red, blue) if kinds.endswith("red_blue") else (
                        red, blue, blue, red)
                    for index, paint in enumerate(colors):
                        Color(paint)
                        RoundedRectangle(pos=(cx - 34 * s + index * 18 * s,
                                              cy - 15 * s),
                                         size=(16 * s, 30 * s), radius=[(4 * s, 4 * s)])
                elif kinds in ("sharing_blocks", "grabbing_blocks"):
                    for index, paint in enumerate((red, blue, yellow, green)):
                        Color(paint)
                        Rectangle(pos=(cx - 23 * s + index * 13 * s,
                                       cy - 12 * s + (index % 2) * 12 * s),
                                  size=(15 * s, 15 * s))
                    if kinds == "grabbing_blocks":
                        Color(red)
                        Line(points=(cx - 32 * s, cy - 31 * s, cx + 32 * s, cy + 31 * s),
                             width=4 * s)
                elif kinds in ("purple_jojo", "green_jojo", "orange_jojo"):
                    Color((0.55, 0.30, 0.74, 1) if kinds.startswith("purple") else
                          green if kinds.startswith("green") else (0.95, 0.52, 0.17, 1))
                    Ellipse(pos=(cx - 22 * s, cy - 24 * s), size=(44 * s, 48 * s))
                    Color(1, 1, 1, 1)
                    Ellipse(pos=(cx - 12 * s, cy + 3 * s), size=(8 * s, 9 * s))
                    Ellipse(pos=(cx + 4 * s, cy + 3 * s), size=(8 * s, 9 * s))
                    Color(dark)
                    Ellipse(pos=(cx - 9 * s, cy + 6 * s), size=(3 * s, 4 * s))
                    Ellipse(pos=(cx + 7 * s, cy + 6 * s), size=(3 * s, 4 * s))
                    Color(red)
                    Line(points=(cx - 8 * s, cy - 9 * s, cx, cy - 13 * s,
                                 cx + 8 * s, cy - 9 * s), width=2 * s)
                elif kinds in ("mouse_help", "mouse_ignore"):
                    Color((0.62, 0.61, 0.60, 1))
                    Ellipse(pos=(cx - 20 * s, cy - 10 * s), size=(40 * s, 28 * s))
                    Ellipse(pos=(cx + 8 * s, cy + 3 * s), size=(22 * s, 21 * s))
                    Ellipse(pos=(cx + 5 * s, cy + 19 * s), size=(12 * s, 13 * s))
                    Ellipse(pos=(cx + 21 * s, cy + 19 * s), size=(12 * s, 13 * s))
                    Color(dark)
                    Ellipse(pos=(cx + 22 * s, cy + 11 * s), size=(4 * s, 4 * s))
                    Line(points=(cx - 18 * s, cy - 8 * s, cx - 31 * s, cy - 1 * s,
                                 cx - 34 * s, cy + 13 * s), width=2 * s)
                    if kinds == "mouse_help":
                        Color(brown)
                        Line(points=(cx - 24 * s, cy - 15 * s, cx + 24 * s, cy - 15 * s),
                             width=2 * s)
                        Line(points=(cx - 15 * s, cy - 22 * s, cx + 16 * s, cy - 22 * s),
                             width=2 * s)
                    else:
                        Color(red)
                        Line(points=(cx - 30 * s, cy - 30 * s, cx + 30 * s, cy + 30 * s),
                             width=4 * s)
                elif kinds in ("game_fair", "game_unfair"):
                    Color(green)
                    Rectangle(pos=(cx - 37 * s, cy - 29 * s), size=(74 * s, 58 * s))
                    Color(yellow)
                    Ellipse(pos=(cx - 29 * s, cy - 14 * s), size=(20 * s, 20 * s))
                    Ellipse(pos=(cx + 10 * s, cy - 14 * s), size=(20 * s, 20 * s))
                    Color(blue)
                    Line(points=(cx, cy - 25 * s, cx, cy + 25 * s), width=2 * s)
                    if kinds == "game_unfair":
                        Color(red)
                        Line(points=(cx - 32 * s, cy - 31 * s, cx + 32 * s, cy + 31 * s),
                             width=4 * s)
                elif kinds in ("trusted_adult", "online_stranger"):
                    Color((0.78, 0.52, 0.36, 1) if kinds == "trusted_adult" else dark)
                    Ellipse(pos=(cx - 11 * s, cy + 13 * s), size=(22 * s, 24 * s))
                    Color(green if kinds == "trusted_adult" else dark)
                    RoundedRectangle(pos=(cx - 18 * s, cy - 22 * s),
                                     size=(36 * s, 38 * s), radius=[(9 * s, 9 * s)])
                    if kinds == "online_stranger":
                        Color(red)
                        Triangle(points=(cx + 20 * s, cy + 31 * s, cx + 39 * s,
                                         cy - 4 * s, cx + 1 * s, cy - 4 * s))
                        Color(1, 1, 1, 1)
                        Line(points=(cx + 20 * s, cy + 17 * s, cx + 20 * s, cy + 4 * s),
                             width=3 * s)
                        Ellipse(pos=(cx + 18 * s, cy - 1 * s), size=(4 * s, 4 * s))
                else:
                    Color((0.82, 0.55, 0.37, 1))
                    Ellipse(pos=(cx - 12 * s, cy + 12 * s), size=(24 * s, 24 * s))
                    Color(blue)
                    RoundedRectangle(pos=(cx - 19 * s, cy - 23 * s),
                                     size=(38 * s, 39 * s), radius=[(9 * s, 9 * s)])
                    Color(dark)
                    Line(points=(cx - 8 * s, cy + 8 * s, cx - 13 * s, cy - 6 * s),
                         width=3 * s)
                    Line(points=(cx + 8 * s, cy + 8 * s, cx + 13 * s, cy - 6 * s),
                         width=3 * s)
                    Color(yellow if kinds in ("thank_you", "listening", "listen_turn")
                          else red)
                    RoundedRectangle(pos=(cx + 13 * s, cy + 14 * s),
                                     size=(24 * s, 17 * s), radius=[(5 * s, 5 * s)])
                    if kinds in ("interrupting", "unkind_words", "teasing"):
                        Color(red)
                        Line(points=(cx - 33 * s, cy - 30 * s, cx + 33 * s, cy + 30 * s),
                             width=4 * s)
                    if kinds == "silly_face":
                        Color(dark)
                        Ellipse(pos=(cx - 6 * s, cy + 22 * s), size=(4 * s, 4 * s))
                        Ellipse(pos=(cx + 4 * s, cy + 22 * s), size=(4 * s, 4 * s))
                        Color(red)
                        Line(points=(cx - 8 * s, cy + 13 * s, cx, cy + 8 * s,
                                     cx + 8 * s, cy + 13 * s), width=2 * s)
            elif kinds in ("moon_sky_reflection", "moon_under_water"):
                Color((0.16, 0.29, 0.48, 1))
                Rectangle(pos=(cx - 39 * s, cy - 30 * s), size=(78 * s, 60 * s))
                Color((0.21, 0.56, 0.77, 1))
                Rectangle(pos=(cx - 39 * s, cy - 30 * s), size=(78 * s, 26 * s))
                Color(yellow)
                Ellipse(pos=(cx + 11 * s, cy + 8 * s), size=(21 * s, 21 * s))
                Color((0.95, 0.95, 0.87, 1))
                Ellipse(pos=(cx + 17 * s, cy + 12 * s), size=(21 * s, 21 * s))
                Color(yellow)
                Ellipse(pos=(cx + 11 * s, cy + 8 * s), size=(21 * s, 21 * s))
                Color((0.78, 0.86, 0.91, 1))
                Line(points=(cx - 26 * s, cy - 6 * s, cx + 30 * s, cy - 6 * s),
                     width=2 * s)
                if kinds.endswith("under_water"):
                    Color(red)
                    Line(points=(cx - 30 * s, cy + 27 * s, cx + 30 * s, cy - 27 * s),
                         width=4 * s)
            elif kinds in ("umbrella_large", "umbrella_small"):
                scale = 1 if kinds.endswith("large") else 0.62
                Color(red if kinds.endswith("large") else blue)
                Ellipse(pos=(cx - 36 * scale * s, cy - 2 * s),
                        size=(72 * scale * s, 47 * scale * s),
                        angle_start=0, angle_end=180)
                Line(points=(cx - 36 * scale * s, cy - 2 * s,
                             cx, cy - 2 * s, cx + 36 * scale * s, cy - 2 * s),
                     width=3 * s)
                Color(brown)
                Line(points=(cx, cy - 2 * s, cx, cy - 34 * scale * s,
                             cx + 9 * scale * s, cy - 34 * scale * s),
                     width=4 * s, joint="round")
                for child_x in (-14, 0, 14):
                    Color((0.82, 0.55, 0.37, 1))
                    Ellipse(pos=(cx + child_x * scale * s - 5 * s,
                                 cy - 29 * s), size=(10 * s, 10 * s))
                    Color(green)
                    Line(points=(cx + child_x * scale * s, cy - 19 * s,
                                 cx + child_x * scale * s, cy - 34 * s), width=3 * s)
            elif kinds in ("rain_cloud", "sandwich_cloud", "shoe_cloud"):
                Color((0.64, 0.73, 0.82, 1))
                for dx, dy, radius in ((-15, 0, 17), (0, 9, 22), (17, 0, 17)):
                    Ellipse(pos=(cx + (dx - radius) * s, cy + (dy - radius) * s),
                            size=(2 * radius * s, 2 * radius * s))
                if kinds == "rain_cloud":
                    Color(blue)
                    for dx in (-20, 0, 20):
                        Line(points=(cx + dx * s, cy - 17 * s,
                                     cx + (dx - 4) * s, cy - 27 * s), width=4 * s)
                elif kinds == "sandwich_cloud":
                    Color((0.84, 0.53, 0.25, 1))
                    Triangle(points=(cx - 21 * s, cy - 17 * s, cx + 21 * s,
                                     cy - 17 * s, cx, cy - 36 * s))
                    Color(green)
                    Line(points=(cx - 15 * s, cy - 23 * s, cx + 15 * s, cy - 23 * s),
                         width=4 * s)
                else:
                    Color(brown)
                    Ellipse(pos=(cx - 22 * s, cy - 27 * s), size=(35 * s, 13 * s))
                    RoundedRectangle(pos=(cx - 13 * s, cy - 16 * s),
                                     size=(24 * s, 22 * s), radius=[(8 * s, 8 * s)])
            elif kinds in ("cat_rain", "hen_rain"):
                if kinds == "cat_rain":
                    Color((0.58, 0.58, 0.62, 1))
                    Ellipse(pos=(cx - 22 * s, cy - 15 * s), size=(43 * s, 31 * s))
                    Ellipse(pos=(cx + 7 * s, cy + 1 * s), size=(21 * s, 21 * s))
                    Triangle(points=(cx + 7 * s, cy + 16 * s, cx + 9 * s,
                                     cy + 32 * s, cx + 20 * s, cy + 17 * s))
                    Triangle(points=(cx + 18 * s, cy + 16 * s, cx + 27 * s,
                                     cy + 32 * s, cx + 30 * s, cy + 8 * s))
                    Color(dark)
                    for leg_x in (-15, 0, 18, 25):
                        Line(points=(cx + leg_x * s, cy - 10 * s,
                                     cx + leg_x * s, cy - 28 * s), width=3 * s)
                    Line(points=(cx - 18 * s, cy - 2 * s, cx - 32 * s,
                                 cy + 7 * s, cx - 35 * s, cy + 16 * s), width=3 * s)
                else:
                    Color((0.87, 0.50, 0.20, 1))
                    Ellipse(pos=(cx - 25 * s, cy - 13 * s), size=(43 * s, 30 * s))
                    Ellipse(pos=(cx + 7 * s, cy + 2 * s), size=(19 * s, 20 * s))
                    Color(red)
                    Ellipse(pos=(cx + 12 * s, cy + 19 * s), size=(7 * s, 8 * s))
                    Color(dark)
                    for leg_x in (-14, -3, 16, 24):
                        Line(points=(cx + leg_x * s, cy - 10 * s,
                                     cx + leg_x * s, cy - 28 * s), width=2 * s)
                Color(blue)
                for dx in (-23, 0, 24):
                    Line(points=(cx + dx * s, cy + 37 * s,
                                 cx + (dx - 4) * s, cy + 28 * s), width=2.5 * s)
            elif kinds.startswith("action_") or kinds.startswith("sense_"):
                Color(blue)
                Ellipse(pos=(cx - 12 * s, cy + 16 * s), size=(24 * s, 24 * s))
                Color(green)
                RoundedRectangle(pos=(cx - 14 * s, cy - 16 * s),
                                 size=(28 * s, 35 * s), radius=[(8 * s, 8 * s)])
                Color(dark)
                Line(points=(cx - 7 * s, cy - 14 * s, cx - 18 * s, cy - 32 * s),
                     width=5 * s)
                Line(points=(cx + 7 * s, cy - 14 * s, cx + 18 * s, cy - 32 * s),
                     width=5 * s)
                if kinds.endswith("jumping"):
                    Line(points=(cx - 12 * s, cy + 3 * s, cx - 30 * s, cy + 23 * s,
                                 cx - 38 * s, cy + 16 * s), width=4 * s)
                    Line(points=(cx + 12 * s, cy + 3 * s, cx + 30 * s, cy + 23 * s,
                                 cx + 38 * s, cy + 16 * s), width=4 * s)
            elif kinds.startswith("name_") or kinds.startswith("farewell_") or kinds.startswith("greeting_"):
                Color((0.98, 0.91, 0.67, 1))
                RoundedRectangle(pos=(cx - 34 * s, cy - 22 * s),
                                 size=(68 * s, 44 * s), radius=[(6 * s, 6 * s)])
                Color(blue if kinds.endswith("kind") or kinds.endswith("card") else red)
                Line(points=(cx - 20 * s, cy + 7 * s, cx + 20 * s, cy + 7 * s),
                     width=4 * s)
                Line(points=(cx - 20 * s, cy - 5 * s, cx + 11 * s, cy - 5 * s),
                     width=3 * s)
                Line(points=(cx - 20 * s, cy - 14 * s, cx + 2 * s, cy - 14 * s),
                     width=3 * s)
            elif kinds.startswith("story_order_") or kinds.startswith("dream_order_"):
                for index in range(3):
                    x0 = cx - 29 * s + index * 29 * s
                    Color((0.93, 0.73, 0.37, 1) if index == 0 else
                          (0.55, 0.72, 0.87, 1) if index == 1 else
                          (0.53, 0.74, 0.52, 1))
                    RoundedRectangle(pos=(x0, cy - 16 * s), size=(24 * s, 32 * s),
                                     radius=[(4 * s, 4 * s)])
                    Color(1, 1, 1, 1)
                    Ellipse(pos=(x0 + 8 * s, cy + 2 * s), size=(8 * s, 8 * s))
                    Line(points=(x0 + 6 * s, cy - 6 * s, x0 + 18 * s, cy - 6 * s),
                         width=1.5 * s)
                if kinds.endswith("bad"):
                    Color(red)
                    Line(points=(cx - 30 * s, cy - 27 * s, cx + 30 * s, cy + 27 * s),
                         width=4 * s)
            elif kinds.startswith("cloud_"):
                Color((0.78, 0.85, 0.91, 1))
                for dx, dy, radius in ((-15, 0, 17), (0, 9, 22), (17, 0, 17)):
                    Ellipse(pos=(cx + (dx - radius) * s, cy + (dy - radius) * s),
                            size=(2 * radius * s, 2 * radius * s))
                if kinds.endswith("sheep"):
                    Color(1, 1, 1, 1)
                    Ellipse(pos=(cx - 17 * s, cy - 13 * s), size=(34 * s, 20 * s))
                    Ellipse(pos=(cx + 11 * s, cy - 7 * s), size=(14 * s, 14 * s))
                elif kinds.endswith("chair"):
                    Color(brown)
                    Rectangle(pos=(cx - 12 * s, cy - 24 * s), size=(25 * s, 5 * s))
                    Rectangle(pos=(cx - 10 * s, cy - 19 * s), size=(5 * s, 23 * s))
                    Rectangle(pos=(cx + 8 * s, cy - 19 * s), size=(5 * s, 23 * s))
                    Rectangle(pos=(cx - 10 * s, cy + 4 * s), size=(5 * s, 18 * s))
            elif kinds.startswith("town_") or kinds in ("library", "bakery", "bus_stop"):
                Color(blue if "library" in kinds else red if "bakery" in kinds else yellow)
                Rectangle(pos=(cx - 25 * s, cy - 27 * s), size=(50 * s, 43 * s))
                Color(brown)
                Triangle(points=(cx - 31 * s, cy + 16 * s, cx + 31 * s, cy + 16 * s,
                                 cx, cy + 36 * s))
                Color(1, 1, 1, 1)
                Rectangle(pos=(cx - 7 * s, cy - 27 * s), size=(14 * s, 25 * s))
                for dx in (-17, 13):
                    Rectangle(pos=(cx + dx * s, cy - 4 * s), size=(8 * s, 10 * s))
            elif kinds.startswith("safe_step") or kinds.startswith("wobbly_stack"):
                Color(brown)
                for index in range(3):
                    x0 = cx - 30 * s + index * 10 * s if kinds.startswith("safe") else cx - (index + 1) * 14 * s
                    y0 = cy - 28 * s + index * 16 * s
                    Color(blue if index % 2 else yellow)
                    RoundedRectangle(pos=(x0, y0), size=(28 * s, 14 * s),
                                     radius=[(2 * s, 2 * s)])
                if kinds.startswith("wobbly"):
                    Color(red)
                    Line(points=(cx - 31 * s, cy - 31 * s, cx + 31 * s, cy + 31 * s),
                         width=4 * s)
            elif kinds.startswith("ant_"):
                Color(dark)
                for ax in (-11, 0, 11):
                    Ellipse(pos=(cx + ax * s - 6 * s, cy - 4 * s), size=(12 * s, 10 * s))
                for leg_x in (-9, 0, 9):
                    Line(points=(cx + leg_x * s, cy - 2 * s,
                                 cx + (leg_x - 8) * s, cy - 14 * s), width=2 * s)
                    Line(points=(cx + leg_x * s, cy - 2 * s,
                                 cx + (leg_x + 8) * s, cy - 14 * s), width=2 * s)
                Line(points=(cx + 17 * s, cy + 3 * s, cx + 24 * s,
                             cy + 14 * s, cx + 29 * s, cy + 3 * s), width=2 * s)
                if kinds.endswith("poke"):
                    Color(red)
                    Line(points=(cx - 31 * s, cy + 26 * s, cx - 10 * s, cy + 5 * s),
                         width=5 * s)
            elif kinds.startswith("pond_"):
                Color((0.41, 0.68, 0.85, 1))
                Ellipse(pos=(cx - 37 * s, cy - 21 * s), size=(74 * s, 40 * s))
                Color((0.74, 0.56, 0.34, 1))
                Line(ellipse=(cx - 37 * s, cy - 21 * s, 74 * s, 40 * s), width=4 * s)
                if kinds.endswith("bin"):
                    Color(green)
                    Rectangle(pos=(cx + 18 * s, cy - 28 * s), size=(18 * s, 26 * s))
                    Line(points=(cx + 16 * s, cy - 1 * s, cx + 38 * s, cy - 1 * s),
                         width=3 * s)
                else:
                    Color(red)
                    Ellipse(pos=(cx - 5 * s, cy + 4 * s), size=(13 * s, 8 * s))
                    Color(yellow)
                    Ellipse(pos=(cx + 15 * s, cy - 3 * s), size=(11 * s, 8 * s))
            elif kinds.startswith("seed_") or kinds in ("radish_below", "radish_tree"):
                Color((0.56, 0.34, 0.20, 1))
                Rectangle(pos=(cx - 36 * s, cy - 30 * s), size=(72 * s, 20 * s))
                Color((0.72, 0.52, 0.35, 1))
                for ridge in range(4):
                    Line(points=(cx - 35 * s, cy - 25 * s + ridge * 4 * s,
                                 cx + 35 * s, cy - 25 * s + ridge * 4 * s),
                         width=1 * s)
                if kinds.startswith("seed"):
                    Color((0.86, 0.65, 0.31, 1))
                    Ellipse(pos=(cx - 7 * s, cy - 4 * s), size=(14 * s, 9 * s))
                    if kinds.endswith("water"):
                        Color(blue)
                        for dx in (-12, 0, 12):
                            Ellipse(pos=(cx + dx * s, cy + 5 * s), size=(5 * s, 9 * s))
                        Color(green)
                        Line(points=(cx, cy - 3 * s, cx, cy + 22 * s,
                                     cx - 13 * s, cy + 31 * s), width=4 * s)
                    else:
                        Color(red)
                        RoundedRectangle(pos=(cx - 23 * s, cy + 5 * s),
                                         size=(46 * s, 23 * s), radius=[(4 * s, 4 * s)])
                elif kinds.endswith("below"):
                    Color(red)
                    Triangle(points=(cx - 9 * s, cy - 8 * s, cx + 9 * s, cy - 8 * s,
                                     cx, cy - 32 * s))
                    Color(green)
                    Line(points=(cx, cy - 8 * s, cx, cy + 28 * s,
                                 cx - 14 * s, cy + 35 * s), width=4 * s)
                else:
                    Color(green)
                    Line(points=(cx, cy - 8 * s, cx, cy + 31 * s), width=4 * s)
                    Ellipse(pos=(cx - 22 * s, cy + 13 * s), size=(24 * s, 19 * s))
                    Ellipse(pos=(cx - 4 * s, cy + 19 * s), size=(26 * s, 18 * s))
            elif kinds.startswith("farm_to_meal") or kinds.startswith("meal_to_farm"):
                Color(green)
                Rectangle(pos=(cx - 37 * s, cy - 25 * s), size=(23 * s, 34 * s))
                for row in range(3):
                    Line(points=(cx - 35 * s, cy - 19 * s + row * 9 * s,
                                 cx - 16 * s, cy - 19 * s + row * 9 * s),
                         width=2 * s)
                Color(yellow)
                Triangle(points=(cx - 9 * s, cy, cx - 1 * s, cy + 6 * s,
                                 cx - 9 * s, cy + 12 * s))
                Color((0.96, 0.88, 0.70, 1))
                Ellipse(pos=(cx + 7 * s, cy - 23 * s), size=(35 * s, 23 * s))
                Color(red)
                Ellipse(pos=(cx + 15 * s, cy - 16 * s), size=(11 * s, 8 * s))
                Color(green)
                Ellipse(pos=(cx + 29 * s, cy - 14 * s), size=(8 * s, 9 * s))
                if kinds.endswith("meal_to_farm"):
                    Color(red)
                    Line(points=(cx - 35 * s, cy + 30 * s, cx + 35 * s, cy - 30 * s),
                         width=4 * s)
            elif kinds.startswith("frog_"):
                Color(green if kinds.endswith("frog") or kinds.endswith("rain") else brown)
                if "frog" in kinds:
                    Ellipse(pos=(cx - 22 * s, cy - 15 * s), size=(44 * s, 29 * s))
                    for dx in (-14, 14):
                        Ellipse(pos=(cx + dx * s - 9 * s, cy + 7 * s), size=(18 * s, 18 * s))
                        Color(1, 1, 1, 1)
                        Ellipse(pos=(cx + dx * s - 3 * s, cy + 15 * s), size=(7 * s, 7 * s))
                    Color(dark)
                    Line(points=(cx - 11 * s, cy - 2 * s, cx, cy - 6 * s,
                                 cx + 11 * s, cy - 2 * s), width=2 * s)
                    Color(green)
                    Line(points=(cx - 14 * s, cy - 12 * s, cx - 29 * s, cy - 26 * s,
                                 cx - 5 * s, cy - 16 * s), width=5 * s)
                    Line(points=(cx + 14 * s, cy - 12 * s, cx + 29 * s, cy - 26 * s,
                                 cx + 5 * s, cy - 16 * s), width=5 * s)
                else:
                    Ellipse(pos=(cx - 23 * s, cy - 7 * s), size=(42 * s, 20 * s))
                    Ellipse(pos=(cx + 8 * s, cy + 2 * s), size=(19 * s, 18 * s))
                    Color(yellow)
                    Triangle(points=(cx + 26 * s, cy + 7 * s, cx + 35 * s, cy + 3 * s,
                                     cx + 26 * s, cy))
            elif kinds.startswith("direction_"):
                Color(blue)
                Line(points=(cx, cy - 27 * s, cx, cy + 27 * s,
                             cx - 22 * s, cy + 5 * s, cx, cy + 27 * s,
                             cx + 22 * s, cy + 5 * s), width=4 * s, joint="round")
                Color(red if kinds.endswith("left") else green if kinds.endswith("right")
                      else yellow)
                Ellipse(pos=(cx - 8 * s, cy - 8 * s), size=(16 * s, 16 * s))
            elif kinds.startswith("mangoes_"):
                amount = int(kinds.rsplit("_", 1)[1])
                Color(0.70, 0.41, 0.15, 1)
                RoundedRectangle(pos=(cx - 39 * s, cy - 33 * s),
                                 size=(78 * s, 12 * s), radius=[(4 * s, 4 * s)])
                for i in range(4):
                    Rectangle(pos=(cx - 33 * s + i * 22 * s, cy - 39 * s),
                              size=(5 * s, 19 * s))
                for index in range(amount):
                    row, column = divmod(index, 4)
                    fx = cx - 27 * s + column * 18 * s + (row % 2) * 5 * s
                    fy = cy - 18 * s + row * 21 * s
                    Color(yellow if index % 2 else (0.94, 0.57, 0.16, 1))
                    Ellipse(pos=(fx - 7 * s, fy - 9 * s), size=(14 * s, 18 * s))
                    Color(green)
                    Ellipse(pos=(fx + 2 * s, fy + 6 * s), size=(7 * s, 4 * s))
                    Color(brown)
                    Line(points=(fx, fy + 7 * s, fx + 2 * s, fy + 10 * s),
                         width=1.5 * s)
            elif kinds.startswith("birds_"):
                amount = int(kinds.rsplit("_", 1)[1])
                for index in range(amount):
                    row, column = divmod(index, 5)
                    bx = cx - 38 * s + column * 19 * s
                    by = cy - 25 * s + row * 22 * s
                    Color(yellow if index % 2 else (0.42, 0.63, 0.86, 1))
                    Ellipse(pos=(bx - 6 * s, by - 3 * s), size=(13 * s, 9 * s))
                    Ellipse(pos=(bx + 3 * s, by + 1 * s), size=(7 * s, 7 * s))
                    Color(dark)
                    Ellipse(pos=(bx + 7 * s, by + 4 * s), size=(1.6 * s, 1.6 * s))
                    Color(yellow)
                    Triangle(points=(bx + 9 * s, by + 4 * s, bx + 14 * s, by + 2 * s,
                                     bx + 9 * s, by + 1 * s))
                    Color(brown)
                    Line(points=(bx - 1 * s, by - 3 * s, bx - 2 * s, by - 8 * s),
                         width=1 * s)
            elif kinds.startswith("vegetables_"):
                amount = int(kinds.rsplit("_", 1)[1])
                for index in range(amount):
                    row, column = divmod(index, 5)
                    vx = cx - 34 * s + column * 17 * s
                    vy = cy - 25 * s + row * 19 * s
                    Color(green if index % 2 else (0.94, 0.48, 0.28, 1))
                    Ellipse(pos=(vx - 5 * s, vy - 7 * s), size=(11 * s, 16 * s))
                    Color(green)
                    Line(points=(vx, vy + 6 * s, vx - 3 * s, vy + 12 * s),
                         width=1.5 * s)
                    Ellipse(pos=(vx - 8 * s, vy + 5 * s), size=(8 * s, 4 * s))
            elif kinds.startswith("counters_"):
                groups = [int(value) for value in kinds.split("_")[1:]]
                for group_index, amount in enumerate(groups):
                    gx = cx + (-23 if group_index == 0 else 23) * s
                    Color((0.37, 0.61, 0.84, 1) if group_index == 0
                          else (0.93, 0.57, 0.23, 1))
                    for index in range(amount):
                        column, row = index % 3, index // 3
                        Ellipse(pos=(gx + (column - 1) * 13 * s - 4 * s,
                                     cy + (row - 1) * 13 * s - 4 * s),
                                size=(8 * s, 8 * s))
                    Color(dark)
                    Line(points=(gx - 19 * s, cy - 31 * s, gx + 19 * s, cy - 31 * s),
                         width=1.5 * s)
            elif kinds.startswith("coins_"):
                values = [int(value) for value in re.findall(r"\d+", kinds)]
                for group_index, amount in enumerate(values):
                    x0 = cx - 20 * s + group_index * 41 * s
                    for index in range(amount):
                        row = index // 2
                        column = index % 2
                        Color(yellow if group_index == 0 else (0.78, 0.79, 0.82, 1))
                        Ellipse(pos=(x0 + column * 13 * s - 6 * s,
                                     cy - 18 * s + row * 13 * s - 6 * s),
                                size=(13 * s, 13 * s))
                        Color(brown)
                        Line(ellipse=(x0 + column * 13 * s - 3 * s,
                                      cy - 15 * s + row * 13 * s - 3 * s,
                                      7 * s, 7 * s), width=1 * s)
            elif kinds.startswith("base_ten_"):
                number = int(kinds.rsplit("_", 1)[1])
                tens, ones = divmod(number, 10)
                for index in range(tens):
                    x0 = cx - 38 * s + index * 19 * s
                    Color((0.28, 0.57, 0.77, 1))
                    RoundedRectangle(pos=(x0, cy - 19 * s), size=(14 * s, 40 * s),
                                     radius=[(2 * s, 2 * s)])
                    Color(0.82, 0.91, 0.96, 1)
                    for row in range(1, 10):
                        Line(points=(x0 + 1 * s, cy - 19 * s + row * 4 * s,
                                     x0 + 13 * s, cy - 19 * s + row * 4 * s),
                             width=0.7 * s)
                for index in range(ones):
                    Color(yellow)
                    RoundedRectangle(pos=(cx - 31 * s + index * 9 * s,
                                          cy - 35 * s),
                                     size=(7 * s, 9 * s), radius=[(1 * s, 1 * s)])
            elif kinds.startswith("cups_buttons_"):
                amount = int(kinds.rsplit("_", 1)[1])
                remaining = amount
                for cup in range(3):
                    cup_x = cx - 31 * s + cup * 31 * s
                    Color(blue)
                    Line(points=(cup_x - 10 * s, cy - 4 * s, cup_x - 7 * s,
                                 cy - 30 * s, cup_x + 7 * s, cy - 30 * s,
                                 cup_x + 10 * s, cy - 4 * s),
                         close=True, width=2.5 * s)
                    button_count = min(2, remaining)
                    remaining -= button_count
                    for button in range(button_count):
                        Color(red if button else yellow)
                        Ellipse(pos=(cup_x - 4 * s + button * 7 * s,
                                     cy - 2 * s), size=(7 * s, 7 * s))
            elif kinds.startswith("pencil_"):
                length = 62 if kinds.endswith("10cm") else 38
                left = cx - length * s / 2
                right = cx + length * s / 2
                Color(yellow)
                Line(points=(left, cy, right - 9 * s, cy), width=13 * s, cap="square")
                Color(red)
                Line(points=(right - 9 * s, cy, right, cy), width=13 * s, cap="square")
                Color(brown)
                Triangle(points=(left, cy - 6 * s, left - 11 * s, cy,
                                 left, cy + 6 * s))
                Color(dark)
                Line(points=(left, cy - 14 * s, right, cy - 14 * s), width=1.5 * s)
                for tick in range(6):
                    tx = left + tick * (length / 5) * s
                    Line(points=(tx, cy - 12 * s, tx, cy - (18 if tick % 5 == 0 else 15) * s),
                         width=1 * s)
            elif kinds.startswith("book_"):
                spans = int(kinds.split("_")[1])
                book_length = spans * 13
                Color(red if spans == 4 else blue)
                RoundedRectangle(pos=(cx - book_length * s / 2, cy - 25 * s),
                                 size=(book_length * s, 50 * s),
                                 radius=[(4 * s, 4 * s)])
                Color(1, 1, 1, 1)
                Line(points=(cx, cy - 21 * s, cx, cy + 21 * s), width=2 * s)
                for line_y in (-12, 0, 12):
                    Line(points=(cx - book_length * s / 2 + 5 * s, cy + line_y * s,
                                 cx - 3 * s, cy + line_y * s), width=1 * s)
                    Line(points=(cx + 4 * s, cy + line_y * s,
                                 cx + book_length * s / 2 - 5 * s,
                                 cy + line_y * s), width=1 * s)
            elif kinds.startswith("toy_"):
                # A single toy is shown in a different position relative to furniture.
                Color(brown)
                if kinds.endswith("under_chair"):
                    Rectangle(pos=(cx - 28 * s, cy + 18 * s), size=(56 * s, 5 * s))
                    Rectangle(pos=(cx - 25 * s, cy - 30 * s), size=(5 * s, 50 * s))
                    Rectangle(pos=(cx + 20 * s, cy - 30 * s), size=(5 * s, 50 * s))
                    Rectangle(pos=(cx - 25 * s, cy + 23 * s), size=(5 * s, 22 * s))
                    Rectangle(pos=(cx + 20 * s, cy + 23 * s), size=(5 * s, 22 * s))
                    toy_y = cy - 15 * s
                elif kinds.endswith("inside_box"):
                    Line(points=(cx - 30 * s, cy - 20 * s, cx - 25 * s, cy + 17 * s,
                                 cx + 25 * s, cy + 17 * s, cx + 30 * s, cy - 20 * s),
                         close=True, width=3 * s)
                    toy_y = cy - 1 * s
                elif kinds.endswith("behind_chair"):
                    Color((0.72, 0.57, 0.39, 1))
                    Rectangle(pos=(cx - 28 * s, cy - 7 * s), size=(56 * s, 5 * s))
                    Rectangle(pos=(cx - 24 * s, cy - 32 * s), size=(5 * s, 27 * s))
                    Rectangle(pos=(cx + 19 * s, cy - 32 * s), size=(5 * s, 27 * s))
                    Rectangle(pos=(cx - 24 * s, cy - 2 * s), size=(5 * s, 35 * s))
                    Rectangle(pos=(cx + 19 * s, cy - 2 * s), size=(5 * s, 35 * s))
                    toy_y = cy - 17 * s
                elif kinds.endswith("in_cup"):
                    Color(blue)
                    Line(points=(cx - 25 * s, cy + 6 * s, cx - 19 * s, cy - 27 * s,
                                 cx + 19 * s, cy - 27 * s, cx + 25 * s, cy + 6 * s),
                         close=True, width=4 * s)
                    toy_y = cy - 1 * s
                else:
                    Rectangle(pos=(cx - 34 * s, cy - 2 * s), size=(68 * s, 6 * s))
                    Rectangle(pos=(cx - 28 * s, cy - 28 * s), size=(5 * s, 27 * s))
                    Rectangle(pos=(cx + 23 * s, cy - 28 * s), size=(5 * s, 27 * s))
                    toy_y = cy + 9 * s
                Color(red)
                Ellipse(pos=(cx - 10 * s, toy_y - 10 * s), size=(20 * s, 20 * s))
                Color(yellow)
                Ellipse(pos=(cx - 5 * s, toy_y - 4 * s), size=(5 * s, 5 * s))
            elif kinds.startswith("red_ball_") or kinds.startswith("blue_ball_"):
                ball_color = red if kinds.startswith("red") else blue
                Color(ball_color)
                Ellipse(pos=(cx - 30 * s, cy - 20 * s), size=(39 * s, 39 * s))
                Color(1, 1, 1, 0.8)
                Line(ellipse=(cx - 24 * s, cy - 14 * s, 27 * s, 27 * s), width=2 * s)
                Color(red if "red_cup" in kinds else blue)
                Line(points=(cx + 8 * s, cy + 10 * s, cx + 12 * s, cy - 20 * s,
                             cx + 36 * s, cy - 20 * s, cx + 40 * s, cy + 10 * s),
                     close=True, width=3 * s)
            elif kinds in ("bird", "hen", "horse", "cow", "fish", "snake"):
                if kinds == "horse":
                    Color(brown)
                    Ellipse(pos=(cx - 26 * s, cy - 8 * s), size=(48 * s, 27 * s))
                    Ellipse(pos=(cx + 7 * s, cy + 6 * s), size=(19 * s, 30 * s))
                    Ellipse(pos=(cx + 15 * s, cy + 19 * s), size=(21 * s, 15 * s))
                    Color(dark)
                    for leg_x in (-19, -5, 12, 24):
                        Line(points=(cx + leg_x * s, cy - 7 * s,
                                     cx + (leg_x - 2) * s, cy - 34 * s), width=4 * s)
                    Line(points=(cx - 23 * s, cy + 5 * s, cx - 34 * s,
                                 cy + 21 * s, cx - 29 * s, cy + 25 * s),
                         width=4 * s, joint="round")
                    Color((0.15, 0.12, 0.11, 1))
                    Line(points=(cx + 9 * s, cy + 20 * s, cx + 3 * s, cy + 8 * s,
                                 cx + 13 * s, cy - 1 * s), width=5 * s)
                    Color(1, 1, 1, 1)
                    Ellipse(pos=(cx + 26 * s, cy + 25 * s), size=(4 * s, 4 * s))
                    Color(dark)
                    Ellipse(pos=(cx + 27 * s, cy + 26 * s), size=(2 * s, 2 * s))
                elif kinds == "cow":
                    Color(0.94, 0.91, 0.82, 1)
                    Ellipse(pos=(cx - 28 * s, cy - 12 * s), size=(54 * s, 32 * s))
                    Ellipse(pos=(cx + 12 * s, cy + 3 * s), size=(20 * s, 25 * s))
                    Color(dark)
                    Ellipse(pos=(cx - 14 * s, cy - 3 * s), size=(13 * s, 12 * s))
                    Ellipse(pos=(cx + 4 * s, cy - 2 * s), size=(10 * s, 12 * s))
                    for leg_x in (-19, -5, 14, 25):
                        Line(points=(cx + leg_x * s, cy - 10 * s,
                                     cx + leg_x * s, cy - 34 * s), width=4 * s)
                    Color(red)
                    Ellipse(pos=(cx + 18 * s, cy + 4 * s), size=(13 * s, 8 * s))
                    Color(dark)
                    Line(points=(cx - 25 * s, cy + 3 * s, cx - 34 * s,
                                 cy - 10 * s), width=3 * s)
                elif kinds == "hen":
                    Color((0.87, 0.50, 0.20, 1))
                    Ellipse(pos=(cx - 25 * s, cy - 13 * s), size=(43 * s, 30 * s))
                    Ellipse(pos=(cx + 7 * s, cy + 2 * s), size=(19 * s, 20 * s))
                    Color(red)
                    Ellipse(pos=(cx + 12 * s, cy + 19 * s), size=(7 * s, 8 * s))
                    Color(yellow)
                    Triangle(points=(cx + 23 * s, cy + 10 * s, cx + 34 * s, cy + 6 * s,
                                     cx + 23 * s, cy + 2 * s))
                    Color(dark)
                    Ellipse(pos=(cx + 19 * s, cy + 14 * s), size=(3 * s, 3 * s))
                    Line(points=(cx - 5 * s, cy - 11 * s, cx - 7 * s,
                                 cy - 28 * s), width=2 * s)
                    Line(points=(cx + 8 * s, cy - 11 * s, cx + 10 * s,
                                 cy - 28 * s), width=2 * s)
                elif kinds == "fish":
                    Color(blue)
                    Ellipse(pos=(cx - 27 * s, cy - 14 * s), size=(49 * s, 29 * s))
                    Triangle(points=(cx + 19 * s, cy, cx + 36 * s, cy + 14 * s,
                                     cx + 36 * s, cy - 14 * s))
                    Color(yellow)
                    Triangle(points=(cx - 3 * s, cy, cx + 11 * s, cy + 11 * s,
                                     cx + 10 * s, cy - 11 * s))
                    Color(dark)
                    Ellipse(pos=(cx - 17 * s, cy + 4 * s), size=(4 * s, 4 * s))
                elif kinds == "snake":
                    Color(green)
                    Line(points=(cx - 31 * s, cy - 18 * s, cx - 18 * s, cy - 4 * s,
                                 cx - 3 * s, cy - 17 * s, cx + 11 * s, cy - 3 * s,
                                 cx + 24 * s, cy - 13 * s, cx + 30 * s, cy + 2 * s),
                         width=11 * s, joint="round", cap="round")
                    Ellipse(pos=(cx + 22 * s, cy - 2 * s), size=(17 * s, 15 * s))
                    Color(1, 1, 1, 1)
                    Ellipse(pos=(cx + 32 * s, cy + 6 * s), size=(4 * s, 4 * s))
                    Color(dark)
                    Ellipse(pos=(cx + 34 * s, cy + 7 * s), size=(2 * s, 2 * s))
                else:
                    Color(yellow if kinds == "bird" else (0.87, 0.50, 0.20, 1))
                    Ellipse(pos=(cx - 25 * s, cy - 12 * s), size=(43 * s, 29 * s))
                    Ellipse(pos=(cx + 6 * s, cy + 2 * s), size=(20 * s, 20 * s))
                    Color((0.95, 0.62, 0.30, 1))
                    Ellipse(pos=(cx - 8 * s, cy - 4 * s), size=(20 * s, 13 * s))
                    Color(yellow)
                    Triangle(points=(cx + 23 * s, cy + 10 * s, cx + 35 * s, cy + 5 * s,
                                     cx + 23 * s, cy))
                    Color(dark)
                    Ellipse(pos=(cx + 18 * s, cy + 13 * s), size=(3 * s, 3 * s))
                    Line(points=(cx - 5 * s, cy - 10 * s, cx - 7 * s, cy - 28 * s),
                         width=2 * s)
                    Line(points=(cx + 8 * s, cy - 10 * s, cx + 10 * s, cy - 28 * s),
                         width=2 * s)
            elif "pencil" in kinds or kinds == "sticks":
                Color(yellow if "long" in kinds else red)
                Line(points=(cx - 28 * s, cy - 20 * s, cx + 27 * s, cy + 20 * s),
                     width=11 * s, cap="round")
                Color(brown)
                Triangle(points=(cx + 22 * s, cy + 16 * s, cx + 35 * s, cy + 25 * s,
                                 cx + 28 * s, cy + 7 * s))
            elif kinds in ("friend", "family", "grandparent", "adult", "person"):
                people = 3 if kinds == "family" else 1
                for index in range(people):
                    px = cx + (index - 1) * 24 * s if people == 3 else cx
                    scale = 0.76 if people == 3 else 1
                    Color((0.83, 0.55, 0.37, 1) if index % 2 else
                          (0.68, 0.42, 0.29, 1))
                    Ellipse(pos=(px - 10 * scale * s, cy + 13 * scale * s),
                            size=(20 * scale * s, 23 * scale * s))
                    Color(blue if index % 2 else red)
                    RoundedRectangle(pos=(px - 12 * scale * s, cy - 16 * scale * s),
                                     size=(24 * scale * s, 31 * scale * s),
                                     radius=[(7 * scale * s, 7 * scale * s)])
                    Color(dark)
                    Line(points=(px - 5 * scale * s, cy - 14 * scale * s,
                                 px - 7 * scale * s, cy - 34 * scale * s),
                         width=4 * scale * s)
                    Line(points=(px + 5 * scale * s, cy - 14 * scale * s,
                                 px + 7 * scale * s, cy - 34 * scale * s),
                         width=4 * scale * s)
                    Line(points=(px - 10 * scale * s, cy + 3 * scale * s,
                                 px - 19 * scale * s, cy - 5 * scale * s),
                         width=4 * scale * s)
                    Line(points=(px + 10 * scale * s, cy + 3 * scale * s,
                                 px + 19 * scale * s, cy - 5 * scale * s),
                         width=4 * scale * s)
                    Color(dark if kinds == "grandparent" else brown)
                    Ellipse(pos=(px - 12 * scale * s, cy + 31 * scale * s),
                            size=(24 * scale * s, 7 * scale * s))
                    Color(1, 1, 1, 1)
                    Ellipse(pos=(px + 2 * scale * s, cy + 24 * scale * s),
                            size=(3 * scale * s, 3 * scale * s))
            elif kinds == "food":
                Color((0.93, 0.63, 0.39, 1))
                Ellipse(pos=(cx - 36 * s, cy - 25 * s), size=(72 * s, 48 * s))
                Color((0.98, 0.98, 0.94, 1))
                Ellipse(pos=(cx - 30 * s, cy - 19 * s), size=(60 * s, 36 * s))
                for fx, fy, food_color in ((-13, 2, red), (2, 4, green), (15, -3, yellow)):
                    Color(food_color)
                    Ellipse(pos=(cx + fx * s - 8 * s, cy + fy * s - 7 * s),
                            size=(16 * s, 14 * s))
            elif kinds == "corn":
                    Color(yellow)
                    Ellipse(pos=(cx - 15 * s, cy - 30 * s), size=(30 * s, 59 * s))
                    Color((0.98, 0.84, 0.35, 1))
                    for row in range(5):
                        for column in range(2):
                            Ellipse(pos=(cx - 8 * s + column * 9 * s,
                                         cy - 22 * s + row * 10 * s),
                                    size=(6 * s, 6 * s))
                    Color(green)
                    Triangle(points=(cx - 12 * s, cy - 9 * s, cx - 30 * s,
                                     cy - 28 * s, cx - 8 * s, cy + 1 * s))
                    Triangle(points=(cx + 12 * s, cy - 9 * s, cx + 30 * s,
                                     cy - 28 * s, cx + 8 * s, cy + 1 * s))
                    Line(points=(cx, cy + 28 * s, cx + 1 * s, cy + 35 * s),
                         width=3 * s)
            elif kinds == "vegetable":
                    Color(red)
                    Triangle(points=(cx - 22 * s, cy + 23 * s,
                                     cx + 22 * s, cy + 23 * s, cx, cy - 31 * s))
                    Color(green)
                    for dx in (-13, -4, 5, 14):
                        Line(points=(cx + dx * s, cy + 23 * s,
                                     cx + (dx - 5) * s, cy + 37 * s), width=4 * s)
            elif kinds == "sweet":
                    Color(yellow)
                    Line(circle=(cx, cy, 25 * s), width=10 * s)
                    Line(circle=(cx, cy, 12 * s), width=7 * s)
                    Color(red)
                    Ellipse(pos=(cx - 5 * s, cy - 5 * s), size=(10 * s, 10 * s))
            elif kinds == "mango":
                    Color(yellow)
                    Ellipse(pos=(cx - 24 * s, cy - 29 * s), size=(48 * s, 58 * s))
                    Color(green)
                    Ellipse(pos=(cx + 3 * s, cy + 18 * s), size=(20 * s, 11 * s),
                            angle_start=20, angle_end=300)
                    Color(brown)
                    Line(points=(cx, cy + 27 * s, cx + 2 * s, cy + 36 * s),
                         width=3 * s)
            elif kinds in ("bird", "hen", "horse", "cow", "fish", "snake"):
                Color(yellow if kinds in ("bird", "hen") else brown)
                Ellipse(pos=(cx - 23 * s, cy - 14 * s), size=(46 * s, 34 * s))
                Color(red if kinds in ("bird", "hen") else brown)
                Ellipse(pos=(cx + 6 * s, cy + 5 * s), size=(24 * s, 24 * s))
                Color(dark)
                Ellipse(pos=(cx + 20 * s, cy + 17 * s), size=(4 * s, 4 * s))
                Color(yellow)
                Triangle(points=(cx + 27 * s, cy + 12 * s, cx + 39 * s, cy + 8 * s,
                                 cx + 28 * s, cy + 4 * s))
                Color(dark)
                Line(points=(cx - 12 * s, cy - 13 * s, cx - 17 * s, cy - 29 * s),
                     width=3 * s)
                Line(points=(cx + 8 * s, cy - 13 * s, cx + 12 * s, cy - 29 * s),
                     width=3 * s)
            elif "leaf" in kinds or kinds in ("plant", "leaves", "flower"):
                Color(red if "red" in kinds else blue if "blue" in kinds else green)
                Ellipse(pos=(cx - 8 * s, cy - 20 * s), size=(35 * s, 52 * s),
                        angle_start=35, angle_end=325)
                Color(green)
                Line(points=(cx - 25 * s, cy - 28 * s, cx + 19 * s, cy + 28 * s),
                     width=3 * s)
                if kinds in ("flower", "tree"):
                    for dx, dy in ((0, 0), (12, 0), (-12, 0), (0, 12), (0, -12)):
                        Color(red if kinds == "flower" else green)
                        Ellipse(pos=(cx + dx * s - 8 * s, cy + dy * s - 8 * s),
                                size=(16 * s, 16 * s))
                    Color(yellow)
                    Ellipse(pos=(cx - 6 * s, cy - 6 * s), size=(12 * s, 12 * s))
            elif "book" in kinds or kinds in ("beginning", "middle", "end"):
                Color(blue if kinds != "end" else red)
                RoundedRectangle(pos=(cx - 29 * s, cy - 23 * s),
                                 size=(58 * s, 46 * s), radius=[(5 * s, 5 * s)])
                Color(1, 1, 1, 1)
                Line(points=(cx, cy - 19 * s, cx, cy + 19 * s), width=2 * s)
                for offset in (-10, 0, 10):
                    Line(points=(cx - 23 * s, cy + offset * s,
                                 cx - 5 * s, cy + offset * s), width=1.5 * s)
                    Line(points=(cx + 5 * s, cy + offset * s,
                                 cx + 23 * s, cy + offset * s), width=1.5 * s)
            elif "coin" in kinds or "button" in kinds:
                Color(yellow)
                Ellipse(pos=(cx - 26 * s, cy - 26 * s), size=(52 * s, 52 * s))
                Color(brown)
                Line(ellipse=(cx - 19 * s, cy - 19 * s, 38 * s, 38 * s), width=2 * s)
                Ellipse(pos=(cx - 3 * s, cy - 3 * s), size=(6 * s, 6 * s))
            elif "cup" in kinds or "basket" in kinds or "box" in kinds:
                Color(red if kinds == "box" else blue)
                RoundedRectangle(pos=(cx - 25 * s, cy - 22 * s),
                                 size=(50 * s, 43 * s), radius=[(4 * s, 4 * s)])
                Color(dark)
                Line(points=(cx - 25 * s, cy + 21 * s, cx + 25 * s, cy + 21 * s),
                     width=3 * s)
                if kinds == "cup":
                    Line(ellipse=(cx + 18 * s, cy - 9 * s, 21 * s, 20 * s), width=3 * s)
            elif kinds in ("sun", "morning", "afternoon", "evening", "moon", "night"):
                Color(yellow if kinds not in ("moon", "night") else blue)
                Ellipse(pos=(cx - 23 * s, cy - 23 * s), size=(46 * s, 46 * s))
                if kinds in ("sun", "morning", "afternoon", "evening"):
                    for angle in range(0, 360, 45):
                        theta = radians(angle)
                        Line(points=(cx + cos(theta) * 29 * s, cy + sin(theta) * 29 * s,
                                     cx + cos(theta) * 38 * s, cy + sin(theta) * 38 * s),
                             width=3 * s)
                else:
                    Color(1, 1, 1, 1)
                    Ellipse(pos=(cx - 7 * s, cy - 15 * s), size=(42 * s, 42 * s))
                    Color(yellow)
                    for dx, dy in ((-23, 27), (5, 33), (29, 16)):
                        Ellipse(pos=(cx + dx * s, cy + dy * s), size=(3 * s, 3 * s))
            elif kinds in ("cloud", "raincoat", "mittens", "sunglasses", "wave"):
                if kinds == "cloud":
                    Color(blue)
                    for dx, dy, radius in ((-15, 0, 17), (0, 9, 22), (17, 0, 17)):
                        Ellipse(pos=(cx + (dx - radius) * s, cy + (dy - radius) * s),
                                size=(2 * radius * s, 2 * radius * s))
                elif kinds == "sunglasses":
                    Color(dark)
                    RoundedRectangle(pos=(cx - 33 * s, cy - 10 * s),
                                     size=(27 * s, 22 * s), radius=[(7 * s, 7 * s)])
                    RoundedRectangle(pos=(cx + 6 * s, cy - 10 * s),
                                     size=(27 * s, 22 * s), radius=[(7 * s, 7 * s)])
                    Line(points=(cx - 6 * s, cy + 2 * s, cx + 6 * s, cy + 2 * s),
                         width=4 * s)
                    Line(points=(cx - 33 * s, cy + 5 * s, cx - 40 * s, cy + 9 * s),
                         width=3 * s)
                    Line(points=(cx + 33 * s, cy + 5 * s, cx + 40 * s, cy + 9 * s),
                         width=3 * s)
                    Color(0.57, 0.82, 0.95, 0.9)
                    Ellipse(pos=(cx - 29 * s, cy - 6 * s), size=(19 * s, 14 * s))
                    Ellipse(pos=(cx + 10 * s, cy - 6 * s), size=(19 * s, 14 * s))
                elif kinds == "mittens":
                    for dx in (-17, 17):
                        Color(red)
                        Ellipse(pos=(cx + dx * s - 12 * s, cy - 18 * s),
                                size=(25 * s, 43 * s))
                        Ellipse(pos=(cx + (dx - 10) * s, cy - 11 * s),
                                size=(13 * s, 20 * s))
                        Color(brown)
                        Line(points=(cx + (dx - 11) * s, cy - 12 * s,
                                     cx + (dx + 11) * s, cy - 12 * s), width=4 * s)
                elif kinds == "raincoat":
                    Color(yellow)
                    Triangle(points=(cx - 13 * s, cy + 25 * s, cx + 13 * s, cy + 25 * s,
                                     cx, cy + 8 * s))
                    RoundedRectangle(pos=(cx - 20 * s, cy - 27 * s),
                                     size=(40 * s, 47 * s), radius=[(7 * s, 7 * s)])
                    Triangle(points=(cx - 18 * s, cy + 10 * s, cx - 36 * s,
                                     cy - 22 * s, cx - 12 * s, cy - 16 * s))
                    Triangle(points=(cx + 18 * s, cy + 10 * s, cx + 36 * s,
                                     cy - 22 * s, cx + 12 * s, cy - 16 * s))
                    Color(dark)
                    Line(points=(cx, cy - 22 * s, cx, cy + 2 * s), width=2 * s)
                    for button_y in (-16, -7, 2):
                        Ellipse(pos=(cx - 2 * s, cy + button_y * s), size=(4 * s, 4 * s))
                else:
                    Color(blue)
                    RoundedRectangle(pos=(cx - 25 * s, cy - 23 * s),
                                     size=(50 * s, 46 * s), radius=[(12 * s, 12 * s)])
                    Color(1, 1, 1, 1)
                    Line(points=(cx - 15 * s, cy, cx + 15 * s, cy), width=4 * s)
            elif kinds in ("hands", "hand", "feet", "ear"):
                Color(red if kinds == "hands" else brown)
                if kinds == "ear":
                    Line(ellipse=(cx - 17 * s, cy - 26 * s, 34 * s, 54 * s),
                         width=8 * s)
                    Line(ellipse=(cx - 7 * s, cy - 12 * s, 18 * s, 30 * s),
                         width=4 * s)
                elif kinds == "feet":
                    for foot_x in (-14, 14):
                        Ellipse(pos=(cx + foot_x * s - 9 * s, cy - 23 * s),
                                size=(18 * s, 46 * s))
                        for toe in range(3):
                            Ellipse(pos=(cx + (foot_x + (toe - 1) * 5) * s - 3 * s,
                                         cy + 16 * s), size=(6 * s, 7 * s))
                else:
                    Ellipse(pos=(cx - 23 * s, cy - 25 * s), size=(46 * s, 50 * s))
                    for dx in (-17, -6, 6, 17):
                        Line(points=(cx + dx * s, cy + 13 * s, cx + dx * s, cy + 34 * s),
                             width=5 * s, cap="round")
            elif kinds == "fair":
                Color(brown)
                Rectangle(pos=(cx - 31 * s, cy - 25 * s), size=(62 * s, 6 * s))
                Rectangle(pos=(cx - 26 * s, cy - 25 * s), size=(5 * s, 42 * s))
                Rectangle(pos=(cx + 21 * s, cy - 25 * s), size=(5 * s, 42 * s))
                Color(red)
                Triangle(points=(cx - 32 * s, cy + 16 * s, cx + 32 * s, cy + 16 * s,
                                 cx + 23 * s, cy + 31 * s))
                Color(yellow)
                Triangle(points=(cx - 32 * s, cy + 16 * s, cx - 14 * s, cy + 16 * s,
                                 cx - 22 * s, cy + 31 * s))
                Triangle(points=(cx + 5 * s, cy + 16 * s, cx + 32 * s, cy + 16 * s,
                                 cx + 19 * s, cy + 31 * s))
                Color(green)
                Ellipse(pos=(cx - 12 * s, cy - 19 * s), size=(24 * s, 24 * s))
            elif kinds == "tree":
                Color(brown)
                RoundedRectangle(pos=(cx - 7 * s, cy - 33 * s),
                                 size=(14 * s, 47 * s), radius=[(3 * s, 3 * s)])
                Color(green)
                for dx, dy, radius in ((0, 16, 22), (-15, 7, 15), (15, 7, 15),
                                       (0, 31, 15)):
                    Ellipse(pos=(cx + (dx - radius) * s, cy + (dy - radius) * s),
                            size=(radius * 2 * s, radius * 2 * s))
            elif kinds == "watering_can":
                Color(blue)
                RoundedRectangle(pos=(cx - 24 * s, cy - 18 * s),
                                 size=(42 * s, 37 * s), radius=[(5 * s, 5 * s)])
                Line(ellipse=(cx - 10 * s, cy - 10 * s, 37 * s, 35 * s), width=4 * s)
                Color(blue)
                Line(points=(cx + 16 * s, cy + 5 * s, cx + 37 * s, cy + 18 * s,
                             cx + 42 * s, cy + 14 * s), width=5 * s, joint="round")
                for drop in range(3):
                    Color((0.22, 0.61, 0.90, 1))
                    Ellipse(pos=(cx + (35 + drop * 4) * s,
                                 cy + (4 - drop * 7) * s), size=(4 * s, 6 * s))
            elif kinds == "litter":
                Color(red)
                RoundedRectangle(pos=(cx - 22 * s, cy - 22 * s),
                                 size=(17 * s, 13 * s), radius=[(2 * s, 2 * s)])
                Color(yellow)
                Ellipse(pos=(cx + 3 * s, cy - 21 * s), size=(20 * s, 12 * s))
                Color(green)
                Triangle(points=(cx - 7 * s, cy + 15 * s, cx + 3 * s, cy - 4 * s,
                                 cx + 13 * s, cy + 15 * s))
            elif kinds == "glass":
                Color((0.52, 0.78, 0.91, 1))
                Triangle(points=(cx - 28 * s, cy - 22 * s, cx + 5 * s, cy - 25 * s,
                                 cx - 4 * s, cy + 28 * s))
                Triangle(points=(cx + 4 * s, cy - 24 * s, cx + 29 * s, cy - 11 * s,
                                 cx + 5 * s, cy + 19 * s))
                Color(1, 1, 1, 0.9)
                Line(points=(cx - 16 * s, cy - 10 * s, cx - 7 * s, cy + 11 * s),
                     width=3 * s)
            elif kinds == "colour":
                for index, paint in enumerate((red, yellow, blue, green)):
                    Color(paint)
                    Ellipse(pos=(cx - 25 * s + index * 14 * s,
                                 cy - 11 * s + (index % 2) * 19 * s),
                            size=(24 * s, 24 * s))
            elif kinds in ("ball", "red_ball", "blue_ball", "stone"):
                Color(red if "red" in kinds else blue if "blue" in kinds else yellow)
                Ellipse(pos=(cx - 25 * s, cy - 25 * s), size=(50 * s, 50 * s))
                Color(1, 1, 1, 0.8)
                Line(points=(cx - 21 * s, cy, cx + 21 * s, cy), width=2 * s)
            elif kinds == "chair":
                Color(brown)
                RoundedRectangle(pos=(cx - 20 * s, cy - 2 * s),
                                 size=(40 * s, 9 * s), radius=[(2 * s, 2 * s)])
                Rectangle(pos=(cx - 18 * s, cy + 6 * s), size=(7 * s, 25 * s))
                Rectangle(pos=(cx + 11 * s, cy + 6 * s), size=(7 * s, 25 * s))
                Rectangle(pos=(cx - 18 * s, cy - 28 * s), size=(7 * s, 26 * s))
                Rectangle(pos=(cx + 11 * s, cy - 28 * s), size=(7 * s, 26 * s))
            elif kinds in ("toy", "shoe", "spoon"):
                Color(red if kinds == "toy" else brown if kinds == "shoe" else blue)
                if kinds == "spoon":
                    Ellipse(pos=(cx - 18 * s, cy + 7 * s), size=(36 * s, 29 * s))
                    Line(points=(cx, cy + 8 * s, cx, cy - 31 * s), width=8 * s,
                         cap="round")
                elif kinds == "shoe":
                    Ellipse(pos=(cx - 27 * s, cy - 19 * s), size=(56 * s, 22 * s))
                    RoundedRectangle(pos=(cx - 14 * s, cy - 8 * s),
                                     size=(34 * s, 24 * s), radius=[(9 * s, 9 * s)])
                else:
                    RoundedRectangle(pos=(cx - 24 * s, cy - 24 * s),
                                     size=(48 * s, 48 * s), radius=[(8 * s, 8 * s)])
                    Color(yellow)
                    Ellipse(pos=(cx - 9 * s, cy - 9 * s), size=(18 * s, 18 * s))
            elif kinds in ("walking", "running", "claps", "pause", "turn",
                           "listening", "talking", "consent", "sharing"):
                Color(blue if kinds in ("listening", "pause") else green)
                Ellipse(pos=(cx - 10 * s, cy + 17 * s), size=(20 * s, 20 * s))
                Line(points=(cx, cy + 16 * s, cx, cy - 12 * s), width=6 * s)
                Line(points=(cx, cy + 5 * s, cx - 19 * s, cy - 4 * s), width=5 * s)
                Line(points=(cx, cy + 5 * s, cx + 19 * s, cy - 4 * s), width=5 * s)
                if kinds in ("walking", "running", "sharing"):
                    Line(points=(cx, cy - 12 * s, cx - 15 * s, cy - 30 * s),
                         width=5 * s)
                    Line(points=(cx, cy - 12 * s, cx + 15 * s, cy - 30 * s),
                         width=5 * s)
                if kinds == "consent":
                    Color(green)
                    Line(points=(cx + 7 * s, cy - 3 * s, cx + 14 * s, cy - 11 * s,
                                 cx + 27 * s, cy + 5 * s), width=4 * s, joint="round")
            elif kinds in ("hot_pot", "fire"):
                Color(red)
                if kinds == "fire":
                    Triangle(points=(cx - 23 * s, cy - 24 * s, cx + 23 * s, cy - 24 * s,
                                     cx, cy + 30 * s))
                    Color(yellow)
                    Triangle(points=(cx - 11 * s, cy - 22 * s, cx + 11 * s, cy - 22 * s,
                                     cx, cy + 11 * s))
                else:
                    RoundedRectangle(pos=(cx - 24 * s, cy - 17 * s),
                                     size=(48 * s, 34 * s), radius=[(6 * s, 6 * s)])
                    Line(points=(cx - 14 * s, cy + 19 * s, cx + 14 * s, cy + 19 * s),
                         width=4 * s)
                    Line(points=(cx - 17 * s, cy - 22 * s, cx - 21 * s, cy - 31 * s),
                         width=3 * s)
                    Line(points=(cx + 17 * s, cy - 22 * s, cx + 21 * s, cy - 31 * s),
                         width=3 * s)
            elif kinds in ("fair", "bus"):
                Color(yellow if kinds == "fair" else blue)
                RoundedRectangle(pos=(cx - 29 * s, cy - 15 * s),
                                 size=(58 * s, 33 * s), radius=[(5 * s, 5 * s)])
                Color(1, 1, 1, 1)
                for dx in (-17, 0, 17):
                    Rectangle(pos=(cx + dx * s - 5 * s, cy + 1 * s),
                              size=(10 * s, 10 * s))
                Color(dark)
                Ellipse(pos=(cx - 19 * s, cy - 23 * s), size=(12 * s, 12 * s))
                Ellipse(pos=(cx + 7 * s, cy - 23 * s), size=(12 * s, 12 * s))
            elif kinds in ("wall", "litter", "glass"):
                Color(brown if kinds == "wall" else red if kinds == "litter" else blue)
                if kinds == "wall":
                    Rectangle(pos=(cx - 28 * s, cy - 24 * s), size=(56 * s, 48 * s))
                    Line(points=(cx - 28 * s, cy, cx + 28 * s, cy,
                                 cx - 28 * s, cy - 12 * s, cx + 28 * s, cy - 12 * s),
                         width=2 * s)
                elif kinds == "glass":
                    Line(points=(cx - 18 * s, cy + 23 * s, cx - 13 * s, cy - 23 * s,
                                 cx + 13 * s, cy - 23 * s, cx + 18 * s, cy + 23 * s),
                         close=True, width=4 * s)
                else:
                    Triangle(points=(cx - 22 * s, cy - 20 * s, cx + 22 * s, cy - 20 * s,
                                     cx, cy + 20 * s))
            elif kinds in ("potato_road", "rainbow", "watering_can", "mittens",
                           "sunglasses", "raincoat", "wave"):
                Color(green if kinds in ("potato_road", "watering_can") else blue)
                if kinds == "rainbow":
                    for width in (52, 40, 28):
                        Line(ellipse=(cx - width * s / 2, cy - 25 * s,
                                      width * s, width * s), angle_start=0,
                             angle_end=180, width=5 * s)
                elif kinds == "potato_road":
                    Line(points=(cx - 22 * s, cy - 30 * s, cx - 9 * s, cy - 5 * s,
                                 cx - 18 * s, cy + 10 * s, cx - 2 * s, cy + 32 * s),
                         width=12 * s, joint="round")
                    Line(points=(cx + 21 * s, cy - 30 * s, cx + 9 * s, cy - 4 * s,
                                 cx + 18 * s, cy + 11 * s, cx + 2 * s, cy + 32 * s),
                         width=12 * s, joint="round")
                elif kinds == "watering_can":
                    RoundedRectangle(pos=(cx - 22 * s, cy - 15 * s),
                                     size=(37 * s, 32 * s), radius=[(6 * s, 6 * s)])
                    Line(points=(cx + 14 * s, cy + 4 * s, cx + 30 * s, cy + 15 * s),
                         width=5 * s)
                    Line(ellipse=(cx - 8 * s, cy - 1 * s, 34 * s, 32 * s), width=4 * s)
                else:
                    RoundedRectangle(pos=(cx - 25 * s, cy - 23 * s),
                                     size=(50 * s, 46 * s), radius=[(12 * s, 12 * s)])
                    Color(1, 1, 1, 1)
                    Line(points=(cx - 15 * s, cy, cx + 15 * s, cy), width=4 * s)
            else:
                Color(green if kinds not in ("hot_pot", "fire", "glass") else red)
                RoundedRectangle(pos=(cx - 24 * s, cy - 24 * s),
                                 size=(48 * s, 48 * s), radius=[(10 * s, 10 * s)])
