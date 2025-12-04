import pytest
from app.lng.boiloff import boiloff_loss_mmbtu

def test_boiloff_basic():
    # Expected:
    # 0.1% BOR × 10 days × 170,000 m3 × 22.5 MMBtu = 38,250 MMBtu
    assert boiloff_loss_mmbtu(10) == pytest.approx(38250.0, rel=1e-3)
