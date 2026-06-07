"""
gfinance — Production-Grade Google Finance API Library
======================================================

Merges the best of google-finance-api and gfinance-beta into one
battle-tested, Arch-Linux-compatible library.

Features:
  - 26+ RPC endpoints (quotes, charts, news, financials, analysts, AI research...)
  - Auto-healing RPC discovery (Playwright + HTML fallback)
  - Circuit breaker + retry with exponential backoff
  - Both sync and async clients
  - Typed Pydantic models with JSON/Dict/DataFrame export
  - FastAPI server with modular routes
  - Zero auth required — sessions auto-generated

Usage:
    from gfinance import GoogleFinanceClient

    client = GoogleFinanceClient()
    quote = client.quote.get("AAPL")
    print(quote.price, quote.change_percent)
"""

__version__ = "2.0.0"
__author__ = "gfinance contributors"

from gfinance.models import (
    Quote,
    CompanyDetails,
    ChartData,
    ChartTick,
    AnalystRating,
    EarningsData,
    FinancialStatement,
    FinancialStatements,
    SearchResult,
    MarketIndex,
    MarketSummary,
    MarketMovers,
    NewsArticle,
)
from gfinance.client import GoogleFinanceClient
from gfinance.exceptions import (
    GFinanceError,
    SessionError,
    RPCError,
    ParseError,
    EndpointNotFoundError,
    AutoHealError,
    RateLimitError,
)

__all__ = [
    "GoogleFinanceClient",
    "Quote", "CompanyDetails", "ChartData", "ChartTick",
    "AnalystRating", "EarningsData", "FinancialStatement", "FinancialStatements",
    "SearchResult", "MarketIndex", "MarketSummary", "MarketMovers", "NewsArticle",
    "GFinanceError", "SessionError", "RPCError", "ParseError",
    "EndpointNotFoundError", "AutoHealError", "RateLimitError",
]
