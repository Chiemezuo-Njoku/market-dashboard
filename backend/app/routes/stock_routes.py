from fastapi import APIRouter

from app.services.stock_service import (
    get_stock_price,
    get_stock_history
)

router = APIRouter()

# -----------------------------
# Current Stock Price Endpoint
# -----------------------------
@router.get("/{ticker}")
def stock_price(ticker: str):

    return get_stock_price(ticker)


# -----------------------------
# Historical Chart Endpoint
# -----------------------------
@router.get("/history/{ticker}")
def stock_history(ticker: str):

    return get_stock_history(ticker)