"""Research routes."""

from fastapi import APIRouter
from pydantic import BaseModel
from gfinance.fastapi_app import get_client, run_sync

router = APIRouter()


class ResearchQuery(BaseModel):
    symbol: str
    question: str


@router.post("/query")
async def research_query(query: ResearchQuery):
    client = get_client()
    return await run_sync(client.research.query, query.symbol, query.question)


@router.get("/{symbol}")
async def quick_research(symbol: str, question: str = "What are the key investment considerations?"):
    client = get_client()
    return await run_sync(client.research.query, symbol, question)
