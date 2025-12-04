import yfinance as yf
import pandas as pd

async def get_market_snapshot():

    ttf_price = yf.Ticker("TTF=F").history(period="1mo").tail(1)["Close"].values[0]
    hh_price  = yf.Ticker("NG=F").history(period="1mo").tail(1)["Close"].values[0]

    df_weather = pd.DataFrame({
        "metric": ["HDD", "CDD"],
        "value": [18.2, 0.0]
    })

    return {
        "prices": {
            "TTF": float(ttf_price),
            "HenryHub": float(hh_price)
        },
        "weather": df_weather.to_dict(orient="records")
    }
