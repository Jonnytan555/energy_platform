import polars as pl
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


class GasRegressionService:

    async def run_regression(self, df: pl.DataFrame):
        """
        df columns:
        HH, JKM, EUA, FX, TTF
        """

        X = df.select(["HH", "JKM", "EUA", "FX"]).to_numpy()
        y = df["TTF"].to_numpy()

        model = LinearRegression()
        model.fit(X, y)

        preds = model.predict(X)
        r2 = r2_score(y, preds)

        return {
            "coefficients": {
                "HH_beta": float(model.coef_[0]),
                "JKM_beta": float(model.coef_[1]),
                "EUA_beta": float(model.coef_[2]),
                "FX_beta": float(model.coef_[3]),
            },
            "intercept": float(model.intercept_),
            "r2": float(r2),
            "predictions": preds.tolist()
        }

