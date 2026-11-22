"""Curriculum catalogue: classes, subjects, labs, skills and quiz banks.

Labs prove the physics + BKT pipeline. Quizzes add Math, Science and Reasoning
with class-banded questions (1-2, 3-4, 5-6). Strings live in i18n.py.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

from .bkt import BKTParams

CLASS_LEVELS = (1, 2, 3, 4, 5, 6)


@dataclass(frozen=True)
class Skill:
    id: str
    name_key: str
    params: BKTParams
    hint_key: str
    explain_key: str
    subject_id: str = "science"


@dataclass(frozen=True)
class Question:
    id: str
    text_key: str
    option_keys: tuple[str, ...]
    correct: int  # index into option_keys
    classes: tuple[int, ...] = CLASS_LEVELS
    subject_id: str = "science"
    skill_id: str = ""
    xp: int = 10


@dataclass(frozen=True)
class Experiment:
    id: str
    module_key: str
    title_key: str
    desc_key: str
    skill_id: str
    lab: str                      # key in labs.models.MODELS / labs.views.VIEWS
    classes: tuple[int, ...] = (3, 4, 5, 6)
    questions: tuple[Question, ...] = field(default_factory=tuple)
    subject_id: str = "science"


@dataclass(frozen=True)
class Subject:
    id: str
    name_key: str
    desc_key: str
    skill_id: str
    has_labs: bool = False


SUBJECTS: dict[str, Subject] = {
    "science": Subject("science", "subject_science", "subject_science_desc", "science_quiz", True),
    "math": Subject("math", "subject_math", "subject_math_desc", "math_quiz"),
    "reasoning": Subject("reasoning", "subject_reasoning", "subject_reasoning_desc", "reasoning_quiz"),
}

_P = BKTParams(0.25, 0.20, 0.10, 0.33)

SKILLS: dict[str, Skill] = {
    "gravity_equal_fall": Skill("gravity_equal_fall", "skill_gravity_equal_fall",
                                _P, "h_gravity", "e_gravity", "science"),
    "friction": Skill("friction", "skill_friction",
                      _P, "h_friction", "e_friction", "science"),
    "elasticity": Skill("elasticity", "skill_elasticity",
                        _P, "h_elasticity", "e_elasticity", "science"),
    "science_quiz": Skill("science_quiz", "skill_science_quiz",
                          BKTParams(0.28, 0.22, 0.10, 0.30), "h_science_quiz", "e_science_quiz", "science"),
    "math_quiz": Skill("math_quiz", "skill_math_quiz",
                       BKTParams(0.28, 0.22, 0.10, 0.30), "h_math_quiz", "e_math_quiz", "math"),
    "reasoning_quiz": Skill("reasoning_quiz", "skill_reasoning_quiz",
                            BKTParams(0.28, 0.22, 0.10, 0.30), "h_reasoning_quiz", "e_reasoning_quiz", "reasoning"),
}

EXPERIMENTS: dict[str, Experiment] = {
    "gravity": Experiment(
        "gravity", "module_forces", "exp_gravity", "exp_gravity_desc", "gravity_equal_fall", "gravity",
        questions=(
            Question("gravity_q1", "q_gravity_1", ("a_heavy_first", "a_light_first", "a_same_time"), 2),
            Question("gravity_q2", "q_gravity_2", ("a_stone_first", "a_feather_first", "a_same_time"), 2),
            Question("gravity_q3", "q_gravity_3", ("a_yes", "a_no"), 1),
        )),
    "friction": Experiment(
        "friction", "module_forces", "exp_friction", "exp_friction_desc", "friction", "friction",
        questions=(
            Question("friction_q1", "q_friction_1", ("a_ice", "a_wood", "a_rough"), 2),
            Question("friction_q2", "q_friction_2", ("a_ice", "a_wood", "a_rough"), 0),
            Question("friction_q3", "q_friction_3", ("a_slows", "a_speeds", "a_nochange"), 0),
        )),
    "bounce": Experiment(
        "bounce", "module_forces", "exp_bounce", "exp_bounce_desc", "elasticity", "bounce",
        questions=(
            Question("bounce_q1", "q_bounce_1", ("a_higher", "a_lower", "a_same"), 0),
            Question("bounce_q2", "q_bounce_2", ("a_stick", "a_bounce_full"), 0),
            Question("bounce_q3", "q_bounce_3", ("a_ball_hi", "a_ball_lo"), 0),
        )),
}

# Class bands: 1-2 (early), 3-4 (middle), 5-6 (upper primary)
_C12, _C34, _C56 = (1, 2), (3, 4), (5, 6)


def _q(qid, text, options, correct, classes, subject, skill):
    return Question(qid, text, options, correct, classes, subject, skill)


QUIZ_QUESTIONS: tuple[Question, ...] = (
    # ---- math 1-2
    _q("m12_1", "q_m12_1", ("a_4", "a_5", "a_6"), 1, _C12, "math", "math_quiz"),
    _q("m12_2", "q_m12_2", ("a_7", "a_3", "a_equal_num"), 0, _C12, "math", "math_quiz"),
    _q("m12_3", "q_m12_3", ("a_2", "a_3", "a_4"), 1, _C12, "math", "math_quiz"),
    _q("m12_4", "q_m12_4", ("a_8", "a_9", "a_11"), 1, _C12, "math", "math_quiz"),
    _q("m12_5", "q_m12_5", ("a_3", "a_4", "a_5"), 1, _C12, "math", "math_quiz"),
    _q("m12_6", "q_m12_6", ("a_10", "a_12", "a_8"), 0, _C12, "math", "math_quiz"),
    # ---- math 3-4
    _q("m34_1", "q_m34_1", ("a_42", "a_36", "a_49"), 0, _C34, "math", "math_quiz"),
    _q("m34_2", "q_m34_2", ("a_2", "a_4", "a_8"), 1, _C34, "math", "math_quiz"),
    _q("m34_3", "q_m34_3", ("a_55", "a_65", "a_45"), 0, _C34, "math", "math_quiz"),
    _q("m34_4", "q_m34_4", ("a_9", "a_12", "a_6"), 1, _C34, "math", "math_quiz"),
    _q("m34_5", "q_m34_5", ("a_3", "a_4", "a_6"), 1, _C34, "math", "math_quiz"),
    _q("m34_6", "q_m34_6", ("a_30", "a_25", "a_20"), 0, _C34, "math", "math_quiz"),
    # ---- math 5-6
    _q("m56_1", "q_m56_1", ("a_1", "a_half", "a_2"), 0, _C56, "math", "math_quiz"),
    _q("m56_2", "q_m56_2", ("a_20", "a_30", "a_15"), 1, _C56, "math", "math_quiz"),
    _q("m56_3", "q_m56_3", ("a_12", "a_24", "a_10"), 0, _C56, "math", "math_quiz"),
    _q("m56_4", "q_m56_4", ("a_15", "a_8", "a_16"), 0, _C56, "math", "math_quiz"),
    _q("m56_5", "q_m56_5", ("a_9", "a_15", "a_13"), 2, _C56, "math", "math_quiz"),
    _q("m56_6", "q_m56_6", ("a_0", "a_1", "a_2"), 1, _C56, "math", "math_quiz"),
    # ---- science 1-2
    _q("s12_1", "q_s12_1", ("a_sunlight", "a_stones", "a_plastic"), 0, _C12, "science", "science_quiz"),
    _q("s12_2", "q_s12_2", ("a_rock", "a_cat", "a_pencil"), 1, _C12, "science", "science_quiz"),
    _q("s12_3", "q_s12_3", ("a_oxygen", "a_wood", "a_sand"), 0, _C12, "science", "science_quiz"),
    _q("s12_4", "q_s12_4", ("a_star", "a_planet", "a_moon"), 0, _C12, "science", "science_quiz"),
    _q("s12_5", "q_s12_5", ("a_always_solid", "a_liquid_room", "a_metal"), 1, _C12, "science", "science_quiz"),
    _q("s12_6", "q_s12_6", ("a_eyes", "a_legs", "a_nose"), 0, _C12, "science", "science_quiz"),
    # ---- science 3-4
    _q("s34_1", "q_s34_1", ("a_leaf", "a_root", "a_flower"), 0, _C34, "science", "science_quiz"),
    _q("s34_2", "q_s34_2", ("a_moon", "a_sun", "a_mars"), 1, _C34, "science", "science_quiz"),
    _q("s34_3", "q_s34_3", ("a_chemical", "a_physical", "a_nothing"), 1, _C34, "science", "science_quiz"),
    _q("s34_4", "q_s34_4", ("a_air", "a_blood", "a_water"), 1, _C34, "science", "science_quiz"),
    _q("s34_5", "q_s34_5", ("a_wood", "a_iron", "a_plastic"), 1, _C34, "science", "science_quiz"),
    _q("s34_6", "q_s34_6", ("a_solid", "a_liquid", "a_gas"), 2, _C34, "science", "science_quiz"),
    # ---- science 5-6
    _q("s56_1", "q_s56_1", ("a_newton", "a_meter", "a_watt"), 0, _C56, "science", "science_quiz"),
    _q("s56_2", "q_s56_2", ("a_0c", "a_50c", "a_100c"), 2, _C56, "science", "science_quiz"),
    _q("s56_3", "q_s56_3", ("a_cell", "a_organ", "a_tissue"), 0, _C56, "science", "science_quiz"),
    _q("s56_4", "q_s56_4", ("a_air", "a_water", "a_steel"), 2, _C56, "science", "science_quiz"),
    _q("s56_5", "q_s56_5", ("a_own_light", "a_reflects_sun", "a_fire"), 1, _C56, "science", "science_quiz"),
    _q("s56_6", "q_s56_6", ("a_evap", "a_melt", "a_freeze"), 0, _C56, "science", "science_quiz"),
    # ---- reasoning 1-2
    _q("r12_1", "q_r12_1", ("a_7", "a_8", "a_10"), 1, _C12, "reasoning", "reasoning_quiz"),
    _q("r12_2", "q_r12_2", ("a_apple", "a_banana", "a_car", "a_mango"), 2, _C12, "reasoning", "reasoning_quiz"),
    _q("r12_3", "q_r12_3", ("a_flies", "a_swims", "a_drives"), 0, _C12, "reasoning", "reasoning_quiz"),
    _q("r12_4", "q_r12_4", ("a_huge", "a_small", "a_tall"), 1, _C12, "reasoning", "reasoning_quiz"),
    _q("r12_5", "q_r12_5", ("a_triangle", "a_square", "a_circle"), 1, _C12, "reasoning", "reasoning_quiz"),
    _q("r12_6", "q_r12_6", ("a_cat_animal", "a_car_animal", "a_dog_animal"), 1, _C12, "reasoning", "reasoning_quiz"),
    # ---- reasoning 3-4
    _q("r34_1", "q_r34_1", ("a_20", "a_16", "a_25"), 0, _C34, "reasoning", "reasoning_quiz"),
    _q("r34_2", "q_r34_2", ("a_eat", "a_run", "a_sleep"), 0, _C34, "reasoning", "reasoning_quiz"),
    _q("r34_3", "q_r34_3", ("a_circle", "a_square", "a_triangle", "a_book"), 3, _C34, "reasoning", "reasoning_quiz"),
    _q("r34_4", "q_r34_4", ("a_3", "a_4", "a_2"), 0, _C34, "reasoning", "reasoning_quiz"),
    _q("r34_5", "q_r34_5", ("a_thursday", "a_friday", "a_sunday"), 0, _C34, "reasoning", "reasoning_quiz"),
    _q("r34_6", "q_r34_6", ("a_pen", "a_paper", "a_shoe"), 2, _C34, "reasoning", "reasoning_quiz"),
    # ---- reasoning 5-6
    _q("r56_1", "q_r56_1", ("a_30", "a_28", "a_24"), 0, _C56, "reasoning", "reasoning_quiz"),
    _q("r56_2", "q_r56_2", ("a_school", "a_bus", "a_farm"), 0, _C56, "reasoning", "reasoning_quiz"),
    _q("r56_3", "q_r56_3", ("a_flower", "a_tree", "a_animal"), 0, _C56, "reasoning", "reasoning_quiz"),
    _q("r56_4", "q_r56_4", ("a_mercury", "a_venus", "a_earth", "a_moon"), 3, _C56, "reasoning", "reasoning_quiz"),
    _q("r56_5", "q_r56_5", ("a_1min", "a_3min", "a_9min"), 1, _C56, "reasoning", "reasoning_quiz"),
    _q("r56_6", "q_r56_6", ("a_north", "a_south", "a_west"), 1, _C56, "reasoning", "reasoning_quiz"),
)


def experiments_for_class(class_level: int) -> list[Experiment]:
    return [e for e in EXPERIMENTS.values() if class_level in e.classes]


def subjects_for_class(_class_level: int) -> list[Subject]:
    return list(SUBJECTS.values())


def questions_for(subject_id: str, class_level: int) -> list[Question]:
    return [q for q in QUIZ_QUESTIONS if q.subject_id == subject_id and class_level in q.classes]


def pick_question(exp: Experiment, attempts_on_skill: int) -> Question:
    """Rotate through the question bank so repeat attempts see new questions."""
    return exp.questions[attempts_on_skill % len(exp.questions)]


def pick_quiz(subject_id: str, class_level: int, n: int = 5, rng: random.Random | None = None) -> list[Question]:
    pool = questions_for(subject_id, class_level)
    if not pool:
        return []
    rng = rng or random.Random()
    if len(pool) <= n:
        picked = list(pool)
        rng.shuffle(picked)
        return picked
    return rng.sample(pool, n)


def curriculum_payload() -> dict:
    """JSON-serialisable snapshot used by the backend and the desktop client."""
    return {
        "classes": [{"id": n, "label": f"Class {n}"} for n in CLASS_LEVELS],
        "subjects": [
            {"id": s.id, "name_key": s.name_key, "desc_key": s.desc_key,
             "modes": (["lab", "quiz"] if s.has_labs else ["quiz"])}
            for s in SUBJECTS.values()
        ],
        "labs": [
            {"id": e.id, "title_key": e.title_key, "classes": list(e.classes), "subject": e.subject_id}
            for e in EXPERIMENTS.values()
        ],
    }
