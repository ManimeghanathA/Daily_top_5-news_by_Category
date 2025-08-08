import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from database.db_handler import load_users
from news.news_fetcher import get_news

load_dotenv()
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 587
SMTP_LOGIN  = os.getenv("EMAIL_ADDRESS")
SMTP_PASS   = os.getenv("EMAIL_PASSWORD")
BASE_URL    = os.getenv("BASE_URL", "http://127.0.0.1:5000")

def send_news_email(user):
    email = user["email"]
    categories = user["categories"]
    user_id = user["id"]

    articles = get_news(categories)
    if not articles:
        html = "<p>No news available right now. Try again later.</p>"
    else:
        html = "<h3>Your Daily News</h3><ul>"
        for article in articles:
            html += f"<li><a href='{article['url']}'>{article['title']}</a></li>"
        html += "</ul>"

    edit_url = f"{BASE_URL}/edit/{user_id}"
    unsub_url = f"{BASE_URL}/unsubscribe/{user_id}"
    html += f"<hr><p><a href='{edit_url}'>Edit Subscription</a> | <a href='{unsub_url}'>Unsubscribe</a></p>"

    msg = MIMEMultipart()
    msg["From"] = SMTP_LOGIN
    msg["To"] = email
    msg["Subject"] = "Your Daily News Digest"
    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_LOGIN, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        print(f"[✔] Email sent to {email}")
    except Exception as e:
        print(f"[✘] Failed to send email to {email}: {e}")

def check_and_send():
    now = datetime.datetime.now().strftime("%H:%M")
    users = load_users()
    for user in users:
        if user["time"] == now:
            send_news_email(user)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_send, 'interval', minutes=1)
    scheduler.start()
    print("Scheduler started.")
