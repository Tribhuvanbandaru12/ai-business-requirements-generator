"""Helper functions used by the Streamlit app."""

from __future__ import annotations

import re
from datetime import datetime

SECTION_MAP = {
    "Executive Summary": "executive",
    "Business Problem Summary": "problem",
    "Stakeholders and Personas": "stakeholders",
    "Business Requirements": "business_requirements",
    "Functional Requirements": "functional_requirements",
    "Non-Functional Requirements": "non_functional_requirements",
    "User Stories": "user_stories",
    "Acceptance Criteria": "acceptance_criteria",
    "UAT Test Cases": "uat",
    "Requirements Traceability Matrix": "rtm_section",
    "Risks & Assumptions": "risks_assumptions",
    "Risks": "risks",
    "Assumptions": "assumptions",
    "Clarification Questions": "questions",
    "Suggested Next Steps": "next_steps",
    "Analyst Interview Explanation": "interview",
}


def make_title(notes: str, max_length: int = 55) -> str:
    """Create a short title from raw notes."""
    clean = " ".join(notes.split())
    if not clean:
        return f"Untitled Generation {datetime.now().strftime('%H:%M')}"
    return clean[:max_length].rstrip() + ("..." if len(clean) > max_length else "")


def parse_markdown_sections(markdown_text: str) -> dict[str, str]:
    """Split a generated BRD into logical sections based on Markdown headings."""
    parsed = {}
    matches = list(re.finditer(r"^##\s+\d+\.\s+(.+)$", markdown_text, flags=re.MULTILINE))

    for i, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown_text)
        key = None
        for known_heading, mapped_key in SECTION_MAP.items():
            if heading.lower().startswith(known_heading.lower()):
                key = mapped_key
                break
        if key:
            parsed[key] = markdown_text[start:end].strip()

    return parsed


def validate_notes(notes: str) -> tuple[bool, str]:
    """Basic validation before sending text to the AI model."""
    clean = notes.strip()
    if not clean:
        return False, "Please enter stakeholder notes before generating documentation."
    if len(clean.split()) < 20:
        return False, "Please add a little more context. Aim for at least 3-4 sentences of stakeholder notes."
    if len(clean) > 12000:
        return False, "The notes are too long for this version. Please shorten them or paste the most important parts."
    return True, "Notes look ready."


def combine_export_bundle(
    generated_doc: str,
    rtm_doc: str = "",
    jira_doc: str = "",
    quality_review: str = "",
    executive_summary: str = "",
) -> str:
    """Create one combined Markdown export."""
    parts = [generated_doc.strip()]
    optional_sections = [
        ("Requirements Traceability Matrix", rtm_doc),
        ("Jira-Ready User Stories", jira_doc),
        ("BA Quality Review", quality_review),
        ("One-Page Executive Summary", executive_summary),
    ]
    for title, content in optional_sections:
        if content and content.strip():
            parts.append(f"\n---\n\n# {title}\n\n{content.strip()}")
    return "\n\n".join(parts)
