# database/db_handler.py

import os
import uuid
import sqlite3
from contextlib import closing

# database/db_handler.py

import os, uuid, sqlite3
from contextlib import closing

# Compute project root = parent of this file's directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DB_DIR       = os.path.join(PROJECT_ROOT, "database")
DB_PATH      = os.path.join(DB_DIR, "subscriptions.db")

def init_db():
    # Make sure the database directory exists
    os.makedirs(DB_DIR, exist_ok=True)
    first_time = not os.path.exists(DB_PATH)
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id TEXT PRIMARY KEY,
                email TEXT NOT NULL,
                time TEXT NOT NULL,
                categories TEXT NOT NULL
            )
        """)
        conn.commit()
    if first_time:
        print(f"[db_handler] Created new SQLite DB at {DB_PATH}")

# ... rest of your functions unchanged, just keep init_db() at top of each CRUD operation ...


# Ensure the database and table exist
def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id TEXT PRIMARY KEY,
                email TEXT NOT NULL,
                time TEXT NOT NULL,
                categories TEXT NOT NULL -- stored as comma-separated string
            )
        """)
        conn.commit()

# Convert a DB row to a user dict
def row_to_user(row):
    return {
        "id": row[0],
        "email": row[1],
        "time": row[2],
        "categories": row[3].split(",") if row[3] else []
    }

# Load all users
def load_users():
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("SELECT id, email, time, categories FROM subscriptions")
        rows = c.fetchall()
    return [row_to_user(r) for r in rows]

# Add a new user
def add_user(email, time_str, categories):
    init_db()
    user_id = str(uuid.uuid4())
    cats = ",".join(categories)
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO subscriptions (id, email, time, categories) VALUES (?, ?, ?, ?)",
            (user_id, email, time_str, cats)
        )
        conn.commit()
    return user_id

# Delete a user by id
def delete_user(user_id):
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM subscriptions WHERE id = ?", (user_id,))
        conn.commit()

# Update an existing user
def update_user(user_id, email, time_str, categories):
    init_db()
    cats = ",".join(categories)
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("""
            UPDATE subscriptions
            SET email = ?, time = ?, categories = ?
            WHERE id = ?
        """, (email, time_str, cats, user_id))
        conn.commit()
