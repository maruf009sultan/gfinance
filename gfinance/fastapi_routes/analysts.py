"""Analysts routes."""

from fastapi import APIRouter
from gfinance.fastapi_app import get_client, run_sync

router = APIRouter()


@router.get("/{symbol}/ratings")
async def ratings(symbol: str, exchange: str = "NASDAQ"):
    client = get_client()
    result = await run_sync(client.analysts.ratings, symbol, exchange)
    return result.model_dump()


@router.get("/{symbol}/earnings")
async def earnings(symbol: str, exchange: str = "NASDAQ"):
    client = get_client()
    result = await run_sync(client.analysts.earnings, symbol, exchange)
    return result.model_dump()


@router.get("/{symbol}/transcript")
async def transcript(symbol: str):
    client = get_client()
    return await run_sync(client.analysts.transcript, symbol)
