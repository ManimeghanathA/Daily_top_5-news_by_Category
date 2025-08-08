import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "subscribed.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                time TEXT NOT NULL,
                categories TEXT NOT NULL
            )
        ''')
        conn.commit()

def add_user(email, time, categories):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO subscribers (email, time, categories)
                VALUES (?, ?, ?)
            ''', (email, time, ','.join(categories)))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # email exists

def update_user(user_id, email, time, categories):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE subscribers
            SET email = ?, time = ?, categories = ?
            WHERE id = ?
        ''', (email, time, ','.join(categories), user_id))
        conn.commit()

def delete_user(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM subscribers WHERE id = ?', (user_id,))
        conn.commit()

def load_users():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM subscribers')
        rows = cursor.fetchall()
        return [
            {
                "id": str(row["id"]),
                "email": row["email"],
                "time": row["time"],
                "categories": row["categories"].split(",")
            } for row in rows
        ]
