"""Research service — AI-powered research queries via Google Finance."""

from typing import Any, Dict
from gfinance.transport import RPCTransport
from gfinance.parser import recursive_extract


class ResearchService:
    def __init__(self, transport: RPCTransport):
        self._t = transport

    def query(self, symbol: str, question: str) -> Dict[str, Any]:
        data = self._t.call("research", symbol=symbol,
                            payload_overrides={"query": question})
        if not data:
            return {"symbol": symbol, "question": question, "answer": None}
        strings = recursive_extract(data, str)
        return {
            "symbol": symbol,
            "question": question,
            "answer": strings[0] if strings else None,
            "sources": strings[1:] if len(strings) > 1 else [],
        }
