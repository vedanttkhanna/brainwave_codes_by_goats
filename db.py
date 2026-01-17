import sqlite3
from datetime import datetime

DB_PATH = "hackathon.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rules_queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id TEXT,
        question TEXT,
        answer TEXT,
        timestamp TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS github_activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id TEXT,
        repo_url TEXT,
        activity_status TEXT,
        commits_24h INTEGER,
        commits_72h INTEGER,
        contributors INTEGER,
        last_commit_time TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()
