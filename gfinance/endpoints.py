"""
Endpoint registry — maps human-friendly names to obfuscated RPC IDs.

Includes 26+ discovered endpoints with auto-healing support,
disk caching, and data-service-index-based matching.
"""

import copy
import json
import os
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class RPCEndpoint:
    """A single RPC endpoint entry."""
    rpc_id: str
    name: str
    description: str
    category: str
    payload_template: str = "[]"
    entity_type: str = "all"   # stock, crypto, currency, index, all
    params: List[str] = field(default_factory=list)
    data_service_index: Optional[int] = None


# ─── 26+ known endpoints ───

KNOWN_ENDPOINTS: Dict[str, RPCEndpoint] = {
    # ── Navigation ──
    "page_load": RPCEndpoint("zKAP2e", "page_load", "Initial page load data", "navigation", '["{path}"]', params=["path"]),
    "navigation": RPCEndpoint("hgueg", "navigation", "Navigation / sidebar data", "navigation", "[]", data_service_index=0),
    "feature_flags": RPCEndpoint("hgueg", "feature_flags", "Feature flags & config", "session", "[1]"),

    # ── Market ──
    "market_summary": RPCEndpoint("HacE5d", "market_summary", "Market indices & sectors", "market", '["market_summary", 1, {region}]', params=["region"], data_service_index=1),
    "market_status": RPCEndpoint("RiQiSd", "market_status", "Exchange open/close status", "market", "[]", data_service_index=17),
    "market_screener": RPCEndpoint("kA4MVd", "market_screener", "Market movers & screener", "market", '[{category}, {count}, {asset_filter}]', params=["category"], data_service_index=15),
    "market_indices": RPCEndpoint("RmdyKd", "market_indices", "Major market index data", "market", "[1, 0, 2]"),
    "market_categories": RPCEndpoint("YtbmEe", "market_categories", "Sector classification", "market", "[[2,3,1], 4, 0]"),
    "market_regions": RPCEndpoint("xuuV8d", "market_regions", "Regional market data / batch quotes light", "market", "[[{entity_ids}]]"),

    # ── Quote ──
    "quote_core": RPCEndpoint("gCvqoe", "quote_core", "Core price, change, volume, market cap", "quote", "[[{asset}], 1]", entity_type="all", params=["ticker"], data_service_index=2),
    "quote_details": RPCEndpoint("JL8oKc", "quote_details", "Extended quote details", "quote", "[[{asset}]]", params=["ticker"], data_service_index=3),
    "quote_stats": RPCEndpoint("SICF5d", "quote_stats", "Key statistics (P/E, EPS, beta)", "quote", "[{asset}, 4]", params=["ticker"], data_service_index=4),
    "quote_info": RPCEndpoint("YTM9q", "quote_info", "Quote summary info", "quote", "[{asset}]", params=["ticker"], data_service_index=5),
    "realtime_price": RPCEndpoint("in0BVc", "realtime_price", "Real-time price stream", "quote", "[[{asset}], null, null, null, 1]", params=["ticker"]),
    "quote_about": RPCEndpoint("dlNq8b", "quote_about", "About section (sector, CEO)", "quote", "[[{asset}], 1, 1, 1]", params=["ticker"], data_service_index=7),
    "symbol_resolve": RPCEndpoint("gXxkFd", "symbol_resolve", "Symbol resolution", "quote", "[{ticker}, {exchange}]", params=["ticker"]),

    # ── Chart ──
    "chart_data": RPCEndpoint("SICF5d", "chart_data", "Chart data with interval", "chart", "[{asset}, {period}, null, null, 1, {resolution_flag}]", params=["ticker", "interval"], data_service_index=4),
    "chart_crypto": RPCEndpoint("in0BVc", "chart_crypto", "Crypto/currency chart data", "chart", "[[{asset}], null, null, null, 1]", entity_type="crypto", params=["ticker"]),
    "price_history": RPCEndpoint("wKsY8b", "price_history", "Historical price (single period)", "chart", "[{asset}, {period}]", params=["ticker", "period"]),
    "price_history_multi": RPCEndpoint("c2u4wc", "price_history_multi", "Historical price (multi-period)", "chart", "[[{asset}], {period}]", params=["ticker", "period"], data_service_index=8),
    "stock_chart": RPCEndpoint("Xs5i3b", "stock_chart", "Stock chart rendering data", "chart", "[{asset}]", params=["ticker"]),

    # ── News ──
    "news": RPCEndpoint("XB3kn", "news", "General market news feed", "news", '["{query}", null, 1]', params=[]),
    "quote_news": RPCEndpoint("XxQsbd", "quote_news", "Ticker-specific news", "news", "[[{asset}], 1]", params=["ticker"], data_service_index=6),

    # ── Company ──
    "company_info": RPCEndpoint("Iaiw6c", "company_info", "Company description & details", "company", "[[{asset}]]", params=["ticker"]),
    "related_companies": RPCEndpoint("dlNq8b", "related_companies", "Related / similar companies", "company", "[[{asset}], 1]", params=["ticker"], data_service_index=7),
    "related_stocks": RPCEndpoint("TNo8E", "related_stocks", "Related stocks in sector", "company", "[{asset}]", params=["ticker"]),

    # ── Financials ──
    "financial_statements": RPCEndpoint("Pr8h2e", "financial_statements", "Income stmt, balance sheet, CF", "financials", "[[{asset}], null, 1]", params=["ticker"], data_service_index=14),
    "dividends": RPCEndpoint("gXxkFd", "dividends", "Dividend history & yield", "financials", "[[{ticker}, {exchange}]]", params=["ticker"], data_service_index=12),
    "batch_quote_detailed": RPCEndpoint("in0BVc", "batch_quote_detailed", "Detailed batch quotes", "market", "[[{entity_ids}], [null, null, null, 3, null, 1]]"),

    # ── Analysts ──
    "analyst_ratings": RPCEndpoint("K5Y6Xb", "analyst_ratings", "Analyst consensus & targets", "analysts", "[{asset}]", params=["ticker"]),
    "earnings": RPCEndpoint("wj5Bh", "earnings", "EPS estimates & actuals", "analysts", "[{asset}]", params=["ticker"]),
    "earnings_transcript": RPCEndpoint("FinanceHubService/GetEarningsTranscript", "earnings_transcript", "Earnings call transcript", "analysts", "[{ticker}]", params=["ticker"]),

    # ── Watchlist / Research ──
    "watchlist": RPCEndpoint("X12h2b", "watchlist", "User watchlist data", "watchlist", "[]", data_service_index=18),
    "research": RPCEndpoint("FinanceHubService/ExecuteResearchQuery", "research", "AI research query", "research", "[{ticker}, {query}]", params=["ticker", "query"]),
    "search_autocomplete": RPCEndpoint("XB3kn", "search_autocomplete", "Autocomplete search", "search", '["{query}", null, 1]', params=["query"]),
    "async_data": RPCEndpoint("AsyncDataService/GetAsyncData", "async_data", "Async data service", "system", "[]"),
}

RPC_ID_TO_NAME: Dict[str, str] = {ep.rpc_id: name for name, ep in KNOWN_ENDPOINTS.items()}


class EndpointRegistry:
    """Registry with auto-healing, disk cache, and reverse lookup."""

    def __init__(self, cache_dir: str = None):
        self._endpoints: Dict[str, RPCEndpoint] = copy.deepcopy(KNOWN_ENDPOINTS)
        self._rpc_id_map: Dict[str, str] = dict(RPC_ID_TO_NAME)
        self._cache_path = os.path.join(
            cache_dir or os.path.expanduser("~/.cache/gfinance"),
            "rpc_ids.json",
        )
        self._load_cache()

    def get(self, name: str) -> RPCEndpoint:
        if name not in self._endpoints:
            raise KeyError(f"Endpoint '{name}' not found")
        return self._endpoints[name]

    def get_by_rpc_id(self, rpc_id: str) -> RPCEndpoint:
        name = self._rpc_id_map.get(rpc_id)
        if name is None:
            raise KeyError(f"RPC ID '{rpc_id}' not found")
        return self._endpoints[name]

    def update_rpc_id(self, name: str, new_rpc_id: str):
        if name not in self._endpoints:
            return
        old = self._endpoints[name].rpc_id
        if old != new_rpc_id:
            logger.info("RPC ID updated: %s %s -> %s", name, old, new_rpc_id)
            self._endpoints[name].rpc_id = new_rpc_id
            if old in self._rpc_id_map:
                del self._rpc_id_map[old]
            self._rpc_id_map[new_rpc_id] = name
            self._save_cache()

    def list_endpoints(self, category: str = None) -> List[RPCEndpoint]:
        eps = list(self._endpoints.values())
        if category:
            eps = [e for e in eps if e.category == category]
        return eps

    def list_categories(self) -> List[str]:
        return sorted(set(e.category for e in self._endpoints.values()))

    def _load_cache(self):
        if os.path.exists(self._cache_path):
            try:
                with open(self._cache_path) as f:
                    cached = json.load(f)
                for name, rpc_id in cached.get("overrides", {}).items():
                    if name in self._endpoints:
                        old = self._endpoints[name].rpc_id
                        self._endpoints[name].rpc_id = rpc_id
                        if old in self._rpc_id_map:
                            del self._rpc_id_map[old]
                        self._rpc_id_map[rpc_id] = name
                logger.info("Loaded %d cached RPC IDs", len(cached.get("overrides", {})))
            except (json.JSONDecodeError, KeyError):
                pass

    def _save_cache(self):
        try:
            os.makedirs(os.path.dirname(self._cache_path), exist_ok=True)
            overrides = {name: ep.rpc_id for name, ep in self._endpoints.items()}
            with open(self._cache_path, "w") as f:
                json.dump({"overrides": overrides}, f, indent=2)
        except OSError as e:
            logger.warning("Cache save failed: %s", e)

    def clear_cache(self):
        self._endpoints = copy.deepcopy(KNOWN_ENDPOINTS)
        self._rpc_id_map = dict(RPC_ID_TO_NAME)
        if os.path.exists(self._cache_path):
            os.remove(self._cache_path)
