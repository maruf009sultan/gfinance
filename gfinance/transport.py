"""
RPC transport layer — builds and sends batchexecute requests with retry logic.
"""

import json
import time
import logging
from typing import Any, Dict, List, Optional

import requests

from gfinance.session import SessionManager
from gfinance.parser import (
    parse_batchexecute, find_by_rpc_id, find_all_by_rpc_id,
    build_asset_identifier,
)
from gfinance.endpoints import EndpointRegistry
from gfinance.exceptions import RPCError, ParseError, RateLimitError

logger = logging.getLogger(__name__)


class RPCTransport:
    """Low-level transport for batchexecute RPC protocol with retries."""

    def __init__(self, session_manager: SessionManager, registry: EndpointRegistry,
                 max_retries: int = 3, retry_delay: float = 1.0, timeout: float = 30.0):
        self._session_mgr = session_manager
        self._registry = registry
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        self._timeout = timeout

    def call(self, endpoint_name: str, symbol: str = None, exchange: str = None,
             payload_overrides: dict = None) -> Any:
        """Make a single RPC call to a named endpoint."""
        entry = self._registry.get(endpoint_name)
        return self._call_rpc(entry, symbol=symbol, exchange=exchange,
                              payload_overrides=payload_overrides)

    def call_multiple(self, endpoint_names: List[str], symbol: str = None,
                      exchange: str = None) -> Dict[str, Any]:
        """Make multiple RPC calls (sequential for reliability)."""
        results = {}
        for name in endpoint_names:
            try:
                results[name] = self.call(name, symbol=symbol, exchange=exchange)
            except RPCError as e:
                logger.warning("call_multiple: %s failed: %s", name, e)
                results[name] = None
        return results

    def _call_rpc(self, endpoint, symbol: str = None, exchange: str = None,
                  payload_overrides: dict = None) -> Any:
        rpc_id = endpoint.rpc_id
        payload = endpoint.payload_template

        # Substitute asset identifier
        if symbol:
            asset_str = build_asset_identifier(symbol, exchange)
            payload = payload.replace("{asset}", asset_str)
        payload = payload.replace("{ticker}", f'"{symbol}"' if symbol else '""')
        payload = payload.replace("{exchange}", f'"{exchange}"' if exchange else '""')

        # Substitute overrides
        if payload_overrides:
            for key, value in payload_overrides.items():
                payload = payload.replace("{" + key + "}", str(value))

        # Clean unresolved
        payload = payload.replace("{entity_ids}", "null")
        payload = payload.replace("{asset_filter}", "[]")
        payload = payload.replace("{query}", "")
        payload = payload.replace("{path}", "/finance/beta")

        url = self._session_mgr.build_batchexecute_url(rpc_id)
        headers = self._session_mgr.get_session().to_headers(self._session_mgr.base_url)
        body = self._session_mgr.build_f_req(rpc_id, payload)

        for attempt in range(self._max_retries):
            try:
                resp = self._session_mgr.session.post(
                    url, data=body, headers=headers,
                    timeout=self._timeout,
                    cookies=self._session_mgr.get_session().cookies,
                )

                if resp.status_code == 429:
                    delay = self._retry_delay * (2 ** (attempt + 2))
                    logger.warning("Rate limited (429), waiting %.1fs", delay)
                    time.sleep(min(delay, 60))
                    continue

                if resp.status_code in (400, 401, 403):
                    # Session might be stale
                    self._session_mgr.refresh()
                    url = self._session_mgr.build_batchexecute_url(rpc_id)
                    headers = self._session_mgr.get_session().to_headers(self._session_mgr.base_url)
                    body = self._session_mgr.build_f_req(rpc_id, payload)
                    continue

                if resp.status_code != 200:
                    raise RPCError(f"HTTP {resp.status_code}", rpc_id=rpc_id)

                payloads = parse_batchexecute(resp.text)
                data = find_by_rpc_id(payloads, rpc_id)
                if data is not None:
                    return data
                # Try first payload as fallback
                if payloads:
                    return payloads[0].get("data")
                return None

            except (requests.RequestException, ParseError) as e:
                if attempt == self._max_retries - 1:
                    raise RPCError(f"Failed after {self._max_retries} retries: {e}", rpc_id=rpc_id)
                time.sleep(self._retry_delay * (attempt + 1))

        return None
