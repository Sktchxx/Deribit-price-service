from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.price_service import PriceService
from app.repositories.prices import PricePerosytory
from app.db.session import get_db
from app.api.schemas import PriceOut, DateRangeQuery, TickerQuery


router = APIRouter()


def get_price_service(db: AsyncSession = Depends(get_db)) -> PriceService:
    repo = PricePerosytory(db)
    return PriceService(repo)


@router.get('/prices', response_model=list[PriceOut])
async def get_all_prices(
    query: TickerQuery = Depends(),
    service: PriceService = Depends(get_price_service),
):
    items = await service.get_all(query.ticker)
    return items


@router.get('/prices/latest', response_model=PriceOut)
async def get_latest_price(
    query: TickerQuery = Depends(),
    service: PriceService = Depends(get_price_service),
):
    item = await service.get_latest(query.ticker)
    if item is None:
        raise HTTPException(status_code=404, detail="No latest price")
    return item


@router.get('/prices/by-date', response_model=list[PriceOut])
async def get_prices_by_date(
    query: DateRangeQuery = Depends(),
    service: PriceService = Depends(get_price_service),
):
    items = await service.get_by_date(query.ticker, query.from_ts, query.to_ts)
    return items
