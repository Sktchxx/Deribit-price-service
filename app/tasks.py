import time
from app.services.deribit_client import DeribitClient
from app.db.session_sync import SessionLocal
from app.repositories.prices_sync import PriceRepositorySync
from app.db.models import Price
from app.core.config import settings


def collect_prices():
    client = DeribitClient()

    with SessionLocal() as db:
        repo = PriceRepositorySync(db)
        prices = []

        for ticker in settings.tickers:
            price = client.get_price_sync(ticker)
            prices.append(
                Price(
                    ticker=ticker,
                    price=price,
                    timestamp=int(time.time()),
                )
            )

        repo.bulk_insert(prices)
