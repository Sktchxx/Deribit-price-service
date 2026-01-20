from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Price


class PricePerosytory:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find_all(self, ticker: str) -> Sequence[Price]:
        stmt = (select(Price)
                .where(Price.ticker == ticker).order_by(Price.timestamp.asc()))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def find_latest(self, ticker: str) -> Optional[Price]:
        stmt = (
            select(Price)
            .where(Price.ticker == ticker)
            .order_by(Price.timestamp.desc())
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def find_in_range(
            self,
            ticker: str,
            start: int,
            end: int
    ) -> Sequence[Price]:
        stmt = (
            select(Price)
            .where(
                Price.ticker == ticker, Price.timestamp.between(start, end),
                )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
