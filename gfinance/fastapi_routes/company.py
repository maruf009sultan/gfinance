"""Company routes."""

from fastapi import APIRouter
from gfinance.fastapi_app import get_client, run_sync

router = APIRouter()


@router.get("/{symbol}/info")
async def company_info(symbol: str, exchange: str = "NASDAQ"):
    client = get_client()
    result = await run_sync(client.company.info, symbol, exchange)
    return result.model_dump()


@router.get("/{symbol}/related")
async def related_companies(symbol: str, exchange: str = "NASDAQ"):
    client = get_client()
    return await run_sync(client.company.related, symbol, exchange)
