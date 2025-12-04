import pytest
from unittest.mock import AsyncMock
from app.utils.http import safe_get

@pytest.mark.asyncio
async def test_retry_logic(monkeypatch):
    calls = {"n": 0}

    async def failing(*args, **kwargs):
        calls["n"] += 1
        raise Exception("fail")

    monkeypatch.setattr("app.utils.http.httpx.AsyncClient.get", failing)

    with pytest.raises(Exception):
        await safe_get("http://x")

    assert calls["n"] >= 1
