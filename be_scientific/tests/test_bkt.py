import pytest
from bescientific import bkt
from bescientific.bkt import BKTParams

P = BKTParams(p_init=0.3, p_transit=0.15, p_slip=0.1, p_guess=0.2)


def test_posterior_correct_matches_hand_calculation():
    # q = 0.3*0.9 / (0.3*0.9 + 0.7*0.2) = 0.27/0.41
    assert bkt.posterior(0.3, True, P) == pytest.approx(0.27 / 0.41)


def test_posterior_incorrect_matches_hand_calculation():
    # q = 0.3*0.1 / (0.3*0.1 + 0.7*0.8) = 0.03/0.59
    assert bkt.posterior(0.3, False, P) == pytest.approx(0.03 / 0.59)


def test_update_adds_learning_transition():
    q = 0.27 / 0.41
    assert bkt.update(0.3, True, P) == pytest.approx(q + (1 - q) * 0.15)


def test_correct_answers_raise_belief_and_wrong_answers_lower_it():
    p = 0.3
    for _ in range(5):
        new = bkt.update(p, True, P)
        assert new > p
        p = new
    assert p > 0.9
    q = 0.6
    assert bkt.posterior(q, False, P) < q


def test_belief_stays_a_probability_for_extreme_inputs():
    for p in (0.0, 1.0, 1e-12):
        for ok in (True, False):
            assert 0.0 <= bkt.update(p, ok, P) <= 1.0


def test_next_action_policy():
    assert bkt.next_action(0.97, 5) == "mastered"
    assert bkt.next_action(0.2, 3) == "remediate"
    assert bkt.next_action(0.2, 1) == "continue"      # too few attempts to judge
    assert bkt.next_action(0.6, 6) == "continue"


def test_params_validation():
    with pytest.raises(ValueError):
        BKTParams(p_slip=0.6, p_guess=0.5).validated()
    with pytest.raises(ValueError):
        BKTParams(p_init=0.0).validated()
    BKTParams().validated()
