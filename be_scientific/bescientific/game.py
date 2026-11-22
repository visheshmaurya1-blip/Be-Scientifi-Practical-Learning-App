"""Gamified quiz engine: lives, streaks, XP, coins and badges.

Pure Python so the same logic drives the KivyMD 1.x client, the KivyMD 2
desktop shell, and unit tests.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .content import Question

XP_CORRECT = 10
XP_STREAK_STEP = 2          # extra XP per consecutive correct answer
COINS_CORRECT = 1
COINS_STREAK_5 = 5
STARTING_LIVES = 3
QUESTIONS_PER_RUN = 5
XP_PER_LEVEL = 100

BADGE_FIRST_WIN = "first_win"
BADGE_STREAK_5 = "streak_5"
BADGE_STREAK_10 = "streak_10"
BADGE_LEVEL_2 = "level_2"
BADGE_QUIZ_ACE = "quiz_ace"          # 5/5 in a run
BADGE_COMEBACK = "comeback"          # finish with 1 life left and score >= 60%

ALL_BADGES = (
    BADGE_FIRST_WIN, BADGE_STREAK_5, BADGE_STREAK_10,
    BADGE_LEVEL_2, BADGE_QUIZ_ACE, BADGE_COMEBACK,
)


def level_for_xp(xp: int) -> int:
    return max(1, xp // XP_PER_LEVEL + 1)


def xp_into_level(xp: int) -> tuple[int, int]:
    """Return (xp within current level, xp needed for next level)."""
    return xp % XP_PER_LEVEL, XP_PER_LEVEL


@dataclass
class AnswerResult:
    correct: bool
    xp_gain: int
    coins_gain: int
    streak: int
    lives: int
    finished: bool
    new_badges: tuple[str, ...] = ()
    question: Question | None = None
    chosen: int = -1


@dataclass
class QuizSession:
    questions: list[Question]
    skill_id: str
    subject_id: str
    lives: int = STARTING_LIVES
    index: int = 0
    correct_count: int = 0
    xp: int = 0
    coins: int = 0
    streak: int = 0
    best_streak: int = 0
    finished: bool = False
    history: list[AnswerResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.questions)

    @property
    def current(self) -> Question | None:
        if self.finished or self.index >= self.total:
            return None
        return self.questions[self.index]

    @property
    def progress(self) -> float:
        if not self.total:
            return 1.0
        return min(1.0, self.index / self.total)

    @property
    def percent(self) -> int:
        if not self.history:
            return 0
        return round(100 * self.correct_count / len(self.history))

    def answer(self, choice: int) -> AnswerResult:
        q = self.current
        if q is None or self.finished:
            return AnswerResult(False, 0, 0, self.streak, self.lives, True)
        correct = choice == q.correct
        xp_gain = coins_gain = 0
        if correct:
            self.correct_count += 1
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
            xp_gain = XP_CORRECT + XP_STREAK_STEP * max(0, self.streak - 1)
            coins_gain = COINS_CORRECT + (COINS_STREAK_5 if self.streak % 5 == 0 else 0)
            self.xp += xp_gain
            self.coins += coins_gain
        else:
            self.streak = 0
            self.lives = max(0, self.lives - 1)
        self.index += 1
        done = self.index >= self.total or self.lives <= 0
        self.finished = done
        result = AnswerResult(
            correct=correct, xp_gain=xp_gain, coins_gain=coins_gain,
            streak=self.streak, lives=self.lives, finished=done,
            question=q, chosen=choice,
        )
        self.history.append(result)
        return result


def new_badges(had: list[str], stats_xp: int, session: QuizSession) -> list[str]:
    have = set(had)
    earned: list[str] = []

    def award(bid: str):
        if bid not in have:
            earned.append(bid)
            have.add(bid)

    if session.correct_count >= 1:
        award(BADGE_FIRST_WIN)
    if session.best_streak >= 5:
        award(BADGE_STREAK_5)
    if session.best_streak >= 10:
        award(BADGE_STREAK_10)
    if level_for_xp(stats_xp + session.xp) >= 2:
        award(BADGE_LEVEL_2)
    if session.total and session.correct_count == session.total and session.lives > 0:
        award(BADGE_QUIZ_ACE)
    if session.finished and session.lives == 1 and session.percent >= 60:
        award(BADGE_COMEBACK)
    return earned
