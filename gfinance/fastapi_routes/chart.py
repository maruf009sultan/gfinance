"""Chart routes — chart data, OHLCV bars, historical prices."""

from fastapi import APIRouter
from gfinance.fastapi_app import get_client, run_sync

router = APIRouter()


@router.get("/{symbol}")
async def chart_data(symbol: str, exchange: str = "NASDAQ", period: str = "1M"):
    """Get chart data (time-series ticks with price/change/volume)."""
    client = get_client()
    result = await run_sync(client.chart.data, symbol, exchange, period)
    return result.model_dump()


@router.get("/{symbol}/ohlcv")
async def ohlcv_data(symbol: str, exchange: str = "NASDAQ", period: str = "1M"):
    """Get OHLCV (Open-High-Low-Close-Volume) bar data.

    Supported periods: 1D, 5D, 1M, 6M, YTD, 1Y, 5Y, MAX
    """
    client = get_client()
    result = await run_sync(client.chart.ohlcv, symbol, exchange, period)
    return result.model_dump()


@router.get("/{symbol}/history")
async def price_history(symbol: str, exchange: str = "NASDAQ", period: str = "1Y"):
    """Get historical price data (alias for OHLCV with longer default period)."""
    client = get_client()
    result = await run_sync(client.chart.history, symbol, exchange, period)
    return result.model_dump()
