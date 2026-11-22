from pydantic import BaseModel, Field

class AnswerRequest(BaseModel):
    student_id: str = Field(min_length=1, max_length=80)
    concept_id: str
    question_id: str
    answer: str = Field(min_length=1, max_length=500)
    previous_mastery: float = Field(default=0.20, ge=0.0, le=1.0)

class TutorRequest(BaseModel):
    concept_id: str
    question: str = Field(min_length=1, max_length=1000)
    language: str = Field(default="English", pattern="^(English|Hindi)$")
