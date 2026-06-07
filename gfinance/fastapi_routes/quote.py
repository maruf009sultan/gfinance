"""Quote routes."""

from fastapi import APIRouter
from gfinance.fastapi_app import get_client, run_sync

router = APIRouter()


@router.get("/{symbol}")
async def get_quote(symbol: str, exchange: str = "NASDAQ"):
    client = get_client()
    result = await run_sync(client.quote.get, symbol, exchange)
    return result.model_dump()


@router.get("/{symbol}/details")
async def get_details(symbol: str, exchange: str = "NASDAQ"):
    client = get_client()
    result = await run_sync(client.quote.details, symbol, exchange)
    return result.model_dump()


@router.get("/{symbol}/stats")
async def get_stats(symbol: str, exchange: str = "NASDAQ"):
    client = get_client()
    result = await run_sync(client.quote.stats, symbol, exchange)
    return result.model_dump()


@router.get("/{symbol}/realtime")
async def get_realtime(symbol: str, exchange: str = "NASDAQ"):
    client = get_client()
    result = await run_sync(client.quote.realtime, symbol, exchange)
    return result.model_dump()
