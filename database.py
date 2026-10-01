"""SQLite database functions for saving generated BA documents.

Simple explanation:
The Streamlit app is the screen. This file is the app's memory.
It stores generated BRDs, RTMs, Jira stories, and quality reviews locally.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).with_name("history.db")


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    """Create the history table if it does not already exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS requirements_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                title TEXT NOT NULL,
                domain TEXT,
                notes TEXT NOT NULL,
                generated_doc TEXT NOT NULL,
                rtm_doc TEXT DEFAULT '',
                jira_doc TEXT DEFAULT '',
                quality_review TEXT DEFAULT '',
                executive_summary TEXT DEFAULT ''
            )
            """
        )
        conn.commit()


def save_generation(
    title: str,
    notes: str,
    generated_doc: str,
    domain: str = "General Business Process",
    rtm_doc: str = "",
    jira_doc: str = "",
    quality_review: str = "",
    executive_summary: str = "",
) -> int:
    """Save a generated BRD and return its database ID."""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO requirements_history
            (created_at, title, domain, notes, generated_doc, rtm_doc, jira_doc, quality_review, executive_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (created_at, title, domain, notes, generated_doc, rtm_doc, jira_doc, quality_review, executive_summary),
        )
        conn.commit()
        return int(cursor.lastrowid)


def update_generation_addons(
    record_id: int,
    rtm_doc: Optional[str] = None,
    jira_doc: Optional[str] = None,
    quality_review: Optional[str] = None,
    executive_summary: Optional[str] = None,
) -> None:
    """Update optional documents for an existing generation."""
    updates = []
    values = []

    if rtm_doc is not None:
        updates.append("rtm_doc = ?")
        values.append(rtm_doc)
    if jira_doc is not None:
        updates.append("jira_doc = ?")
        values.append(jira_doc)
    if quality_review is not None:
        updates.append("quality_review = ?")
        values.append(quality_review)
    if executive_summary is not None:
        updates.append("executive_summary = ?")
        values.append(executive_summary)

    if not updates:
        return

    values.append(record_id)
    query = f"UPDATE requirements_history SET {', '.join(updates)} WHERE id = ?"

    with get_connection() as conn:
        conn.execute(query, values)
        conn.commit()


def get_history(search_text: str = "") -> list[tuple]:
    """Return saved generations ordered by newest first."""
    with get_connection() as conn:
        if search_text.strip():
            like_value = f"%{search_text.strip()}%"
            cursor = conn.execute(
                """
                SELECT id, created_at, title, domain, notes
                FROM requirements_history
                WHERE title LIKE ? OR notes LIKE ? OR domain LIKE ?
                ORDER BY id DESC
                """,
                (like_value, like_value, like_value),
            )
        else:
            cursor = conn.execute(
                """
                SELECT id, created_at, title, domain, notes
                FROM requirements_history
                ORDER BY id DESC
                """
            )
        return cursor.fetchall()


def get_record(record_id: int) -> Optional[tuple]:
    """Fetch one full saved generation."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT id, created_at, title, domain, notes, generated_doc, rtm_doc, jira_doc, quality_review, executive_summary
            FROM requirements_history
            WHERE id = ?
            """,
            (record_id,),
        )
        return cursor.fetchone()


def delete_record(record_id: int) -> None:
    """Delete one saved generation."""
    with get_connection() as conn:
        conn.execute("DELETE FROM requirements_history WHERE id = ?", (record_id,))
        conn.commit()
