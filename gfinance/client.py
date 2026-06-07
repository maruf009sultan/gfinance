"""
Main synchronous client — the primary entry point.

Combines the best of both original libraries:
  - Modular service architecture from gfinance-beta
  - Typed Pydantic models from google-finance-api
  - Circuit breaker + resilience from google-finance-api
  - Auto-healing from gfinance-beta (Playwright + HTML fallback)
  - SAPISIDHASH auth from gfinance-beta
"""

import logging
from typing import Dict, List, Optional

from gfinance.session import SessionManager
from gfinance.transport import RPCTransport
from gfinance.endpoints import EndpointRegistry
from gfinance.auto_heal import AutoHealEngine
from gfinance.resilience import CircuitBreaker
from gfinance.exceptions import AutoHealError

from gfinance.services import (
    QuoteService, MarketService, ChartService, NewsService,
    CompanyService, FinancialsService, AnalystsService, ResearchService,
)
from gfinance.services.search import SearchService

logger = logging.getLogger(__name__)


class GoogleFinanceClient:
    """
    Production-grade client for Google Finance API.

    Features:
      - Zero auth (sessions auto-generated)
      - Auto-healing RPC discovery
      - Circuit breaker for resilience
      - Modular service architecture
      - Typed Pydantic model responses

    Usage:
        client = GoogleFinanceClient()
        quote = client.quote.get("AAPL")
        print(quote.price)

        # Context manager
        with GoogleFinanceClient() as client:
            chart = client.chart.data("TSLA", period="1M")
    """

    def __init__(
        self,
        proxies: Optional[Dict[str, str]] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: float = 30.0,
        auto_heal: bool = True,
        language: str = "en-US",
    ):
        self._session_mgr = SessionManager(proxies=proxies, timeout=int(timeout), language=language)
        self._registry = EndpointRegistry()
        self._transport = RPCTransport(
            session_manager=self._session_mgr,
            registry=self._registry,
            max_retries=max_retries,
            retry_delay=retry_delay,
            timeout=timeout,
        )
        self._circuit_breaker = CircuitBreaker()
        self._auto_heal_engine = AutoHealEngine(self._registry)
        self._auto_heal_enabled = auto_heal

        # Initialize service modules
        self.quote = QuoteService(self._transport)
        self.market = MarketService(self._transport)
        self.chart = ChartService(self._transport)
        self.news = NewsService(self._transport)
        self.company = CompanyService(self._transport)
        self.financials = FinancialsService(self._transport)
        self.analysts = AnalystsService(self._transport)
        self.research = ResearchService(self._transport)
        self.search = SearchService(self._transport)

        logger.info("GoogleFinanceClient initialized (auto_heal=%s)", auto_heal)

    def heal(self) -> Dict[str, str]:
        """Manually trigger auto-healing to re-discover RPC IDs."""
        return self._auto_heal_engine.heal_sync()

    def refresh_session(self):
        """Force-refresh the session."""
        self._session_mgr.refresh()

    def list_endpoints(self, category: str = None):
        return self._registry.list_endpoints(category=category)

    def list_categories(self):
        return self._registry.list_categories()

    def resilience_stats(self) -> dict:
        return self._circuit_breaker.get_stats()

    def close(self):
        """Close the client and release resources."""
        self._session_mgr.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
