# Careem AI Pair Engineer - PR Readiness Assistant

A Streamlit prototype for the Careem AI challenge. The app acts like an AI pair engineer that reviews short, self-created code snippets before human review and gives practical feedback on readability, maintainability, structure, design risks, refactoring opportunities, missing tests, risk score, and final PR readiness.

## Challenge Selected

The AI Pair Engineer

## Why This Project Is Useful

Engineering teams spend a lot of review time on issues that can be caught before a pull request reaches a human reviewer. This prototype helps developers submit cleaner, safer changes while preserving human judgment for product context, architecture tradeoffs, and ownership decisions. It is especially useful for catching unclear business rules, missing validation, weak error handling, and missing tests early.

## Features

- Streamlit web app with a focused PR-readiness workflow.
- Five self-created dummy snippets across Python, JavaScript, SQL, and Java.
- Deterministic local fallback analyzer that works without an OpenAI API key.
- Optional OpenAI review mode for richer feedback when `OPENAI_API_KEY` is configured.
- Structured output for positive notes, readability issues, design risks, refactor suggestions, recommended tests, risk score, and final decision.
- Pytest coverage for scoring and fallback analyzer behavior.

## Screenshots

### Home / Code Input
![Home](docs/screenshots/01-home.png)

### Review Result
![Review Result](docs/screenshots/02-review-result.png)

### Multi-language Review
![Multi-language Review](docs/screenshots/03-multi-language-review.png)

## Screenshot Checklist

Save final screenshots in `docs/screenshots/` with these exact names:

- `docs/screenshots/01-home.png`: landing page with title, subtitle, sidebar options, and sample code loaded.
- `docs/screenshots/02-review-result.png`: completed review result showing positive note, readability issues, design risks, suggested refactor, recommended tests, risk score, and final PR readiness decision.
- `docs/screenshots/03-multi-language-review.png`: optional AI mode or another language sample, such as SQL or JavaScript, showing multiple review types.

## Project Structure

```text
careem-ai-pair-engineer/
  app.py
  src/
    fallback_analyzer.py
    prompt_templates.py
    reviewer.py
    sample_snippets.py
    scoring.py
  tests/
  docs/
    screenshots/
```

## Run Locally

macOS/Linux:

```bash
cd careem-ai-pair-engineer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
streamlit run app.py
```

Windows:

```bash
cd careem-ai-pair-engineer
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
streamlit run app.py
```

## Optional OpenAI API Key

The app works without an API key by using the local deterministic fallback analyzer. To enable AI review mode locally:

```bash
export OPENAI_API_KEY="your-api-key"
streamlit run app.py
```

For Streamlit Community Cloud, add `OPENAI_API_KEY` in the app secrets settings only if you want AI mode. It is optional. If the key is missing or an API call fails, the app automatically falls back to local review.

## Deploy To Streamlit Community Cloud

1. Go to Streamlit Community Cloud.
2. Sign in with GitHub.
3. Click "New app".
4. Select the repository: `careem-ai-pair-engineer`.
5. Select branch: `main`.
6. Set the main file path to `app.py`.
7. Click Deploy.
8. Copy the deployed app URL.

The app works without secrets using local fallback mode. If you want AI mode, add `OPENAI_API_KEY` in Streamlit secrets, but it is optional. For this job submission, fallback mode is enough because the app demonstrates the workflow safely.

## Dataset

No external dataset required. This prototype uses self-created dummy code snippets only.

## GitHub Publishing Commands

Before pushing, create a new public GitHub repository named `careem-ai-pair-engineer`. Do not commit secrets.

```bash
git init
git status
git add .
git commit -m "Initial submission for Careem AI Pair Engineer challenge"
git branch -M main
git remote add origin https://github.com/<your-github-username>/careem-ai-pair-engineer.git
git push -u origin main
```

## 100-Word Submission Summary

I built an AI Pair Engineer prototype that helps developers prepare code before human review. The assistant accepts a code snippet and reviews it for readability, maintainability, structure, design risks, and missing test cases. Instead of only pointing out syntax issues, it behaves like a senior pair engineer by explaining why the code may be risky, suggesting a cleaner refactor, recommending unit tests, and giving a final PR-readiness decision. I used dummy code examples to avoid confidential data. The goal is to reduce review cycles, improve code quality, and help developers submit cleaner, safer pull requests.
