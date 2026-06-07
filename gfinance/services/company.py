"""Company service — company info, related companies."""

from typing import Any, Dict, List
from gfinance.transport import RPCTransport
from gfinance.models import CompanyDetails
from gfinance.extractors import extract_company_details
from gfinance.parser import recursive_extract


class CompanyService:
    def __init__(self, transport: RPCTransport):
        self._t = transport

    def info(self, symbol: str, exchange: str = "NASDAQ") -> CompanyDetails:
        data = self._t.call("company_info", symbol=symbol, exchange=exchange)
        return extract_company_details(data, symbol=symbol) if data else CompanyDetails(symbol=symbol)

    def related(self, symbol: str, exchange: str = "NASDAQ") -> List[Dict[str, Any]]:
        data = self._t.call("related_companies", symbol=symbol, exchange=exchange)
        if not data: return []
        strings = recursive_extract(data, str)
        nums = recursive_extract(data, (int, float))
        results = []
        i = 0
        while i + 1 < len(strings):
            results.append({"ticker": strings[i], "name": strings[i+1] if i+1 < len(strings) else None})
            i += 2
        return results
