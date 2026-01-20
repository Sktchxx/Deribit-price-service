import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock

from app.services.price_service import PriceService


@pytest.mark.asyncio
async def test_get_all_returns_priceouts():
    rows = [
        SimpleNamespace(ticker="btc_usd", price=42000.5, timestamp=1610000000),
        SimpleNamespace(ticker="btc_usd", price=42100.0, timestamp=1610000060),
    ]

    fake_repo = SimpleNamespace(find_all=AsyncMock(return_value=rows))
    service = PriceService(fake_repo)

    result = await service.get_all("btc_usd")

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].ticker == "btc_usd"
    assert result[0].price == 42000.5


@pytest.mark.asyncio
async def test_get_latest_returns_none_if_missing():
    fake_repo = SimpleNamespace(find_latest=AsyncMock(return_value=None))
    service = PriceService(fake_repo)

    res = await service.get_latest("eth_usd")
    assert res is None


@pytest.mark.asyncio
async def test_get_by_date_calls_repo_and_returns_list():
    rows = [
        SimpleNamespace(ticker="eth_usd", price=200.0, timestamp=1610000000)
    ]
    fake_repo = SimpleNamespace(find_in_range=AsyncMock(return_value=rows))
    service = PriceService(fake_repo)

    res = await service.get_by_date("eth_usd", 1610000000, 1610001000)
    assert isinstance(res, list)
    assert res[0].ticker == "eth_usd"
