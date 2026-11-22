import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "curriculum.json"

def load_curriculum():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def get_concept(concept_id: str):
    return next((item for item in load_curriculum() if item["concept_id"] == concept_id), None)

def get_questions_for_concept(concept_id: str):
    concept = get_concept(concept_id)
    return concept["questions"] if concept else []
