"""
Typed data models for Google Finance API responses.

Pydantic v2 BaseModel for validation + JSON/Dict export,
with a pandas DataFrame helper on ChartData.
"""

from __future__ import annotations

import json
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class Quote(BaseModel):
    """Real-time or latest stock / crypto / index quote."""
    symbol: str = ""
    exchange: str = ""
    name: str = ""
    price: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    currency: str = "USD"
    market_cap: Optional[str] = None
    market_cap_raw: Optional[float] = None
    volume: Optional[int] = None
    avg_volume: Optional[int] = None
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    prev_close: Optional[float] = None
    high_52w: Optional[float] = None
    low_52w: Optional[float] = None
    pe_ratio: Optional[float] = None
    eps: Optional[float] = None
    dividend_yield: Optional[float] = None
    beta: Optional[float] = None
    entity_type: str = "stock"
    timestamp: Optional[str] = None


class CompanyDetails(BaseModel):
    """Detailed company information."""
    symbol: str = ""
    name: str = ""
    exchange: str = ""
    sector: str = ""
    industry: str = ""
    ceo: Optional[str] = None
    employees: Optional[int] = None
    headquarters: Optional[str] = None
    founded: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None


class ChartTick(BaseModel):
    """Single data point in a chart time series."""
    timestamp: str = ""
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    price: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    volume: Optional[int] = None


class ChartData(BaseModel):
    """Chart time-series data for a security."""
    symbol: str = ""
    exchange: str = ""
    period: str = ""
    resolution: str = ""
    ticks: List[ChartTick] = Field(default_factory=list)

    @property
    def latest_price(self) -> Optional[float]:
        if self.ticks:
            last = self.ticks[-1]
            return last.close or last.price
        return None

    @property
    def highest(self) -> Optional[float]:
        highs = [t.high or t.price for t in self.ticks if (t.high or t.price) is not None]
        return max(highs) if highs else None

    @property
    def lowest(self) -> Optional[float]:
        lows = [t.low or t.price for t in self.ticks if (t.low or t.price) is not None]
        return min(lows) if lows else None

    def to_dataframe(self):
        """Convert to pandas DataFrame (requires optional `data` extra)."""
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas is required — install with: pip install gfinance[data]")
        data = [t.model_dump() for t in self.ticks]
        df = pd.DataFrame(data)
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df.set_index("timestamp", inplace=True)
        return df


class AnalystRating(BaseModel):
    """Analyst rating and price target data."""
    symbol: str = ""
    consensus: str = ""
    target_low: Optional[float] = None
    target_mean: Optional[float] = None
    target_high: Optional[float] = None
    target_median: Optional[float] = None
    num_analysts: int = 0
    ratings_breakdown: Dict[str, int] = Field(default_factory=dict)
    individual_ratings: List[Dict[str, Any]] = Field(default_factory=list)


class EarningsData(BaseModel):
    """Earnings history and calendar data."""
    symbol: str = ""
    next_earnings_date: Optional[str] = None
    quarterly_earnings: List[Dict[str, Any]] = Field(default_factory=list)
    consensus_eps: Optional[float] = None
    actual_eps: Optional[float] = None


class FinancialStatement(BaseModel):
    """A single financial statement (income, balance sheet, or cash flow)."""
    statement_type: str = ""
    periods: List[str] = Field(default_factory=list)
    line_items: Dict[str, List[Optional[float]]] = Field(default_factory=dict)


class FinancialStatements(BaseModel):
    """Complete financial statements for a company."""
    symbol: str = ""
    income_statement: Optional[FinancialStatement] = None
    balance_sheet: Optional[FinancialStatement] = None
    cash_flow: Optional[FinancialStatement] = None


class SearchResult(BaseModel):
    """A search result from autocomplete / symbol lookup."""
    symbol: str = ""
    name: str = ""
    exchange: str = ""
    entity_type: str = ""
    google_finance_url: str = ""


class MarketIndex(BaseModel):
    """A market index entry."""
    name: str = ""
    symbol: str = ""
    exchange: str = ""
    price: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None


class MarketSummary(BaseModel):
    """Market summary with indices, sectors, and movers."""
    indices: List[MarketIndex] = Field(default_factory=list)
    sectors: List[Dict[str, Any]] = Field(default_factory=list)
    region: str = ""
    timestamp: Optional[str] = None


class MarketMovers(BaseModel):
    """Market movers data (gainers, losers, most active)."""
    category: str = ""
    entities: List[Quote] = Field(default_factory=list)
    timestamp: Optional[str] = None


class NewsArticle(BaseModel):
    """A news article related to a stock or market."""
    title: str = ""
    source: str = ""
    url: str = ""
    time: Optional[str] = None
    snippet: Optional[str] = None
    image_url: Optional[str] = None
