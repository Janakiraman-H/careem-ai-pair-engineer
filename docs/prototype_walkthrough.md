# Prototype Walkthrough

## What The App Does

Careem AI Pair Engineer reviews short code snippets and returns PR-readiness feedback. It focuses on readability, maintainability, design risks, refactoring, test coverage, and a final decision badge.

## Selecting A Sample

The sidebar includes a sample snippet selector with self-created examples across Python, JavaScript, SQL, and Java. Selecting a sample loads intentionally imperfect code into the editor so the user can immediately try the review flow.

## Reviewing Code

The user can edit the snippet, choose a programming language, set risk tolerance, and click `Review Code`. In local mode, the deterministic analyzer reviews the code using transparent rules. In AI mode, the app uses OpenAI if an API key is available. If the key is missing or the API call fails, it automatically uses the local analyzer.

## Review Sections

- Positive note: What is already clear or useful in the snippet.
- Readability and maintainability issues: Naming, magic numbers, hardcoded rules, long code, and related concerns.
- Design or architecture risks: Missing validation, weak error handling, broad SQL queries, and mixed responsibilities.
- Suggested refactor: A concise improvement path that keeps the change practical.
- Recommended tests: Unit or integration tests that would raise confidence before review.
- Risk score: A 1-10 score based on detected risk signals.
- Final PR readiness decision: Ready for review, Needs cleanup, or Needs rework.

## Risk Score Calculation

Fallback mode starts at 1 and adds one point for each detected signal: magic numbers, missing validation, missing error handling, hardcoded business rules, SQL `SELECT *`, too many branches, long code, and weak naming. The score is capped at 10.

Decision mapping:

- 1-3: Ready for review
- 4-6: Needs cleanup
- 7-10: Needs rework

## Future Extensions

This prototype could be extended to review real pull requests by integrating with GitHub. It could summarize changed files, comment on risky diffs, enforce team coding standards, recommend tests based on touched modules, and run as a CI check before human review. Teams could also configure rules for service boundaries, logging, observability, security, and domain-specific patterns.

