import pytest
import pandas as pd
from unittest.mock import AsyncMock, MagicMock

from app.storage.agsi_client import fetch_agsi_timeseries

class FakeResponse:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data

@pytest.fixture
def sample_curve():
    return pd.DataFrame({
        "month": pd.to_datetime(["2025-01-01", "2025-02-01"]),
        "price": [30.0, 31.0]
    })

@pytest.fixture
def mock_http_response():
    mock = MagicMock()
    mock.json.return_value = {"data": []}
    mock.status_code = 200
    return mock


@pytest.fixture(autouse=True)
def disable_cache(monkeypatch):
    monkeypatch.setattr(
        "app.utils.cache.async_ttl_cache",
        lambda *args, **kwargs: (lambda f: f) 
    )

import pytest

# ---------------------------------------------------------------------
# Disable async cache everywhere for tests
# ---------------------------------------------------------------------
import pytest

# ---------------------------------------------------------------------
# Disable async cache everywhere for tests
# ---------------------------------------------------------------------
@pytest.fixture(autouse=True)
def disable_async_cache(monkeypatch):
    """
    Replace async_ttl_cache decorator with a no-op, so AGSI / ALSI tests
    never receive cached historical responses.
    """
    monkeypatch.setattr(
        "app.utils.cache.async_ttl_cache",
        lambda *args, **kwargs: (lambda f: f)
    )


@pytest.fixture(autouse=True)
def patch_agsi_transform(monkeypatch):
    """
    Force AGSI transform to return the raw dataframe so tests never expand
    into historical synthetic data (5,450 rows).
    """
    def identity(df):
        return df

    monkeypatch.setattr(
        "app.storage.agsi_client._transform",
        identity,
        raising=False
    )

@pytest.fixture(autouse=True)
def disable_async_cache(monkeypatch):
    monkeypatch.setattr(
        "app.utils.cache.async_ttl_cache",
        lambda *args, **kwargs: (lambda f: f)
    )

@pytest.fixture(autouse=True)
def patch_agsi_transform(monkeypatch):
    monkeypatch.setattr(
        "app.storage.agsi_client._transform",
        lambda df: df,
        raising=False
    )

@pytest.fixture(autouse=True)
def disable_cache_and_fallback(monkeypatch):
    monkeypatch.setattr("app.utils.cache.read_cache", lambda *a, **k: None)
    monkeypatch.setattr("app.utils.cache.write_cache", lambda *a, **k: None)

    # disable AGSI fallback parquet loading
    monkeypatch.setattr("app.storage.agsi_client.fetch_agsi_timeseries",
                        lambda zone, allow_fallback=True: fetch_agsi_timeseries(zone, allow_fallback=False))






