import pandas as pd
from .ice_client import ICE_TICKERS, CME_TICKERS, fetch_futures

async def get_futures_snapshot():
    results = {}

    # ICE: TTF, NBP
    for name, ticker in ICE_TICKERS.items():
        df = await fetch_futures(ticker)
        last = df.tail(1).to_dict(orient="records")[0]
        results[name] = {"ticker": ticker, "last": last, "history": df.to_dict(orient="records")}

    # CME: Henry Hub, WTI, RBOB
    for name, ticker in CME_TICKERS.items():
        df = await fetch_futures(ticker)
        last = df.tail(1).to_dict(orient="records")[0]
        results[name] = {"ticker": ticker, "last": last, "history": df.to_dict(orient="records")}

    return results
