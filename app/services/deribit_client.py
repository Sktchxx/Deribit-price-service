import aiohttp
import requests
from app.core.config import settings


class DeribitClient:
    def __init__(self, timeout: int = 10):
        self.base_url = settings.deribit_url
        self.timeout = timeout

    async def get_index_price(self, ticker: str):
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                self.base_url,
                params={'index_name': ticker},
            ) as responce:
                responce.raise_for_status()
                data = await responce.json()
        try:
            price = data['result']['index_price']
            return float(price)
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f'Неправильный ответ: {data}') from e

    def get_price_sync(self, ticker: str) -> float:
        response = requests.get(
            self.base_url,
            params={"index_name": ticker},
            timeout=self.timeout,
        )
        response.raise_for_status()
        try:
            return float(response.json()['result']['index_price'])
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f'Неправильный ответ: {response.text}') from e
