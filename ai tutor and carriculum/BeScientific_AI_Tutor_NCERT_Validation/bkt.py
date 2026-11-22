def update_mastery(previous_mastery: float, is_correct: bool,
                  learning_probability: float = 0.20, slip_probability: float = 0.10,
                  guess_probability: float = 0.20) -> float:
    """Simplified BKT update. Default probabilities are examples, not calibrated values."""
    values = (previous_mastery, learning_probability, slip_probability, guess_probability)
    if not all(0 <= value <= 1 for value in values):
        raise ValueError("All probabilities must be between 0 and 1.")
    if slip_probability >= 1 or guess_probability >= 1:
        raise ValueError("Slip and guess probabilities must be less than 1.")
    if is_correct:
        numerator = previous_mastery * (1 - slip_probability)
        denominator = numerator + (1 - previous_mastery) * guess_probability
    else:
        numerator = previous_mastery * slip_probability
        denominator = numerator + (1 - previous_mastery) * (1 - guess_probability)
    posterior = previous_mastery if denominator == 0 else numerator / denominator
    updated = posterior + (1 - posterior) * learning_probability
    return round(min(1.0, max(0.0, updated)), 4)
