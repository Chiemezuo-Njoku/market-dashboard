from fastapi import APIRouter
from app.services.news_service import get_news

router = APIRouter()

@router.get("/{ticker}")
def news(ticker: str):
    return get_news(ticker)