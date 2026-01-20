from pydantic import BaseModel, model_validator, ConfigDict
from typing import Literal

Ticker = Literal['btc_usd', 'eth_usd']


class PriceOut(BaseModel):
    ticker: Ticker
    price: float
    timestamp: int

    model_config = ConfigDict(from_attributes=True)


class TickerQuery(BaseModel):
    ticker: Ticker


class DateRangeQuery(BaseModel):
    ticker: Ticker
    from_ts: int
    to_ts: int

    @model_validator(mode='after')
    def check_range(self):
        if self.to_ts < self.from_ts:
            raise ValueError('to_ts должно быть >= from_ts')
        return self
