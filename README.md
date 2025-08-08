📰 Daily Top 5 News by Category
A personalized news scheduler that sends the top 5 unbiased news articles directly to your email based on your selected categories and preferred delivery time.

🔗 Live Website: https://daily-top-5-news-by-category-1.onrender.com

Features
- 🌐 Beautiful, responsive web UI built with Flask and HTML/CSS
- 🗂️ Choose 3 news categories from a curated list
- ⏰ Set your preferred time to receive daily news
- 📩 Receive top 5 unbiased news articles in your email inbox
- 🔄 Easily edit or unsubscribe anytime via a simple UI
- 🧠 Backend built with Python, including news scraping, email scheduling, and database handling

📁 Project Structure
news_scheduler_project/
├── app/
│   ├── static/
│   ├── templates/
│   └── main.py                 # Flask web application
├── scheduler/
│   └── email_scheduler.py     # Handles sending emails at the scheduled time
├── news/
│   └── news_fetcher.py        # Fetches top 5 news from selected categories
├── database/
│   ├── users.json             # Stores registered user data
│   └── db_handler.py          # Handles read/write to users.json
├── requirements.txt
└── README.md

🚀 How It Works
User visits the web UI and submits:

Email ID

Preferred Time (e.g. 08:00 AM)

3 News Categories

User data is stored in users.json (or SQLite if extended).

A background scheduler sends emails at the chosen time using smtplib.

News is fetched using NewsAPI or custom web scraping logic and formatted into an email.

🛠️ Tech Stack
Backend: Python, Flask

Frontend: HTML, CSS (Jinja2 Templates)

Scheduling: apscheduler

Emailing: smtplib, email.mime

Data Storage: JSON (or SQLite upgradeable)

Hosting: Render.com

Setup Instructions (Local Development)
Clone the repo

bash
Copy
Edit
git clone https://github.com/yourusername/news_scheduler_project.git
cd news_scheduler_project
Create virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the application

bash
Copy
Edit
python app/main.py
Visit http://127.0.0.1:5000 in your browser.

🌐 Deployment
The app is live on Render.

Production URL: https://daily-top-5-news-by-category-1.onrender.com

Note: For email to work, make sure to configure your sender email credentials in a .env file or environment variables on Render.

🧪 Todo / Improvements
 Migrate from JSON to SQLite for scalable storage

 Add user authentication and verification

 Improve logging and email status tracking

 Add dark mode UI

 Add support for multiple time zones

🤝 Contribution
Feel free to fork this repo and contribute! Suggestions, issues, and pull requests are welcome.

🧑‍💻 Author
Manimeghanath
AI & Software Enthusiast
GitHub: @ManimeghanathA


