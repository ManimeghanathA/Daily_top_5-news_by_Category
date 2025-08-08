# database/db_handler.py

import os
import uuid
import sqlite3
from contextlib import closing

# Path to the SQLite file, next to this script
DB_PATH = os.path.join(os.path.dirname(__file__), "subscriptions.db")

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
