"""
Response data extractors — maps positional-array data to typed Pydantic models.
Uses both position-based extraction AND recursive extraction for robustness.
"""

import logging
from typing import Optional, List, Any

from gfinance.models import (
    Quote, CompanyDetails, ChartData, ChartTick,
    AnalystRating, EarningsData, FinancialStatement, FinancialStatements,
    SearchResult, MarketIndex, MarketSummary, MarketMovers, NewsArticle,
)
from gfinance.parser import recursive_extract, safe_get

logger = logging.getLogger(__name__)


def _f(data, path) -> Optional[float]:
    v = safe_get(data, tuple(path))
    if v is not None:
        try: return float(v)
        except (ValueError, TypeError): return None
    return None

def _i(data, path) -> Optional[int]:
    v = safe_get(data, tuple(path))
    if v is not None:
        try: return int(v)
        except (ValueError, TypeError): return None
    return None

def _s(data, path) -> Optional[str]:
    v = safe_get(data, tuple(path))
    return str(v) if v is not None else None


def _navigate_to_entity(data: Any) -> Any:
    """Navigate the deeply nested response to find the entity data array.
    
    The response format is: data[0][0][0] = [kg_id, [symbol, exchange], name, ...]
    Or sometimes just data[0] = [...]
    The entity is the innermost array that starts with a string (KG ID) or has a known structure.
    """
    current = data
    for _ in range(8):
        if not isinstance(current, list) or not current:
            break
        first = current[0]
        # If the first element is a string (KG ID like "/m/XXXX"), this IS the entity
        if isinstance(first, str):
            return current
        # If the first element is a list starting with a string, drill one more level
        if isinstance(first, list) and first:
            if isinstance(first[0], str):
                return first  # Found the entity at this level
            elif isinstance(first[0], list):
                current = first  # Keep drilling
            else:
                # First element is a number, null, etc. — this might be the entity
                return current
        else:
            break
    return current


def extract_quote(data: Any, symbol: str = "", exchange: str = "") -> Quote:
    if not data or not isinstance(data, list):
        return Quote(symbol=symbol, exchange=exchange)

    q = Quote(symbol=symbol, exchange=exchange)
    
    # Navigate to the entity data array
    entity = _navigate_to_entity(data)
    
    # The entity array structure (from actual Google Finance response):
    # [0] = KG ID ("/m/XXXXX") or null
    # [1] = [symbol, exchange]  OR  symbol string
    # [2] = name string
    # [3] = entity_type (0=stock, etc.)  OR  price data
    # [4] = currency  OR  price array [price, change, change%, ...]
    # [5] = [price, change, change%, ...]  OR  null
    # [7] = prev_close (in some formats)
    
    # Try the observed format first: entity[5] = [price, change, change%, ...]
    price_arr = safe_get(entity, [5])
    if isinstance(price_arr, list) and len(price_arr) >= 3:
        try: q.price = float(price_arr[0])
        except: pass
        try: q.change = float(price_arr[1])
        except: pass
        try: q.change_percent = float(price_arr[2])
        except: pass
    
    # Name and currency
    name_val = safe_get(entity, [2])
    if isinstance(name_val, str):
        q.name = name_val
    
    currency_val = safe_get(entity, [4])
    if isinstance(currency_val, str):
        q.currency = currency_val
    
    # Symbol and exchange from [1]
    ticker_arr = safe_get(entity, [1])
    if isinstance(ticker_arr, list) and len(ticker_arr) >= 2:
        q.symbol = str(ticker_arr[0]) if not q.symbol else q.symbol
        q.exchange = str(ticker_arr[1]) if not q.exchange else q.exchange
    elif isinstance(ticker_arr, str):
        if not q.symbol:
            q.symbol = ticker_arr
    
    # Prev close from [7]
    prev_close_val = safe_get(entity, [7])
    if isinstance(prev_close_val, (int, float)):
        q.prev_close = float(prev_close_val)
    
    # After-hours/extended data at [17]
    ext_price_arr = safe_get(entity, [17])
    if isinstance(ext_price_arr, list) and len(ext_price_arr) >= 3:
        # Extended hours price data
        pass  # Could extract extended price if needed
    
    # Entity type
    et = safe_get(entity, [3])
    if isinstance(et, (int, float)):
        et_val = int(et)
        if et_val == 3: q.entity_type = "crypto"
        elif et_val == 2: q.entity_type = "currency"
        elif et_val == 1: q.entity_type = "index"
        else: q.entity_type = "stock"

    # Fallback: if price is still None, use recursive extraction
    if q.price is None:
        nums = recursive_extract(entity, (int, float))
        float_nums = []
        for n in nums:
            try: float_nums.append(float(n))
            except: pass
        if float_nums:
            q.price = float_nums[0]
        if len(float_nums) > 1 and q.change is None:
            q.change = float_nums[1]
        if len(float_nums) > 2 and q.change_percent is None:
            q.change_percent = float_nums[2]

    return q


def extract_company_details(data: Any, symbol: str = "") -> CompanyDetails:
    d = CompanyDetails(symbol=symbol)
    if not data or not isinstance(data, list):
        return d
    entity = data[0] if isinstance(data[0], list) else data
    d.name = _s(entity, [0, 1]) or _s(entity, [1]) or ""
    d.exchange = _s(entity, [0, 2]) or _s(entity, [2]) or ""
    about = safe_get(entity, [0, 8]) if isinstance(safe_get(entity, [0]), list) else safe_get(entity, [8])
    if isinstance(about, list):
        d.sector = _s(about, [0]) or ""
        d.industry = _s(about, [1]) or ""
        d.ceo = _s(about, [2])
        d.employees = _i(about, [3])
        d.headquarters = _s(about, [4])
        d.description = _s(about, [5])
    # Recursive fallback for missing fields
    if not d.sector:
        strings = recursive_extract(entity, str)
        for i, s in enumerate(strings):
            sl = s.lower() if s else ""
            if "sector" in sl and i + 1 < len(strings):
                d.sector = strings[i + 1]
            elif "industry" in sl and i + 1 < len(strings):
                d.industry = strings[i + 1]
            elif "ceo" in sl and i + 1 < len(strings):
                d.ceo = strings[i + 1]
    return d


def extract_chart_data(data: Any, symbol: str = "", exchange: str = "", period: str = "") -> ChartData:
    chart = ChartData(symbol=symbol, exchange=exchange, period=period)
    if not data or not isinstance(data, list):
        return chart

    ticks_data = _find_ticks(data)
    for tick in ticks_data:
        if isinstance(tick, list):
            ct = _decode_tick(tick)
            if ct:
                chart.ticks.append(ct)

    if chart.ticks and ":" in (chart.ticks[0].timestamp or ""):
        chart.resolution = "intraday"
    elif chart.ticks:
        chart.resolution = "daily"
    return chart


def _find_ticks(data: Any) -> list:
    if not isinstance(data, list): return []
    if data and isinstance(data[0], list) and len(data[0]) >= 2:
        return data
    for item in data:
        if isinstance(item, list):
            r = _find_ticks(item)
            if r and len(r) > 1:
                return r
    return []


def _decode_tick(tick: list) -> Optional[ChartTick]:
    try:
        if len(tick) >= 3 and isinstance(tick[0], list):
            dt = tick[0]
            pi = tick[1] if len(tick) > 1 else []
            vol = tick[2] if len(tick) > 2 else None
            if len(dt) >= 5:
                ts = f"{dt[0]}-{dt[1]:02d}-{dt[2]:02d} {dt[3]:02d}:{dt[4]:02d}"
            elif len(dt) >= 3:
                ts = f"{dt[0]}-{dt[1]:02d}-{dt[2]:02d}"
            else:
                ts = str(dt)
            return ChartTick(
                timestamp=ts,
                price=pi[0] if len(pi) > 0 else None,
                change=pi[1] if len(pi) > 1 else None,
                change_percent=pi[2] if len(pi) > 2 else None,
                volume=int(vol) if vol is not None else None,
            )
        elif len(tick) >= 6 and isinstance(tick[0], (int, float)):
            return ChartTick(
                timestamp=str(tick[4]) if len(tick) > 4 else "",
                open=tick[0], close=tick[1], high=tick[2], low=tick[3],
                volume=int(tick[5]) if len(tick) > 5 else None,
            )
    except Exception as e:
        logger.debug("Tick decode failed: %s", e)
    return None


def extract_analyst_ratings(data: Any, symbol: str = "") -> AnalystRating:
    r = AnalystRating(symbol=symbol)
    if not data or not isinstance(data, list): return r
    entity = data[0] if isinstance(data[0], list) else data

    r.consensus = _s(entity, [0]) or ""
    targets = safe_get(entity, [1])
    if isinstance(targets, list):
        r.target_low = _f(targets, [0])
        r.target_mean = _f(targets, [1])
        r.target_high = _f(targets, [2])
        r.target_median = _f(targets, [3])
        r.num_analysts = _i(targets, [4]) or 0

    breakdown = safe_get(entity, [2])
    if isinstance(breakdown, list):
        labels = ["strong_buy", "buy", "hold", "sell", "strong_sell"]
        for i, label in enumerate(labels):
            if i < len(breakdown):
                r.ratings_breakdown[label] = _i(breakdown, [i]) or 0

    # Recursive fallback for consensus
    if not r.consensus:
        strings = recursive_extract(entity, str)
        for s in strings:
            sl = s.lower() if s else ""
            if sl in ("buy", "strong buy"): r.consensus = "Buy"; break
            elif sl in ("hold", "neutral"): r.consensus = "Hold"; break
            elif sl in ("sell", "strong sell"): r.consensus = "Sell"; break
    return r


def extract_earnings(data: Any, symbol: str = "") -> EarningsData:
    e = EarningsData(symbol=symbol)
    if not data or not isinstance(data, list): return e
    entity = data[0] if isinstance(data[0], list) else data
    e.next_earnings_date = _s(entity, [0])
    quarters = safe_get(entity, [1])
    if isinstance(quarters, list):
        for q in quarters:
            if isinstance(q, list):
                e.quarterly_earnings.append({
                    "quarter": _s(q, [0]) or "",
                    "eps_estimate": _f(q, [1]),
                    "eps_actual": _f(q, [2]),
                    "revenue_estimate": _f(q, [3]),
                    "revenue_actual": _f(q, [4]),
                })
    return e


def extract_financial_statements(data: Any, symbol: str = "") -> FinancialStatements:
    fs = FinancialStatements(symbol=symbol)
    if not data or not isinstance(data, list): return fs
    entity = data[0] if isinstance(data[0], list) else data
    inc = safe_get(entity, [0])
    if isinstance(inc, list): fs.income_statement = _parse_stmt(inc, "income")
    bs = safe_get(entity, [1])
    if isinstance(bs, list): fs.balance_sheet = _parse_stmt(bs, "balance_sheet")
    cf = safe_get(entity, [2])
    if isinstance(cf, list): fs.cash_flow = _parse_stmt(cf, "cash_flow")
    return fs


def _parse_stmt(data: list, stmt_type: str) -> FinancialStatement:
    stmt = FinancialStatement(statement_type=stmt_type)
    periods = safe_get(data, [0])
    if isinstance(periods, list):
        stmt.periods = [str(p) for p in periods if p is not None]
    items = safe_get(data, [1])
    if isinstance(items, list):
        for item in items:
            if isinstance(item, list) and len(item) >= 2:
                label = str(item[0]) if item[0] else ""
                vals = []
                for v in item[1:]:
                    try: vals.append(float(v) if v is not None else None)
                    except: vals.append(None)
                stmt.line_items[label] = vals
    return stmt


def extract_search_results(data: Any) -> List[SearchResult]:
    results = []
    if not data or not isinstance(data, list): return results
    for item in data:
        if not isinstance(item, list): continue
        sr = SearchResult()
        eid = safe_get(item, [0])
        if isinstance(eid, list):
            if len(eid) >= 2 and eid[0] is None and isinstance(eid[1], list):
                parts = eid[1]
                if len(parts) >= 2:
                    sr.symbol = parts[0]
                    sr.exchange = parts[1]
                    sr.entity_type = "stock"
            elif len(eid) >= 3 and eid[0] is None and eid[1] is None and isinstance(eid[2], list):
                parts = eid[2]
                if len(parts) >= 2:
                    sr.symbol = parts[0]
                    sr.exchange = parts[1]
                    sr.entity_type = "currency"
        sr.name = _s(item, [1]) or ""
        if sr.symbol:
            if sr.entity_type == "currency":
                sr.google_finance_url = f"https://www.google.com/finance/quote/{sr.symbol}-{sr.exchange}"
            else:
                sr.google_finance_url = f"https://www.google.com/finance/quote/{sr.symbol}:{sr.exchange}"
        results.append(sr)
    return results


def extract_market_summary(data: Any, region: str = "") -> MarketSummary:
    summary = MarketSummary(region=region)
    if not data or not isinstance(data, list): return summary
    indices = safe_get(data, [0])
    if isinstance(indices, list):
        for idx in indices:
            if isinstance(idx, list):
                summary.indices.append(MarketIndex(
                    name=_s(idx, [0]) or "",
                    symbol=_s(idx, [1]) or "",
                    exchange=_s(idx, [2]) or "",
                    price=_f(idx, [3]),
                    change=_f(idx, [4]),
                    change_percent=_f(idx, [5]),
                ))
    sectors = safe_get(data, [1])
    if isinstance(sectors, list):
        for sec in sectors:
            if isinstance(sec, list):
                summary.sectors.append({"name": _s(sec, [0]) or "", "change_pct": _f(sec, [1])})
    return summary


def extract_market_movers(data: Any, category: str = "") -> MarketMovers:
    movers = MarketMovers(category=category)
    if not data or not isinstance(data, list): return movers
    entities = safe_get(data, [0])
    if isinstance(entities, list):
        for entity in entities:
            if isinstance(entity, list):
                movers.entities.append(extract_quote(entity))
    return movers


def extract_ohlcv(data: Any, symbol: str = "", exchange: str = "", period: str = "") -> ChartData:
    """Extract OHLCV (Open-High-Low-Close-Volume) bar data from chart response.

    Handles the Google Finance price_history_multi (c2u4wc) response format:
      data[0][0][3] = list of periods, each period = [label, entries_list]
      Each entry = [[Y,M,D,h,m,null,null,[tz]], [close, change, change_pct, ...], cum_volume]

    Also handles fallback formats from other endpoints.
    """
    chart = ChartData(symbol=symbol, exchange=exchange, period=period)
    if not data or not isinstance(data, list):
        return chart

    # Try the price_history_multi format first
    periods_data = _extract_periods_from_multi(data)
    if periods_data:
        _build_ohlcv_from_periods(chart, periods_data, period)
        if chart.ticks:
            return chart

    # Fallback: try finding tick arrays directly
    ticks_raw = _find_ohlcv_ticks(data)
    if ticks_raw:
        for tick in ticks_raw:
            if not isinstance(tick, list):
                continue
            ct = _decode_ohlcv_tick(tick)
            if ct:
                chart.ticks.append(ct)
        if chart.ticks:
            first_ts = chart.ticks[0].timestamp or ""
            chart.resolution = "intraday" if ":" in first_ts else "daily"
            return chart

    # Final fallback: use standard chart extraction
    return extract_chart_data(data, symbol=symbol, exchange=exchange, period=period)


def _extract_periods_from_multi(data: Any) -> list:
    """Extract period arrays from price_history_multi response.
    
    Response: data[0][0][3] = [[label, entries], [label, entries], ...]
    """
    try:
        # Navigate: data -> [0] -> [0] -> [3]
        current = data
        for idx in [0, 0, 3]:
            if not isinstance(current, list) or idx >= len(current):
                return []
            current = current[idx]
        if isinstance(current, list) and current:
            # Verify it's the right format
            first = current[0]
            if isinstance(first, list) and len(first) >= 2:
                entries = first[1]
                if isinstance(entries, list):
                    return current
    except (IndexError, TypeError):
        pass
    return []


def _build_ohlcv_from_periods(chart: ChartData, periods: list, period_name: str):
    """Build OHLCV ticks from price_history_multi period data.
    
    Each entry: [[Y,M,D,h,m,null,null,[tz]], [close, change, change_pct, ...], cum_volume]
    For daily+ periods, we derive: open = close - change, volume = cum_vol difference.
    For intraday, same logic applies per tick.
    """
    is_intraday = period_name in ("1D", "5D")
    chart.resolution = "intraday" if is_intraday else "daily"

    # Use the first period (main trading session)
    for period in periods:
        if not isinstance(period, list) or len(period) < 2:
            continue
        entries = period[1]
        if not isinstance(entries, list):
            continue

        prev_cum_vol = 0
        for entry in entries:
            if not isinstance(entry, list) or len(entry) < 2:
                continue
            
            ts_arr = entry[0]
            price_arr = entry[1]
            cum_vol = entry[2] if len(entry) > 2 else None

            # Parse timestamp
            ts = _parse_timestamp(ts_arr)
            
            # Parse price data
            close_price = None
            change = None
            change_pct = None
            if isinstance(price_arr, list) and len(price_arr) >= 3:
                try: close_price = float(price_arr[0])
                except (ValueError, TypeError): pass
                try: change = float(price_arr[1])
                except (ValueError, TypeError): pass
                try: change_pct = float(price_arr[2])
                except (ValueError, TypeError): pass

            # Derive open from close and change
            open_price = None
            if close_price is not None and change is not None:
                open_price = close_price - change

            # Compute volume from cumulative
            volume = None
            if cum_vol is not None:
                try:
                    cv = int(cum_vol)
                    volume = cv - prev_cum_vol
                    if volume < 0:
                        volume = cv  # Reset happened (new period/session)
                    prev_cum_vol = cv
                except (ValueError, TypeError):
                    pass

            if close_price is not None or ts:
                chart.ticks.append(ChartTick(
                    timestamp=ts,
                    open=open_price,
                    close=close_price,
                    change=change,
                    change_percent=change_pct,
                    volume=volume,
                ))


def _parse_timestamp(ts_arr: Any) -> str:
    """Parse timestamp array [Y,M,D,h,m,null,null,[tz]] into string."""
    if not isinstance(ts_arr, list):
        return str(ts_arr) if ts_arr else ""
    try:
        year = ts_arr[0] if len(ts_arr) > 0 and ts_arr[0] is not None else None
        month = ts_arr[1] if len(ts_arr) > 1 and ts_arr[1] is not None else None
        day = ts_arr[2] if len(ts_arr) > 2 and ts_arr[2] is not None else None
        hour = ts_arr[3] if len(ts_arr) > 3 and ts_arr[3] is not None else None
        minute = ts_arr[4] if len(ts_arr) > 4 and ts_arr[4] is not None else None

        if year is not None and month is not None and day is not None:
            if hour is not None and minute is not None:
                return f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}"
            return f"{year}-{month:02d}-{day:02d}"
        return str(ts_arr)
    except (IndexError, TypeError, ValueError):
        return str(ts_arr)


def _find_ohlcv_ticks(data: Any, depth: int = 0) -> list:
    """Recursively find the array that contains OHLCV tick arrays."""
    if depth > 10 or not isinstance(data, list):
        return []
    # Check if this looks like a list of tick arrays
    if data and isinstance(data[0], list):
        first = data[0]
        # Format 1: [[Y,M,D,...], [O,H,L,C,V]] — nested date + price
        if len(first) >= 2 and isinstance(first[0], list) and isinstance(first[1], list):
            if len(first[0]) >= 3 and isinstance(first[0][0], (int, float)):
                return data
        # Format 2: [timestamp, O, H, L, C, V] — flat
        if len(first) >= 6 and isinstance(first[0], (int, float, str)):
            # Check if elements look like price data
            numeric_count = sum(1 for x in first if isinstance(x, (int, float)))
            if numeric_count >= 4:
                return data
        # Format 3: [timestamp, close, change, change_pct, volume] — tick
        if len(first) >= 3 and isinstance(first[0], (int, float, str)):
            return data
    # Drill deeper
    for item in data:
        if isinstance(item, list):
            result = _find_ohlcv_ticks(item, depth + 1)
            if result:
                return result
    return []


def _decode_ohlcv_tick(tick: list) -> Optional[ChartTick]:
    """Decode a single OHLCV tick from various formats."""
    try:
        # Format 1: [[Y,M,D,...], [O,H,L,C,V]] or [[Y,M,D,...], [close, change, change_pct], volume]
        if len(tick) >= 2 and isinstance(tick[0], list) and isinstance(tick[1], list):
            dt = tick[0]
            pi = tick[1]
            vol = tick[2] if len(tick) > 2 else None

            # Build timestamp
            if len(dt) >= 5:
                ts = f"{dt[0]}-{dt[1]:02d}-{dt[2]:02d} {dt[3]:02d}:{dt[4]:02d}"
            elif len(dt) >= 3:
                ts = f"{dt[0]}-{dt[1]:02d}-{dt[2]:02d}"
            else:
                ts = str(dt)

            # Determine if pi is OHLCV or [close, change, change_pct]
            if len(pi) >= 5:
                # Could be [open, high, low, close, volume] or [close, change, change_pct, ...]
                # Heuristic: if values are close in magnitude, likely OHLCV
                vals = [pi[0], pi[1], pi[2], pi[3]]
                try:
                    all_float = [float(v) for v in vals if v is not None]
                except (ValueError, TypeError):
                    all_float = []

                if len(all_float) >= 4:
                    max_v = max(abs(v) for v in all_float)
                    min_v = min(abs(v) for v in all_float)
                    if max_v > 0 and min_v / max_v > 0.5:
                        # Values are similar magnitude — likely OHLC
                        return ChartTick(
                            timestamp=ts,
                            open=pi[0], high=pi[1], low=pi[2], close=pi[3],
                            volume=int(pi[4]) if len(pi) > 4 and pi[4] is not None else (int(vol) if vol is not None else None),
                        )

            if len(pi) >= 3:
                # [close, change, change_pct] format
                return ChartTick(
                    timestamp=ts,
                    close=pi[0] if pi[0] is not None else None,
                    change=pi[1] if len(pi) > 1 and pi[1] is not None else None,
                    change_percent=pi[2] if len(pi) > 2 and pi[2] is not None else None,
                    volume=int(vol) if vol is not None else None,
                )

            if len(pi) >= 1:
                return ChartTick(
                    timestamp=ts,
                    price=pi[0] if pi[0] is not None else None,
                    volume=int(vol) if vol is not None else None,
                )

        # Format 2: flat [timestamp_or_seq, open, close, high, low, volume]
        elif len(tick) >= 6 and isinstance(tick[0], (int, float, str)):
            ts = str(tick[0]) if not isinstance(tick[0], str) else tick[0]
            # Try to convert numeric timestamp
            try:
                import datetime
                ts_num = int(float(str(tick[0])))
                if ts_num > 1e9:
                    ts = datetime.datetime.fromtimestamp(ts_num).strftime("%Y-%m-%d %H:%M")
                elif ts_num > 1e6:
                    ts = datetime.datetime.fromtimestamp(ts_num).strftime("%Y-%m-%d")
            except (ValueError, OSError, OverflowError):
                pass
            return ChartTick(
                timestamp=ts,
                open=tick[1], close=tick[2], high=tick[3], low=tick[4],
                volume=int(tick[5]) if tick[5] is not None else None,
            )

        # Format 3: [timestamp, price, change, change_pct, ...]
        elif len(tick) >= 3 and isinstance(tick[0], (int, float, str)):
            ts = str(tick[0])
            return ChartTick(
                timestamp=ts,
                close=tick[1] if tick[1] is not None else None,
                change=tick[2] if len(tick) > 2 and tick[2] is not None else None,
            )

    except Exception as e:
        logger.debug("OHLCV tick decode failed: %s", e)
    return None


def extract_news(data: Any) -> List[NewsArticle]:
    articles = []
    if not data or not isinstance(data, list): return articles
    for item in data:
        if not isinstance(item, list): continue
        articles.append(NewsArticle(
            title=_s(item, [0]) or "",
            source=_s(item, [1]) or "",
            url=_s(item, [2]) or "",
            time=_s(item, [3]),
            snippet=_s(item, [4]),
            image_url=_s(item, [5]),
        ))
    return articles
