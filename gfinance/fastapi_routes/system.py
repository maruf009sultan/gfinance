"""System routes — health, heal, endpoints."""

from fastapi import APIRouter
from gfinance.fastapi_app import get_client, run_sync

router = APIRouter()


@router.get("/health")
async def health():
    client = get_client()
    return {"status": "ok", "service": "gfinance", "resilience": client.resilience_stats()}


@router.post("/api/v1/heal")
async def heal():
    client = get_client()
    updates = await run_sync(client.heal)
    return {"status": "ok", "updates": updates}


@router.get("/api/v1/endpoints")
async def list_endpoints(category: str = None):
    client = get_client()
    eps = client.list_endpoints(category=category)
    return {"endpoints": [{"name": e.name, "rpc_id": e.rpc_id, "description": e.description, "category": e.category} for e in eps]}


@router.get("/api/v1/categories")
async def list_categories():
    client = get_client()
    return {"categories": client.list_categories()}
