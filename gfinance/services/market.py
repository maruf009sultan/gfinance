"""Market service — indices, summary, movers."""

from typing import Any, Dict
from gfinance.transport import RPCTransport
from gfinance.models import MarketSummary, MarketMovers
from gfinance.extractors import extract_market_summary, extract_market_movers


class MarketService:
    def __init__(self, transport: RPCTransport):
        self._t = transport

    def summary(self, region: str = "us") -> MarketSummary:
        region_map = {"us": 1, "europe": 2, "asia": 3, "americas": 1}
        region_code = region_map.get(region.lower(), 1)
        data = self._t.call("market_summary", payload_overrides={"region": str(region_code)})
        return extract_market_summary(data, region=region) if data else MarketSummary(region=region)

    def indices(self) -> MarketSummary:
        data = self._t.call("market_indices")
        return extract_market_summary(data, region="global") if data else MarketSummary()

    def movers(self, category: str = "most_active") -> MarketMovers:
        cat_map = {"most_active": 2, "gainers": 1, "losers": 3}
        cat_code = cat_map.get(category.lower(), 2)
        data = self._t.call("market_screener",
                            payload_overrides={"category": str(cat_code), "count": "20", "asset_filter": "[]"})
        return extract_market_movers(data, category=category) if data else MarketMovers(category=category)
