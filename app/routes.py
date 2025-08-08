from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
# Note: we do NOT import load_users or send_news_email here at top to avoid circular imports

app = Blueprint('app', __name__)

@app.route("/", methods=["GET", "POST"])
def index():
    from database.db_handler import add_user, load_users  # local import
    email      = request.form.get("email", "").strip() if request.method == "POST" else None
    time_str   = request.form.get("time", "").strip() if request.method == "POST" else None
    categories = request.form.getlist("categories") if request.method == "POST" else []

    if request.method == "POST":
        # Validate
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

    # On GET, load subscriptions to display
    subs = None
    try:
        from database.db_handler import load_users
        subs = load_users()
    except:
        subs = []
    return render_template("index.html", subscriptions=subs)


@app.route("/unsubscribe/<user_id>")
def unsubscribe(user_id):
    from database.db_handler import delete_user
    delete_user(user_id)
    flash("You have been unsubscribed successfully.", "success")
    return redirect(url_for('app.index'))


@app.route("/edit/<user_id>", methods=["GET", "POST"])
def edit_subscription(user_id):
    from database.db_handler import load_users, update_user
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

    # GET: render form with user data
    return render_template("edit.html", user=user)


# ── Debug endpoints ────────────────────────────────────────────────────────────

@app.route("/_debug/subscriptions")
def debug_subscriptions():
    from database.db_handler import load_users
    users = load_users()
    return jsonify(users)

@app.route("/_debug/send-all")
def debug_send_all():
    from database.db_handler import load_users
    from scheduler.email_scheduler import send_news_email
    users = load_users()
    for u in users:
        send_news_email(u)
    return f"Attempted sending to {len(users)} users; check logs."



@app.route("/_debug/db-files")
def debug_db_files():
    # List files in your database directory
    db_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, "database")
    files = os.listdir(db_dir)
    return jsonify({"database_dir": db_dir, "files": files})

