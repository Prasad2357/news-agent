# tools/dedupe.py
import sqlite3
import os
from datetime import datetime
from config import DB_PATH

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sent (
        id TEXT PRIMARY KEY,
        url TEXT,
        title TEXT,
        sent_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def is_sent(item_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM sent WHERE id=?", (item_id,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def mark_sent(item):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO sent(id, url, title, sent_at) VALUES(?,?,?,?)",
                (item["id"], item.get("url"), item.get("title"), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
