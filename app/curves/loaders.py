import pandas as pd
from app.market.ice_client import ICE_TICKERS, CME_TICKERS, fetch_futures


async def load_market_futures(market: str, days: int):
    """
    Load futures from ICE, CME or fallback.
    Standardizes into schema: date, price
    """

    m = market.upper()

    if m in ICE_TICKERS:
        ticker = ICE_TICKERS[m]
    elif m in CME_TICKERS:
        ticker = CME_TICKERS[m]
    else:
        raise ValueError(f"Unknown market '{m}'")

    df = await fetch_futures(ticker, days)

    df = df.rename(columns={"Date": "date", "Close": "price"})
    df["date"] = pd.to_datetime(df["date"])

    return df[["date", "price"]].sort_values("date")
