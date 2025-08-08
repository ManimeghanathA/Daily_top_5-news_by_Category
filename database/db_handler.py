# database/db_handler.py

import os, json, uuid
import datetime
from database.db_handler import load_users


USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def add_user(email, time_str, categories):
    users = load_users()
    user_id = str(uuid.uuid4())
    users.append({
        "id": user_id,
        "email": email,
        "time": time_str,
        "categories": categories
    })
    save_users(users)
    return user_id

def delete_user(user_id):
    users = load_users()
    users = [u for u in users if u["id"] != user_id]
    save_users(users)

def update_user(user_id, email, time_str, categories):
    users = load_users()
    for u in users:
        if u["id"] == user_id:
            u["email"] = email
            u["time"] = time_str
            u["categories"] = categories
            break
    save_users(users)

def check_and_send():
    now = datetime.datetime.utcnow().strftime("%H:%M")     # use UTC for consistency
    users = load_users()
    print(f"[Scheduler] UTC now={now} | loaded {len(users)} users: {users}")
    for user in users:
        if user.get("time") == now:
            print(f"[Scheduler] Sending to {user['email']}")
            send_news_email(user)
