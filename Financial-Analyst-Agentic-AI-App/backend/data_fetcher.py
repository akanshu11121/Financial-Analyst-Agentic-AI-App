# backend/data_fetcher.py
import yfinance as yf
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt

def symbol_for_yahoo(symbol: str, exchange: str) -> str:
    """
    Formats a stock symbol for Yahoo Finance API based on its exchange.
    - NSE symbols are appended with '.NS'.
    - BSE symbols are appended with '.BO'.

    Args:
        symbol (str): The stock symbol (e.g., "RELIANCE").
        exchange (str): The stock exchange ("NSE" or "BSE").

    Returns:
        str: The formatted symbol for Yahoo Finance (e.g., "RELIANCE.NS").
    """
    if exchange.upper() == "NSE":
        return f"{symbol}.NS"
    if exchange.upper() == "BSE":
        return f"{symbol}.BO"
    return symbol

def fetch_history(symbol: str, exchange: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """
    Fetches historical price data for a given stock symbol from Yahoo Finance.

    Args:
        symbol (str): The stock symbol.
        exchange (str): The stock exchange ("NSE" or "BSE").
        period (str, optional): The time period for the data (e.g., "1y", "6mo"). Defaults to "6mo".
        interval (str, optional): The data interval (e.g., "1d", "1wk"). Defaults to "1d".

    Returns:
        pd.DataFrame: A DataFrame containing the historical price data.
    """
    ticker = symbol_for_yahoo(symbol, exchange)
    t = yf.Ticker(ticker)
    df = t.history(period=period, interval=interval)
    return df

def plot_history_to_bytes(df: pd.DataFrame, title: str = "Price") -> BytesIO:
    """
    Generates a PNG plot of the closing price from a DataFrame and returns it as bytes.

    Args:
        df (pd.DataFrame): DataFrame containing stock history with a 'Close' column.
        title (str, optional): The title of the plot. Defaults to "Price".

    Returns:
        BytesIO: A bytes buffer containing the PNG image of the plot.
    """
    plt.ioff()
    fig, ax = plt.subplots(figsize=(8, 4))
    df['Close'].plot(ax=ax)
    ax.set_title(title)
    ax.set_ylabel("Price (INR)")
    ax.grid(True, linestyle=':', linewidth=0.5)
    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=120)
    plt.close(fig)
    buf.seek(0)
    return buf
