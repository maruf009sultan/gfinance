"""
Session manager — zero-auth session acquisition with auto-refresh.

Extracts WIZ_global_data, f.sid, bl, at, SAPISIDHASH from Google Finance.
"""

import re
import time
import hashlib
import logging
from typing import Dict, Optional, Any
from dataclasses import dataclass, field

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from gfinance.exceptions import SessionError

logger = logging.getLogger(__name__)

FINANCE_BASE = "https://www.google.com/finance/beta"
SESSION_TTL = 1800  # 30 minutes


@dataclass
class FinanceSession:
    """Holds session tokens and cookies."""
    cookies: Dict[str, str] = field(default_factory=dict)
    f_sid: str = ""
    bl: str = ""
    at: str = ""
    sapisid: str = ""
    created_at: float = 0.0

    @property
    def is_expired(self) -> bool:
        return (time.time() - self.created_at) > SESSION_TTL

    def to_headers(self, base_url: str = FINANCE_BASE) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "Origin": "https://www.google.com",
            "Referer": f"{base_url}/",
            "X-Same-Domain": "1",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        }
        if self.sapisid:
            origin = "https://www.google.com"
            ts = str(int(time.time() * 1000))
            hash_input = f"{ts} {self.sapisid} {origin}"
            hash_val = hashlib.sha1(hash_input.encode()).hexdigest()
            headers["Authorization"] = f"SAPISIDHASH {ts}_{hash_val}"
        return headers


class SessionManager:
    """Zero-auth session manager with auto-refresh."""

    def __init__(self, base_url: str = FINANCE_BASE, proxies: Optional[Dict[str, str]] = None,
                 timeout: int = 30, language: str = "en-US"):
        self.base_url = base_url
        self.timeout = timeout
        self.language = language
        self._session: Optional[requests.Session] = None
        self._finance_session: Optional[FinanceSession] = None
        self._proxies = proxies
        self._reqid_counter = 100000

    def _create_session(self) -> requests.Session:
        s = requests.Session()
        retry = Retry(total=3, backoff_factor=1.0, status_forcelist=[429, 500, 502, 503, 504],
                      allowed_methods=["HEAD", "GET", "OPTIONS", "POST"])
        adapter = HTTPAdapter(max_retries=retry)
        s.mount("https://", adapter)
        s.mount("http://", adapter)
        s.headers.update({
            "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": self.language,
        })
        if self._proxies:
            s.proxies.update(self._proxies)
        return s

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = self._create_session()
        return self._session

    def get_session(self, force_refresh: bool = False) -> FinanceSession:
        if force_refresh or self._finance_session is None or self._finance_session.is_expired:
            self._finance_session = self._acquire()
        return self._finance_session

    def refresh(self) -> FinanceSession:
        return self.get_session(force_refresh=True)

    def next_reqid(self) -> str:
        self._reqid_counter += 100000
        return str(self._reqid_counter)

    def _acquire(self) -> FinanceSession:
        logger.info("Acquiring Google Finance session...")
        try:
            resp = self.session.get(self.base_url, timeout=self.timeout, allow_redirects=True)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise SessionError(f"Failed to fetch Google Finance page: {e}")

        html = resp.text
        fs = FinanceSession(created_at=time.time())

        # Extract tokens
        m = re.search(r'"FdrFJe"\s*:\s*"(-?\d+)"', html)
        if m:
            fs.f_sid = m.group(1)

        m = re.search(r'"cfb2h"\s*:\s*"([^"]+)"', html)
        if m:
            fs.bl = m.group(1)

        m = re.search(r'"SNlM0e"\s*:\s*"([^"]+)"', html)
        if m:
            fs.at = m.group(1)

        # Collect cookies
        for name, value in self.session.cookies.items():
            fs.cookies[name] = value
            if name.upper() == "SAPISID":
                fs.sapisid = value

        # Fallback f.sid from cookies
        if not fs.f_sid:
            for name, value in fs.cookies.items():
                if "sid" in name.lower() and "sapi" not in name.lower():
                    fs.f_sid = value
                    break

        logger.info("Session acquired: f.sid=%s..., bl=%s, at=%s, cookies=%d",
                     fs.f_sid[:20] if fs.f_sid else "NONE",
                     fs.bl[:30] if fs.bl else "NONE",
                     "yes" if fs.at else "no",
                     len(fs.cookies))
        return fs

    def build_batchexecute_url(self, rpc_id: str, source_path: str = "/finance/beta") -> str:
        fs = self.get_session()
        params = {
            "rpcids": rpc_id,
            "source-path": source_path,
            "f.sid": fs.f_sid,
            "bl": fs.bl,
            "hl": self.language,
            "authuser": "0",
            "soc-app": "1",
            "soc-platform": "1",
            "soc-device": "1",
            "_reqid": self.next_reqid(),
            "rt": "c",
        }
        param_str = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.base_url}/_/FinHubUi/data/batchexecute?{param_str}"

    def build_f_req(self, rpc_id: str, payload: str, reference: str = "generic") -> str:
        """Build the form body using json.dumps for proper encoding."""
        import json as _json
        fs = self.get_session()
        # The inner payload is already a JSON string; wrap it in the f.req structure
        f_req_data = [[[rpc_id, payload, None, reference]]]
        f_req_json = _json.dumps(f_req_data)
        at_val = fs.at or ""
        return f"f.req={f_req_json}&at={at_val}"

    def close(self):
        if self._session:
            self._session.close()
            self._session = None
