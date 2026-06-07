"""Service modules for Google Finance API."""

from gfinance.services.quote import QuoteService
from gfinance.services.market import MarketService
from gfinance.services.chart import ChartService
from gfinance.services.news import NewsService
from gfinance.services.company import CompanyService
from gfinance.services.financials import FinancialsService
from gfinance.services.analysts import AnalystsService
from gfinance.services.research import ResearchService

__all__ = [
    "QuoteService", "MarketService", "ChartService", "NewsService",
    "CompanyService", "FinancialsService", "AnalystsService", "ResearchService",
]
