import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("genai_history.db")

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                source_name TEXT,
                task TEXT NOT NULL,
                word_count INTEGER DEFAULT 0,
                output TEXT NOT NULL,
                model TEXT
            )
        """)

def save_record(source_name, task, word_count, output, model):
    with connect() as conn:
        conn.execute(
            "INSERT INTO history (created_at, source_name, task, word_count, output, model) VALUES (?, ?, ?, ?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), source_name, task, word_count, output, model)
        )

def get_history(limit=100):
    with connect() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM history ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(row) for row in rows]
