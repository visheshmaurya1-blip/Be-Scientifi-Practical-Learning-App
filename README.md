# Be Scientific

Be Scientific is an offline-first learning app for Classes 1–6. It includes
Science virtual labs, Math and Reasoning activities, class-banded quiz banks,
and quiz rewards (lives, streaks, XP, coins, and badges).

## Run the desktop app

From this folder, create and activate a virtual environment, then install the
desktop dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

The root `main.py` launches the unified KivyMD app in `app\`. Its offline
learning engine, local database, tutor, labs, and synchronization client are
provided by `be_scientific\bescientific\`. Student progress continues to work
without network access. Image assets are intentionally omitted from this public
repository until their redistribution rights are confirmed. If the classroom
background is unavailable, the app shows a quiet, non-animated landscape
fallback; the app also runs without a custom logo or icon.

Class 1 starts with the NCERT core books for Mathematics (*Joyful Mathematics*),
English (*Mridang*), and Hindi (*Sarangi*). The app includes original,
bilingual lesson notes, activities, and quick checks for each listed book
unit; it links back to the official [NCERT textbook catalog](https://ncert.nic.in/textbook.php).
The Class 1 Urdu textbook is not included in this first review pack.
Every one of the 41 Class 1 Maths, English, and Hindi lesson activities also
has a bilingual, interactive virtual try-it scene. Learners tap illustrated
activity-specific objects to perform each activity and receive visual result
feedback. Counted items are drawn as separate objects, and comparison activities
show their different sizes or groupings. Open a lesson and choose
**Try it virtually**. The original hands-on activity remains available
alongside the simulation, especially for tasks that involve real movement,
conversation, or observing the world.
Class 2 now follows the same format for its current *Joyful Mathematics*,
*Mridang*, and *Sarangi* units. All 50 Class 2 lesson activities now include
bilingual virtual labs with illustrated, activity-specific objects that
learners tap to perform the activity and see feedback. Urdu remains outside
the reviewed core pack.
Class 3 extends virtual labs to all 56 lessons across *Maths Mela*, *Santoor*,
*Veena*, and the integrated *Our Wondrous World* course. Learners interact
with illustrated maths manipulatives, story objects, plants, animals, community
scenes, and sorting materials; original real-world observation and speaking
activities remain available alongside the simulations. Arts and Physical
Education textbooks are not yet offered as separate study packs.
Class 4 adds 49 bilingual lesson guides across the same four current NCERT
books and now provides interactive illustrated virtual labs for all 49 lessons.
Class 5 adds virtual labs for all 45 bilingual guides across its current
*Maths Mela*, *Santoor*, *Veena*, and *Our Wondrous World* units.
Class 6 adds virtual labs for all 81 original bilingual guides for
*Ganita Prakash*, *Poorvi*, *Malhar*, *Curiosity*, *Exploring Society: India and
Beyond*, and *Deepakam*.
Separate Class 6 Arts, Physical Education, and Vocational Education study packs
are not included.
Hindi is rendered with the bundled Noto Sans Devanagari font under its SIL Open
Font License.
Hindi course metadata and lesson guides for all 322 Class 1–6 units are also
seeded into the local SQLite database (`hindi_study_courses` and
`hindi_study_lessons`). Hindi study screens read from this offline catalog;
the bundled curriculum refreshes those tables when the app starts.

## NCERT tutor

After login, a bunny tutor button stays in the lower-right corner on app screens.
Students can also open it from Home or ask about a lesson from its study screen.
The chat searches the selected student's available Class 1–6 lesson guides,
answers in English or Hindi, and links to the related official NCERT book. It
works offline and does not send student questions to an external AI service.
This is a curriculum-grounded retrieval chatbot, not a generative LLM: it uses
the app's original lesson guides and refuses adult-content or out-of-curriculum
questions instead of making up answers. The separate `Python code for Project`
prototype contains demonstration curriculum entries marked unverified, so
those entries are not used as authoritative NCERT content in the app.

## Optional backends

The project has two separate FastAPI services:

* `be_scientific\server\` provides the learning engine's tutor and `/v1/sync`
  endpoints. Configure `BESCIENTIFIC_API_URL` and, if required,
  `BESCIENTIFIC_API_KEY` to enable its background sync.
* `bescientific_backend\` provides school administration, analytics, and the
  platform curriculum. Install `bescientific_backend\requirements.txt` and run
  `uvicorn app.main:app --reload` from the `bescientific_backend` folder.
  Configure `BESCIENTIFIC_PLATFORM_URL` in the desktop app to display its
  connection and curriculum status. The two backends have distinct APIs and
  configuration; the platform URL is not a substitute for the `/v1/sync` URL.

The app has an offline curriculum fallback, so either service can be omitted.

## Build for Android

The root `buildozer.spec` packages the unified KivyMD 2 app and allows portrait
and landscape layouts. Buildozer needs Linux; on Windows, use WSL 2 with Ubuntu
and run these commands from the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install buildozer cython
buildozer android debug
```

The first build downloads the Android SDK/NDK and can take a while. Install the
resulting APK from `bin/` on a device or emulator. An Android SDK/NDK build has
not been run from this Windows workspace.

## Tests

Run the learning-engine tests from the root virtual environment:

```powershell
pip install pytest fastapi sqlalchemy httpx
python -m pytest be_scientific\tests
```

The legacy standalone app in `be_scientific\` pins KivyMD 1.2.0, while the
unified root app uses KivyMD 2.x. Do not install
`be_scientific\requirements-dev.txt` into the root app's environment; use a
separate virtual environment if you need to run the legacy app.

The platform API tests are in `bescientific_backend\tests\` and use that
service's requirements.
