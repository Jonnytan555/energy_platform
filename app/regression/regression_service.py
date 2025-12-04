import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

async def run_regression():

    df = pd.DataFrame({
        "HH": [2.1, 2.8, 3.0, 3.5],
        "TTF": [25.0, 26.1, 27.4, 29.0]
    })

    model = LinearRegression()
    model.fit(df[["HH"]], df["TTF"])

    return {
        "coef": float(model.coef_[0]),
        "intercept": float(model.intercept_),
        "r2": float(model.score(df[["HH"]], df["TTF"]))
    }
