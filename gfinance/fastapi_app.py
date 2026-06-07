"""FastAPI application factory."""

import asyncio
import logging
from functools import partial
from typing import Callable, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gfinance.client import GoogleFinanceClient
from gfinance.exceptions import GFinanceError

logger = logging.getLogger(__name__)

_client: GoogleFinanceClient = None


def get_client() -> GoogleFinanceClient:
    global _client
    if _client is None:
        _client = GoogleFinanceClient()
    return _client


async def run_sync(func: Callable, *args, **kwargs) -> Any:
    """Run a synchronous function in a thread pool to avoid blocking the event loop."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(func, *args, **kwargs))


def create_app() -> FastAPI:
    app = FastAPI(
        title="gfinance API",
        description="Production-grade REST API for Google Finance data — zero auth, auto-healing.",
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from gfinance.fastapi_routes import (
        quote_router, market_router, chart_router, news_router,
        company_router, financials_router, analysts_router,
        research_router, system_router,
    )

    app.include_router(system_router, tags=["System"])
    app.include_router(quote_router, prefix="/api/v1/quote", tags=["Quote"])
    app.include_router(market_router, prefix="/api/v1/market", tags=["Market"])
    app.include_router(chart_router, prefix="/api/v1/chart", tags=["Chart"])
    app.include_router(news_router, prefix="/api/v1/news", tags=["News"])
    app.include_router(company_router, prefix="/api/v1/company", tags=["Company"])
    app.include_router(financials_router, prefix="/api/v1/financials", tags=["Financials"])
    app.include_router(analysts_router, prefix="/api/v1/analysts", tags=["Analysts"])
    app.include_router(research_router, prefix="/api/v1/research", tags=["Research"])

    @app.exception_handler(GFinanceError)
    async def gfinance_error_handler(request, exc):
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=502, content={"error": exc.message, "type": type(exc).__name__})

    return app
