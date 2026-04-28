from fastapi import APIRouter
from app.services.dashboard_service import get_dashboard_data

router = APIRouter()

@router.get("/{ticker}")
def dashboard(ticker: str):
    return get_dashboard_data(ticker)