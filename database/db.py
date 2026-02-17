import sqlite3
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "hostel_expenses.db"

def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            meal_type TEXT,
            description TEXT,
            total_cost REAL NOT NULL,
            created_at TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS meal_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER,
            friend_name TEXT,
            share_cost REAL,
            FOREIGN KEY(meal_id) REFERENCES meals(id)
        )
        """)
        conn.commit()

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def insert_meal(date, meal_type, description, total_cost, participants, share):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO meals (date, meal_type, description, total_cost, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (date, meal_type, description, total_cost, datetime.utcnow().isoformat()))
        meal_id = cur.lastrowid

        for p in participants:
            cur.execute("""
                INSERT INTO meal_participants (meal_id, friend_name, share_cost)
                VALUES (?, ?, ?)
            """, (meal_id, p, share))

def fetch_meals(start=None, end=None):
    with get_connection() as conn:
        cur = conn.cursor()
        query = "SELECT * FROM meals WHERE 1=1"
        params = []
        if start:
            query += " AND date >= ?"
            params.append(start)
        if end:
            query += " AND date <= ?"
            params.append(end)
        cur.execute(query, params)
        return cur.fetchall()

def fetch_participant_totals(start=None, end=None):
    with get_connection() as conn:
        cur = conn.cursor()
        query = """
        SELECT friend_name, SUM(share_cost)
        FROM meal_participants mp
        JOIN meals m ON mp.meal_id = m.id
        WHERE 1=1
        """
        params = []
        if start:
            query += " AND m.date >= ?"
            params.append(start)
        if end:
            query += " AND m.date <= ?"
            params.append(end)

        query += " GROUP BY friend_name"
        cur.execute(query, params)
        return cur.fetchall()
