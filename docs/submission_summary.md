# Careem AI Pair Engineer - Submission Summary

## Challenge Selected

The AI Pair Engineer

## Prototype Link

<add Streamlit deployed app link here>

## GitHub Repository

<add GitHub repository link here>

## Dataset

No external dataset required. This prototype uses self-created dummy code snippets only.

## 100-word Summary

I built an AI Pair Engineer prototype that helps developers prepare code before human review. The assistant accepts a code snippet and reviews it for readability, maintainability, structure, design risks, and missing test cases. Instead of only pointing out syntax issues, it behaves like a senior pair engineer by explaining why the code may be risky, suggesting a cleaner refactor, recommending unit tests, and giving a final PR-readiness decision. I used dummy code examples to avoid confidential data. The goal is to reduce review cycles, improve code quality, and help developers submit cleaner, safer pull requests.

## Tools Used

- Python
- Streamlit
- Pytest
- Optional OpenAI API integration
- Local deterministic fallback analyzer

## Why This Is Useful

This prototype reduces review cycles by helping developers catch quality issues before opening a pull request. It can support engineering teams by improving consistency, encouraging better tests, identifying maintainability risks early, and helping junior developers learn from senior-style feedback.

## Deployment Steps

1. Go to Streamlit Community Cloud.
2. Sign in with GitHub.
3. Click "New app".
4. Select the repository: `careem-ai-pair-engineer`.
5. Select branch: `main`.
6. Set the main file path to `app.py`.
7. Click Deploy.
8. Copy the deployed app URL.

The app works without secrets using local fallback mode. If AI mode is needed, add `OPENAI_API_KEY` in Streamlit secrets. For this job submission, fallback mode is enough because the app demonstrates the workflow safely.

## Final Application Answer

```text
Challenge selected: The AI Pair Engineer

Prototype link: <Streamlit deployed app link>
GitHub link: <GitHub repository link>
Dataset: Not applicable - I used self-created dummy code snippets only.

Summary:
I built an AI Pair Engineer prototype that helps developers prepare code before human review. The assistant accepts a code snippet and reviews it for readability, maintainability, structure, design risks, and missing test cases. Instead of only pointing out syntax issues, it behaves like a senior pair engineer by explaining why the code may be risky, suggesting a cleaner refactor, recommending unit tests, and giving a final PR-readiness decision. I used dummy code examples to avoid confidential data. The goal is to reduce review cycles, improve code quality, and help developers submit cleaner, safer pull requests.
```

## Final Checklist

- App runs locally.
- Tests pass.
- README is polished.
- Screenshots are added.
- No secrets committed.
- GitHub repo is public.
- Streamlit app URL works.
- Submission summary has the final links.
- The app works without an API key.
- Project name and challenge selected are consistent everywhere.
