import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'subscribed.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            time TEXT,
            categories TEXT,
            subscribed_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(email, time, categories):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    subscribed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT OR REPLACE INTO users (email, time, categories, subscribed_at)
        VALUES (?, ?, ?, ?)
    ''', (email, time, ','.join(categories), subscribed_at))
    conn.commit()
    conn.close()

def get_user(email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "email": row[0],
            "time": row[1],
            "categories": row[2].split(','),
            "subscribed_at": row[3]
        }
    return None

def update_user(email, new_time, new_categories):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET time = ?, categories = ?
        WHERE email = ?
    ''', (new_time, ','.join(new_categories), email))
    conn.commit()
    conn.close()

def delete_user(email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE email = ?', (email,))
    conn.commit()
    conn.close()

def load_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    users = []
    for row in rows:
        users.append({
            "id": row[0],  # Using email as ID
            "email": row[0],
            "time": row[1],
            "categories": row[2].split(','),
            "subscribed_at": row[3]
        })
    return users


