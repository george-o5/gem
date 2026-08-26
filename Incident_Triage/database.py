import sqlite3
import json
from datetime import datetime
from typing import Optional

DB_FILE = "incidents.db"


def init_db():
    """Creates the incidents table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT,
            raw_log TEXT,
            root_cause TEXT,
            severity TEXT,
            fix TEXT,
            status TEXT DEFAULT 'OPEN',
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_incident(service: str, raw_log: str, root_cause: str, severity: str, fix: str) -> int:
    """Saves a diagnosed incident and returns its ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO incidents (service, raw_log, root_cause, severity, fix, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (service, raw_log, root_cause, severity, fix, "OPEN", now))
    incident_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return incident_id


def get_all_incidents():
    """Fetches all incidents, newest first."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_status(incident_id: int, new_status: str):
    """Marks an incident as RESOLVED or OPEN."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE incidents SET status = ? WHERE id = ?", (new_status, incident_id))
    conn.commit()
    conn.close()


# Auto-init on import
init_db()