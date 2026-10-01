# Run This First

This is the improved version of the AI Business Requirements Generator.

## What changed from the base version

1. Cleaner prompt design with stricter BA output rules.
2. Added Executive Summary, Stakeholders, Interview Explanation, and Quality Review.
3. Added a Learning Guide page so you understand why each feature exists.
4. Improved database structure for BRD, RTM, Jira stories, quality review, and executive summary.
5. Added validation before sending notes to the AI.
6. Added sample inputs.
7. Added .gitignore and .env.example for safer GitHub upload.
8. Rewrote README in a more professional and realistic way.

## How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Paste your Gemini API key in the sidebar.
