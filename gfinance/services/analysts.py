"""Analysts service — ratings, earnings, transcripts."""

from typing import Any, Dict
from gfinance.transport import RPCTransport
from gfinance.models import AnalystRating, EarningsData
from gfinance.extractors import extract_analyst_ratings, extract_earnings
from gfinance.parser import recursive_extract


class AnalystsService:
    def __init__(self, transport: RPCTransport):
        self._t = transport

    def ratings(self, symbol: str, exchange: str = "NASDAQ") -> AnalystRating:
        data = self._t.call("analyst_ratings", symbol=symbol, exchange=exchange)
        return extract_analyst_ratings(data, symbol=symbol) if data else AnalystRating(symbol=symbol)

    def earnings(self, symbol: str, exchange: str = "NASDAQ") -> EarningsData:
        data = self._t.call("earnings", symbol=symbol, exchange=exchange)
        return extract_earnings(data, symbol=symbol) if data else EarningsData(symbol=symbol)

    def transcript(self, symbol: str) -> Dict[str, Any]:
        data = self._t.call("earnings_transcript", symbol=symbol)
        if not data:
            return {"symbol": symbol, "text": None}
        strings = recursive_extract(data, str)
        return {
            "symbol": symbol,
            "quarter": strings[0] if strings else None,
            "date": strings[1] if len(strings) > 1 else None,
            "text": " ".join(strings[2:]) if len(strings) > 2 else None,
        }
