"""Chart service — historical prices, OHLCV, bar data, chart data."""

import logging
from typing import Any, Dict, List, Optional
from gfinance.transport import RPCTransport
from gfinance.models import ChartData, ChartTick
from gfinance.extractors import extract_chart_data, extract_ohlcv

logger = logging.getLogger(__name__)

VALID_PERIODS = {"1D", "5D", "1M", "6M", "YTD", "1Y", "5Y", "MAX"}

# Period codes for the price_history_multi (c2u4wc) endpoint
# This endpoint returns the most complete tick data with close/change/volume
PERIOD_CODE_MAP = {"1D": 1, "5D": 2, "1M": 3, "6M": 4, "YTD": 5, "1Y": 6, "5Y": 7, "MAX": 8}

# Period codes for the older chart_data (SICF5d) endpoint
CHART_PERIOD_MAP = {"1D": 1, "5D": 2, "1M": 3, "6M": 4, "YTD": 5, "1Y": 6, "5Y": 7, "MAX": 8}


class ChartService:
    def __init__(self, transport: RPCTransport):
        self._t = transport

    def data(self, symbol: str, exchange: str = "NASDAQ", period: str = "1M",
             include_volume: bool = True) -> ChartData:
        """Get chart data (time-series ticks with price/change/volume).

        This method uses the price_history_multi endpoint which returns
        tick-level data with close price, change, and cumulative volume.
        """
        period = period.upper()
        if period not in VALID_PERIODS:
            period = "1M"
        period_code = PERIOD_CODE_MAP.get(period, 3)

        # Primary: use price_history_multi (c2u4wc) — best data quality
        data = self._t.call("price_history_multi", symbol=symbol, exchange=exchange,
                            payload_overrides={"period": str(period_code)})
        if data:
            result = extract_ohlcv(data, symbol=symbol, exchange=exchange, period=period)
            if result.ticks:
                return result

        # Fallback: chart_data endpoint
        vol_flag = 1 if include_volume else 0
        endpoint = "chart_crypto" if "-" in symbol and not exchange else "chart_data"
        data = self._t.call(endpoint, symbol=symbol, exchange=exchange,
                            payload_overrides={"period": str(period_code), "resolution_flag": str(vol_flag)})
        return extract_chart_data(data, symbol=symbol, exchange=exchange, period=period) if data else ChartData(symbol=symbol, exchange=exchange, period=period)

    def ohlcv(self, symbol: str, exchange: str = "NASDAQ", period: str = "1M") -> ChartData:
        """Get OHLCV (Open-High-Low-Close-Volume) bar data.

        Returns a ChartData with ChartTick entries containing open, high, low,
        close, volume fields. For intraday periods (1D, 5D), ticks are
        aggregated into 1-minute bars. For daily periods (1M+), each tick is
        a daily bar with open derived from (close - change).

        Supported periods: 1D, 5D, 1M, 6M, YTD, 1Y, 5Y, MAX

        Usage:
            client = GoogleFinanceClient()
            bars = client.chart.ohlcv("AAPL", period="1Y")
            for tick in bars.ticks:
                print(tick.timestamp, tick.open, tick.high, tick.low, tick.close, tick.volume)

            # Convert to pandas DataFrame
            df = bars.to_dataframe()
            print(df[['open', 'high', 'low', 'close', 'volume']])
        """
        return self.data(symbol, exchange, period, include_volume=True)

    def history(self, symbol: str, exchange: str = "NASDAQ", period: str = "1Y") -> ChartData:
        """Alias for ohlcv() — get historical bar data."""
        return self.ohlcv(symbol, exchange, period)

    def intraday(self, symbol: str, exchange: str = "NASDAQ", period: str = "1D") -> ChartData:
        """Get intraday tick data (1-minute resolution for 1D, hourly for 5D)."""
        return self.data(symbol, exchange, period, include_volume=True)
