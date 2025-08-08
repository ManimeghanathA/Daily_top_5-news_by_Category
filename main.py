import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Initialize database (after .env is loaded)
from database.db_handler import init_db
init_db()

# Setup Flask app
app = Flask(__name__,
            static_folder="app/static",
            template_folder="app/templates")

# Use secret key from environment, fallback if not set
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# Register routes
from app.routes import app as routes_blueprint
app.register_blueprint(routes_blueprint)

# Start scheduler
from scheduler.email_scheduler import start_scheduler

if __name__ == "__main__":
    start_scheduler()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
