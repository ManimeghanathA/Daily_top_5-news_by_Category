# news/news_fetcher.py

import os
import math
import requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("NEWS_API_KEY", "")

def fetch_top_news(categories):
    """
    Fetch a total of 5 unique articles across the selected categories.
    Calculates per-category fetch count = ceil(5 / num_categories).
    Falls back to general if any category yields zero.
    """
    articles = []
    per_cat = math.ceil(5 / len(categories))  # e.g., 1 cat=>5, 2=>3, 3=>2

    for category in categories:
        # 1) Try 'everything' for relevancy
        url = (
            "https://newsapi.org/v2/everything"
            f"?q={category}"
            f"&pageSize={per_cat}"
            "&sortBy=relevancy"
            f"&apiKey={KEY}"
        )
        resp = requests.get(url).json()

        # 2) Fallback if none
        if resp.get("status") != "ok" or resp.get("totalResults", 0) == 0:
            url = (
                "https://newsapi.org/v2/top-headlines"
                "?category=general"
                f"&pageSize={per_cat}"
                f"&apiKey={KEY}"
            )
            resp = requests.get(url).json()

        # 3) Collect articles
        for art in resp.get("articles", []):
            title = art.get("title")
            link  = art.get("url")
            desc  = art.get("description") or art.get("content") or ""
            if title and link:
                articles.append({
                    "title": title.strip(),
                    "url": link,
                    "description": desc.strip()
                })

    # 4) De-duplicate and limit to 5 total
    seen, unique = set(), []
    for a in articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)
        if len(unique) >= 5:
            break

    return unique
