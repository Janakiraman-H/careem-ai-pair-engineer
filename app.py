from __future__ import annotations

import html
import os

import streamlit as st

from src.reviewer import review_code
from src.sample_snippets import get_sample_code, get_sample_names


st.set_page_config(
    page_title="Careem AI Pair Engineer",
    page_icon=":white_check_mark:",
    layout="wide",
    initial_sidebar_state="expanded",
)


CSS = """
<style>
    .main .block-container {
        padding-top: 2rem;
        max-width: 1180px;
    }
    .hero {
        border-bottom: 1px solid #e8ecef;
        margin-bottom: 1.2rem;
        padding-bottom: 1rem;
    }
    .hero h1 {
        font-size: 2.4rem;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #425466;
        font-size: 1.05rem;
        margin-bottom: 0.7rem;
    }
    .small-copy {
        color: #536471;
        line-height: 1.55;
    }
    .review-card {
        background: #ffffff;
        border: 1px solid #e4e8ee;
        border-radius: 8px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }
    .review-card h3 {
        font-size: 1.02rem;
        margin: 0 0 0.55rem 0;
        color: #17202a;
    }
    .badge {
        display: inline-block;
        border-radius: 999px;
        padding: 0.22rem 0.7rem;
        font-weight: 700;
        font-size: 0.82rem;
        border: 1px solid transparent;
    }
    .badge-ready {
        color: #05603a;
        background: #dcfae6;
        border-color: #abefc6;
    }
    .badge-cleanup {
        color: #93370d;
        background: #fef0c7;
        border-color: #fedf89;
    }
    .badge-rework {
        color: #912018;
        background: #fee4e2;
        border-color: #fecdca;
    }
    .metric-box {
        background: #f8fafc;
        border: 1px solid #e4e8ee;
        border-radius: 8px;
        padding: 1rem;
    }
    .footer {
        color: #667085;
        border-top: 1px solid #e8ecef;
        margin-top: 2rem;
        padding-top: 1rem;
        font-size: 0.9rem;
    }
</style>
"""


def main() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    _render_header()

    with st.sidebar:
        st.subheader("Challenge")
        st.info("The AI Pair Engineer")
        mode = st.radio(
            "Mode",
            ["Local fallback review", "AI review using OpenAI API"],
            help="AI mode uses OpenAI when a key is configured, otherwise it falls back locally.",
        )
        language = st.selectbox("Programming language", ["Python", "JavaScript", "Java", "SQL"])
        sample_name = st.selectbox("Sample snippet", get_sample_names(language))
        risk_tolerance = st.select_slider("Risk tolerance", options=["Low", "Medium", "High"], value="Medium")

    default_code = get_sample_code(sample_name)
    code = st.text_area(
        "Code snippet",
        value=default_code,
        height=360,
        help="Use dummy or self-created snippets only.",
    )

    col_a, col_b = st.columns([0.22, 0.78])
    with col_a:
        review_clicked = st.button("Review Code", type="primary", use_container_width=True)
    with col_b:
        st.caption("Reviews focus on PR readiness, not syntax perfection.")

    if review_clicked:
        if not code.strip():
            st.warning("Add a code snippet before requesting a review.")
            return

        api_key = _get_api_key()
        result, warning = review_code(
            code=code,
            language=language,
            risk_tolerance=risk_tolerance,
            mode=mode,
            api_key=api_key,
        )
        if warning:
            st.warning(warning)
        _render_review(result)

    st.markdown(
        '<div class="footer">Built with dummy examples for an AI challenge submission. No confidential code used.</div>',
        unsafe_allow_html=True,
    )


def _render_header() -> None:
    st.markdown(
        """
        <div class="hero">
            <h1>Careem AI Pair Engineer</h1>
            <div class="subtitle">PR Readiness Assistant for cleaner, safer code reviews</div>
            <div class="small-copy">
                A lightweight prototype that reviews short, self-created code snippets before human review.
                It highlights maintainability risks, recommends tests, suggests a focused refactor, and gives a practical PR-readiness decision.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_review(result: dict) -> None:
    decision = result["decision_badge"]
    badge_class = {
        "Ready for review": "badge-ready",
        "Needs cleanup": "badge-cleanup",
        "Needs rework": "badge-rework",
    }.get(decision, "badge-cleanup")

    top_left, top_right = st.columns([0.66, 0.34])
    with top_left:
        _card("Positive note", result["positive_note"])
    with top_right:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.markdown(f'<span class="badge {badge_class}">{decision}</span>', unsafe_allow_html=True)
        st.metric("Risk score", f"{result['risk_score']} / 10")
        st.progress(result["risk_score"] / 10)
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        _card("Readability and maintainability issues", _items(result["readability_issues"]), body_is_html=True)
        _card("Suggested refactor", result["suggested_refactor"])
    with col2:
        _card("Design or architecture risks", _items(result["design_risks"]), body_is_html=True)
        _card("Recommended tests", _items(result["recommended_tests"]), body_is_html=True)

    _card("Final PR readiness decision", result["final_decision"])


def _card(title: str, body: str, body_is_html: bool = False) -> None:
    rendered_body = body if body_is_html else html.escape(body)
    st.markdown(f'<div class="review-card"><h3>{html.escape(title)}</h3>{rendered_body}</div>', unsafe_allow_html=True)


def _items(values: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{html.escape(value)}</li>" for value in values) + "</ul>"


def _get_api_key() -> str | None:
    if os.getenv("OPENAI_API_KEY"):
        return os.getenv("OPENAI_API_KEY")
    try:
        return st.secrets.get("OPENAI_API_KEY")
    except Exception:
        return None


if __name__ == "__main__":
    main()
