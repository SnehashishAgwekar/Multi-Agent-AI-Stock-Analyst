import yfinance as yf
from crewai.tools import tool

@tool("Live Stock Information Tool")
def get_stock_price(stock_symbol: str) -> str:
    """
    Retrieves the latest stock price and other relevant info for a given stock symbol using Yahoo Finance.

    Parameters:
      stock_symbol (str): The ticker symbol of the stock (e.g., AAPL, TSLA, MSFT).

    Returns:
      str: A summary of the stock current price, daily change, and other key data.
    """
    stock = yf.Ticker(stock_symbol)
    info = stock.info

    current_price  = info.get("regularMarketPrice") or info.get("currentPrice")
    change         = info.get("regularMarketChange")
    change_percent = info.get("regularMarketChangePercent")
    currency       = info.get("currency", "USD")
    volume         = info.get("regularMarketVolume")
    market_cap     = info.get("marketCap")

    if current_price is None:
        return f"Could not fetch price for {stock_symbol}. Please check the symbol."

    result = (
        f"Stock: {stock_symbol.upper()}\n"
        f"Price: {current_price} {currency}\n"
        f"Change: {change} ({round(change_percent, 2) if change_percent else 'N/A'}%)\n"
    )
    if volume:
        result += f"Volume: {volume:,}\n"
    if market_cap:
        result += f"Market Cap: {market_cap:,}\n"
    return result
