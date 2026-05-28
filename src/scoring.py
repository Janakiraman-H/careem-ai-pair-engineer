"""Risk scoring for deterministic fallback reviews."""

from __future__ import annotations


DECISION_READY = "Ready for review"
DECISION_CLEANUP = "Needs cleanup"
DECISION_REWORK = "Needs rework"


def compute_risk_score(signals: dict[str, bool]) -> int:
    """Compute a capped 1-10 risk score from analyzer signals."""
    score = 1
    weighted_signals = (
        "magic_numbers",
        "missing_validation",
        "missing_error_handling",
        "hardcoded_business_rules",
        "sql_select_star",
        "sql_missing_where",
        "too_many_branches",
        "long_code",
        "weak_naming",
    )
    for signal in weighted_signals:
        if signals.get(signal, False):
            score += 1
    return max(1, min(score, 10))


def decision_from_score(score: int) -> str:
    if score <= 3:
        return DECISION_READY
    if score <= 6:
        return DECISION_CLEANUP
    return DECISION_REWORK
