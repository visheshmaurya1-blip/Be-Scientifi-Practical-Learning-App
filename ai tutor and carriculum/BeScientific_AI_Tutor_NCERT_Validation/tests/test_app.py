from fastapi.testclient import TestClient
from app import app
from bkt import update_mastery

client = TestClient(app)

def test_bkt_probability_is_valid():
    assert 0 <= update_mastery(0.2, True) <= 1

def test_correct_answer_gives_higher_mastery_than_incorrect():
    assert update_mastery(0.2, True) > update_mastery(0.2, False)

def test_curriculum_endpoint():
    response = client.get("/curriculum")
    assert response.status_code == 200
    assert response.json()["count"] >= 1

def test_curriculum_filter():
    response = client.get("/curriculum?class_level=5&subject=Mathematics")
    assert response.status_code == 200
    assert all(x["subject"] == "Mathematics" for x in response.json()["items"])

def test_unknown_concept_returns_404():
    assert client.get("/curriculum/not_real").status_code == 404

def test_tutor_returns_curated_hint():
    response = client.post("/tutor", json={"concept_id":"class5_math_fractions",
        "question":"What are equivalent fractions?","language":"English"})
    assert response.status_code == 200
    assert response.json()["provider"] == "curated_rule_based"
    assert response.json()["hint"]

def test_unknown_question_returns_404():
    response = client.post("/answer", json={"student_id":"test_student",
        "concept_id":"class5_math_fractions","question_id":"missing",
        "answer":"2/4","previous_mastery":0.2})
    assert response.status_code == 404

def test_submit_correct_answer():
    response = client.post("/answer", json={"student_id":"test_student",
        "concept_id":"class5_math_fractions","question_id":"frac_q1",
        "answer":"2/4","previous_mastery":0.2})
    assert response.status_code == 200
    assert response.json()["is_correct"] is True
