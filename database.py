import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "news_analysis.db"

def get_connection():
    """Create a SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create the news_analysis table if it does not already exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS news_analysis (
                analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
                news_title TEXT NOT NULL,
                news_text TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                sentiment_score REAL NOT NULL,
                clickbait_status TEXT NOT NULL,
                warning_signals TEXT,
                credibility_score INTEGER NOT NULL,
                risk_category TEXT NOT NULL,
                summary TEXT,
                analyzed_date TEXT NOT NULL
            )
        """)
        conn.commit()

def save_analysis(news_title, news_text, sentiment, sentiment_score, clickbait_status,
                  warning_signals, credibility_score, risk_category, summary):
    """Insert one analysis record and return its new ID."""
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO news_analysis (
                news_title, news_text, sentiment, sentiment_score, clickbait_status,
                warning_signals, credibility_score, risk_category, summary, analyzed_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            news_title, news_text, sentiment, float(sentiment_score), clickbait_status,
            json.dumps(warning_signals, ensure_ascii=False), int(credibility_score),
            risk_category, summary, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        return cursor.lastrowid

def get_analyses():
    """Return all analyses newest first as dictionaries."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM news_analysis ORDER BY analyzed_date DESC, analysis_id DESC"
        ).fetchall()
    records = []
    for row in rows:
        item = dict(row)
        try:
            item["warning_signals"] = "; ".join(json.loads(item["warning_signals"] or "[]"))
        except (json.JSONDecodeError, TypeError):
            pass
        records.append(item)
    return records

def get_analysis_by_id(analysis_id):
    """Fetch a single saved record by its ID."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM news_analysis WHERE analysis_id = ?", (analysis_id,)
        ).fetchone()
    if not row:
        return None
    item = dict(row)
    try:
        item["warning_signals"] = "; ".join(json.loads(item["warning_signals"] or "[]"))
    except (json.JSONDecodeError, TypeError):
        pass
    return item

def delete_analysis(analysis_id):
    """Delete one record; parameterized SQL avoids unsafe string concatenation."""
    with get_connection() as conn:
        conn.execute("DELETE FROM news_analysis WHERE analysis_id = ?", (analysis_id,))
        conn.commit()
