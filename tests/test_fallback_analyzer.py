from src.fallback_analyzer import REQUIRED_KEYS, analyze_code
from src.sample_snippets import get_sample_code


def test_fallback_analyzer_returns_all_required_keys():
    result = analyze_code(get_sample_code("Python pricing calculation"), "Python")

    assert REQUIRED_KEYS.issubset(result.keys())


def test_risk_score_is_always_between_one_and_ten():
    result = analyze_code("def x(a):\n    return a\n", "Python")

    assert 1 <= result["risk_score"] <= 10


def test_sql_select_star_increases_risk_and_creates_issue():
    result = analyze_code("SELECT * FROM trips;", "SQL")

    assert result["risk_score"] >= 3
    assert any("SELECT *" in issue for issue in result["readability_issues"])
    assert any("WHERE clause" in risk for risk in result["design_risks"])


def test_javascript_fetch_without_try_catch_creates_error_handling_issue():
    code = "async function getTrips() { const r = await fetch('/trips'); return r.json(); }"
    result = analyze_code(code, "JavaScript")

    assert any("error handling" in risk.lower() for risk in result["design_risks"])


def test_python_pricing_sample_missing_validation_is_detected():
    result = analyze_code(get_sample_code("Python pricing calculation"), "Python")

    assert any("validation" in risk.lower() for risk in result["design_risks"])


def test_java_external_call_without_try_catch_creates_error_handling_issue():
    result = analyze_code(get_sample_code("Java service method"), "Java")

    assert any("error handling" in risk.lower() for risk in result["design_risks"])
