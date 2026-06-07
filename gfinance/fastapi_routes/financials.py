"""Financials routes."""

from fastapi import APIRouter
from gfinance.fastapi_app import get_client, run_sync

router = APIRouter()


@router.get("/{symbol}/statements")
async def statements(symbol: str, exchange: str = "NASDAQ"):
    client = get_client()
    result = await run_sync(client.financials.statements, symbol, exchange)
    return result.model_dump()


@router.get("/{symbol}/statistics")
async def statistics(symbol: str, exchange: str = "NASDAQ"):
    client = get_client()
    result = await run_sync(client.financials.statistics, symbol, exchange)
    return result.model_dump()


@router.get("/{symbol}/dividends")
async def dividends(symbol: str, exchange: str = "NASDAQ"):
    client = get_client()
    return await run_sync(client.financials.dividends, symbol, exchange)
