import yfinance as yf


def _fetch_stock_history(ticker: str, period: str):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)

    if data.empty:
        return None, {"error": f"No stock data found for ticker '{ticker.upper()}'"}

    return data, None


# -----------------------------
# Get Current Stock Price
# -----------------------------
def get_stock_price(ticker: str):
    ticker = ticker.upper()
    data, error = _fetch_stock_history(ticker, period="1d")

    if error:
        return error

    try:
        return {
            "ticker": ticker,
            "price": float(data["Close"].iloc[-1]),
            "volume": int(data["Volume"].iloc[-1])
        }
    except (KeyError, IndexError, ValueError):
        return {"error": f"Unable to parse price data for ticker '{ticker}'"}


# -----------------------------
# Get Historical Data for Chart
# -----------------------------
def get_stock_history(ticker: str):
    ticker = ticker.upper()
    data, error = _fetch_stock_history(ticker, period="1mo")

    if error:
        return error

    try:
        return {
            "ticker": ticker,
            "dates": data.index.strftime('%Y-%m-%d').tolist(),
            "prices": data["Close"].round(2).tolist()
        }
    except (KeyError, ValueError):
        return {"error": f"Unable to parse historical data for ticker '{ticker}'"}


def get_stock_data(ticker: str):
    ticker = ticker.upper()
    price_data = get_stock_price(ticker)
    if "error" in price_data:
        return price_data

    history_data = get_stock_history(ticker)
    if "error" in history_data:
        return history_data

    return {
        "ticker": ticker,
        "price": price_data["price"],
        "volume": price_data["volume"],
        "history": history_data["prices"],
        "dates": history_data["dates"]
    }