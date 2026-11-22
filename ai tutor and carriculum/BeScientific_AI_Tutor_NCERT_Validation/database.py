import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "be_scientific.db"

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with get_connection() as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT NOT NULL,
            concept_id TEXT NOT NULL, question_id TEXT NOT NULL,
            is_correct INTEGER NOT NULL, mastery REAL NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)""")

def save_attempt(student_id, concept_id, question_id, is_correct, mastery):
    with get_connection() as connection:
        connection.execute("""INSERT INTO attempts
            (student_id, concept_id, question_id, is_correct, mastery)
            VALUES (?, ?, ?, ?, ?)""",
            (student_id, concept_id, question_id, int(is_correct), mastery))

def get_student_progress(student_id):
    with get_connection() as connection:
        rows = connection.execute("""SELECT concept_id, question_id, is_correct, mastery, created_at
            FROM attempts WHERE student_id = ? ORDER BY id DESC""", (student_id,)).fetchall()
    return [dict(row) for row in rows]
