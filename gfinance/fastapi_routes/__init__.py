"""FastAPI route modules."""

from gfinance.fastapi_routes.system import router as system_router
from gfinance.fastapi_routes.quote import router as quote_router
from gfinance.fastapi_routes.market import router as market_router
from gfinance.fastapi_routes.chart import router as chart_router
from gfinance.fastapi_routes.news import router as news_router
from gfinance.fastapi_routes.company import router as company_router
from gfinance.fastapi_routes.financials import router as financials_router
from gfinance.fastapi_routes.analysts import router as analysts_router
from gfinance.fastapi_routes.research import router as research_router

__all__ = [
    "system_router", "quote_router", "market_router", "chart_router",
    "news_router", "company_router", "financials_router", "analysts_router",
    "research_router",
]
