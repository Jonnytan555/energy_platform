import httpx
import pandas as pd

ICE_API = "https://query1.finance.yahoo.com/v7/finance/download"

ICE_TICKERS = {
    "TTF": "TTF=F",
    "NBP": "NBP=F",
}

CME_TICKERS = {
    "HH": "NG=F",
    "WTI": "CL=F",
}

async def fetch_futures(ticker: str, days: int = 180):
    url = f"{ICE_API}/{ticker}"

    params = {
        "period1": "0",
        "period2": "9999999999",
        "interval": "1d",
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
        r.raise_for_status()

    df = pd.read_csv(pd.compat.StringIO(r.text))
    df["Date"] = pd.to_datetime(df["Date"])

    df = df.tail(days)

    return df[["Date", "Close"]]
