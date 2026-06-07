"""
Batchexecute protocol parser.

Handles Google's proprietary streaming response format:
  - XSSI prefix removal  )]}'\\n
  - Length-prefixed chunk parsing
  - Multi-level JSON unescaping (up to 3 levels)
  - Recursive data extraction for deeply nested arrays
"""

import json
import re
import logging
from typing import Any, Optional, List, Tuple

logger = logging.getLogger(__name__)

XSSI_PREFIX = ")]}'"


def strip_xssi(text: str) -> str:
    """Remove the anti-XSSI prefix and any leading whitespace/newlines."""
    if text.startswith(XSSI_PREFIX):
        cleaned = text[len(XSSI_PREFIX):]
        # Strip all leading whitespace/newlines aggressively
        return cleaned.lstrip("\r\n \t")
    return text.lstrip()


def parse_chunks(text: str) -> List[str]:
    """
    Parse length-prefixed chunk format.
    
    Google's batchexecute format:
      <byte_length>\\n<json_data>\\n<next_length>\\n<next_data>\\n...
    """
    chunks = []
    remaining = text.strip()
    while remaining:
        nl = remaining.find("\n")
        if nl == -1:
            # Last chunk without newline
            if remaining.strip():
                chunks.append(remaining)
            break
        try:
            chunk_len = int(remaining[:nl].strip())
        except ValueError:
            # Not a length prefix — try to parse as raw JSON
            remaining = remaining[nl + 1:]
            continue
        start = nl + 1
        end = start + chunk_len
        if end <= len(remaining):
            chunk_data = remaining[start:end]
            if chunk_data.strip():
                chunks.append(chunk_data)
            remaining = remaining[end:].lstrip("\r\n")
        else:
            # Incomplete chunk — take what we can
            chunk_data = remaining[start:]
            if chunk_data.strip():
                chunks.append(chunk_data)
            break
    return chunks


def unescape_json(escaped: Any, levels: int = 5) -> Any:
    """Iteratively JSON-parse until we get a non-string result."""
    result = escaped
    for _ in range(levels):
        if isinstance(result, str):
            try:
                parsed = json.loads(result)
                result = parsed
                if not isinstance(parsed, str):
                    break
            except (json.JSONDecodeError, TypeError):
                break
        else:
            break
    return result


def parse_batchexecute(response_text: str) -> List[dict]:
    """
    Full parse pipeline. Returns list of {rpc_id, data, reference}.
    
    Handles multiple response formats:
    1. Standard chunked: )]}\\n<len>\\n<json>\\n
    2. Simple: )]}\\n<json>
    """
    clean = strip_xssi(response_text)
    if not clean:
        return []
    
    chunks = parse_chunks(clean)
    results = []
    
    for chunk in chunks:
        try:
            outer = json.loads(chunk)
        except json.JSONDecodeError:
            # Try fixing common issues (trailing commas, etc.)
            try:
                # Sometimes the JSON has trailing content
                for end_char in [']]', ']}', ']']:
                    idx = chunk.rfind(end_char)
                    if idx > 0:
                        try:
                            outer = json.loads(chunk[:idx + len(end_char)])
                            break
                        except json.JSONDecodeError:
                            continue
                else:
                    continue
            except Exception:
                continue
        
        if not isinstance(outer, list):
            continue
        
        for item in outer:
            if not isinstance(item, list) or len(item) < 3:
                continue
            if item[0] != "wrb.fr":
                continue
            rpc_id = item[1]
            data_string = item[2]
            reference = item[6] if len(item) > 6 else None
            try:
                data = unescape_json(data_string)
            except Exception as e:
                logger.debug("Unescape failed for %s: %s", rpc_id, e)
                data = data_string
            results.append({"rpc_id": rpc_id, "data": data, "reference": reference})
    
    return results


def find_by_rpc_id(payloads: List[dict], rpc_id: str) -> Optional[Any]:
    for p in payloads:
        if isinstance(p, dict) and p.get("rpc_id") == rpc_id:
            return p.get("data")
    return None


def find_all_by_rpc_id(payloads: List[dict], rpc_id: str) -> List[Any]:
    return [p["data"] for p in payloads if isinstance(p, dict) and p.get("rpc_id") == rpc_id]


def recursive_extract(data: Any, target_type: type = None, max_depth: int = 50) -> List[Any]:
    """Recursively search nested arrays/dicts for values of a target type."""
    results = []
    def _walk(obj, depth):
        if depth > max_depth:
            return
        if target_type and isinstance(obj, target_type):
            results.append(obj)
        elif isinstance(obj, list):
            for item in obj:
                _walk(item, depth + 1)
        elif isinstance(obj, dict):
            for val in obj.values():
                _walk(val, depth + 1)
    _walk(data, 0)
    return results


def safe_get(data: Any, path: Tuple[int, ...], default: Any = None) -> Any:
    """Navigate nested lists by index path."""
    current = data
    for idx in path:
        try:
            current = current[idx]
        except (IndexError, TypeError, KeyError):
            return default
    return current


def build_asset_identifier(symbol: str, exchange: str = None) -> str:
    """Build a Google Finance asset identifier string."""
    if exchange:
        return f'[null, ["{symbol}", "{exchange}"]]'
    elif "-" in symbol:
        parts = symbol.split("-", 1)
        return f'[null, null, ["{parts[0]}", "{parts[1]}"]]'
    else:
        return f'[null, ["{symbol}", ""]]'
