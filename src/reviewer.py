"""Review orchestration for local and optional OpenAI-powered reviews."""

from __future__ import annotations

import json
import os
from typing import Any

from src.fallback_analyzer import REQUIRED_KEYS, analyze_code
from src.prompt_templates import build_review_prompt
from src.scoring import decision_from_score


DEFAULT_MODEL = "gpt-4o-mini"


def review_code(
    code: str,
    language: str,
    risk_tolerance: str,
    mode: str,
    api_key: str | None = None,
) -> tuple[dict[str, Any], str | None]:
    """Return a review result and an optional warning message."""
    if mode != "AI review using OpenAI API":
        return analyze_code(code, language, risk_tolerance), None

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        return (
            analyze_code(code, language, risk_tolerance),
            "OpenAI API key is not configured, so local fallback review was used.",
        )

    try:
        result = _review_with_openai(code, language, risk_tolerance, key)
        return _normalize_review(result), None
    except Exception as exc:  # pragma: no cover - depends on external service
        return (
            analyze_code(code, language, risk_tolerance),
            f"AI review was unavailable ({exc}). Local fallback review was used.",
        )


def _review_with_openai(code: str, language: str, risk_tolerance: str, api_key: str) -> dict[str, Any]:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    prompt = build_review_prompt(language=language, risk_tolerance=risk_tolerance, code=code)
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": "Return strict JSON only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    return json.loads(content)


def _normalize_review(result: dict[str, Any]) -> dict[str, Any]:
    missing = REQUIRED_KEYS.difference(result)
    if missing:
        raise ValueError(f"AI response missed required keys: {', '.join(sorted(missing))}")

    risk_score = int(result.get("risk_score", 1))
    risk_score = max(1, min(risk_score, 10))
    final_decision = str(result.get("final_decision") or decision_from_score(risk_score))
    if final_decision not in {"Ready for review", "Needs cleanup", "Needs rework"}:
        final_decision = decision_from_score(risk_score)

    return {
        "positive_note": str(result["positive_note"]),
        "readability_issues": _as_string_list(result["readability_issues"]),
        "design_risks": _as_string_list(result["design_risks"]),
        "suggested_refactor": str(result["suggested_refactor"]),
        "recommended_tests": _as_string_list(result["recommended_tests"])[:5],
        "risk_score": risk_score,
        "final_decision": final_decision,
        "decision_badge": final_decision,
    }


def _as_string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value]
    return ["No specific item returned."]

