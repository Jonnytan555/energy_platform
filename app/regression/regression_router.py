from fastapi import APIRouter
import polars as pl
from .regression_service import GasRegressionService

router = APIRouter(prefix="/regression", tags=["Regression"])
svc = GasRegressionService()


@router.post("/gas-lng")
async def regression(data: list[dict]):
    """
    Input example:
    [
      {"HH":2.3, "JKM":13.2, "EUA":68, "FX":1.08, "TTF":32.1},
      {"HH":2.5, "JKM":13.8, "EUA":69, "FX":1.07, "TTF":33.4}
    ]
    """
    df = pl.DataFrame(data)
    return await svc.run_regression(df)

