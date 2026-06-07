"""News routes."""

from fastapi import APIRouter
from gfinance.fastapi_app import get_client, run_sync

router = APIRouter()


@router.get("/market")
async def market_news():
    client = get_client()
    result = await run_sync(client.news.market)
    return [a.model_dump() for a in result]


@router.get("/{symbol}")
async def ticker_news(symbol: str, exchange: str = "NASDAQ"):
    client = get_client()
    result = await run_sync(client.news.ticker, symbol, exchange)
    return [a.model_dump() for a in result]
