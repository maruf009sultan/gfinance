"""Financials service — statements, statistics, dividends."""

from typing import Any, Dict
from gfinance.transport import RPCTransport
from gfinance.models import FinancialStatements, Quote
from gfinance.extractors import extract_financial_statements, extract_quote


class FinancialsService:
    def __init__(self, transport: RPCTransport):
        self._t = transport

    def statements(self, symbol: str, exchange: str = "NASDAQ") -> FinancialStatements:
        data = self._t.call("financial_statements", symbol=symbol, exchange=exchange)
        return extract_financial_statements(data, symbol=symbol) if data else FinancialStatements(symbol=symbol)

    def statistics(self, symbol: str, exchange: str = "NASDAQ") -> Quote:
        data = self._t.call("quote_stats", symbol=symbol, exchange=exchange)
        return extract_quote(data, symbol=symbol, exchange=exchange) if data else Quote(symbol=symbol, exchange=exchange)

    def dividends(self, symbol: str, exchange: str = "NASDAQ") -> Dict[str, Any]:
        data = self._t.call("dividends", symbol=symbol, exchange=exchange)
        if not data:
            return {"symbol": symbol, "history": [], "yield": None}
        from gfinance.parser import recursive_extract
        strings = recursive_extract(data, str)
        nums = [float(n) for n in recursive_extract(data, (int, float)) if isinstance(n, (int, float))]
        history = []
        i = 0
        num_idx = 0
        while i < len(strings) and num_idx < len(nums):
            entry = {"date": strings[i], "amount": nums[num_idx] if num_idx < len(nums) else None}
            if entry["date"] and entry["amount"]:
                history.append(entry)
            i += 2
            num_idx += 1
        return {"symbol": symbol, "yield": nums[0] if nums else None, "history": history}
