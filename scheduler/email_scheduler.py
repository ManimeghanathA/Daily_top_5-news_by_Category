# scheduler/email_scheduler.py

import os
import datetime
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from apscheduler.schedulers.background import BackgroundScheduler
from database.db_handler import load_users
from news.news_fetcher import fetch_top_news

# ─── Load configuration from .env ─────────────────────────────────────────────
load_dotenv()
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 587
SMTP_LOGIN  = os.getenv("MAIL_USER")
SMTP_PASS   = os.getenv("MAIL_PASS")
BASE_URL    = os.getenv("BASE_URL", "http://127.0.0.1:5000")

# ─── Email Sending Logic ───────────────────────────────────────────────────────
def send_news_email(user):
    email      = user["email"]
    categories = user["categories"]
    user_id    = user["id"]

    # Fetch top 5 articles
    articles = fetch_top_news(categories)

    # Build HTML content
    if not articles:
        html = "<p>Sorry, we couldn’t fetch any news right now. Please try again later.</p>"
    else:
        html = """
        <h2>Your Top 5 News</h2>
        <ul style="list-style:none; padding:0;">
        """
        for art in articles:
            html += f"""
            <li style="margin-bottom:20px;">
              <a href="{art['url']}" style="font-size:18px; color:#1B4F72; text-decoration:none;">
                <strong>{art['title']}</strong>
              </a><br>
              <p style="margin:5px 0 0; color:#333;">{art['description']}</p>
            </li>
            """
        html += "</ul>"

    # Append Edit/Unsubscribe links
    edit_url  = f"{BASE_URL}/edit/{user_id}"
    unsub_url = f"{BASE_URL}/unsubscribe/{user_id}"
    html += f"""
      <hr>
      <p style="font-size:0.9em;">
        <a href="{edit_url}">✏️ Edit Subscription</a> |
        <a href="{unsub_url}">❌ Unsubscribe</a>
      </p>
    """

    # Compose and send the email
    msg = MIMEMultipart()
    msg["From"]    = SMTP_LOGIN
    msg["To"]      = email
    msg["Subject"] = "Your Daily News Digest"
    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_LOGIN, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        print(f"[{datetime.datetime.now()}] Email sent to {email}")
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")

# ─── Scheduler Job ────────────────────────────────────────────────────────────
def check_and_send():
    """
    Check current time against subscribers and send emails to those
    whose scheduled time matches the current HH:MM.
    """
    now = datetime.datetime.now().strftime("%H:%M")
    users = load_users()
    for user in users:
        if user.get("time") == now:
            send_news_email(user)

# ─── Scheduler Startup ────────────────────────────────────────────────────────
def start_scheduler():
    """
    Start the APScheduler to run `check_and_send` every minute.
    """
    scheduler = BackgroundScheduler()
    # Run check_and_send every 1 minute
    scheduler.add_job(
        check_and_send,
        trigger='interval',
        minutes=1,
        next_run_time=datetime.datetime.now()
    )
    scheduler.start()
    print("Scheduler started: running check_and_send every minute.")
