import yfinance as yf

def get_stock_data(ticker: str):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")

    if data.empty:
        return {"error": "Invalid ticker symbol"}
    
    price = float(data["Close"].iloc[-1])
    volume = int(data["Volume"].iloc[-1])
    return {
        "ticker": ticker,
        "price": price,
        "volume": volume,
    }