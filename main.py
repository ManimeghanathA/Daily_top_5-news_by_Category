import os
from flask import Flask
from app.routes import app as routes_blueprint
from  scheduler.email_scheduler import start_scheduler
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__,
            static_folder="app/static",
            template_folder="app/templates")
app.secret_key = os.urandom(24)  # secure random key for session/flash
app.register_blueprint(routes_blueprint)

if __name__ == "__main__":
            start_scheduler()
            port = int(os.environ.get("PORT", 5000))
            app.run(host='0.0.0.0', port=port, debug=True)

