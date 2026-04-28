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

    if ticker in cache:
        cached_data, timestamp = cache[ticker]
        if time.time() - timestamp < CACHE_DURATION:
            return cached_data
        
    url = "https://gnews.io/api/v4/search"

    # Better search query
    query = f"{ticker} stock OR {ticker} company"

    params = {
        "q": query,
        "lang": "en",
        "max": 5,
        "token": GNEWS_API_KEY
    }

   
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {"error": "Failed to fetch news(possible rate limit)"}
    
    data = response.json()

    articles = []

    # Handle case where API fails
    if "articles" not in data:
        return {"error": "Failed to fetch news"}

    for article in data["articles"]:
        sentiment = analyze_sentiment(article["title"])
        articles.append({
            "title": article["title"],
            "source": article["source"]["name"],
            "url": article["url"],
            "sentiment": sentiment
        })

    cache[ticker] = (articles, time.time())

    return articles