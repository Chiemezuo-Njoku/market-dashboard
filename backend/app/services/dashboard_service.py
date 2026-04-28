from app.services.stock_service import get_stock_data
from app.services.news_service import get_news

def get_dashboard_data(ticker: str):
    
    stock_data = get_stock_data(ticker)
    news_data = get_news(ticker)

    return {
        "ticker": ticker.upper(),
        "stock": stock_data,
        "news": news_data
    }