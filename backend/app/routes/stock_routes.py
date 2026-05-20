from fastapi import APIRouter
from app.services.stock_service import get_stock_data
from app.services.stock_service import get_stock_history

router = APIRouter()

@router.get("/history/{ticker}")
def read_stock_history(ticker: str):
    return get_stock_history(ticker)

@router.get("/{ticker}")
def read_stock(ticker: str):
    return get_stock_data(ticker)
