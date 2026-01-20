from typing import List, Optional
from app.repositories.prices import PricePerosytory
from app.api.schemas import PriceOut


class PriceService:
    def __init__(self, repo: PricePerosytory) -> None:
        self.repo = repo

    async def get_all(self, ticker: str) -> List[PriceOut]:
        rows = await self.repo.find_all(ticker)
        return [PriceOut.model_validate(r) for r in rows]

    async def get_latest(self, ticker: str) -> Optional[PriceOut]:
        row = await self.repo.find_latest(ticker)
        return PriceOut.model_validate(row) if row else None

    async def get_by_date(
            self, ticker: str,
            start: int,
            end: int
    ) -> List[PriceOut]:
        rows = await self.repo.find_in_range(ticker, start, end)
        return [PriceOut.model_validate(r) for r in rows]
