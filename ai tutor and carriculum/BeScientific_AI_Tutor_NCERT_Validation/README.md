# Be Scientific: AI Tutor, NCERT Mapping, and Validation Prototype

All code, identifiers, comments, and API responses are in English. Hindi appears only in optional Hindi tutoring content.

## Features
- `/tutor`: reviewed, concept-specific hints and explanations; currently rule-based, not an LLM.
- `/curriculum`: searchable class/subject curriculum records.
- `/answer`: answer checking and illustrative BKT mastery update.
- `/progress/{student_id}`: saved attempt history in SQLite.
- `tests/test_app.py`: validation tests for API and BKT behavior.

## Important NCERT note
The included curriculum is **demonstration data, not verified official NCERT mapping**. Verify every entry against the current official NCERT textbook and edition. Record book title, class, chapter, page/section, learning outcome, and official source. Do not claim placeholders are official.

## Setup on Windows (VS Code terminal)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
If PowerShell blocks activation, use Command Prompt: `.venv\Scripts\activate.bat`

## Run
```powershell
uvicorn app:app --reload
```
Open `http://127.0.0.1:8000/docs`.

## Example tutor request
POST `/tutor`:
```json
{"concept_id":"class5_math_fractions","question":"What are equivalent fractions?","language":"English"}
```
Use `Hindi` for the included Hindi hint and explanation.

## Example answer request
POST `/answer`:
```json
{"student_id":"demo_student_01","concept_id":"class5_math_fractions","question_id":"frac_q1","answer":"2/4","previous_mastery":0.2}
```

## Run tests
```powershell
pytest -q
```

## Suggested work plan for your assigned role
1. Verify each curriculum item against current official NCERT materials.
2. Add learning outcomes, questions, answer keys, and reviewed English/Hindi explanations.
3. Test tutor responses in both languages and test invalid concept IDs.
4. Validate correct/incorrect answer paths and mastery probability bounds.
5. Keep a test log containing test case, expected result, actual result, pass/fail, defect, and fix.
6. After this stable baseline, add an actual LLM provider behind a separate module, with API keys stored in environment variables, timeouts, exception handling, and age-appropriate response checks.

## Limitations
This is a backend prototype, not a complete Kivy/Android app. It does not call an LLM, BKT parameters are not calibrated from learner data, and authentication, child-data privacy controls, production deployment, and offline synchronization are not implemented.
