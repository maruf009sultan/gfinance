"""
Auto-healing engine — re-discovers RPC IDs via Playwright or HTML fallback.
"""

import re
import json
import asyncio
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

from gfinance.endpoints import EndpointRegistry, KNOWN_ENDPOINTS
from gfinance.exceptions import AutoHealError

logger = logging.getLogger(__name__)


@dataclass
class DiscoveredEndpoint:
    rpc_id: str
    data_service_key: str = "unknown"
    sample_keys: List[str] = None


class AutoHealEngine:
    """Re-discovers RPC function IDs when Google updates deployments."""

    def __init__(self, registry: EndpointRegistry):
        self.registry = registry

    async def heal_all(self) -> Dict[str, str]:
        """Re-discover all RPC IDs. Returns {endpoint_name: new_rpc_id}."""
        try:
            discoveries = await self._scan_with_playwright()
        except ImportError:
            logger.warning("Playwright not installed — falling back to HTML heal")
            return self._heal_html()
        except Exception as e:
            logger.warning("Playwright heal failed: %s — falling back", e)
            return self._heal_html()

        updates = {}
        for disc in discoveries:
            name = self._match(disc)
            if name:
                old = self.registry.get(name).rpc_id
                if old != disc.rpc_id:
                    logger.info("Healed: %s %s -> %s", name, old, disc.rpc_id)
                    self.registry.update_rpc_id(name, disc.rpc_id)
                    updates[name] = disc.rpc_id
        return updates

    def heal_sync(self) -> Dict[str, str]:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, self.heal_all())
                    return future.result(timeout=120)
            return loop.run_until_complete(self.heal_all())
        except RuntimeError:
            return asyncio.run(self.heal_all())

    # ─── Playwright-based scan ───

    async def _scan_with_playwright(self) -> List[DiscoveredEndpoint]:
        from playwright.async_api import async_playwright

        discoveries = []
        pages = ["/", "/quote/AAPL:NASDAQ", "/markets"]

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            responses = []

            async def on_response(response):
                if "batchexecute" in response.url:
                    try:
                        responses.append(await response.text())
                    except Exception:
                        pass

            page = await context.new_page()
            page.on("response", on_response)

            for path in pages:
                try:
                    await page.goto(f"https://www.google.com/finance{path}",
                                    wait_until="networkidle", timeout=30000)
                    await page.wait_for_timeout(2000)
                except Exception as e:
                    logger.warning("Failed to visit %s: %s", path, e)

            await browser.close()

        for raw in responses:
            discoveries.extend(self._parse_raw_for_rpc_ids(raw))
        return discoveries

    def _parse_raw_for_rpc_ids(self, raw: str) -> List[DiscoveredEndpoint]:
        discoveries = []
        try:
            if raw.startswith(")]}'"):
                raw = raw[4:].strip()
            data = json.loads(raw)

            def find_wrb(obj):
                if isinstance(obj, list):
                    for item in obj:
                        if isinstance(item, list) and len(item) >= 3 and item[0] == "wrb.fr":
                            discoveries.append(DiscoveredEndpoint(rpc_id=item[1]))
                        elif isinstance(item, list):
                            find_wrb(item)
            find_wrb(data)
        except (json.JSONDecodeError, IndexError):
            pass
        return discoveries

    # ─── HTML fallback ───

    def _heal_html(self) -> Dict[str, str]:
        import requests as req
        updates = {}
        try:
            resp = req.get("https://www.google.com/finance", headers={
                "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                               "Chrome/126.0.0.0 Safari/537.36"),
            }, timeout=30)
            html = resp.text

            # Extract ds:N -> RPC_ID from AF_initDataCallback
            pattern = r"AF_initDataCallback\(\{key:\s*'ds:(\d+)'.*?hash:\s*'[^']*'.*?data:(\[.*?\])\s*\}\)"
            for match in re.finditer(pattern, html, re.DOTALL):
                ds_index = int(match.group(1))
                try:
                    data = json.loads(match.group(2))
                    rpc_ids = self._find_rpc_ids(data)
                    for rpc_id in rpc_ids:
                        for name, ep in KNOWN_ENDPOINTS.items():
                            if ep.data_service_index == ds_index and ep.rpc_id != rpc_id:
                                self.registry.update_rpc_id(name, rpc_id)
                                updates[name] = rpc_id
                except (json.JSONDecodeError, ValueError):
                    continue

            # Also try ds:0 -> rpcid pattern
            ds_pattern = re.compile(r'"ds:(\d+)":\s*\["rpcid",\s*"([^"]+)"', re.MULTILINE)
            for m in ds_pattern.finditer(html):
                ds_index = int(m.group(1))
                rpc_id = m.group(2)
                for name, ep in KNOWN_ENDPOINTS.items():
                    if ep.data_service_index == ds_index and ep.rpc_id != rpc_id:
                        self.registry.update_rpc_id(name, rpc_id)
                        updates[name] = rpc_id
        except Exception as e:
            raise AutoHealError(f"HTML heal failed: {e}")
        return updates

    def _find_rpc_ids(self, data) -> List[str]:
        ids = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, list) and len(item) >= 2 and item[0] == "wrb.fr":
                    if isinstance(item[1], str):
                        ids.append(item[1])
                elif isinstance(item, list):
                    ids.extend(self._find_rpc_ids(item))
        return ids

    def _match(self, disc: DiscoveredEndpoint) -> Optional[str]:
        for name, ep in KNOWN_ENDPOINTS.items():
            if ep.rpc_id == disc.rpc_id:
                return name
        # Try by data_service_key
        m = re.match(r'ds:(\d+)', disc.data_service_key)
        if m:
            ds_index = int(m.group(1))
            for name, ep in KNOWN_ENDPOINTS.items():
                if ep.data_service_index == ds_index:
                    return name
        return None
