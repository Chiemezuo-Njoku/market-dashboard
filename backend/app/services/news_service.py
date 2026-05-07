import requests
import os
import time
from dotenv import load_dotenv
from app.services.sentiment_service import analyze_sentiment

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

cache = {}
CACHE_DURATION = 300  # Cache duration in seconds

def get_news(ticker: str):
    ticker = ticker.upper()

    if GNEWS_API_KEY is None:
        return {"error": "Missing GNEWS_API_KEY environment variable"}

    if ticker in cache:
        cached_data, timestamp = cache[ticker]
        if time.time() - timestamp < CACHE_DURATION:
            return cached_data

    url = "https://gnews.io/api/v4/search"
    query = f"{ticker} stock OR {ticker} company"

    params = {
        "q": query,
        "lang": "en",
        "max": 5,
        "token": GNEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.RequestException:
        return {"error": "Unable to contact news service"}

    if response.status_code != 200:
        return {"error": "Failed to fetch news", "status_code": response.status_code}

    try:
        data = response.json()
    except ValueError:
        return {"error": "Invalid JSON response from news service"}

    articles_data = data.get("articles")
    if not isinstance(articles_data, list):
        return {"error": "Unexpected news API response"}

    articles = []
    for article in articles_data[:5]:
        title = article.get("title") or article.get("headline") or ""
        source_info = article.get("source") or {}
        source_name = source_info.get("name") if isinstance(source_info, dict) else source_info
        articles.append({
            "title": title,
            "source": source_name or "Unknown",
            "url": article.get("url", ""),
            "sentiment": analyze_sentiment(title)
        })

    cache[ticker] = (articles, time.time())
    return articles