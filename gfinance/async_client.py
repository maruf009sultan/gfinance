"""
Async client for Google Finance API — high-performance concurrent access.
"""

import re
import json
import time
import asyncio
import logging
from typing import Any, Dict, List, Optional

import aiohttp

from gfinance.endpoints import EndpointRegistry
from gfinance.parser import (
    parse_batchexecute, find_by_rpc_id, build_asset_identifier,
)
from gfinance.models import (
    Quote, CompanyDetails, ChartData, AnalystRating, EarningsData,
    FinancialStatements, SearchResult, MarketSummary, MarketMovers, NewsArticle,
)
from gfinance.extractors import (
    extract_quote, extract_company_details, extract_chart_data,
    extract_analyst_ratings, extract_earnings, extract_financial_statements,
    extract_search_results, extract_market_summary, extract_market_movers, extract_news,
    extract_ohlcv,
)

logger = logging.getLogger(__name__)

FINANCE_BASE = "https://www.google.com/finance/beta"


class AsyncGoogleFinanceClient:
    """Async client using aiohttp for concurrent, non-blocking access."""

    def __init__(self, timeout: float = 30.0, language: str = "en-US"):
        self._registry = EndpointRegistry()
        self._timeout = timeout
        self._language = language
        self._session: Optional[aiohttp.ClientSession] = None
        self._f_sid = ""
        self._bl = ""
        self._at = ""
        self._reqid = 100000
        self._last_refresh = 0.0
        self._refresh_interval = 1800.0
        self._success = 0
        self._failure = 0

    async def _ensure_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={"User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                                         "Chrome/126.0.0.0 Safari/537.36"),
                          "Accept-Language": self._language},
                timeout=aiohttp.ClientTimeout(total=self._timeout),
            )
            await self._init_session()
        elif self._is_expired():
            await self._init_session()

    def _is_expired(self) -> bool:
        return not self._f_sid or (time.time() - self._last_refresh) > self._refresh_interval

    async def _init_session(self):
        try:
            async with self._session.get(FINANCE_BASE) as resp:
                html = await resp.text()
                m = re.search(r'"FdrFJe"\s*:\s*"(-?\d+)"', html)
                if m: self._f_sid = m.group(1)
                m = re.search(r'"cfb2h"\s*:\s*"([^"]+)"', html)
                if m: self._bl = m.group(1)
                m = re.search(r'"SNlM0e"\s*:\s*"([^"]+)"', html)
                if m: self._at = m.group(1)
                self._last_refresh = time.time()
                logger.info("Async session initialized: f.sid=%s...", self._f_sid[:20] if self._f_sid else "NONE")
        except Exception as e:
            logger.error("Async session init failed: %s", e)

    async def _call_rpc(self, endpoint_name: str, symbol: str = None, exchange: str = None,
                        payload_overrides: dict = None) -> Any:
        await self._ensure_session()
        entry = self._registry.get(endpoint_name)
        rpc_id = entry.rpc_id
        payload = entry.payload_template
        if symbol:
            payload = payload.replace("{asset}", build_asset_identifier(symbol, exchange))
        payload = payload.replace("{ticker}", f'"{symbol}"' if symbol else '""')
        payload = payload.replace("{exchange}", f'"{exchange}"' if exchange else '""')
        if payload_overrides:
            for k, v in payload_overrides.items():
                payload = payload.replace("{" + k + "}", str(v))
        payload = payload.replace("{entity_ids}", "null").replace("{asset_filter}", "[]")
        payload = payload.replace("{query}", "").replace("{path}", "/finance/beta")

        self._reqid += 100000
        params = {
            "rpcids": rpc_id, "source-path": "/finance/beta",
            "f.sid": self._f_sid, "bl": self._bl, "hl": self._language,
            "soc-app": "1", "soc-platform": "1", "soc-device": "1",
            "_reqid": str(self._reqid), "rt": "c",
        }
        # Use json.dumps for proper escaping (payload may contain quotes)
        import json as _json
        f_req_data = [[[rpc_id, payload, None, "generic"]]]
        f_req_json = _json.dumps(f_req_data)
        body = f"f.req={f_req_json}&at={self._at or ''}"
        url = f"{FINANCE_BASE}/_/FinHubUi/data/batchexecute"

        try:
            async with self._session.post(url, params=params, data=body, headers={
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                "X-Same-Domain": "1", "Referer": f"{FINANCE_BASE}/",
            }) as resp:
                if resp.status != 200:
                    self._failure += 1
                    if resp.status in (400, 401, 403):
                        self._last_refresh = 0
                    return None
                text = await resp.text()
                payloads = parse_batchexecute(text)
                for p in payloads:
                    if p.get("rpc_id") == rpc_id:
                        self._success += 1
                        return p["data"]
                if payloads:
                    self._success += 1
                    return payloads[0]["data"]
                self._failure += 1
                return None
        except Exception as e:
            self._failure += 1
            logger.error("Async RPC failed: %s", e)
            return None

    async def get_quote(self, symbol: str, exchange: str = "NASDAQ") -> Quote:
        data = await self._call_rpc("quote_core", symbol=symbol, exchange=exchange)
        return extract_quote(data, symbol=symbol, exchange=exchange) if data else Quote(symbol=symbol, exchange=exchange)

    async def get_chart(self, symbol: str, exchange: str = "NASDAQ", period: str = "1M") -> ChartData:
        period_map = {"1D": 1, "5D": 2, "1M": 3, "6M": 4, "YTD": 5, "1Y": 6, "5Y": 7, "MAX": 8}
        period_code = period_map.get(period.upper(), 3)

        # Primary: use price_history_multi (best data quality)
        data = await self._call_rpc("price_history_multi", symbol=symbol, exchange=exchange,
                                     payload_overrides={"period": str(period_code)})
        if data:
            result = extract_ohlcv(data, symbol=symbol, exchange=exchange, period=period)
            if result.ticks:
                return result

        # Fallback: chart_data endpoint
        endpoint = "chart_crypto" if "-" in symbol and not exchange else "chart_data"
        data = await self._call_rpc(endpoint, symbol=symbol, exchange=exchange,
                                     payload_overrides={"period": str(period_code), "resolution_flag": "1"})
        return extract_ohlcv(data, symbol=symbol, exchange=exchange, period=period) if data else ChartData(symbol=symbol, exchange=exchange, period=period)

    async def get_company_details(self, symbol: str, exchange: str = "NASDAQ") -> CompanyDetails:
        data = await self._call_rpc("quote_details", symbol=symbol, exchange=exchange)
        return extract_company_details(data, symbol=symbol) if data else CompanyDetails(symbol=symbol)

    async def get_market_summary(self, region: str = "us") -> MarketSummary:
        region_map = {"us": 1, "europe": 2, "asia": 3}
        data = await self._call_rpc("market_summary", payload_overrides={"region": str(region_map.get(region, 1))})
        return extract_market_summary(data, region=region) if data else MarketSummary(region=region)

    async def search(self, query: str) -> List[SearchResult]:
        data = await self._call_rpc("search_autocomplete", payload_overrides={"query": query})
        return extract_search_results(data) if data else []

    async def get_news(self, symbol: str = None, exchange: str = None) -> List[NewsArticle]:
        if symbol:
            data = await self._call_rpc("quote_news", symbol=symbol, exchange=exchange)
        else:
            data = await self._call_rpc("news", payload_overrides={"query": "", "count": "10"})
        return extract_news(data) if data else []

    async def get_analyst_ratings(self, symbol: str, exchange: str = "NASDAQ") -> AnalystRating:
        data = await self._call_rpc("analyst_ratings", symbol=symbol, exchange=exchange)
        return extract_analyst_ratings(data, symbol=symbol) if data else AnalystRating(symbol=symbol)

    async def get_financial_statements(self, symbol: str, exchange: str = "NASDAQ") -> FinancialStatements:
        data = await self._call_rpc("financial_statements", symbol=symbol, exchange=exchange)
        return extract_financial_statements(data, symbol=symbol) if data else FinancialStatements(symbol=symbol)

    async def get_batch_quotes(self, symbols: List[tuple]) -> List[Quote]:
        tasks = [self.get_quote(sym, exch) for sym, exch in symbols]
        return await asyncio.gather(*tasks)

    def get_resilience_stats(self) -> dict:
        return {"success": self._success, "failure": self._failure,
                "session_healthy": not self._is_expired(), "f_sid_set": bool(self._f_sid)}

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False
