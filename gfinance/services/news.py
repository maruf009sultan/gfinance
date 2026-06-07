"""News service — market news and ticker-specific news."""

from typing import List
from gfinance.transport import RPCTransport
from gfinance.models import NewsArticle
from gfinance.extractors import extract_news


class NewsService:
    def __init__(self, transport: RPCTransport):
        self._t = transport

    def market(self) -> List[NewsArticle]:
        data = self._t.call("news", payload_overrides={"query": "", "count": "10"})
        return extract_news(data) if data else []

    def ticker(self, symbol: str, exchange: str = "NASDAQ") -> List[NewsArticle]:
        data = self._t.call("quote_news", symbol=symbol, exchange=exchange)
        return extract_news(data) if data else []
