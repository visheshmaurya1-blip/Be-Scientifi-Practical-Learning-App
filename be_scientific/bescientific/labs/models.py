"""Physics models for the virtual labs (pure Pymunk - no Kivy imports).

Keeping simulation separate from drawing means the labs are unit-testable on
any machine and the same model can later be rendered by a different front end.

World units: a 800 x 480 box, y pointing UP (same as Kivy's coordinate system).
Each model exposes the same small interface:

    reset()            rebuild the scene
    start()            begin the run (drop / release)
    step(dt)           advance the simulation
    shapes()           drawable primitives: ("circle", x, y, r, tag) | ("poly", [(x,y),...], tag)
                       | ("segment", x1, y1, x2, y2, tag)
    finished           True when the run is complete
    result()           measurements the UI shows and the questions refer to
"""
from __future__ import annotations

import math

import pymunk

WORLD_W, WORLD_H = 800.0, 480.0
FLOOR_Y = 60.0
GRAVITY = 900.0           # units / s^2
FIXED_DT = 1.0 / 120.0


class _BaseModel:
    run_time = 4.0

    def __init__(self) -> None:
        if not hasattr(self, "params"):          # subclasses set their defaults before calling us
            self.params: dict = {}
        self.reset()

    # -- lifecycle
    def reset(self) -> None:
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 0.0)          # gravity only switched on by start()
        self.t = 0.0
        self.running = False
        self.finished = False
        self._acc = 0.0
        self._build()

    def start(self) -> None:
        if not self.running and not self.finished:
            self.running = True
            self.space.gravity = (0.0, -GRAVITY)
            self._on_start()

    def set_param(self, key: str, value) -> None:
        """Change a student-controlled parameter; rebuilds the idle scene."""
        self.params[key] = value
        if not self.running:
            self.reset()

    def step(self, dt: float) -> None:
        if not self.running or self.finished:
            return
        self._acc += min(dt, 0.1)
        while self._acc >= FIXED_DT and not self.finished:
            self.space.step(FIXED_DT)
            self.t += FIXED_DT
            self._after_step()
            self._acc -= FIXED_DT
            if self.t >= self.run_time:
                self.finished = True
                self.running = False

    def run_to_completion(self) -> dict:
        """Headless helper (tests, auto-demo)."""
        self.start()
        while not self.finished:
            self.step(FIXED_DT)
        return self.result()

    # -- hooks
    def _build(self) -> None: ...
    def _on_start(self) -> None: ...
    def _after_step(self) -> None: ...
    def shapes(self) -> list: ...
    def result(self) -> dict: ...

    # -- helpers
    def _floor(self, friction: float = 1.0, elasticity: float = 0.0) -> pymunk.Segment:
        seg = pymunk.Segment(self.space.static_body, (-100, FLOOR_Y), (WORLD_W + 100, FLOOR_Y), 2.0)
        seg.friction, seg.elasticity = friction, elasticity
        self.space.add(seg)
        return seg

    @staticmethod
    def _ball(space, x, y, r, mass, friction=0.5, elasticity=0.0):
        body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, r))
        body.position = (x, y)
        shape = pymunk.Circle(body, r)
        shape.friction, shape.elasticity = friction, elasticity
        space.add(body, shape)
        return body, shape


# --------------------------------------------------------------------------- gravity
class GravityModel(_BaseModel):
    """A heavy and a light ball released together from the same height (no air)."""
    run_time = 3.0
    HEAVY = dict(mass=8.0, r=24.0, x=300.0)
    LIGHT = dict(mass=1.0, r=14.0, x=500.0)

    def __init__(self) -> None:
        self.params = {"height": 300.0}
        super().__init__()

    def _build(self) -> None:
        self._floor()
        self.balls = {}
        self.landed: dict[str, float] = {}
        for name, d in (("heavy", self.HEAVY), ("light", self.LIGHT)):
            y = FLOOR_Y + d["r"] + self.params["height"]       # same release height of the *bottom*
            body, shape = self._ball(self.space, d["x"], y, d["r"], d["mass"])
            self.balls[name] = (body, shape, d["r"])

    def _after_step(self) -> None:
        for name, (body, _, r) in self.balls.items():
            if name not in self.landed and body.position.y - r <= FLOOR_Y + 2.5:
                self.landed[name] = self.t
        if len(self.landed) == 2 and self.t > max(self.landed.values()) + 0.3:
            self.finished, self.running = True, False

    def shapes(self):
        out = [("segment", -100, FLOOR_Y, WORLD_W + 100, FLOOR_Y, "floor")]
        for name, (body, _, r) in self.balls.items():
            out.append(("circle", body.position.x, body.position.y, r, name))
        return out

    def result(self) -> dict:
        return {"heavy": self.landed.get("heavy"), "light": self.landed.get("light")}


# --------------------------------------------------------------------------- friction
SURFACES = {"ice": 0.05, "wood": 0.40, "rough": 0.90}


class FrictionModel(_BaseModel):
    """A block on a 30-degree ramp. tan(30 deg) = 0.58, so rough (0.9) grips and does not slide."""
    run_time = 4.0
    ANGLE = math.radians(30.0)
    RAMP_RUN = 320.0

    def __init__(self) -> None:
        self.params = {"surface": "wood"}
        super().__init__()

    def _build(self) -> None:
        mu = SURFACES[self.params["surface"]]
        x0, x1 = 80.0, 80.0 + self.RAMP_RUN
        y1 = FLOOR_Y
        y0 = y1 + math.tan(self.ANGLE) * self.RAMP_RUN
        self.ramp = ((x0, y0), (x1, y1))
        for a, b in (((x0, y0), (x1, y1)), ((x1, y1), (WORLD_W + 200, y1))):
            seg = pymunk.Segment(self.space.static_body, a, b, 2.0)
            seg.friction = mu                      # block friction is 1.0, so contact mu = this value
            self.space.add(seg)
        # stop wall at the right edge so a fast block on ice stays on screen
        wall = pymunk.Segment(self.space.static_body, (WORLD_W - 12, y1), (WORLD_W - 12, y1 + 140), 2.0)
        wall.friction = 0.0
        self.space.add(wall)
        # block resting on the upper part of the ramp
        w, h = 44.0, 30.0
        mass = 2.0
        body = pymunk.Body(mass, pymunk.moment_for_box(mass, (w, h)))
        t = 0.25                                    # fraction along the ramp
        cx = x0 + t * (x1 - x0)
        cy = y0 + t * (y1 - y0)
        nx, ny = math.sin(self.ANGLE), math.cos(self.ANGLE)   # ramp normal (pointing up/right)
        body.position = (cx + nx * (h / 2 + 3.0), cy + ny * (h / 2 + 3.0))
        body.angle = -self.ANGLE
        shape = pymunk.Poly.create_box(body, (w, h))
        shape.friction = 1.0
        self.space.add(body, shape)
        self.block, self.block_shape = body, shape
        self.start_x = body.position.x

    def shapes(self):
        (x0, y0), (x1, y1) = self.ramp
        verts = [tuple(self.block.local_to_world(v)) for v in self.block_shape.get_vertices()]
        return [("segment", x0, y0, x1, y1, "ramp"),
                ("segment", x1, y1, WORLD_W, y1, "floor"),
                ("segment", WORLD_W - 12, FLOOR_Y, WORLD_W - 12, FLOOR_Y + 140, "wall"),
                ("poly", verts, "block")]

    def result(self) -> dict:
        return {"distance": abs(self.block.position.x - self.start_x), "surface": self.params["surface"]}


# --------------------------------------------------------------------------- bounce
class BounceModel(_BaseModel):
    """A ball dropped on a floor whose elasticity the student sets (0..1)."""
    run_time = 3.5

    def __init__(self) -> None:
        self.params = {"elasticity": 0.7, "height": 300.0}
        super().__init__()

    def _build(self) -> None:
        e = float(self.params["elasticity"])
        self._floor(friction=0.5, elasticity=e)        # contact elasticity = ball(1.0) * floor(e)
        r = 20.0
        self.r = r
        self.ball, _ = self._ball(self.space, 400.0, FLOOR_Y + r + self.params["height"], r, 1.0,
                                  elasticity=1.0)
        self.hit_floor = False
        self.max_after_bounce = 0.0
        self._prev_vy = 0.0

    def _after_step(self) -> None:
        vy = self.ball.velocity.y
        if not self.hit_floor and self._prev_vy < -1.0 and vy >= 0.0:
            self.hit_floor = True                       # velocity flipped sign: first impact
        if self.hit_floor:
            self.max_after_bounce = max(self.max_after_bounce, self.ball.position.y - self.r - FLOOR_Y)
        self._prev_vy = vy

    def shapes(self):
        return [("segment", -100, FLOOR_Y, WORLD_W + 100, FLOOR_Y, "floor"),
                ("circle", self.ball.position.x, self.ball.position.y, self.r, "ball")]

    def result(self) -> dict:
        return {"bounce_height": self.max_after_bounce, "drop_height": self.params["height"]}


MODELS = {"gravity": GravityModel, "friction": FrictionModel, "bounce": BounceModel}
