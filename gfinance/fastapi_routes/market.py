"""Market routes."""

from fastapi import APIRouter
from gfinance.fastapi_app import get_client, run_sync

router = APIRouter()


@router.get("/summary")
async def market_summary(region: str = "us"):
    client = get_client()
    result = await run_sync(client.market.summary, region)
    return result.model_dump()


@router.get("/indices")
async def market_indices():
    client = get_client()
    result = await run_sync(client.market.indices)
    return result.model_dump()


@router.get("/movers")
async def market_movers(category: str = "most_active"):
    client = get_client()
    result = await run_sync(client.market.movers, category)
    return result.model_dump()
