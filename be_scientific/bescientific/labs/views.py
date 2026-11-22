"""Kivy view for the physics models: draws shapes, runs the simulation loop."""
from __future__ import annotations

from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, Quad, Rectangle
from kivy.uix.widget import Widget

from .models import SURFACES, WORLD_H, WORLD_W

BG = (0.96, 0.97, 0.99, 1)
COLOURS = {
    "floor": (0.30, 0.30, 0.33, 1),
    "wall": (0.30, 0.30, 0.33, 1),
    "heavy": (0.84, 0.22, 0.22, 1),
    "light": (0.20, 0.45, 0.85, 1),
    "ball": (0.15, 0.65, 0.35, 1),
    "block": (0.95, 0.60, 0.10, 1),
}
RAMP_BY_SURFACE = {
    "ice": (0.62, 0.85, 0.95, 1),
    "wood": (0.55, 0.37, 0.20, 1),
    "rough": (0.38, 0.38, 0.38, 1),
}
assert set(RAMP_BY_SURFACE) == set(SURFACES)


class LabView(Widget):
    """Renders `model.shapes()` scaled to fit the widget (world y-up == Kivy y-up)."""

    def __init__(self, model, on_finished=None, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.on_finished = on_finished
        self._event = None
        self._notified = False
        self.bind(pos=self.redraw, size=self.redraw)

    # ------------------------------------------------------------- lifecycle
    def start_loop(self) -> None:
        if self._event is None:
            self._event = Clock.schedule_interval(self._tick, 1 / 60.0)

    def stop_loop(self) -> None:
        if self._event is not None:
            self._event.cancel()
            self._event = None

    def reset(self) -> None:
        self.model.reset()
        self._notified = False
        self.redraw()

    def _tick(self, dt: float) -> None:
        self.model.step(dt)
        self.redraw()
        if self.model.finished and not self._notified:
            self._notified = True
            if self.on_finished:
                self.on_finished(self.model.result())

    # --------------------------------------------------------------- drawing
    def _scale(self):
        s = min(self.width / WORLD_W, self.height / WORLD_H)
        ox = self.x + (self.width - WORLD_W * s) / 2
        oy = self.y + (self.height - WORLD_H * s) / 2
        return s, ox, oy

    def redraw(self, *_args) -> None:
        if self.width <= 1 or self.height <= 1:
            return
        s, ox, oy = self._scale()
        mx = lambda x: ox + x * s
        my = lambda y: oy + y * s
        self.canvas.clear()
        with self.canvas:
            Color(*BG)
            Rectangle(pos=self.pos, size=self.size)
            for shp in self.model.shapes():
                kind, tag = shp[0], shp[-1]
                if kind == "circle":
                    _, cx, cy, r, _ = shp
                    Color(*COLOURS.get(tag, (0, 0, 0, 1)))
                    Ellipse(pos=(mx(cx - r), my(cy - r)), size=(2 * r * s, 2 * r * s))
                elif kind == "segment":
                    _, x1, y1, x2, y2, _ = shp
                    if tag == "ramp":
                        col = RAMP_BY_SURFACE[self.model.params.get("surface", "wood")]
                    else:
                        col = COLOURS.get(tag, (0, 0, 0, 1))
                    Color(*col)
                    # clip the very long floor segment to the visible world
                    x1, x2 = max(x1, 0), min(x2, WORLD_W)
                    Line(points=[mx(x1), my(y1), mx(x2), my(y2)], width=max(2.0, 3.0 * s))
                elif kind == "poly":
                    _, verts, _ = shp
                    Color(*COLOURS.get(tag, (0, 0, 0, 1)))
                    pts = [c for v in verts for c in (mx(v[0]), my(v[1]))]
                    if len(verts) == 4:
                        Quad(points=pts)
                    else:
                        Line(points=pts, close=True, width=2)
