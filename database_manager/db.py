import sqlite3
from datetime import datetime

from config import DATABASE_PATH


def _get_conn():
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _get_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            title TEXT,
            platform TEXT,
            quality TEXT,
            location TEXT,
            status TEXT,
            date TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def add_entry(url, title, platform, quality, location, status):
    conn = _get_conn()
    conn.execute(
        "INSERT INTO history (url, title, platform, quality, location, status, date) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (url, title, platform, quality, location, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()


def get_history(limit=200):
    conn = _get_conn()
    rows = conn.execute("SELECT * FROM history ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_entry(entry_id):
    conn = _get_conn()
    conn.execute("DELETE FROM history WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()


def clear_history():
    conn = _get_conn()
    conn.execute("DELETE FROM history")
    conn.commit()
    conn.close()


def search_history(term):
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM history WHERE title LIKE ? OR url LIKE ? ORDER BY id DESC",
        (f"%{term}%", f"%{term}%"),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
