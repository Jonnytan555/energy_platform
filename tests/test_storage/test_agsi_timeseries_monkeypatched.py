import pytest
from unittest.mock import AsyncMock
import app.utils.http as http_mod
from app.storage.agsi_client import fetch_agsi_timeseries

class FakeResponse:
    def __init__(self, js):
        self._js = js
    def json(self):
        return self._js

@pytest.mark.asyncio
async def test_agsi_timeseries_monkeypatched(monkeypatch):
    monkeypatch.setattr(
        "app.utils.http.safe_get",
        AsyncMock(return_value=FakeResponse({"data": [], "last_page": 1}))
    )

    df = await fetch_agsi_timeseries("EU")
    assert df.empty

