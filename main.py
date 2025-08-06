import os
from flask import Flask
from app.routes import app as routes_blueprint
from scheduler.email_scheduler import start_scheduler
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__,
            static_folder="app/static",
            template_folder="app/templates")
app.secret_key = os.urandom(24)  # secure random key for session/flash
app.register_blueprint(routes_blueprint)

if __name__ == "__main__":
    # Only start scheduler in the child process to avoid duplicates
    if os.getenv("WERKZEUG_RUN_MAIN") == "true":
        start_scheduler()
    app.run(debug=True)
