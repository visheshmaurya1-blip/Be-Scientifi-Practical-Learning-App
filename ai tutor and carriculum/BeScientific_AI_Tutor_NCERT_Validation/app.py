from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from database import init_db, save_attempt, get_student_progress
from schemas import AnswerRequest, TutorRequest
from curriculum import load_curriculum, get_concept, get_questions_for_concept
from bkt import update_mastery
from tutor import generate_tutor_response

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Be Scientific Learning API", version="1.0.0", lifespan=lifespan)

@app.get("/")
def home():
    return {"project": "Be Scientific", "message": "Learning API is running.", "docs": "/docs",
            "note": "Curriculum entries are examples and must be verified against current official NCERT material."}

@app.get("/curriculum")
def curriculum(class_level: int | None = None, subject: str | None = None):
    items = load_curriculum()
    if class_level is not None:
        items = [x for x in items if x["class_level"] == class_level]
    if subject is not None:
        items = [x for x in items if x["subject"].lower() == subject.lower()]
    return {"count": len(items), "items": items}

@app.get("/curriculum/{concept_id}")
def curriculum_concept(concept_id: str):
    item = get_concept(concept_id)
    if item is None:
        raise HTTPException(404, "Concept not found")
    return item

@app.get("/questions/{concept_id}")
def questions(concept_id: str):
    if get_concept(concept_id) is None:
        raise HTTPException(404, "Concept not found")
    return {"concept_id": concept_id, "questions": get_questions_for_concept(concept_id)}

@app.post("/answer")
def submit_answer(request: AnswerRequest):
    if get_concept(request.concept_id) is None:
        raise HTTPException(404, "Concept not found")
    question = next((q for q in get_questions_for_concept(request.concept_id)
                     if q["question_id"] == request.question_id), None)
    if question is None:
        raise HTTPException(404, "Question not found")
    correct = request.answer.strip().casefold() == question["correct_answer"].strip().casefold()
    mastery = update_mastery(request.previous_mastery, correct)
    save_attempt(request.student_id, request.concept_id, request.question_id, correct, mastery)
    return {"student_id": request.student_id, "concept_id": request.concept_id,
            "is_correct": correct, "feedback": "Correct! Well done." if correct else
            "Not quite. Review the hint and try another question.",
            "previous_mastery": request.previous_mastery, "updated_mastery": mastery,
            "mastery_is_estimate": True}

@app.get("/progress/{student_id}")
def progress(student_id: str):
    return {"student_id": student_id, "attempts": get_student_progress(student_id)}

@app.post("/tutor")
def tutor(request: TutorRequest):
    concept = get_concept(request.concept_id)
    if concept is None:
        raise HTTPException(404, "Concept not found")
    return generate_tutor_response(concept, request.question, request.language)
