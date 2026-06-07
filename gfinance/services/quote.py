"""Quote service — stock prices, real-time quotes, details."""

from typing import Any, Dict, Optional, List
from gfinance.transport import RPCTransport
from gfinance.models import Quote, CompanyDetails
from gfinance.extractors import extract_quote, extract_company_details


class QuoteService:
    def __init__(self, transport: RPCTransport):
        self._t = transport

    def get(self, symbol: str, exchange: str = "NASDAQ") -> Quote:
        """Get core quote data (price, change, volume, etc.)."""
        data = self._t.call("quote_core", symbol=symbol, exchange=exchange)
        return extract_quote(data, symbol=symbol, exchange=exchange) if data else Quote(symbol=symbol, exchange=exchange)

    def details(self, symbol: str, exchange: str = "NASDAQ") -> CompanyDetails:
        """Get company details (name, sector, CEO, etc.)."""
        data = self._t.call("quote_details", symbol=symbol, exchange=exchange)
        return extract_company_details(data, symbol=symbol) if data else CompanyDetails(symbol=symbol)

    def stats(self, symbol: str, exchange: str = "NASDAQ") -> Quote:
        """Get key statistics (P/E, EPS, beta, etc.)."""
        data = self._t.call("quote_stats", symbol=symbol, exchange=exchange)
        return extract_quote(data, symbol=symbol, exchange=exchange) if data else Quote(symbol=symbol, exchange=exchange)

    def realtime(self, symbol: str, exchange: str = "NASDAQ") -> Quote:
        """Get real-time price data."""
        data = self._t.call("realtime_price", symbol=symbol, exchange=exchange)
        if data:
            return extract_quote(data, symbol=symbol, exchange=exchange)
        return self.get(symbol, exchange)

    def batch_quotes(self, symbols: List[tuple]) -> List[Quote]:
        """Get quotes for multiple symbols at once."""
        results = []
        for sym, exch in symbols:
            results.append(self.get(sym, exch))
        return results
