import pandas as pd

def boiloff_loss_mmbtu(
    voyage_days: float,
    daily_bor=0.10 / 100,  # 0.10% per day typical XDF
    cargo_mmbtu=170_000 * 52,
):
    """
    Returns boil-off volume lost (MMBtu) during voyage.
    """
    return cargo_mmbtu * (daily_bor * voyage_days)
