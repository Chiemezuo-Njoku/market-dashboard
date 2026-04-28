from fastapi import APIRouter
from app.services.stock_service import get_stock_data

router = APIRouter()

@router.get("/{ticker}")
def read_stock(ticker: str):
    return get_stock_data(ticker)