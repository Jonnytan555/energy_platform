import pytest
from app.lng.netback import compute_netback


def test_netback_basic():
    result = compute_netback(
        jkm=20.0,
        freight=2.5,
        losses_pct=0.07
    )
    assert round(result, 2) == 16.10
