"""Deterministic local review engine used when AI mode is unavailable."""

from __future__ import annotations

import re

from src.scoring import compute_risk_score, decision_from_score


REQUIRED_KEYS = {
    "positive_note",
    "readability_issues",
    "design_risks",
    "suggested_refactor",
    "recommended_tests",
    "risk_score",
    "final_decision",
    "decision_badge",
}


def analyze_code(code: str, language: str, risk_tolerance: str = "Medium") -> dict:
    normalized_language = language.lower()
    lines = [line for line in code.splitlines() if line.strip()]
    signals = {
        "magic_numbers": _has_magic_numbers(code),
        "missing_validation": _missing_validation(code, normalized_language),
        "missing_error_handling": _missing_error_handling(code, normalized_language),
        "hardcoded_business_rules": _has_hardcoded_strings(code),
        "sql_select_star": normalized_language == "sql" and bool(re.search(r"select\s+\*", code, re.I)),
        "sql_missing_where": _sql_missing_where(code, normalized_language),
        "too_many_branches": _count_branches(code) >= 4,
        "long_code": len(lines) > 35,
        "weak_naming": _has_weak_names(code),
    }

    readability_issues = _build_readability_issues(code, normalized_language, signals)
    design_risks = _build_design_risks(code, normalized_language, signals)
    risk_score = compute_risk_score(signals)
    final_decision = decision_from_score(risk_score)

    return {
        "positive_note": _positive_note(normalized_language),
        "readability_issues": readability_issues or ["The snippet is compact and easy to scan at a first pass."],
        "design_risks": design_risks or ["No major structural risk was detected by the local analyzer."],
        "suggested_refactor": _suggest_refactor(normalized_language, signals, risk_tolerance),
        "recommended_tests": _recommended_tests(normalized_language, signals),
        "risk_score": risk_score,
        "final_decision": final_decision,
        "decision_badge": final_decision,
    }


def _has_magic_numbers(code: str) -> bool:
    numbers = re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w.])", code)
    allowed = {"0", "1", "-1"}
    return any(number not in allowed for number in numbers)


def _has_hardcoded_strings(code: str) -> bool:
    strings = re.findall(r"""["']([^"']{3,})["']""", code)
    business_like = [value for value in strings if not value.startswith("/") and " " not in value.strip()]
    return len(business_like) >= 2


def _missing_validation(code: str, language: str) -> bool:
    lowered = code.lower()
    validation_terms = ("validate", "required", "none", "null", "empty", "length", "regex", "check")
    has_function = any(token in lowered for token in ("def ", "function ", "public ", "private ", "async function"))
    return has_function and not any(term in lowered for term in validation_terms)


def _missing_error_handling(code: str, language: str) -> bool:
    lowered = code.lower()
    if language == "javascript" and "fetch(" in lowered:
        return not (_contains_keyword(lowered, "try") and _contains_keyword(lowered, "catch"))
    risky_calls = ("requests.", "fetch(", "paymentgateway", "send_", "charge(", "execute(")
    has_risky_call = any(call in lowered for call in risky_calls)
    handles_errors = any(_contains_keyword(lowered, token) for token in ("try", "except", "catch"))
    return has_risky_call and not handles_errors


def _contains_keyword(code: str, keyword: str) -> bool:
    return bool(re.search(rf"\b{re.escape(keyword)}\b", code))


def _sql_missing_where(code: str, language: str) -> bool:
    if language != "sql":
        return False
    lowered = code.lower()
    return "select" in lowered and " from " in lowered and not re.search(r"\bwhere\b", lowered)


def _count_branches(code: str) -> int:
    return len(re.findall(r"\b(if|elif|else if|switch|case|when)\b", code, re.I))


def _has_weak_names(code: str) -> bool:
    weak_patterns = (
        r"\b(data|item|tmp|obj|val|foo|bar)\b",
        r"\b[a-z]\b\s*=",
    )
    return any(re.search(pattern, code) for pattern in weak_patterns)


def _python_functions_without_docstrings(code: str) -> bool:
    return bool(re.search(r"def\s+\w+\([^)]*\):\n(?!\s+[\"'])", code))


def _has_repeated_logic(code: str) -> bool:
    stripped = [line.strip() for line in code.splitlines() if line.strip()]
    return len(stripped) != len(set(stripped))


def _build_readability_issues(code: str, language: str, signals: dict[str, bool]) -> list[str]:
    issues = []
    if signals["magic_numbers"]:
        issues.append("Magic numbers make the business rules harder to understand and tune safely.")
    if signals["hardcoded_business_rules"]:
        issues.append("Hardcoded strings appear to encode business states or categories inline.")
    if signals["weak_naming"]:
        issues.append("Generic names such as data or item reduce readability when logic grows.")
    if signals["long_code"]:
        issues.append("The snippet is long enough that extracting smaller helpers would improve scanning.")
    if language == "python" and _python_functions_without_docstrings(code):
        issues.append("Python functions should include a short docstring when they encode business behavior.")
    if _has_repeated_logic(code):
        issues.append("Some repeated logic could be consolidated into a helper or shared expression.")
    if language == "sql" and signals["sql_select_star"]:
        issues.append("SELECT * hides the real data contract and can make query changes risky.")
    return issues


def _build_design_risks(code: str, language: str, signals: dict[str, bool]) -> list[str]:
    risks = []
    if signals["missing_validation"]:
        risks.append("Inputs are used without clear validation, which can create edge-case defects.")
    if signals["missing_error_handling"]:
        risks.append("External or failure-prone operations do not have explicit error handling.")
    if signals["too_many_branches"]:
        risks.append("Multiple conditional branches suggest business rules are mixed into one flow.")
    if language == "sql":
        if signals["sql_select_star"]:
            risks.append("The query may retrieve unnecessary columns and couple callers to schema changes.")
        if signals["sql_missing_where"]:
            risks.append("The query has no WHERE clause, so it may scan or return more data than intended.")
    lowered = code.lower()
    if language == "java" and all(term in lowered for term in ("payment", "notification", "analytics")):
        risks.append("Payment, notification, analytics, and receipt creation are handled in one method.")
    return risks


def _suggest_refactor(language: str, signals: dict[str, bool], risk_tolerance: str) -> str:
    tolerance = risk_tolerance.lower()
    if language == "sql":
        return "Select explicit columns, add an appropriate WHERE filter, and move ordering/pagination expectations into the query contract."
    if signals["too_many_branches"] or signals["magic_numbers"]:
        return "Extract named constants and small helper functions for each business rule before changing behavior."
    if signals["missing_error_handling"]:
        return "Wrap the risky operation with explicit success, empty, and failure paths that callers can handle."
    if tolerance == "low":
        return "Add validation and tests first, then make the smallest readability refactor."
    return "Clarify names, validate inputs, and keep the main function focused on orchestration."


def _recommended_tests(language: str, signals: dict[str, bool]) -> list[str]:
    tests = [
        "Happy-path behavior with representative valid input.",
        "Invalid or missing input should fail clearly without partial side effects.",
        "Boundary values around pricing, filtering, or branch conditions.",
    ]
    if signals["missing_error_handling"]:
        tests.append("Failure path for external calls or unsuccessful responses.")
    if language == "sql":
        tests.append("Query returns only expected columns and respects filtering assumptions.")
    return tests[:4]


def _positive_note(language: str) -> str:
    labels = {
        "python": "The snippet is small enough to review quickly, which is a good starting point for tightening the business rules.",
        "javascript": "The async flow is straightforward, so improving resilience should be a focused change.",
        "java": "The method exposes the full workflow clearly, making responsibility boundaries visible.",
        "sql": "The query intent is easy to recognize, which helps target the performance and contract improvements.",
    }
    return labels.get(language, "The snippet has a clear intent and can be improved with focused changes.")
