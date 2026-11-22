def generate_tutor_response(concept: dict, question: str, language: str = "English") -> dict:
    """Rule-based tutor baseline. This function does not call an external LLM."""
    hindi = language == "Hindi"
    return {
        "concept_id": concept["concept_id"],
        "language": language,
        "student_question": question,
        "hint": concept["hint_hi"] if hindi else concept["hint_en"],
        "explanation": concept["explanation_hi"] if hindi else concept["explanation_en"],
        "provider": "curated_rule_based",
        "llm_enabled": False,
        "note": "No external AI request was made."
    }
