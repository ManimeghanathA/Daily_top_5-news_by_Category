# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db_handler import add_user, load_users, delete_user, update_user
import os
from scheduler.email_scheduler import send_news_email
from flask import jsonify

app = Blueprint('app', __name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email      = request.form.get("email", "").strip()
        time_str   = request.form.get("time", "").strip()
        categories = request.form.getlist("categories")

        # Validation
        errors = False
        if not email:
            flash("Email is required.", "error"); errors = True
        if not time_str:
            flash("Time is required.", "error"); errors = True
        if not (1 <= len(categories) <= 3):
            flash("Select between 1 and 3 categories.", "error"); errors = True

        if errors:
            return redirect(url_for('app.index'))

        add_user(email, time_str, categories)
        flash(
            f"Subscription successful for {email}! "
            f"News will be sent daily at {time_str} for: {', '.join(categories)}",
            "success"
        )
        return redirect(url_for('app.index'))

    # GET → load all subscriptions
    subs = load_users()
    return render_template("index.html", subscriptions=subs)


@app.route("/unsubscribe/<user_id>")
def unsubscribe(user_id):
    delete_user(user_id)
    flash("You have been unsubscribed successfully.", "success")
    return redirect(url_for('app.index'))


@app.route("/edit/<user_id>", methods=["GET", "POST"])
def edit_subscription(user_id):
    # Load and find the specific user
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        flash("Subscription not found.", "error")
        return redirect(url_for('app.index'))

    if request.method == "POST":
        email      = request.form.get("email", "").strip()
        time_str   = request.form.get("time", "").strip()
        categories = request.form.getlist("categories")

        errors = False
        if not email:
            flash("Email is required.", "error"); errors = True
        if not time_str:
            flash("Time is required.", "error"); errors = True
        if not (1 <= len(categories) <= 3):
            flash("Select between 1 and 3 categories.", "error"); errors = True

        if errors:
            return redirect(url_for('app.edit_subscription', user_id=user_id))

        update_user(user_id, email, time_str, categories)
        flash(
            f"Subscription updated for {email}! "
            f"News will be sent daily at {time_str} for: {', '.join(categories)}",
            "success"
        )
        return redirect(url_for('app.index'))

    # GET → render edit form with `user` provided
    return render_template("edit.html", user=user)


@app.route("/test-mail")
def test_mail():
    """
    Manually trigger an email to verify SMTP in production.
    """
    # Use your own address or the MAIL_USER env var
    test_email = os.getenv("MAIL_USER")
    if not test_email:
        return "MAIL_USER env var not set", 500

    # A dummy user payload
    user = {
        "email": test_email,
        "categories": ["technology","sports"],
        "id": "test-id"
    }

    send_news_email(user)
    return "Test mail attempted—check your inbox and the server logs."


@app.route("/_debug/subscriptions")
def debug_subscriptions():
    users = load_users()
    return jsonify(users)



@app.route("/_debug/send-all")
def debug_send_all():
    users = load_users()
    for u in users:
        send_news_email(u)
    return f"Attempted sending to {len(users)} users; check logs."



