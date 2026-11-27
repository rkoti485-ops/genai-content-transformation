"""SQLite database for AI content transformation history."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "history.db"


def get_connection():
    """Create a connection to the project database."""
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the history table if it does not exist."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL DEFAULT
                    (datetime('now', 'localtime')),
                source_name TEXT NOT NULL,
                task TEXT NOT NULL,
                word_count INTEGER DEFAULT 0,
                output TEXT,
                model TEXT
            )
        """)
        connection.commit()


def save_record(source_name, task, word_count, output, model):
    """Save one completed AI transformation."""
    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO history
            (source_name, task, word_count, output, model)
            VALUES (?, ?, ?, ?, ?)
        """, (
            source_name,
            task,
            int(word_count or 0),
            output,
            model
        ))
        connection.commit()
        return cursor.lastrowid


def get_history(limit=None):
    """Retrieve transformation history, newest first."""
    query = """
        SELECT id, created_at, source_name, task,
               word_count, output, model
        FROM history
        ORDER BY id DESC
    """

    if limit is not None:
        query += " LIMIT ?"
        params = (int(limit),)
    else:
        params = ()

    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()

    return [dict(row) for row in rows]


def delete_record(record_id):
    """Delete one history record by its ID."""
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM history WHERE id = ?",
            (int(record_id),)
        )
        connection.commit()
        return cursor.rowcount > 0


def clear_history():
    """Delete all transformation history."""
    with get_connection() as connection:
        connection.execute("DELETE FROM history")
        connection.commit()