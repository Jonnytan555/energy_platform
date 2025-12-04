import pandas as pd

from .loaders import load_market_futures
from .expand import expand_strips_to_months
from .fit import fit_monthly_curve
from .daily import interpolate_daily
from .validator import validate_curve


async def build_curve(market: str, days: int = 180):
    """
    Full professional forward curve engine.
    Steps:
        1. Load raw futures data (ICE/CME)
        2. Expand strips → monthly curve
        3. Fit spline curve
        4. Create daily curve
        5. Validate
    """

    # 1 — Load raw data
    raw = await load_market_futures(market, days)

    # 2 — Expand strips → monthly buckets
    monthly = expand_strips_to_months(raw)

    # 3 — Fit smooth spline curve
    fitted = fit_monthly_curve(monthly)

    # 4 — Create daily forward curve
    daily = interpolate_daily(fitted)

    # 5 — Validate
    validate_curve(fitted)

    return {
        "market": market.upper(),
        "raw": raw.to_dict(orient="records"),
        "monthly": fitted.to_dict(orient="records"),
        "daily": daily.to_dict(orient="records"),
    }
