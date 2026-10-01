# AI Business Requirements Generator

> **Project Status**: *Not public yet; I'm cleaning it up and will publish it with a README and sample outputs.*

An AI-powered analyst automation project that converts messy stakeholder notes into structured Business Analyst documentation.

This project is designed for Business Analyst, Business Systems Analyst, Data Analyst, Operations Analyst, Project Analyst, and Product Analyst portfolios. It demonstrates how AI can support real analyst workflows such as requirements documentation, UAT preparation, traceability, and executive reporting.

## Problem Statement

Business Analysts often receive unclear information from meetings, emails, stakeholder conversations, or process complaints. Before a project can move forward, this raw input must be converted into structured business requirements, functional requirements, user stories, acceptance criteria, UAT test cases, risks, assumptions, and clarification questions.

This process can be repetitive and time-consuming. The goal of this project is to generate a strong first draft of BA documentation while keeping the analyst in control of review and validation.

## What the App Does

The app allows a user to paste unstructured stakeholder notes and generate:

- Business Requirements Document (BRD)
- Executive summary
- Business problem summary
- Stakeholders and personas
- Business requirements
- Functional requirements
- Non-functional requirements
- User stories
- Gherkin acceptance criteria
- UAT test cases
- Risks and assumptions
- Clarification questions
- Requirements Traceability Matrix (RTM)
- Jira-ready user stories
- BA quality review
- One-page executive summary


- This is not a generic chatbot project. It is built around a specific analyst workflow:

1. Capture messy stakeholder input.
2. Convert it into structured BA documentation.
3. Validate the output through traceability and quality review.
4. Export the final analyst pack.
5. Save previous sessions for review.

## Tech Stack

- Python 3.10+
- Streamlit
- Google Gemini API using `google-genai`
- SQLite
- Pandas
- Python dotenv
- Markdown exports

## Repository Structure

```text
ai-business-requirements-generator/
├── app.py                  # Main Streamlit application
├── prompts.py              # AI prompts and learning explanations
├── database.py             # SQLite storage layer
├── utils.py                # Helper functions for validation, parsing, and exports
├── mock_data.py            # Canned and dynamic mocks for Demo Mode
├── requirements.txt        # Python dependencies
├── .env.example            # Example API key environment file
├── .gitignore              # Files to exclude from GitHub
├── .streamlit/
│   └── config.toml         # Streamlit theme settings
├── sample_inputs/
│   ├── refund_process_notes.txt
│   └── customer_onboarding_notes.txt
├── sample_outputs/
│   └── README.md
└── docs/
    └── learning_guide.md
```

## How to Run Locally

### 1. Create and activate a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the App

```bash
streamlit run app.py
```

### 4. Running Modes

- **Demo Mode (No API key required)**: The app launches in Demo Mode by default. You can test and explore pre-built sample deliverables (Refund Process, Customer Onboarding) or enter custom notes with simulated outputs immediately.
- **Gemini Mode (Live API)**: Switch the sidebar mode to *Gemini Mode* and enter your Gemini API Key in the sidebar or create a `.env` file:
  ```text
  GEMINI_API_KEY=your_api_key_here
  ```

## Sample Input

```text
The customer service team is receiving too many complaints about delayed refund processing. Currently, refunds are tracked manually in Excel and there is no clear status visibility for customers or managers. Agents need to check multiple systems before confirming refund status. Managers want a dashboard showing pending refunds, delayed refunds, refund amount, and responsible team. The new process should reduce manual follow-ups and improve transparency.
```

## Main Features

### 1. BRD Generator

Converts raw stakeholder notes into a structured Business Requirements Document.

### 2. Requirements Traceability Matrix

Links business requirements to functional requirements, user stories, and UAT test cases.

### 3. Jira-Ready User Stories

Formats user stories and acceptance criteria into a table suitable for backlog preparation.

### 4. BA Quality Review

Reviews the generated BRD for clarity, completeness, traceability, testability, risks, and stakeholder readiness.

### 5. Executive Summary

Creates a one-page non-technical summary for managers and stakeholders.

### 6. Saved History

Stores generated documents locally using SQLite so previous outputs can be reviewed, loaded, exported, or deleted.

### 7. Learning Guide

Explains why each project step matters in simple analyst language, making this project useful for learning while building.

## Business Value

This project demonstrates how AI can help analysts:

- Reduce repetitive documentation effort
- Create consistent first drafts of BA artefacts
- Improve requirement clarity
- Prepare UAT test cases faster
- Identify missing information through clarification questions
- Support stakeholder communication
- Connect business requirements to testing through traceability

## What I Learned

- How to design prompts for structured business outputs
- How to build a Streamlit analyst automation app
- How to use an LLM API inside a business workflow
- How to store generated outputs using SQLite
- How to create traceability between requirements and test cases
- How to review AI-generated outputs instead of accepting them blindly
- How to explain AI automation in a Business Analyst context


## Future Improvements

- Word document export
- PDF export
- Editable generated output before saving
- Login and multi-user project workspace
- Jira API integration
- Power BI-style dashboard showing generated document statistics
- Model comparison between Gemini, OpenAI, and local LLMs
