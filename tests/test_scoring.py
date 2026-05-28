from src.scoring import compute_risk_score, decision_from_score


def test_compute_risk_score_caps_between_one_and_ten():
    signals = {
        "magic_numbers": True,
        "missing_validation": True,
        "missing_error_handling": True,
        "hardcoded_business_rules": True,
        "sql_select_star": True,
        "sql_missing_where": True,
        "too_many_branches": True,
        "long_code": True,
        "weak_naming": True,
    }

    assert compute_risk_score(signals) == 10


def test_decision_mapping():
    assert decision_from_score(3) == "Ready for review"
    assert decision_from_score(4) == "Needs cleanup"
    assert decision_from_score(7) == "Needs rework"
