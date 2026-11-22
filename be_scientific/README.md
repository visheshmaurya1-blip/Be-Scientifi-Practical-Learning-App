# Be Scientific - starter implementation

Offline-first, multilingual virtual-lab app for primary science (Classes 1-6) with a
Bayesian Knowledge Tracing tutor, plus a FastAPI backend for sync, teacher analytics and
(optional) LLM hints. This is the code counterpart of the paper: it implements the
architecture end to end, but with **3 experiments, not 100+**. See "What is and is not here".

```
bescientific/            Android/desktop client (Kivy + KivyMD)
  bkt.py                 BKT maths (paper eqs. 1-3), mastery/remediation policy
  db.py                  SQLite store: students, events, mastery, `synced` flags
  sync.py                delay-tolerant uploader + background worker with back-off
  tutor.py               offline hints + optional cloud (LLM) hint with fallback
  content.py             skills, experiments, question banks (grow this)
  i18n.py                English + Hindi strings
  labs/models.py         Pymunk physics (no Kivy): gravity, friction ramp, bouncing ball
  labs/views.py          Kivy canvas renderer + simulation loop
  ui/                    app, screens (welcome, home, lab, progress, teacher), fonts
server/                  FastAPI backend (SQLAlchemy; PostgreSQL or SQLite)
tests/                   pytest suite + tests/smoke_ui.py (headless Kivy smoke test)
main.py                  entry point;  buildozer.spec  Android packaging
```

## Run the app on a computer

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Flow: create a student -> pick an experiment -> run it (Do) -> answer a question (Reflect)
-> BKT updates mastery (Think) and chooses continue / remediate / mastered. "My progress"
and "Teacher view" read the same local database, so everything works with no network.

**Hindi:** *Noto Sans Devanagari* is bundled in `assets/fonts/` with its SIL Open Font
License. The language button falls back to "Hindi" in Latin only if the font is absent.

## Run the backend

```bash
pip install -r server/requirements.txt
uvicorn server.main:app --host 0.0.0.0 --port 8000        # SQLite file by default
# production:
export DATABASE_URL=postgresql+psycopg://user:pass@host:5432/bescientific
export API_KEY=choose-a-long-random-secret                 # clients must send X-API-Key
uvicorn server.main:app --host 0.0.0.0 --port 8000
```

Endpoints: `POST /v1/sync` (idempotent upload), `GET /v1/students/{id}/mastery`,
`GET /v1/dashboard?class_level=4`, `POST /v1/tutor/hint`, `GET /health`. Interactive docs at `/docs`.

Point the app at it (omit both to stay fully offline):

```bash
export BESCIENTIFIC_API_URL=http://192.168.1.10:8000
export BESCIENTIFIC_API_KEY=choose-a-long-random-secret
python main.py
```

(On Android put `{"api_url": "...", "api_key": "..."}` in `settings.json` inside the app's data dir.)

LLM hints (optional): set `LLM_PROVIDER=anthropic|openai`, `LLM_MODEL=<model>`, the provider's
API key, and `pip install langchain-anthropic` (or `langchain-openai`). Any failure falls back
to the built-in hints, so learners are never blocked.

## Tests

```bash
pip install -r requirements-dev.txt
pytest                                                    # 29 tests: BKT, physics, DB, sync, API
xvfb-run -a python tests/smoke_ui.py                      # Linux; drives every screen headlessly
```

## Build the Android APK

```bash
pip install buildozer cython
buildozer android debug          # first build downloads the SDK/NDK; needs Linux/WSL
```

`buildozer.spec` is a reasonable starting point but **was not built here** (no Android SDK in
the environment this code was written in), so expect to tune requirements/versions on first build.

## Adding an experiment (towards the paper's 100+)

1. `content.py`: add a `Skill` (BKT parameters), an `Experiment`, and 2-3 `Question`s.
2. `labs/models.py`: add a model class with `reset/start/step/shapes/result` and register it in `MODELS`.
3. `labs/views.py`: add colours for any new shape tags.
4. `ui/screens.py` -> `LabScreen._build_controls`: add its controls; `_on_finished`: add its result text.
5. `i18n.py`: add English + Hindi strings (a test fails if any catalogue string is missing).

## What is and is not here

Implemented and tested: BKT (checked against hand calculations), SQLite offline store and
unsynced-queue semantics, idempotent sync with failure/back-off, API-key check, teacher dashboard
(local and server), three physics labs (assertions on the physics, e.g. equal fall time, ice > wood > rough),
English/Hindi catalogue, headless UI smoke test.

Not done / needs your decisions:
- **Experiment count:** 3 of the paper's 100+; no 3D, no Class 1-2 content yet.
- **Real BKT parameters:** `content.py` uses reasonable defaults. Fit them from pilot data (pyBKT) before claiming adaptivity works.
- **Collaborative labs:** real-time multi-device synchronisation is not implemented.
- **Teacher view has no login** and student records are not encrypted on device; add authentication
  and consent/privacy handling before real classrooms (these are children's data).
- **LLM path** is written but untested without credentials; **speech** (plyer TTS) and the **APK build** are untested here.
- Uses KivyMD 1.2.0 (stable on python-for-android, marked deprecated upstream); migrating to KivyMD 2.x changes widget APIs.
