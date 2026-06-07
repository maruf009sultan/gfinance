"""Search service — autocomplete / symbol lookup."""

from typing import List
from gfinance.transport import RPCTransport
from gfinance.models import SearchResult
from gfinance.extractors import extract_search_results


class SearchService:
    def __init__(self, transport: RPCTransport):
        self._t = transport

    def query(self, query: str) -> List[SearchResult]:
        data = self._t.call("search_autocomplete", payload_overrides={"query": query})
        return extract_search_results(data) if data else []
