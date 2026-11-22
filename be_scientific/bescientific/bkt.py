"""Bayesian Knowledge Tracing (BKT) for the on-device AI tutor.

Implements the four-parameter model described in the paper: every skill is a
two-state hidden Markov model (unlearned / learned).

    P(L0) - probability the skill is already known before the first attempt
    P(T)  - probability of learning the skill after one opportunity
    P(S)  - slip:  wrong answer although the skill is known
    P(G)  - guess: right answer although the skill is not known

After each observation the posterior is

    correct:   q = p(1-s) / ( p(1-s) + (1-p)g )
    incorrect: q = p s    / ( p s    + (1-p)(1-g) )

and the belief carried into the next opportunity is

    p' = q + (1-q) * T

Everything here is pure Python so it runs on the phone without extra packages.
"""
from __future__ import annotations

from dataclasses import dataclass

_EPS = 1e-6

# Policy thresholds (tunable; see README).
MASTERED_AT = 0.95          # >= this: concept considered mastered
REMEDIATE_BELOW = 0.40      # < this (after MIN_ATTEMPTS): offer remedial help
MIN_ATTEMPTS = 2


@dataclass(frozen=True)
class BKTParams:
    p_init: float = 0.25
    p_transit: float = 0.20
    p_slip: float = 0.10
    p_guess: float = 0.30

    def validated(self) -> "BKTParams":
        for name in ("p_init", "p_transit", "p_slip", "p_guess"):
            v = getattr(self, name)
            if not (0.0 < v < 1.0):
                raise ValueError(f"{name} must be strictly between 0 and 1, got {v}")
        if self.p_slip + self.p_guess >= 1.0:
            raise ValueError("p_slip + p_guess must be < 1 (model degeneracy)")
        return self


def posterior(p_known: float, correct: bool, params: BKTParams) -> float:
    """P(L_t | observation): Bayes update of the knowledge belief."""
    p = min(max(p_known, _EPS), 1.0 - _EPS)
    s, g = params.p_slip, params.p_guess
    if correct:
        num = p * (1.0 - s)
        den = num + (1.0 - p) * g
    else:
        num = p * s
        den = num + (1.0 - p) * (1.0 - g)
    return num / den


def update(p_known: float, correct: bool, params: BKTParams) -> float:
    """Full BKT step: observation update followed by the learning transition."""
    q = posterior(p_known, correct, params)
    return q + (1.0 - q) * params.p_transit


def next_action(p_known: float, attempts: int) -> str:
    """Return 'mastered', 'remediate' or 'continue' for the adaptive curriculum."""
    if p_known >= MASTERED_AT:
        return "mastered"
    if attempts >= MIN_ATTEMPTS and p_known < REMEDIATE_BELOW:
        return "remediate"
    return "continue"
