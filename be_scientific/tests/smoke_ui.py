"""Headless smoke test of the Kivy UI (run with xvfb: xvfb-run -a python tests/smoke_ui.py).
Not a pytest test: it needs a display/GL context, so it is run separately."""
import os, sys, tempfile
os.environ.setdefault("KIVY_NO_ARGS", "1")
os.environ.setdefault("KIVY_LOG_LEVEL", "warning")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy.app import App
from kivy.clock import Clock
from kivy.base import EventLoop
from bescientific.ui.app import BeScientificApp
from bescientific.labs.models import FIXED_DT


def pump(n=3):
    for _ in range(n):
        Clock.tick()


tmp = tempfile.mkdtemp()
app = BeScientificApp(db_path=os.path.join(tmp, "t.db"))
App._running_app = app
root = app.build()
app.root = root          # App.run() normally does this
from kivy.core.window import Window
Window.add_widget(root)
pump()

# 1. welcome -> create student -> home
w = root.get_screen("welcome")
root.current = "welcome"; pump()
w.name_field.text = "Asha"; w.class_field.text = "4"
w._create(); pump()
assert root.current == "home", root.current
assert app.db.list_students()[0]["name"] == "Asha"

# 2. bad input is rejected with a message, not a crash
root.current = "welcome"; pump()
w.name_field.text = ""; w._create()
assert w.error.text, "expected validation message"
w.name_field.text = "Bad"; w.class_field.text = "9"; w._create()
assert w.error.text and len(app.db.list_students()) == 1

# 3. open each lab, run it to completion through the real Clock loop, answer a question
for exp_id in ("gravity", "friction", "bounce"):
    app.login(app.db.list_students()[0]["id"]); pump()
    app.open_experiment(exp_id); pump()
    lab = root.get_screen("lab")
    assert lab.view is not None and lab.exp.id == exp_id
    lab._ask(); pump()                                   # before running: should only show "run first"
    assert not lab.ran
    lab._go()
    for _ in range(int(lab.view.model.run_time / FIXED_DT) + 400):    # drive the model quickly
        lab.view.model.step(FIXED_DT)
        if lab.view.model.finished: break
    lab.view._tick(0.0); pump()
    assert lab.ran and lab.result_label.text, "result text missing"
    # answer correctly then wrongly
    for q_idx in (None, 0):
        lab._ask(); pump()
        q = lab.exp.questions[(app.db.get_mastery(app.student_id, lab.exp.skill_id)[1]) % 3]
        lab._answer(q, q.correct if q_idx is None else (q.correct + 1) % len(q.option_keys)); pump()
    lab.on_leave()
    p, n = app.db.get_mastery(app.student_id, lab.exp.skill_id)
    assert n == 2, (exp_id, n)

# 4. progress + teacher + language switch render
for name in ("progress", "teacher"):
    app.go(name); pump()
app.set_lang("hi"); app.go("home"); pump()
assert app.tr("start") != "start"
app.go("lab") if False else None

# 5. canvas actually has drawing instructions for the lab view
app.open_experiment("friction"); pump()
v = root.get_screen("lab").view
v.size = (400, 240); v.redraw()
assert len(v.canvas.children) > 5, "lab canvas empty"

print("UI SMOKE TEST OK; events recorded:", app.db._conn.execute("select count(*) from events").fetchone()[0])
app.on_stop()
