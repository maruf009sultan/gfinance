<div align="center">

# 🏦 gfinance

### Production-Grade Google Finance API Library

**Reverse-Engineered · Auto-Healing · Zero-Auth · Async + Sync · FastAPI Server**

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Version 2.0.0](https://img.shields.io/badge/Version-2.0.0-00C853?style=for-the-badge&logo=semver&logoColor=white)](https://github.com/maruf009sultan/gfinance)
[![License MIT](https://img.shields.io/badge/License-MIT-FDD835?style=for-the-badge&logo=open-source-initiative&logoColor=black)](https://opensource.org/licenses/MIT)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Arch Linux](https://img.shields.io/badge/Arch_Linux-Tested-1793D1?style=for-the-badge&logo=arch-linux&logoColor=white)](https://archlinux.org)

---

**The best of both worlds**: Merges `google-finance-api` (typed models, async, resilience) with `gfinance-beta` (modular services, Playwright auto-heal, robust parsing, SAPISIDHASH auth) into one battle-tested, production-grade library.

[🚀 Quick Start](#-quick-start) · [📦 Installation](#-installation) · [📖 Documentation](#-table-of-contents) · [🏗️ Architecture](#-architecture-deep-dive) · [🌐 REST API](#-fastapi-rest-api-server) · [⚖️ Legal](#-usage-guidelines--legal-disclaimer)

</div>

---

## 📑 Table of Contents

- [🌟 Why gfinance?](#-why-gfinance)
- [✨ Features Overview](#-features-overview)
- [📦 Installation](#-installation)
- [🚀 Quick Start](#-quick-start)
  - [Synchronous Client](#synchronous-client)
  - [Asynchronous Client](#asynchronous-client)
  - [FastAPI REST Server](#fastapi-rest-server)
- [📖 Deep Feature Analysis](#-deep-feature-analysis)
  - [1. Quote Service — Real-Time Stock Prices](#1-quote-service--real-time-stock-prices)
  - [2. Chart Service — Historical Price Data & OHLCV](#2-chart-service--historical-price-data--ohlcv)
  - [3. Market Service — Indices, Summaries & Movers](#3-market-service--indices-summaries--movers)
  - [4. News Service — Market & Ticker News](#4-news-service--market--ticker-news)
  - [5. Company Service — Company Info & Related Entities](#5-company-service--company-info--related-entities)
  - [6. Financials Service — Statements, Statistics & Dividends](#6-financials-service--statements-statistics--dividends)
  - [7. Analysts Service — Ratings, Earnings & Transcripts](#7-analysts-service--ratings-earnings--transcripts)
  - [8. Research Service — AI-Powered Investment Research](#8-research-service--ai-powered-investment-research)
  - [9. Search Service — Symbol Lookup & Autocomplete](#9-search-service--symbol-lookup--autocomplete)
- [🏗️ Architecture Deep Dive](#-architecture-deep-dive)
  - [System Architecture Diagram](#system-architecture-diagram)
  - [Core Components](#core-components)
  - [Request Lifecycle](#request-lifecycle)
  - [Data Flow: From Google to You](#data-flow-from-google-to-you)
- [🔌 RPC Endpoint Registry — 36+ Endpoints](#-rpc-endpoint-registry--36-endpoints)
  - [Complete Endpoint Reference Table](#complete-endpoint-reference-table)
  - [Endpoint Categories](#endpoint-categories)
- [🩹 Auto-Healing Engine](#-auto-healing-engine)
  - [How Auto-Healing Works](#how-auto-healing-works)
  - [Playwright-Based Discovery](#playwright-based-discovery)
  - [HTML Fallback Discovery](#html-fallback-discovery)
  - [Disk Caching](#disk-caching)
- [🛡️ Resilience & Circuit Breaker](#-resilience--circuit-breaker)
  - [Circuit Breaker States](#circuit-breaker-states)
  - [Retry with Exponential Backoff](#retry-with-exponential-backoff)
  - [Rate Limit Handling](#rate-limit-handling)
- [🔐 Session Management & Zero-Auth](#-session-management--zero-auth)
  - [SAPISIDHASH Authentication](#sapisidhash-authentication)
  - [Session Auto-Refresh](#session-auto-refresh)
- [📊 Pydantic Models Reference](#-pydantic-models-reference)
  - [Quote Model](#quote-model)
  - [CompanyDetails Model](#companydetails-model)
  - [ChartData & ChartTick Models](#chartdata--charttick-models)
  - [AnalystRating Model](#analystrating-model)
  - [EarningsData Model](#earningsdata-model)
  - [FinancialStatements Models](#financialstatements-models)
  - [SearchResult Model](#searchresult-model)
  - [MarketIndex, MarketSummary & MarketMovers Models](#marketindex-marketsummary--marketmovers-models)
  - [NewsArticle Model](#newsarticle-model)
- [🌐 FastAPI REST API Server](#-fastapi-rest-api-server)
  - [Complete API Reference](#complete-api-reference)
  - [Swagger UI & ReDoc](#swagger-ui--redoc)
  - [CORS Configuration](#cors-configuration)
  - [Error Handling](#error-handling)
  - [Running in Production](#running-in-production)
- [⚙️ Configuration Reference](#-configuration-reference)
  - [Client Configuration](#client-configuration)
  - [Async Client Configuration](#async-client-configuration)
  - [Server Configuration](#server-configuration)
  - [Environment Variables](#environment-variables)
- [🧪 Real Output Examples](#-real-output-examples)
  - [Live Test Results](#live-test-results)
- [📝 Advanced Usage Patterns](#-advanced-usage-patterns)
  - [Context Manager Pattern](#context-manager-pattern)
  - [Batch Processing](#batch-processing)
  - [DataFrame Export](#dataframe-export)
  - [Proxy Configuration](#proxy-configuration)
  - [Custom Retry Strategies](#custom-retry-strategies)
  - [Error Handling Patterns](#error-handling-patterns)
  - [Building a Stock Screener](#building-a-stock-screener)
  - [Building a Portfolio Tracker](#building-a-portfolio-tracker)
  - [Intraday Trading Dashboard](#intraday-trading-dashboard)
- [📦 Pydantic Model Export Methods](#-pydantic-model-export-methods)
- [🧩 Extending gfinance](#-extending-gfinance)
  - [Adding Custom Endpoints](#adding-custom-endpoints)
  - [Adding Custom Extractors](#adding-custom-extractors)
  - [Adding Custom FastAPI Routes](#adding-custom-fastapi-routes)
- [🧪 Batchexecute Protocol Internals](#-batchexecute-protocol-internals)
  - [XSSI Protection](#xssi-protection)
  - [Length-Prefixed Chunks](#length-prefixed-chunks)
  - [Multi-Level JSON Unescaping](#multi-level-json-unescaping)
  - [f.req Body Structure](#freq-body-structure)
- [🗺️ Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [📈 Marketing & SEO](#-marketing--seo)
  - [Project Keywords & Tags](#project-keywords--tags)
  - [Search Engine Optimization](#search-engine-optimization)
  - [Community & Social](#community--social)
  - [Package Registry SEO](#package-registry-seo)
  - [GitHub Repository SEO](#github-repository-seo)
  - [Content Marketing Ideas](#content-marketing-ideas)
- [⚖️ Usage Guidelines & Legal Disclaimer](#-usage-guidelines--legal-disclaimer)
  - [Important Legal Notice](#important-legal-notice)
  - [Terms of Service Compliance](#terms-of-service-compliance)
  - [Intended Use](#intended-use)
  - [Limitation of Liability](#limitation-of-liability)
  - [Data Accuracy Disclaimer](#data-accuracy-disclaimer)
  - [Rate Limiting & Responsible Use](#rate-limiting--responsible-use)
  - [No Warranty](#no-warranty)
  - [Indemnification](#indemnification)
  - [Jurisdiction](#jurisdiction)
- [📜 License](#-license)
- [🙏 Acknowledgements](#-acknowledgements)
- [📊 Project Statistics](#-project-statistics)

---

## 🌟 Why gfinance?

If you've ever tried to access Google Finance data programmatically, you know the pain: Google doesn't offer a public API for their finance platform. The data is served through a complex, obfuscated internal RPC protocol called `batchexecute`, which uses length-prefixed chunks, XSSI protection, multi-level JSON escaping, and cryptic RPC function IDs that change with every Google deployment.

**gfinance** solves all of this. It's the culmination of extensive reverse engineering of Google Finance's internal APIs, combining the best features from two previous libraries into one unified, battle-tested, production-grade package. Whether you need a quick stock quote for a personal project, real-time chart data for analysis, or a full REST API server for your team, gfinance has you covered.

### What Makes gfinance Different?

| Aspect | gfinance | yfinance | google-finance-api (original) |
|--------|----------|----------|-------------------------------|
| Data Source | Google Finance (batchexecute RPC) | Yahoo Finance (undocumented API) | Google Finance (limited) |
| Auto-Healing | ✅ Playwright + HTML fallback | ❌ Breaks on API changes | ❌ No healing |
| Circuit Breaker | ✅ Built-in resilience | ❌ No resilience | ✅ Basic |
| Async Support | ✅ Native aiohttp | ⚠️ Limited | ✅ Basic |
| Typed Models | ✅ Pydantic v2 (15 models) | ❌ Custom DataFrame-based | ✅ Pydantic v1 |
| REST API Server | ✅ FastAPI with Swagger | ❌ No server | ❌ No server |
| Auth Required | ❌ Zero auth (auto-session) | ❌ No auth | ⚠️ Session management |
| AI Research | ✅ Google Finance AI queries | ❌ Not available | ❌ Not available |
| Financial Statements | ✅ Income/BS/CF | ⚠️ Limited | ✅ Basic |
| Market Movers | ✅ Gainers/Losers/Active | ❌ Not available | ❌ Not available |
| Analyst Ratings | ✅ Consensus + targets | ⚠️ Basic | ✅ Basic |
| Earnings Transcripts | ✅ Full text | ❌ Not available | ❌ Not available |
| Search/Autocomplete | ✅ Google-powered | ⚠️ Basic | ❌ Not available |

---

## ✨ Features Overview

| Feature | Details |
|---------|---------|
| 🔥 **36+ RPC Endpoints** | Quotes, charts, news, financials, analysts, AI research, dividends, watchlist, search, and more — all discovered and mapped from Google Finance's internal API |
| 🩹 **Auto-Healing** | When Google updates their deployment and RPC IDs change, gfinance automatically re-discovers them via Playwright browser automation or HTML fallback parsing |
| 🔄 **Async + Sync** | Both `GoogleFinanceClient` (synchronous, requests-based) and `AsyncGoogleFinanceClient` (asynchronous, aiohttp-based) for any use case |
| 🛡️ **Circuit Breaker** | Prevents cascading failures by monitoring success/failure rates and automatically opening/closing the circuit to protect downstream systems |
| 🧱 **Typed Pydantic Models** | 15 Pydantic v2 models with `.model_dump()`, `.model_dump_json()`, DataFrame export, and full type safety for IDE autocompletion |
| 🚀 **FastAPI Server** | Production-ready REST API server with 24+ endpoints, Swagger UI, ReDoc, CORS middleware, and async-compatible `run_sync` helper |
| 🔐 **Zero Auth** | No API keys, no OAuth, no tokens — sessions are automatically generated with SAPISIDHASH authentication extracted from Google Finance |
| 📦 **Modern Packaging** | `pyproject.toml` only (no `setup.py`), PEP 621 compliant, optional dependency groups, CLI entry point |
| 🐧 **Arch-Tested** | Tested on Linux (Arch/Garuda compatible) with auto-dependency installation |
| 🔍 **Symbol Search** | Google-powered autocomplete search for stocks, crypto, currencies, and indices |
| 📊 **OHLCV Data** | Full Open-High-Low-Close-Volume chart data with 8 period options (1D to MAX) and pandas DataFrame export |
| 📰 **News Integration** | Both general market news and ticker-specific news articles with source, URL, and snippets |
| 💰 **Financial Statements** | Complete income statements, balance sheets, and cash flow statements with multi-period data |
| 📈 **Analyst Coverage** | Analyst consensus ratings, price targets, EPS estimates vs. actuals, and earnings call transcripts |
| 🤖 **AI Research** | Access Google Finance's AI-powered research queries for investment analysis |
| 💾 **Disk Caching** | RPC ID discoveries are cached to disk so healing results persist across restarts |
| 🔁 **Smart Retries** | Exponential backoff with jitter, automatic session refresh on auth failures, and rate limit awareness |

---

## 📦 Installation

### Basic Installation (Core Library Only)

The core library requires only `requests` and `pydantic` — minimal dependencies for maximum compatibility:

```bash
# Install from PyPI (when published)
pip install gfinance

# Or install from source
git clone https://github.com/maruf009sultan/gfinance.git
cd gfinance
pip install -e .
```

### Installation with Optional Dependencies

gfinance uses optional dependency groups so you only install what you need:

```bash
# With FastAPI server support
pip install -e ".[fastapi]"

# With async support (aiohttp)
pip install -e ".[async]"

# With auto-healing (requires Playwright + Chromium)
pip install -e ".[heal]"
playwright install chromium

# With pandas DataFrame export
pip install -e ".[data]"

# With development tools (pytest, httpx)
pip install -e ".[dev]"

# Everything at once
pip install -e ".[all]"
```

### Dependency Groups Reference

| Group | Packages | Purpose |
|-------|----------|---------|
| (core) | `requests>=2.28.0`, `pydantic>=2.0.0` | Minimum required — sync client + typed models |
| `async` | `aiohttp>=3.8.0` | Async client for concurrent, non-blocking access |
| `fastapi` | `fastapi>=0.100.0`, `uvicorn>=0.20.0` | REST API server with Swagger UI |
| `heal` | `playwright>=1.30.0` | Browser-based auto-healing for RPC ID discovery |
| `data` | `pandas>=1.5.0` | DataFrame export for chart/financial data |
| `dev` | `pytest>=7.0.0`, `pytest-asyncio>=0.21.0`, `httpx>=0.24.0` | Testing and development |
| `all` | All of the above | Complete installation |

### Arch Linux / Garuda Linux Setup

gfinance is tested on Arch Linux and Garuda Linux. Here's the quick setup:

```bash
# Install Python and pip
sudo pacman -S python python-pip

# Install gfinance with FastAPI server
pip install fastapi uvicorn requests pydantic

# Clone and install
git clone https://github.com/maruf009sultan/gfinance.git
cd gfinance
pip install -e ".[fastapi]"

# Start the server
python run.py
# Or: gfinance-server
# Or: uvicorn gfinance.fastapi_app:create_app --factory
```

### Verifying Installation

```python
import gfinance
print(gfinance.__version__)  # 2.0.0

from gfinance import GoogleFinanceClient
client = GoogleFinanceClient()
quote = client.quote.get("AAPL")
print(f"AAPL: ${quote.price}")  # Should print a real price
client.close()
```

---

## 🚀 Quick Start

### Synchronous Client

The `GoogleFinanceClient` is the primary entry point for synchronous access. It handles session management, RPC transport, and auto-healing automatically:

```python
from gfinance import GoogleFinanceClient

# Create client (auto-initializes session, no auth needed)
with GoogleFinanceClient() as client:
    # Get a stock quote
    quote = client.quote.get("AAPL", "NASDAQ")
    print(f"AAPL: ${quote.price} ({quote.change_percent:.2f}%)")
    print(f"Name: {quote.name}, Currency: {quote.currency}")
    # Output: AAPL: $307.34 (-1.25%)
    #         Name: Apple Inc, Currency: USD

    # Search for securities
    results = client.search.query("Bitcoin")
    for r in results:
        print(f"{r.symbol} - {r.name}")

    # Get market summary
    summary = client.market.summary("us")
    for idx in summary.indices:
        print(f"{idx.name}: {idx.price}")

    # Get company information
    info = client.company.info("TSLA", "NASDAQ")
    print(f"Sector: {info.sector}, CEO: {info.ceo}")

    # Get financial statements
    stmts = client.financials.statements("AAPL", "NASDAQ")
    print(f"Income stmt periods: {stmts.income_statement.periods if stmts.income_statement else 'N/A'}")

    # Get chart data
    chart = client.chart.data("AAPL", "NASDAQ", "1M")
    print(f"Chart ticks: {len(chart.ticks)}")
    if chart.ticks:
        latest = chart.ticks[-1]
        print(f"Latest: {latest.timestamp}, Close: ${latest.close}")

    # Get analyst ratings
    rating = client.analysts.ratings("AAPL", "NASDAQ")
    print(f"Consensus: {rating.consensus}")

    # Get market news
    news = client.news.market()
    for article in news:
        print(f"{article.title} - {article.source}")

    # Get dividend data
    dividends = client.financials.dividends("AAPL", "NASDAQ")
    print(f"Dividend yield: {dividends.get('yield')}")
```

### Asynchronous Client

The `AsyncGoogleFinanceClient` uses `aiohttp` for high-performance concurrent access. Perfect for fetching multiple quotes simultaneously, building async web applications, or processing large batches of symbols:

```python
import asyncio
from gfinance.async_client import AsyncGoogleFinanceClient

async def main():
    async with AsyncGoogleFinanceClient() as client:
        # Single quote
        quote = await client.get_quote("AAPL", "NASDAQ")
        print(f"AAPL: ${quote.price}")
        # Output: AAPL: $307.34

        # Concurrent batch quotes — fetch multiple symbols in parallel
        quotes = await client.get_batch_quotes([
            ("AAPL", "NASDAQ"),
            ("GOOGL", "NASDAQ"),
            ("MSFT", "NASDAQ"),
            ("AMZN", "NASDAQ"),
            ("NVDA", "NASDAQ"),
        ])
        for q in quotes:
            print(f"{q.symbol}: ${q.price} ({q.change_percent:.2f}%)")
        # Output:
        #   AAPL: $307.34 (-1.25%)
        #   GOOGL: $368.53 (-0.98%)
        #   MSFT: $416.67 (-2.66%)
        #   AMZN: $246.03 (-3.06%)
        #   NVDA: $205.10 (-6.20%)

        # Chart data
        chart = await client.get_chart("TSLA", "NASDAQ", "1M")
        print(f"TSLA chart: {len(chart.ticks)} ticks")

        # Market summary
        summary = await client.get_market_summary("us")
        for idx in summary.indices:
            print(f"{idx.name}: {idx.price}")

        # Search
        results = await client.search("NVIDIA")
        print(f"Found {len(results)} results")

        # Company details
        company = await client.get_company_details("MSFT", "NASDAQ")
        print(f"Microsoft: {company.name}")

        # Financial statements
        stmts = await client.get_financial_statements("AAPL", "NASDAQ")
        print(f"Has income statement: {stmts.income_statement is not None}")

        # Analyst ratings
        analyst = await client.get_analyst_ratings("AAPL")
        print(f"AAPL consensus: {analyst.consensus}")

        # News
        news = await client.get_news("AAPL")
        print(f"AAPL news articles: {len(news)}")

        # Check resilience stats
        stats = client.get_resilience_stats()
        print(f"Success: {stats['success']}, Failures: {stats['failure']}")
        print(f"Session healthy: {stats['session_healthy']}")

asyncio.run(main())
```

### FastAPI REST Server

gfinance includes a production-ready FastAPI server with 24+ REST endpoints, automatic Swagger UI documentation, CORS support, and async-compatible request handling:

```bash
# Start the server (auto-installs missing dependencies)
python run.py

# Or use the CLI entry point
gfinance-server

# Or use uvicorn directly with production settings
uvicorn gfinance.fastapi_app:create_app --factory --host 0.0.0.0 --port 8000 --workers 4
```

Then visit **http://localhost:8000/docs** for the interactive Swagger UI, or **http://localhost:8000/redoc** for the ReDoc documentation.

Quick test with curl:

```bash
# Health check
curl http://localhost:8000/health

# Get AAPL quote
curl http://localhost:8000/api/v1/quote/AAPL

# Get AAPL chart data (1 month)
curl http://localhost:8000/api/v1/chart/AAPL?period=1M

# Get market summary
curl http://localhost:8000/api/v1/market/summary?region=us

# Get market movers (gainers)
curl http://localhost:8000/api/v1/market/movers?category=gainers

# Get AAPL news
curl http://localhost:8000/api/v1/news/AAPL

# Get AAPL financial statements
curl http://localhost:8000/api/v1/financials/AAPL/statements

# Get AAPL analyst ratings
curl http://localhost:8000/api/v1/analysts/AAPL/ratings

# AI research query
curl -X POST http://localhost:8000/api/v1/research/query \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "question": "What are the key investment risks?"}'

# Trigger auto-healing
curl -X POST http://localhost:8000/api/v1/heal

# List all RPC endpoints
curl http://localhost:8000/api/v1/endpoints
```

---

## 📖 Deep Feature Analysis

This section provides an exhaustive, in-depth analysis of every feature, service, and component in gfinance. Each subsection covers the purpose, internal mechanics, API surface, real output examples, and best practices.

### 1. Quote Service — Real-Time Stock Prices

The `QuoteService` is the most frequently used service in gfinance. It provides access to real-time and delayed stock prices, company details, key statistics, and batch quote capabilities.

#### Methods

| Method | Endpoint Used | Description | Returns |
|--------|--------------|-------------|---------|
| `get(symbol, exchange)` | `quote_core` | Core price data: price, change, change%, volume, market cap | `Quote` |
| `details(symbol, exchange)` | `quote_details` | Extended company details: sector, CEO, employees | `CompanyDetails` |
| `stats(symbol, exchange)` | `quote_stats` | Key statistics: P/E ratio, EPS, beta, dividend yield | `Quote` |
| `realtime(symbol, exchange)` | `realtime_price` | Real-time price stream data (falls back to `get()`) | `Quote` |
| `batch_quotes(symbols)` | `quote_core` (loop) | Multiple quotes sequentially | `List[Quote]` |

#### How It Works

When you call `client.quote.get("AAPL", "NASDAQ")`, the following sequence occurs internally:

1. **Asset Identifier Construction**: The symbol and exchange are formatted into Google's internal asset identifier format: `[null, ["AAPL", "NASDAQ"]]`
2. **Payload Template Substitution**: The `quote_core` endpoint's payload template `[[{asset}], 1]` gets the asset identifier injected
3. **Session Acquisition**: The `SessionManager` provides the current session tokens (f.sid, bl, at, SAPISIDHASH)
4. **RPC Transport**: The `RPCTransport` builds the batchexecute URL and f.req body, then sends the POST request
5. **Response Parsing**: The raw response goes through XSSI stripping, chunk parsing, multi-level JSON unescaping
6. **Data Extraction**: The `extract_quote()` function navigates the deeply nested positional arrays to extract price, change, name, etc.
7. **Model Construction**: A typed `Quote` Pydantic model is returned with all extracted fields

#### Real Output Example

```python
from gfinance import GoogleFinanceClient

with GoogleFinanceClient() as client:
    quote = client.quote.get("AAPL", "NASDAQ")
    print(quote.model_dump())
```

Output (live data):

```python
{
    'symbol': 'AAPL',
    'exchange': 'NASDAQ',
    'name': 'Apple Inc',
    'price': 307.34,
    'change': -3.8900146,
    'change_percent': -1.2498841,
    'currency': 'USD',
    'market_cap': None,
    'market_cap_raw': None,
    'volume': None,
    'avg_volume': None,
    'open_price': None,
    'high_price': None,
    'low_price': None,
    'prev_close': 311.23,
    'high_52w': None,
    'low_52w': None,
    'pe_ratio': None,
    'eps': None,
    'dividend_yield': None,
    'beta': None,
    'entity_type': 'stock',
    'timestamp': None
}
```

#### Entity Type Detection

The Quote model automatically detects the entity type from Google's response:

- `entity_type = 0` → `"stock"` (equities like AAPL, TSLA)
- `entity_type = 1` → `"index"` (S&P 500, Dow Jones)
- `entity_type = 2` → `"currency"` (forex pairs)
- `entity_type = 3` → `"crypto"` (Bitcoin, Ethereum)

#### Batch Quotes

For fetching multiple quotes, the `batch_quotes()` method processes a list of (symbol, exchange) tuples:

```python
with GoogleFinanceClient() as client:
    quotes = client.quote.batch_quotes([
        ("AAPL", "NASDAQ"),
        ("GOOGL", "NASDAQ"),
        ("MSFT", "NASDAQ"),
        ("TSLA", "NASDAQ"),
        ("AMZN", "NASDAQ"),
    ])
    for q in quotes:
        print(f"{q.symbol}: ${q.price} ({q.change_percent:+.2f}%)")
```

For concurrent batch quotes, use the async client's `get_batch_quotes()` method which fetches all quotes in parallel using `asyncio.gather()`.

---

### 2. Chart Service — Historical Price Data & OHLCV

The `ChartService` provides comprehensive historical price data with support for 8 different time periods, OHLCV (Open-High-Low-Close-Volume) bar data, and pandas DataFrame export.

#### Methods

| Method | Description | Periods Supported |
|--------|-------------|-------------------|
| `data(symbol, exchange, period)` | Primary chart data method with automatic endpoint selection | 1D, 5D, 1M, 6M, YTD, 1Y, 5Y, MAX |
| `ohlcv(symbol, exchange, period)` | Get OHLCV bar data (alias for `data()` with `include_volume=True`) | Same as above |
| `history(symbol, exchange, period)` | Get historical data with 1Y default (alias for `ohlcv()`) | Same as above |
| `intraday(symbol, exchange, period)` | Get intraday tick data (1D or 5D) | 1D, 5D |

#### Supported Periods

| Period | Code | Resolution | Description |
|--------|------|-----------|-------------|
| `1D` | 1 | Intraday (1-min bars) | Single trading day with minute-level granularity |
| `5D` | 2 | Intraday (hourly) | Five trading days with hourly aggregation |
| `1M` | 3 | Daily | One month of daily closing prices |
| `6M` | 4 | Daily | Six months of daily OHLCV data |
| `YTD` | 5 | Daily | Year-to-date daily data |
| `1Y` | 6 | Daily | One full year of daily bars |
| `5Y` | 7 | Weekly | Five years of weekly data |
| `MAX` | 8 | Monthly | Maximum available historical data |

#### Endpoint Selection Strategy

The ChartService uses an intelligent fallback strategy for maximum data quality:

1. **Primary**: `price_history_multi` (RPC: `c2u4wc`) — Returns the most complete tick-level data with close price, change, change percentage, and cumulative volume. This endpoint provides the best data quality and is always tried first.

2. **Fallback**: `chart_data` (RPC: `SICF5d`) or `chart_crypto` (RPC: `in0BVc`) — Used when the primary endpoint returns empty data. The crypto-specific endpoint is automatically selected when the symbol contains a hyphen (e.g., `BTC-USDT`).

#### OHLCV Data Derivation

Google Finance doesn't always provide full OHLCV data directly. gfinance derives missing fields:

- **Open Price**: Calculated as `close - change` when only close and change are available
- **Volume**: Derived from cumulative volume by computing the difference between consecutive ticks
- **Resolution**: Automatically detected as `"intraday"` or `"daily"` based on timestamp format

#### Real Output Example

```python
with GoogleFinanceClient() as client:
    chart = client.chart.data("AAPL", "NASDAQ", "1M")
    print(f"Symbol: {chart.symbol}, Period: {chart.period}")
    print(f"Resolution: {chart.resolution}, Ticks: {len(chart.ticks)}")
    if chart.ticks:
        latest = chart.ticks[-1]
        print(f"Latest: {latest.timestamp}")
        print(f"  Open: ${latest.open}, Close: ${latest.close}")
        print(f"  Change: {latest.change} ({latest.change_percent}%)")
        print(f"  Volume: {latest.volume}")

    # DataFrame export (requires pandas)
    df = chart.to_dataframe()
    print(df.head())
```

Output (live data):

```
Symbol: AAPL, Period: 1M
Resolution: daily, Ticks: 22
Latest: 2026-06-05
  Open: $311.23, Close: $307.34
  Change: -3.8900146 (-1.2498841%)
  Volume: None
```

#### ChartTick Structure

Each tick in the `ChartData.ticks` list contains:

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `str` | Date/time string (YYYY-MM-DD or YYYY-MM-DD HH:MM) |
| `open` | `Optional[float]` | Opening price for the period |
| `high` | `Optional[float]` | Highest price during the period |
| `low` | `Optional[float]` | Lowest price during the period |
| `close` | `Optional[float]` | Closing price for the period |
| `price` | `Optional[float]` | Last traded price (alternative to close) |
| `change` | `Optional[float]` | Absolute price change from previous period |
| `change_percent` | `Optional[float]` | Percentage price change |
| `volume` | `Optional[int]` | Trading volume for the period |

#### ChartData Computed Properties

The `ChartData` model includes convenient computed properties:

```python
chart = client.chart.data("AAPL", "NASDAQ", "1M")

# Get the latest price (close or price of the last tick)
latest = chart.latest_price  # 307.34

# Get the highest price across all ticks
high = chart.highest  # e.g., 325.50

# Get the lowest price across all ticks
low = chart.lowest  # e.g., 295.12
```

---

### 3. Market Service — Indices, Summaries & Movers

The `MarketService` provides market-wide data including index summaries, sector performance, and market movers (gainers, losers, most active).

#### Methods

| Method | Endpoint Used | Description | Returns |
|--------|--------------|-------------|---------|
| `summary(region)` | `market_summary` | Market indices and sector performance | `MarketSummary` |
| `indices()` | `market_indices` | Major global market indices | `MarketSummary` |
| `movers(category)` | `market_screener` | Market movers by category | `MarketMovers` |

#### Supported Regions for Market Summary

| Region | Code | Description |
|--------|------|-------------|
| `"us"` | 1 | United States markets (default) |
| `"europe"` | 2 | European markets |
| `"asia"` | 3 | Asian markets |
| `"americas"` | 1 | Americas (alias for US) |

#### Supported Mover Categories

| Category | Code | Description |
|----------|------|-------------|
| `"most_active"` | 2 | Most actively traded securities (default) |
| `"gainers"` | 1 | Top price gainers |
| `"losers"` | 3 | Top price losers |

#### Real Output Example

```python
with GoogleFinanceClient() as client:
    # US Market summary
    summary = client.market.summary("us")
    for idx in summary.indices:
        print(f"{idx.name}: {idx.price} ({idx.change_percent}%)")

    # Market movers — top gainers
    gainers = client.market.movers("gainers")
    print(f"Category: {gainers.category}")
    for entity in gainers.entities[:5]:
        print(f"  {entity.symbol}: ${entity.price} ({entity.change_percent}%)")

    # Market movers — most active
    active = client.market.movers("most_active")
    print(f"Most active: {len(active.entities)} entities")

    # Global indices
    indices = client.market.indices()
    print(f"Global indices: {len(indices.indices)} entries")
```

Output (live data):

```
Equity benchmarks plunge as robust labor data fuels hawkish pivot: None (None%)
Semiconductor sector faces heavy losses amid cooling AI sentiment: None (None%)
Bitcoin and precious metals retreat in broad risk-off shift: None (None%)
Energy market volatility persists amid geopolitical and supply concerns: None (None%)
```

> **Note**: The market summary currently returns descriptive headlines rather than structured index data. The extractors parse what Google provides, and the response format may vary. The `indices()` method may return more structured data.

---

### 4. News Service — Market & Ticker News

The `NewsService` provides access to both general market news and ticker-specific news articles sourced from Google Finance's news feed.

#### Methods

| Method | Endpoint Used | Description | Returns |
|--------|--------------|-------------|---------|
| `market()` | `news` | General market news feed | `List[NewsArticle]` |
| `ticker(symbol, exchange)` | `quote_news` | Ticker-specific news articles | `List[NewsArticle]` |

#### NewsArticle Model

Each news article contains:

| Field | Type | Description |
|-------|------|-------------|
| `title` | `str` | Article headline |
| `source` | `str` | News source (Reuters, Bloomberg, etc.) |
| `url` | `str` | Direct link to the full article |
| `time` | `Optional[str]` | Publication time |
| `snippet` | `Optional[str]` | Article preview/snippet text |
| `image_url` | `Optional[str]` | Thumbnail image URL |

#### Real Output Example

```python
with GoogleFinanceClient() as client:
    # General market news
    news = client.news.market()
    print(f"Market news: {len(news)} articles")
    for article in news:
        print(f"  {article.title}")
        print(f"  Source: {article.source}, URL: {article.url}")

    # Ticker-specific news
    aapl_news = client.news.ticker("AAPL", "NASDAQ")
    for article in aapl_news:
        print(f"  {article.title} - {article.source}")
```

---

### 5. Company Service — Company Info & Related Entities

The `CompanyService` provides detailed company information and related company discovery.

#### Methods

| Method | Endpoint Used | Description | Returns |
|--------|--------------|-------------|---------|
| `info(symbol, exchange)` | `company_info` | Company description, sector, CEO, employees | `CompanyDetails` |
| `related(symbol, exchange)` | `related_companies` | Related/similar companies in the same sector | `List[Dict]` |

#### CompanyDetails Model

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | `str` | Stock ticker symbol |
| `name` | `str` | Company name |
| `exchange` | `str` | Stock exchange |
| `sector` | `str` | Business sector (e.g., "Technology") |
| `industry` | `str` | Industry classification |
| `ceo` | `Optional[str]` | Chief Executive Officer name |
| `employees` | `Optional[int]` | Number of employees |
| `headquarters` | `Optional[str]` | Company headquarters location |
| `founded` | `Optional[str]` | Year founded |
| `description` | `Optional[str]` | Company description |
| `website` | `Optional[str]` | Company website URL |

#### Extraction Strategy

The company details extractor uses a dual strategy for maximum field recovery:

1. **Position-based extraction**: Navigates the known positions in Google's nested arrays (sector at `about[0]`, industry at `about[1]`, CEO at `about[2]`, etc.)
2. **Recursive fallback**: If position-based extraction fails, uses `recursive_extract()` to find all strings in the response and matches them by keyword patterns ("sector", "industry", "ceo")

This dual approach ensures robustness against changes in Google's response format.

#### Real Output Example

```python
with GoogleFinanceClient() as client:
    info = client.company.info("TSLA", "NASDAQ")
    print(f"Name: {info.name}")
    print(f"Sector: {info.sector}")
    print(f"CEO: {info.ceo}")
    print(f"Employees: {info.employees}")
    print(f"Headquarters: {info.headquarters}")

    # Related companies
    related = client.company.related("AAPL", "NASDAQ")
    for r in related:
        print(f"  {r.get('ticker')}: {r.get('name')}")
```

---

### 6. Financials Service — Statements, Statistics & Dividends

The `FinancialsService` provides comprehensive financial data including income statements, balance sheets, cash flow statements, key statistics, and dividend history.

#### Methods

| Method | Endpoint Used | Description | Returns |
|--------|--------------|-------------|---------|
| `statements(symbol, exchange)` | `financial_statements` | Complete financial statements | `FinancialStatements` |
| `statistics(symbol, exchange)` | `quote_stats` | Key financial statistics | `Quote` |
| `dividends(symbol, exchange)` | `dividends` | Dividend history and yield | `Dict` |

#### FinancialStatements Model

```python
class FinancialStatements(BaseModel):
    symbol: str
    income_statement: Optional[FinancialStatement] = None
    balance_sheet: Optional[FinancialStatement] = None
    cash_flow: Optional[FinancialStatement] = None

class FinancialStatement(BaseModel):
    statement_type: str  # "income", "balance_sheet", or "cash_flow"
    periods: List[str]  # e.g., ["Q2 2026", "Q1 2026", "Q4 2025"]
    line_items: Dict[str, List[Optional[float]]]  # e.g., {"Revenue": [111.18B, 95.36B, ...]}
```

#### Real Output Example

```python
with GoogleFinanceClient() as client:
    stmts = client.financials.statements("AAPL", "NASDAQ")

    # Income statement
    if stmts.income_statement:
        print(f"Periods: {stmts.income_statement.periods}")
        for item, values in stmts.income_statement.line_items.items():
            print(f"  {item}: {values}")

    # Balance sheet
    if stmts.balance_sheet:
        print(f"Balance sheet periods: {stmts.balance_sheet.periods}")

    # Cash flow
    if stmts.cash_flow:
        print(f"Cash flow periods: {stmts.cash_flow.periods}")

    # Dividends
    divs = client.financials.dividends("AAPL", "NASDAQ")
    print(f"Dividend yield: {divs.get('yield')}")
    for entry in divs.get('history', []):
        print(f"  {entry['date']}: ${entry['amount']}")
```

The financial statements endpoint returns incredibly rich data. For Apple (AAPL), the response includes detailed quarterly data going back many years, with line items like Revenue, Net Income, Operating Income, EPS, and dozens more financial metrics for each period.

---

### 7. Analysts Service — Ratings, Earnings & Transcripts

The `AnalystsService` provides analyst consensus ratings, price targets, EPS estimates vs. actuals, and even earnings call transcripts.

#### Methods

| Method | Endpoint Used | Description | Returns |
|--------|--------------|-------------|---------|
| `ratings(symbol, exchange)` | `analyst_ratings` | Analyst consensus & price targets | `AnalystRating` |
| `earnings(symbol, exchange)` | `earnings` | EPS estimates & actuals | `EarningsData` |
| `transcript(symbol)` | `earnings_transcript` | Earnings call transcript text | `Dict` |

#### AnalystRating Model

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | `str` | Stock ticker |
| `consensus` | `str` | Overall analyst consensus (Buy/Hold/Sell) |
| `target_low` | `Optional[float]` | Lowest price target |
| `target_mean` | `Optional[float]` | Average price target |
| `target_high` | `Optional[float]` | Highest price target |
| `target_median` | `Optional[float]` | Median price target |
| `num_analysts` | `int` | Number of analysts covering |
| `ratings_breakdown` | `Dict[str, int]` | Breakdown by rating (strong_buy, buy, hold, sell, strong_sell) |
| `individual_ratings` | `List[Dict]` | Individual analyst ratings with details |

#### EarningsData Model

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | `str` | Stock ticker |
| `next_earnings_date` | `Optional[str]` | Next earnings report date |
| `quarterly_earnings` | `List[Dict]` | Quarterly EPS estimates vs. actuals |
| `consensus_eps` | `Optional[float]` | Current consensus EPS estimate |
| `actual_eps` | `Optional[float]` | Most recent actual EPS |

Each entry in `quarterly_earnings` contains:

```python
{
    "quarter": "Q2 2026",
    "eps_estimate": 1.94,
    "eps_actual": 2.01,
    "revenue_estimate": 109580000000,
    "revenue_actual": 111180000000
}
```

#### Real Output Example

```python
with GoogleFinanceClient() as client:
    # Analyst ratings
    rating = client.analysts.ratings("AAPL", "NASDAQ")
    print(f"Consensus: {rating.consensus}")
    print(f"Target mean: ${rating.target_mean}")
    print(f"Target range: ${rating.target_low} - ${rating.target_high}")
    print(f"Breakdown: {rating.ratings_breakdown}")

    # Earnings data
    earnings = client.analysts.earnings("AAPL", "NASDAQ")
    print(f"Next earnings: {earnings.next_earnings_date}")
    for q in earnings.quarterly_earnings:
        print(f"  {q['quarter']}: Est ${q['eps_estimate']}, Actual ${q['eps_actual']}")

    # Earnings transcript
    transcript = client.analysts.transcript("AAPL")
    print(f"Quarter: {transcript.get('quarter')}")
    print(f"Date: {transcript.get('date')}")
    if transcript.get('text'):
        print(transcript['text'][:500])
```

---

### 8. Research Service — AI-Powered Investment Research

The `ResearchService` accesses Google Finance's AI-powered research queries, allowing you to ask natural language questions about stocks and receive AI-generated analysis.

#### Methods

| Method | Endpoint Used | Description | Returns |
|--------|--------------|-------------|---------|
| `query(symbol, question)` | `research` | Ask an AI research question about a stock | `Dict` |

#### Usage

```python
with GoogleFinanceClient() as client:
    # Ask a research question
    result = client.research.query("AAPL", "What are the key investment risks?")
    print(f"Symbol: {result['symbol']}")
    print(f"Question: {result['question']}")
    print(f"Answer: {result['answer']}")
    print(f"Sources: {result.get('sources', [])}")

    # More research queries
    result2 = client.research.query("TSLA", "What is Tesla's competitive advantage?")
    result3 = client.research.query("NVDA", "How does NVIDIA's GPU business compare to competitors?")
```

The research endpoint uses Google Finance's internal `FinanceHubService/ExecuteResearchQuery` RPC, which leverages Google's AI capabilities to generate investment analysis. The response includes the AI-generated answer along with source references.

> **Note**: This feature depends on Google Finance's AI research functionality being available, which may vary by region and stock.

---

### 9. Search Service — Symbol Lookup & Autocomplete

The `SearchService` provides Google-powered autocomplete search for stocks, crypto, currencies, indices, and other financial instruments.

#### Methods

| Method | Endpoint Used | Description | Returns |
|--------|--------------|-------------|---------|
| `query(query)` | `search_autocomplete` | Search for securities by name or symbol | `List[SearchResult]` |

#### SearchResult Model

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | `str` | Ticker symbol (e.g., "AAPL", "BTC") |
| `name` | `str` | Full name (e.g., "Apple Inc", "Bitcoin") |
| `exchange` | `str` | Exchange (e.g., "NASDAQ", "USDT") |
| `entity_type` | `str` | Type: "stock", "currency", etc. |
| `google_finance_url` | `str` | Direct link to Google Finance page |

#### Real Output Example

```python
with GoogleFinanceClient() as client:
    results = client.search.query("Bitcoin")
    for r in results:
        print(f"{r.symbol}:{r.exchange} - {r.name} ({r.entity_type})")
        print(f"  URL: {r.google_finance_url}")

    results2 = client.search.query("Tesla")
    for r in results2:
        print(f"{r.symbol}:{r.exchange} - {r.name}")
```

The search service handles different entity types automatically. For crypto pairs like "BTC-USDT", it generates the correct Google Finance URL format. For stocks, it uses the colon format (e.g., `AAPL:NASDAQ`).

---

## 🏗️ Architecture Deep Dive

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Your Application                          │
├─────────────────────┬───────────────────────────────────────────┤
│   Sync Client       │          Async Client                     │
│  (GoogleFinance     │     (AsyncGoogleFinance                   │
│    Client)          │      Client)                               │
│                     │                                            │
│  ┌───────────────┐  │  ┌──────────────────┐                     │
│  │  Services     │  │  │  Direct Methods   │                     │
│  │  • QuoteService│  │  │  • get_quote()    │                     │
│  │  • MarketService│  │  │  • get_chart()    │                     │
│  │  • ChartService│  │  │  • get_company()  │                     │
│  │  • NewsService │  │  │  • search()       │                     │
│  │  • CompanyServ.│  │  │  • get_batch()    │                     │
│  │  • FinancialsS.│  │  └──────────────────┘                     │
│  │  • AnalystsS.  │  │                                            │
│  │  • ResearchS.  │  │                                            │
│  │  • SearchS.    │  │                                            │
│  └───────┬───────┘  │                                            │
│          │          │                                            │
├──────────┼──────────┴───────────────────────────────────────────┤
│          ▼                                                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    RPCTransport                            │  │
│  │  • Build batchexecute URLs                                │  │
│  │  • Construct f.req bodies                                 │  │
│  │  • Handle retries with exponential backoff                │  │
│  │  • Auto-refresh sessions on auth failures                 │  │
│  └───────────┬───────────────────────────────────────────────┘  │
│              │                                                   │
│  ┌───────────┼───────────────────────────────────────────────┐  │
│  │           ▼                                               │  │
│  │  ┌─────────────────┐    ┌─────────────────────────┐      │  │
│  │  │ SessionManager   │    │  EndpointRegistry       │      │  │
│  │  │ • f.sid token    │    │  • 36+ RPC endpoints    │      │  │
│  │  │ • bl token       │    │  • Payload templates    │      │  │
│  │  │ • at token       │    │  • Category mapping     │      │  │
│  │  │ • SAPISIDHASH    │    │  • Disk caching         │      │  │
│  │  │ • Cookie jar     │    │  • Reverse lookup       │      │  │
│  │  │ • Auto-refresh   │    │                          │      │  │
│  │  └────────┬────────┘    └───────────┬──────────────┘      │  │
│  │           │                         │                      │  │
│  │           ▼                         ▼                      │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │               Google Finance Beta                    │  │  │
│  │  │  https://www.google.com/finance/beta                 │  │  │
│  │  │                                                       │  │  │
│  │  │  /_/FinHubUi/data/batchexecute                       │  │  │
│  │  │  ┌───────────────────────────────────────────────┐   │  │  │
│  │  │  │  Response Pipeline:                            │   │  │  │
│  │  │  │  1. XSSI prefix removal  )]}'\\n              │   │  │  │
│  │  │  │  2. Length-prefixed chunk parsing              │   │  │  │
│  │  │  │  3. Multi-level JSON unescaping (up to 5)     │   │  │  │
│  │  │  │  4. RPC ID matching                           │   │  │  │
│  │  │  └───────────────────────────────────────────────┘   │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Resilience Layer                         │  │
│  │  ┌─────────────────┐    ┌───────────────────────────┐    │  │
│  │  │ CircuitBreaker   │    │  AutoHealEngine           │    │  │
│  │  │ • Failure count  │    │  • Playwright scan        │    │  │
│  │  │ • Success count  │    │  • HTML fallback          │    │  │
│  │  │ • Open/Closed    │    │  • RPC ID matching        │    │  │
│  │  │ • Reset timeout  │    │  • Disk cache persistence │    │  │
│  │  └─────────────────┘    └───────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Parser & Extractors                      │  │
│  │  • strip_xssi()          • extract_quote()                │  │
│  │  • parse_chunks()        • extract_company_details()      │  │
│  │  • unescape_json()       • extract_ohlcv()                │  │
│  │  • parse_batchexecute()  • extract_analyst_ratings()      │  │
│  │  • recursive_extract()   • extract_earnings()             │  │
│  │  • safe_get()            • extract_financial_statements() │  │
│  │  • build_asset_identifier() • extract_search_results()    │  │
│  │                           • extract_market_summary()      │  │
│  │                           • extract_market_movers()       │  │
│  │                           • extract_news()                │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   FastAPI Server Layer                      │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │  │
│  │  │ Quote    │ │ Market   │ │ Chart    │ │ News     │    │  │
│  │  │ Routes   │ │ Routes   │ │ Routes   │ │ Routes   │    │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │  │
│  │  │ Company  │ │Financials│ │ Analysts │ │ Research │    │  │
│  │  │ Routes   │ │ Routes   │ │ Routes   │ │ Routes   │    │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │  │
│  │  ┌──────────┐                                              │  │
│  │  │ System   │  CORS Middleware  ·  Swagger UI  ·  ReDoc   │  │
│  │  │ Routes   │                                              │  │
│  │  └──────────┘                                              │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. `GoogleFinanceClient` (client.py)

The main synchronous entry point. It orchestrates all other components:

```python
class GoogleFinanceClient:
    def __init__(self, proxies=None, max_retries=3, retry_delay=1.0,
                 timeout=30.0, auto_heal=True, language="en-US"):
        self._session_mgr = SessionManager(proxies=proxies, timeout=timeout, language=language)
        self._registry = EndpointRegistry()
        self._transport = RPCTransport(session_manager, registry, max_retries, retry_delay, timeout)
        self._circuit_breaker = CircuitBreaker()
        self._auto_heal_engine = AutoHealEngine(registry)

        # 9 service modules
        self.quote = QuoteService(transport)
        self.market = MarketService(transport)
        self.chart = ChartService(transport)
        self.news = NewsService(transport)
        self.company = CompanyService(transport)
        self.financials = FinancialsService(transport)
        self.analysts = AnalystsService(transport)
        self.research = ResearchService(transport)
        self.search = SearchService(transport)
```

The client is designed as a facade pattern — it provides a clean, simple interface while delegating to specialized internal components. Each service module is independently responsible for its domain, making the codebase modular and maintainable.

#### 2. `AsyncGoogleFinanceClient` (async_client.py)

The asynchronous counterpart using aiohttp. Unlike the sync client which delegates to service modules, the async client implements all methods directly for maximum performance:

```python
class AsyncGoogleFinanceClient:
    async def get_quote(self, symbol, exchange="NASDAQ") -> Quote
    async def get_chart(self, symbol, exchange="NASDAQ", period="1M") -> ChartData
    async def get_company_details(self, symbol, exchange="NASDAQ") -> CompanyDetails
    async def get_market_summary(self, region="us") -> MarketSummary
    async def search(self, query) -> List[SearchResult]
    async def get_news(self, symbol=None, exchange=None) -> List[NewsArticle]
    async def get_analyst_ratings(self, symbol, exchange="NASDAQ") -> AnalystRating
    async def get_financial_statements(self, symbol, exchange="NASDAQ") -> FinancialStatements
    async def get_batch_quotes(self, symbols) -> List[Quote]  # Concurrent!
```

The key advantage of the async client is `get_batch_quotes()`, which uses `asyncio.gather()` to fetch all quotes concurrently rather than sequentially, providing significant speedup for batch operations.

#### 3. `SessionManager` (session.py)

Manages the zero-auth session lifecycle. Key responsibilities:

- **Session Acquisition**: Visits Google Finance Beta, extracts f.sid, bl, and at tokens from the HTML
- **Cookie Management**: Maintains the request session with all cookies including SAPISID
- **SAPISIDHASH Generation**: Computes the SHA1-based authentication hash required by Google
- **Session Refresh**: Automatically refreshes expired sessions (30-minute TTL)
- **URL Building**: Constructs the batchexecute URL with all required parameters
- **Body Building**: Constructs the f.req form body with proper JSON encoding

#### 4. `RPCTransport` (transport.py)

The low-level transport layer for the batchexecute RPC protocol:

- **Endpoint Resolution**: Looks up RPC IDs and payload templates from the registry
- **Payload Construction**: Substitutes asset identifiers, ticker symbols, and custom overrides
- **Request Execution**: Sends POST requests with proper headers, cookies, and body
- **Retry Logic**: Handles 429 (rate limit) with exponential backoff, 400/401/403 with session refresh
- **Response Parsing**: Delegates to the parser module for batchexecute protocol handling

#### 5. `EndpointRegistry` (endpoints.py)

Maps human-friendly endpoint names to Google's obfuscated RPC function IDs:

- **36+ Known Endpoints**: Pre-mapped with discovered RPC IDs and payload templates
- **Disk Caching**: Persists RPC ID overrides to `~/.cache/gfinance/rpc_ids.json`
- **Reverse Lookup**: Can look up endpoints by RPC ID
- **Category Grouping**: Endpoints organized into 13 categories (quote, chart, market, etc.)
- **Runtime Updates**: RPC IDs can be updated at runtime (by auto-healing) and persist across restarts

#### 6. `AutoHealEngine` (auto_heal.py)

Re-discovers RPC function IDs when Google updates their deployment:

- **Playwright Scan**: Launches headless Chromium, visits Google Finance pages, and captures batchexecute responses to extract current RPC IDs
- **HTML Fallback**: When Playwright isn't available, parses the Google Finance HTML for `AF_initDataCallback` patterns
- **Data Service Index Matching**: Maps discovered endpoints using `data_service_index` when RPC IDs don't match directly
- **Cache Persistence**: Updated RPC IDs are saved to disk through the EndpointRegistry

#### 7. `CircuitBreaker` (resilience/__init__.py)

Prevents cascading failures in distributed systems:

- **Closed State**: Normal operation, requests flow through
- **Open State**: Too many failures detected, requests are blocked
- **Half-Open State**: After reset timeout, allows one test request to check if the service has recovered
- **Failure Threshold**: Opens after 5 consecutive failures (configurable)
- **Reset Timeout**: 60 seconds before trying again (configurable)
- **Gradual Recovery**: Each success decrements the failure count

#### 8. `Parser` (parser.py)

Handles Google's proprietary batchexecute response format:

- **XSSI Stripping**: Removes the `)]}'` anti-cross-site scripting prefix
- **Chunk Parsing**: Parses length-prefixed chunk format (`<len>\\n<data>\\n<len>\\n<data>...`)
- **Multi-Level JSON Unescaping**: Iteratively unescapes JSON strings up to 5 levels deep
- **Recursive Extraction**: Searches deeply nested arrays/dicts for specific types
- **Safe Navigation**: `safe_get()` for navigating nested lists by index path without IndexError

#### 9. `Extractors` (extractors.py)

Maps positional-array data to typed Pydantic models:

- **Position-Based**: Uses known array positions to extract fields (e.g., `entity[5]` = price array)
- **Recursive Fallback**: When position-based extraction fails, uses `recursive_extract()` to find values by type
- **Entity Navigation**: `_navigate_to_entity()` traverses the nested response structure to find the entity data array
- **Multi-Format Support**: Handles multiple response formats from different endpoints
- **Type Coercion**: Safely converts values to float, int, str with error handling

### Request Lifecycle

Here's what happens when you call `client.quote.get("AAPL", "NASDAQ")`:

```
1. GoogleFinanceClient.quote.get("AAPL", "NASDAQ")
   └── QuoteService.get("AAPL", "NASDAQ")
       └── RPCTransport.call("quote_core", symbol="AAPL", exchange="NASDAQ")
           ├── EndpointRegistry.get("quote_core")
           │   └── Returns RPCEndpoint(rpc_id="gCvqoe", payload_template="[[{asset}], 1]")
           ├── build_asset_identifier("AAPL", "NASDAQ")
           │   └── Returns '[null, ["AAPL", "NASDAQ"]]'
           ├── Payload substitution: "[[null, ["AAPL", "NASDAQ"]], 1]"
           ├── SessionManager.get_session()
           │   ├── Check if session expired (30-min TTL)
           │   ├── If expired: GET https://www.google.com/finance/beta
           │   ├── Extract tokens: f.sid, bl, at, SAPISID cookie
           │   └── Compute SAPISIDHASH: SHA1(timestamp + " " + SAPISID + " " + origin)
           ├── Build batchexecute URL with query params
           ├── Build f.req body: f.req=[[["gCvqoe", "[[null, [\"AAPL\", \"NASDAQ\"]], 1]", null, "generic"]]]&at=<token>
           ├── POST request with headers + cookies
           │   ├── Retry on 429 (rate limit) with exponential backoff
           │   ├── Refresh session on 400/401/403 (auth failure)
           │   └── Raise RPCError on other HTTP errors
           └── Parse response:
               ├── strip_xssi() — Remove )]}' prefix
               ├── parse_chunks() — Parse length-prefixed chunks
               ├── json.loads() — Parse outer JSON
               ├── Find "wrb.fr" entries — Extract RPC response
               ├── unescape_json() — Multi-level JSON unescaping
               └── find_by_rpc_id() — Match to our RPC ID "gCvqoe"
                   └── Returns parsed data array
                       └── extract_quote(data, symbol="AAPL", exchange="NASDAQ")
                           ├── _navigate_to_entity() — Find entity array
                           ├── Extract price array from entity[5]
                           ├── Extract name from entity[2]
                           ├── Extract currency from entity[4]
                           ├── Extract prev_close from entity[7]
                           ├── Detect entity_type from entity[3]
                           └── Return Quote(symbol="AAPL", price=307.34, ...)
```

### Data Flow: From Google to You

```
Google Finance Server
  │
  │ HTTP Response (batchexecute)
  │ )]}'<length>
  │ [["wrb.fr","gCvqoe","[[\"/m/0k8z\",[\"AAPL\",\"NASDAQ\"],
  │    \"Apple Inc\",0,\"USD\",[307.34,-3.89,-1.25],...]]]",null,null,null,"generic"]]
  │
  ▼
Parser Module
  │ strip_xssi()    → Remove )]}' prefix
  │ parse_chunks()  → Split into chunks by length prefix
  │ json.loads()    → Parse outer JSON array
  │ unescape_json() → Unescape nested JSON strings (up to 5 levels)
  │ Result: [{"rpc_id": "gCvqoe", "data": [[...]], "reference": "generic"}]
  │
  ▼
Extractor Module
  │ _navigate_to_entity() → Drill into nested arrays to find entity
  │ Position extraction    → entity[5] = [307.34, -3.89, -1.25]
  │ Field mapping          → price=307.34, change=-3.89, change_percent=-1.25
  │ Fallback extraction    → recursive_extract() for missing fields
  │
  ▼
Pydantic Model
  │ Quote(
  │   symbol="AAPL",
  │   exchange="NASDAQ",
  │   name="Apple Inc",
  │   price=307.34,
  │   change=-3.89,
  │   change_percent=-1.25,
  │   currency="USD",
  │   entity_type="stock",
  │   prev_close=311.23
  │ )
  │
  ▼
Your Application
  │ quote.model_dump()  → {"symbol": "AAPL", "price": 307.34, ...}
  │ quote.model_dump_json() → '{"symbol":"AAPL","price":307.34,...}'
  │ chart.to_dataframe() → pandas DataFrame
```

---

## 🔌 RPC Endpoint Registry — 36+ Endpoints

### Complete Endpoint Reference Table

The `EndpointRegistry` maintains a mapping of 36+ discovered RPC endpoints. Each endpoint has an obfuscated RPC function ID (like `gCvqoe`), a human-friendly name, a description, a category, and a payload template.

| Name | RPC ID | Description | Category | Entity Type |
|------|--------|-------------|----------|-------------|
| `page_load` | `zKAP2e` | Initial page load data | navigation | all |
| `navigation` | `hgueg` | Navigation / sidebar data | navigation | all |
| `feature_flags` | `hgueg` | Feature flags & config | session | all |
| `market_summary` | `HacE5d` | Market indices & sectors | market | all |
| `market_status` | `RiQiSd` | Exchange open/close status | market | all |
| `market_screener` | `kA4MVd` | Market movers & screener | market | all |
| `market_indices` | `RmdyKd` | Major market index data | market | all |
| `market_categories` | `YtbmEe` | Sector classification | market | all |
| `market_regions` | `xuuV8d` | Regional market data / batch quotes light | market | all |
| `quote_core` | `gCvqoe` | Core price, change, volume, market cap | quote | all |
| `quote_details` | `JL8oKc` | Extended quote details | quote | all |
| `quote_stats` | `SICF5d` | Key statistics (P/E, EPS, beta) | quote | all |
| `quote_info` | `YTM9q` | Quote summary info | quote | all |
| `realtime_price` | `in0BVc` | Real-time price stream | quote | all |
| `quote_about` | `dlNq8b` | About section (sector, CEO) | quote | all |
| `symbol_resolve` | `gXxkFd` | Symbol resolution | quote | all |
| `chart_data` | `SICF5d` | Chart data with interval | chart | stock |
| `chart_crypto` | `in0BVc` | Crypto/currency chart data | chart | crypto |
| `price_history` | `wKsY8b` | Historical price (single period) | chart | stock |
| `price_history_multi` | `c2u4wc` | Historical price (multi-period) | chart | stock |
| `stock_chart` | `Xs5i3b` | Stock chart rendering data | chart | stock |
| `news` | `XB3kn` | General market news feed | news | all |
| `quote_news` | `XxQsbd` | Ticker-specific news | news | all |
| `company_info` | `Iaiw6c` | Company description & details | company | stock |
| `related_companies` | `dlNq8b` | Related / similar companies | company | stock |
| `related_stocks` | `TNo8E` | Related stocks in sector | company | stock |
| `financial_statements` | `Pr8h2e` | Income stmt, balance sheet, CF | financials | stock |
| `dividends` | `gXxkFd` | Dividend history & yield | financials | stock |
| `batch_quote_detailed` | `in0BVc` | Detailed batch quotes | market | all |
| `analyst_ratings` | `K5Y6Xb` | Analyst consensus & targets | analysts | stock |
| `earnings` | `wj5Bh` | EPS estimates & actuals | analysts | stock |
| `earnings_transcript` | `FinanceHubService/GetEarningsTranscript` | Earnings call transcript | analysts | stock |
| `watchlist` | `X12h2b` | User watchlist data | watchlist | all |
| `research` | `FinanceHubService/ExecuteResearchQuery` | AI research query | research | stock |
| `search_autocomplete` | `XB3kn` | Autocomplete search | search | all |
| `async_data` | `AsyncDataService/GetAsyncData` | Async data service | system | all |

### Endpoint Categories

| Category | Count | Description |
|----------|-------|-------------|
| `navigation` | 2 | Page navigation and initial load data |
| `session` | 1 | Feature flags and configuration |
| `market` | 7 | Market-wide data: indices, movers, screener |
| `quote` | 7 | Security quotes: price, details, stats |
| `chart` | 5 | Historical price charts and OHLCV data |
| `news` | 2 | Market and ticker-specific news |
| `company` | 3 | Company information and related entities |
| `financials` | 2 | Financial statements and dividends |
| `analysts` | 3 | Analyst ratings, earnings, transcripts |
| `watchlist` | 1 | User watchlist management |
| `research` | 1 | AI-powered research queries |
| `search` | 1 | Symbol lookup and autocomplete |
| `system` | 1 | Internal async data service |

---

## 🩹 Auto-Healing Engine

One of gfinance's most powerful features is the auto-healing engine. Google periodically updates their deployments, which can change the obfuscated RPC function IDs (like `gCvqoe` becoming `xKp3mn`). When this happens, API calls start failing because the old RPC IDs are no longer valid. The auto-healing engine re-discovers the current RPC IDs automatically.

### How Auto-Healing Works

```
1. User calls client.quote.get("AAPL")
2. RPCTransport sends request with rpc_id="gCvqoe"
3. Google returns empty/error response (RPC ID changed!)
4. AutoHealEngine.heal_all() is triggered
5. ┌─────────────────────────────────────┐
   │  Try Playwright:                     │
   │  • Launch headless Chromium          │
   │  • Visit /finance, /finance/quote/AAPL, /finance/markets
   │  • Capture batchexecute responses    │
   │  • Extract "wrb.fr" entries          │
   │  • Match to known endpoints          │
   └─────────────────────────────────────┘
   │
   │  If Playwright fails:
   │  ┌─────────────────────────────────────┐
   │  │  HTML Fallback:                      │
   │  │  • GET /finance HTML                 │
   │  │  • Find AF_initDataCallback patterns │
   │  │  • Extract ds:N → RPC ID mappings   │
   │  │  • Match by data_service_index       │
   │  └─────────────────────────────────────┘
6. Updated RPC IDs saved to disk cache
7. Future requests use the new RPC IDs
```

### Playwright-Based Discovery

The primary healing method uses Playwright browser automation:

1. **Browser Launch**: Launches headless Chromium with a clean context
2. **Page Navigation**: Visits key Google Finance pages (home, quote page, markets page)
3. **Response Interception**: Captures all batchexecute network responses
4. **RPC ID Extraction**: Parses responses for `"wrb.fr"` entries to discover current RPC IDs
5. **Endpoint Matching**: Matches discovered RPC IDs against the known endpoint list

```python
# Trigger manual healing
client = GoogleFinanceClient()
updates = client.heal()
print(f"Updated endpoints: {updates}")
# Output: {'quote_core': 'xKp3mn', 'chart_data': 'mNr4pq'}
```

### HTML Fallback Discovery

When Playwright isn't installed, the engine falls back to HTML parsing:

1. **Fetch HTML**: GETs the Google Finance homepage
2. **Pattern Matching**: Looks for `AF_initDataCallback` blocks in the HTML
3. **Data Service Index**: Extracts `ds:N` → RPC ID mappings
4. **Cross-Reference**: Matches discovered RPC IDs to known endpoints using `data_service_index`

### Disk Caching

Discovered RPC IDs are persisted to disk at `~/.cache/gfinance/rpc_ids.json`:

```json
{
  "overrides": {
    "quote_core": "gCvqoe",
    "chart_data": "SICF5d",
    "market_summary": "HacE5d"
  }
}
```

This cache is loaded on startup, so healing results persist across application restarts. You can clear the cache with:

```python
client._registry.clear_cache()  # Reset to default RPC IDs
```

---

## 🛡️ Resilience & Circuit Breaker

### Circuit Breaker States

```
                    ┌──────────────┐
                    │   CLOSED     │
                    │  (Normal)    │
                    │  Requests    │
                    │  flow freely │
                    └──────┬───────┘
                           │
                      5+ failures
                           │
                           ▼
                    ┌──────────────┐
                    │    OPEN      │
                    │  (Blocked)   │
                    │  Requests    │
                    │  rejected    │
                    └──────┬───────┘
                           │
                    60s timeout
                           │
                           ▼
                    ┌──────────────┐
                    │  HALF-OPEN   │
                    │  (Testing)   │
                    │  1 request   │
                    │  allowed     │
                    └──────┬───────┘
                       │         │
                  Success    Failure
                       │         │
                       ▼         ▼
                  CLOSED      OPEN
```

### Retry with Exponential Backoff

The `RPCTransport` implements retry logic with exponential backoff:

```python
# Default configuration
max_retries = 3
retry_delay = 1.0  # Base delay in seconds

# Retry delays (approximate):
# Attempt 1: Immediate
# Attempt 2: 1.0s delay
# Attempt 3: 2.0s delay
# For rate limits (429): delay * 2^(attempt+2), capped at 60s
```

The `resilience` module also provides a `with_retry` decorator:

```python
from gfinance.resilience import with_retry

@with_retry(max_retries=3, base_delay=1.0, max_delay=30.0)
def fetch_data(symbol):
    # This will be retried on failure
    return client.quote.get(symbol)
```

### Rate Limit Handling

When Google returns a 429 (Too Many Requests) response:

1. The transport layer detects the 429 status code
2. Computes an exponential backoff delay: `retry_delay * 2^(attempt+2)`, capped at 60 seconds
3. Logs a warning with the wait time
4. Waits the computed delay
5. Retries the request

When Google returns 400/401/403 (auth failure):

1. The transport layer refreshes the session (re-acquires f.sid, bl, at tokens)
2. Rebuilds the batchexecute URL and f.req body with new session data
3. Retries the request with the fresh session

---

## 🔐 Session Management & Zero-Auth

### SAPISIDHASH Authentication

Google Finance requires SAPISIDHASH authentication for batchexecute requests. The `SessionManager` handles this automatically:

```python
# SAPISIDHASH computation
timestamp = str(int(time.time() * 1000))  # Current time in milliseconds
origin = "https://www.google.com"
hash_input = f"{timestamp} {sapisid} {origin}"
hash_value = hashlib.sha1(hash_input.encode()).hexdigest()
authorization = f"SAPISIDHASH {timestamp}_{hash_value}"
```

This hash is included in every request's `Authorization` header. The session manager automatically extracts the `SAPISID` cookie from the Google Finance page visit and computes the hash for each request.

### Session Auto-Refresh

Sessions have a 30-minute TTL (Time To Live). The `SessionManager` automatically refreshes expired sessions:

```python
SESSION_TTL = 1800  # 30 minutes

class FinanceSession:
    @property
    def is_expired(self) -> bool:
        return (time.time() - self.created_at) > SESSION_TTL
```

You can also force a refresh:

```python
client = GoogleFinanceClient()
client.refresh_session()  # Force-refresh the session
```

---

## 📊 Pydantic Models Reference

All data models use Pydantic v2 with full type annotations, optional fields, and export methods.

### Quote Model

The most commonly used model, representing a stock/crypto/index quote:

```python
class Quote(BaseModel):
    symbol: str = ""                    # Ticker symbol (e.g., "AAPL")
    exchange: str = ""                  # Exchange (e.g., "NASDAQ")
    name: str = ""                      # Company/security name
    price: Optional[float] = None       # Current or last traded price
    change: Optional[float] = None      # Absolute price change
    change_percent: Optional[float] = None  # Percentage price change
    currency: str = "USD"               # Trading currency
    market_cap: Optional[str] = None    # Market capitalization (formatted)
    market_cap_raw: Optional[float] = None  # Market cap (raw number)
    volume: Optional[int] = None        # Trading volume
    avg_volume: Optional[int] = None    # Average trading volume
    open_price: Optional[float] = None  # Opening price
    high_price: Optional[float] = None  # Day's high price
    low_price: Optional[float] = None   # Day's low price
    prev_close: Optional[float] = None  # Previous close price
    high_52w: Optional[float] = None    # 52-week high
    low_52w: Optional[float] = None     # 52-week low
    pe_ratio: Optional[float] = None    # Price-to-earnings ratio
    eps: Optional[float] = None         # Earnings per share
    dividend_yield: Optional[float] = None  # Dividend yield percentage
    beta: Optional[float] = None        # Beta coefficient
    entity_type: str = "stock"          # "stock", "crypto", "currency", "index"
    timestamp: Optional[str] = None     # Last update timestamp
```

### CompanyDetails Model

```python
class CompanyDetails(BaseModel):
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
```

### ChartData & ChartTick Models

```python
class ChartTick(BaseModel):
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
    symbol: str = ""
    exchange: str = ""
    period: str = ""
    resolution: str = ""          # "intraday" or "daily"
    ticks: List[ChartTick] = []

    @property
    def latest_price(self) -> Optional[float]: ...

    @property
    def highest(self) -> Optional[float]: ...

    @property
    def lowest(self) -> Optional[float]: ...

    def to_dataframe(self) -> pd.DataFrame: ...  # Requires pandas
```

### AnalystRating Model

```python
class AnalystRating(BaseModel):
    symbol: str = ""
    consensus: str = ""           # "Buy", "Hold", "Sell"
    target_low: Optional[float] = None
    target_mean: Optional[float] = None
    target_high: Optional[float] = None
    target_median: Optional[float] = None
    num_analysts: int = 0
    ratings_breakdown: Dict[str, int] = {}  # strong_buy, buy, hold, sell, strong_sell
    individual_ratings: List[Dict[str, Any]] = []
```

### EarningsData Model

```python
class EarningsData(BaseModel):
    symbol: str = ""
    next_earnings_date: Optional[str] = None
    quarterly_earnings: List[Dict[str, Any]] = []
    consensus_eps: Optional[float] = None
    actual_eps: Optional[float] = None
```

### FinancialStatements Models

```python
class FinancialStatement(BaseModel):
    statement_type: str = ""       # "income", "balance_sheet", "cash_flow"
    periods: List[str] = []        # ["Q2 2026", "Q1 2026", ...]
    line_items: Dict[str, List[Optional[float]]] = {}  # {"Revenue": [111.18B, ...]}

class FinancialStatements(BaseModel):
    symbol: str = ""
    income_statement: Optional[FinancialStatement] = None
    balance_sheet: Optional[FinancialStatement] = None
    cash_flow: Optional[FinancialStatement] = None
```

### SearchResult Model

```python
class SearchResult(BaseModel):
    symbol: str = ""
    name: str = ""
    exchange: str = ""
    entity_type: str = ""          # "stock", "currency"
    google_finance_url: str = ""
```

### MarketIndex, MarketSummary & MarketMovers Models

```python
class MarketIndex(BaseModel):
    name: str = ""
    symbol: str = ""
    exchange: str = ""
    price: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None

class MarketSummary(BaseModel):
    indices: List[MarketIndex] = []
    sectors: List[Dict[str, Any]] = []
    region: str = ""
    timestamp: Optional[str] = None

class MarketMovers(BaseModel):
    category: str = ""              # "gainers", "losers", "most_active"
    entities: List[Quote] = []
    timestamp: Optional[str] = None
```

### NewsArticle Model

```python
class NewsArticle(BaseModel):
    title: str = ""
    source: str = ""
    url: str = ""
    time: Optional[str] = None
    snippet: Optional[str] = None
    image_url: Optional[str] = None
```

---

## 🌐 FastAPI REST API Server

### Complete API Reference

The FastAPI server exposes 24+ REST endpoints organized by domain. All endpoints return JSON responses with proper error handling.

#### System Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/health` | Health check + resilience stats | None |
| `POST` | `/api/v1/heal` | Trigger auto-healing | None |
| `GET` | `/api/v1/endpoints` | List all RPC endpoints | `category` (optional) |
| `GET` | `/api/v1/categories` | List endpoint categories | None |

#### Quote Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/api/v1/quote/{symbol}` | Real-time stock quote | `exchange` (default: NASDAQ) |
| `GET` | `/api/v1/quote/{symbol}/details` | Company details | `exchange` |
| `GET` | `/api/v1/quote/{symbol}/stats` | Key statistics | `exchange` |
| `GET` | `/api/v1/quote/{symbol}/realtime` | Real-time price | `exchange` |

#### Market Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/api/v1/market/summary` | Market summary | `region` (default: us) |
| `GET` | `/api/v1/market/indices` | Major indices | None |
| `GET` | `/api/v1/market/movers` | Market movers | `category` (default: most_active) |

#### Chart Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/api/v1/chart/{symbol}` | Chart data | `exchange`, `period` (default: 1M) |
| `GET` | `/api/v1/chart/{symbol}/ohlcv` | OHLCV bar data | `exchange`, `period` |
| `GET` | `/api/v1/chart/{symbol}/history` | Historical prices | `exchange`, `period` (default: 1Y) |

#### News Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/api/v1/news/market` | Market news | None |
| `GET` | `/api/v1/news/{symbol}` | Ticker news | `exchange` |

#### Company Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/api/v1/company/{symbol}/info` | Company info | `exchange` |
| `GET` | `/api/v1/company/{symbol}/related` | Related companies | `exchange` |

#### Financials Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/api/v1/financials/{symbol}/statements` | Financial statements | `exchange` |
| `GET` | `/api/v1/financials/{symbol}/statistics` | Key statistics | `exchange` |
| `GET` | `/api/v1/financials/{symbol}/dividends` | Dividend data | `exchange` |

#### Analysts Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/api/v1/analysts/{symbol}/ratings` | Analyst ratings | `exchange` |
| `GET` | `/api/v1/analysts/{symbol}/earnings` | Earnings data | `exchange` |
| `GET` | `/api/v1/analysts/{symbol}/transcript` | Earnings transcript | None |

#### Research Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `POST` | `/api/v1/research/query` | AI research query | Body: `{"symbol": "...", "question": "..."}` |
| `GET` | `/api/v1/research/{symbol}` | Quick research | `question` (default: investment considerations) |

### Swagger UI & ReDoc

The FastAPI server auto-generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs` — Interactive API explorer with try-it-out functionality
- **ReDoc**: `http://localhost:8000/redoc` — Clean, professional API documentation

### CORS Configuration

The server is configured with permissive CORS settings for development:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],      # Allow all HTTP methods
    allow_headers=["*"],      # Allow all headers
)
```

For production, you should restrict `allow_origins` to your specific domains.

### Error Handling

All `GFinanceError` exceptions are caught by a global handler and returned as structured JSON:

```json
{
    "error": "RPC call failed (rpc_id=gCvqoe)",
    "type": "RPCError"
}
```

HTTP status codes:
- `200` — Success
- `502` — gfinance error (session, RPC, parse, etc.)

### Running in Production

```bash
# With uvicorn directly (production)
uvicorn gfinance.fastapi_app:create_app --factory \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info \
  --access-log

# With Gunicorn + Uvicorn workers (recommended for production)
pip install gunicorn
gunicorn gfinance.fastapi_app:create_app \
  --worker-class uvicorn.workers.UvicornWorker \
  --workers 4 \
  --bind 0.0.0.0:8000

# With Docker
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -e ".[fastapi]"
EXPOSE 8000
CMD ["uvicorn", "gfinance.fastapi_app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
```

---

## ⚙️ Configuration Reference

### Client Configuration

```python
from gfinance import GoogleFinanceClient

client = GoogleFinanceClient(
    proxies=None,           # Dict of proxy URLs: {"http": "...", "https": "..."}
    max_retries=3,          # Maximum retry attempts per request
    retry_delay=1.0,        # Base delay in seconds between retries
    timeout=30.0,           # Request timeout in seconds
    auto_heal=True,         # Enable auto-healing on RPC ID changes
    language="en-US",       # Accept-Language header value
)
```

### Async Client Configuration

```python
from gfinance.async_client import AsyncGoogleFinanceClient

client = AsyncGoogleFinanceClient(
    timeout=30.0,           # Request timeout in seconds
    language="en-US",       # Accept-Language header value
)
```

### Server Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `GFINANCE_HOST` | `0.0.0.0` | Server bind address |
| `GFINANCE_PORT` | `8000` | Server bind port |
| `GFINANCE_RELOAD` | `1` | Auto-reload on code changes (set to `0` for production) |

### Environment Variables

```bash
# Server configuration
export GFINANCE_HOST=0.0.0.0
export GFINANCE_PORT=8000
export GFINANCE_RELOAD=0  # Disable auto-reload in production

# Python configuration
export PYTHONUNBUFFERED=1  # Disable output buffering for Docker
export LOG_LEVEL=INFO      # Logging level
```

---

## 🧪 Real Output Examples

### Live Test Results

These are actual outputs from running gfinance against Google Finance's live API on June 8, 2026:

#### AAPL Stock Quote

```python
from gfinance import GoogleFinanceClient

with GoogleFinanceClient() as client:
    quote = client.quote.get("AAPL", "NASDAQ")
```

Output:

```python
{
    'symbol': 'AAPL',
    'exchange': 'NASDAQ',
    'name': 'Apple Inc',
    'price': 307.34,
    'change': -3.8900146,
    'change_percent': -1.2498841,
    'currency': 'USD',
    'prev_close': 311.23,
    'entity_type': 'stock'
}
```

#### Batch Quotes (Async)

```python
async with AsyncGoogleFinanceClient() as client:
    quotes = await client.get_batch_quotes([
        ("AAPL", "NASDAQ"), ("GOOGL", "NASDAQ"),
        ("MSFT", "NASDAQ"), ("AMZN", "NASDAQ"),
        ("NVDA", "NASDAQ")
    ])
```

Output:

```
AAPL: $307.34 (-1.25%)
GOOGL: $368.53 (-0.98%)
MSFT: $416.67 (-2.66%)
AMZN: $246.03 (-3.06%)
NVDA: $205.10 (-6.20%)
```

#### AAPL Chart Data (1 Month)

```python
chart = client.chart.data("AAPL", "NASDAQ", "1M")
```

Output:

```
Symbol: AAPL, Period: 1M
Resolution: daily, Ticks: 22
Latest: 2026-06-05, Close: $307.34
```

#### TSLA Chart Data (1 Month)

```python
chart = await client.get_chart("TSLA", "NASDAQ", "1M")
```

Output:

```
TSLA chart: 21 ticks
Latest: 2026-06-05, close=391.0
```

#### Market Summary

```python
summary = client.market.summary("us")
```

Output:

```
Equity benchmarks plunge as robust labor data fuels hawkish pivot
Semiconductor sector faces heavy losses amid cooling AI sentiment
Bitcoin and precious metals retreat in broad risk-off shift
Energy market volatility persists amid geopolitical and supply concerns
```

#### Resilience Stats

```python
stats = client.get_resilience_stats()  # Async client
```

Output:

```python
{'success': 10, 'failure': 0, 'session_healthy': True, 'f_sid_set': True}
```

#### Endpoint Discovery

```python
eps = client.list_endpoints()
cats = client.list_categories()
```

Output:

```
Total endpoints: 36
Categories: ['analysts', 'chart', 'company', 'financials', 'market', 'navigation',
             'news', 'quote', 'research', 'search', 'session', 'system', 'watchlist']
```

---

## 📝 Advanced Usage Patterns

### Context Manager Pattern

Always use the context manager to ensure proper resource cleanup:

```python
# ✅ Recommended: Using context manager
with GoogleFinanceClient() as client:
    quote = client.quote.get("AAPL")
    # Session is automatically closed when exiting the block

# ❌ Manual management (don't forget to close!)
client = GoogleFinanceClient()
try:
    quote = client.quote.get("AAPL")
finally:
    client.close()

# ✅ Async context manager
async with AsyncGoogleFinanceClient() as client:
    quote = await client.get_quote("AAPL")
    # Session is automatically closed
```

### Batch Processing

For processing large numbers of symbols, use the async client for concurrent requests:

```python
import asyncio
from gfinance.async_client import AsyncGoogleFinanceClient

async def process_portfolio(symbols):
    """Fetch quotes for a large portfolio concurrently."""
    async with AsyncGoogleFinanceClient() as client:
        # Process in chunks to avoid rate limiting
        chunk_size = 10
        results = []
        for i in range(0, len(symbols), chunk_size):
            chunk = symbols[i:i+chunk_size]
            quotes = await client.get_batch_quotes(chunk)
            results.extend(quotes)
            if i + chunk_size < len(symbols):
                await asyncio.sleep(1)  # Rate limit protection
        return results

# Run
symbols = [("AAPL", "NASDAQ"), ("GOOGL", "NASDAQ"), ("MSFT", "NASDAQ"),
           ("AMZN", "NASDAQ"), ("TSLA", "NASDAQ"), ("NVDA", "NASDAQ"),
           ("META", "NASDAQ"), ("NFLX", "NASDAQ"), ("AMD", "NASDAQ"),
           ("INTC", "NASDAQ")]
results = asyncio.run(process_portfolio(symbols))
for q in results:
    if q.price:
        print(f"{q.symbol}: ${q.price:.2f} ({q.change_percent:+.2f}%)")
```

### DataFrame Export

Convert chart data to pandas DataFrames for analysis:

```python
# Requires: pip install gfinance[data]
from gfinance import GoogleFinanceClient

with GoogleFinanceClient() as client:
    chart = client.chart.data("AAPL", "NASDAQ", "1Y")
    df = chart.to_dataframe()

    # Basic analysis
    print(df.head())
    print(df.describe())

    # Calculate returns
    df['daily_return'] = df['close'].pct_change()

    # Calculate moving averages
    df['ma_20'] = df['close'].rolling(window=20).mean()
    df['ma_50'] = df['close'].rolling(window=50).mean()

    # Find crossover signals
    df['signal'] = (df['ma_20'] > df['ma_50']).astype(int)
    df['crossover'] = df['signal'].diff()

    print(df[df['crossover'] != 0])  # Buy/sell signals
```

### Proxy Configuration

Route requests through proxy servers:

```python
# HTTP proxy
client = GoogleFinanceClient(
    proxies={"http": "http://proxy:8080", "https": "http://proxy:8080"}
)

# SOCKS5 proxy (requires requests[socks])
client = GoogleFinanceClient(
    proxies={"http": "socks5://proxy:1080", "https": "socks5://proxy:1080"}
)

# Authenticated proxy
client = GoogleFinanceClient(
    proxies={"http": "http://user:pass@proxy:8080",
             "https": "http://user:pass@proxy:8080"}
)
```

### Custom Retry Strategies

Use the `with_retry` decorator for custom retry logic:

```python
from gfinance.resilience import with_retry

@with_retry(max_retries=5, base_delay=2.0, max_delay=60.0)
def fetch_with_persistence(symbol):
    """Fetch a quote with aggressive retry settings."""
    with GoogleFinanceClient() as client:
        return client.quote.get(symbol)
```

### Error Handling Patterns

```python
from gfinance import GoogleFinanceClient
from gfinance.exceptions import SessionError, RPCError, ParseError, RateLimitError

with GoogleFinanceClient() as client:
    try:
        quote = client.quote.get("AAPL")
    except SessionError as e:
        print(f"Session failed: {e.message}")
        # Try refreshing the session
        client.refresh_session()
        quote = client.quote.get("AAPL")
    except RateLimitError as e:
        print(f"Rate limited. Retry after: {e.retry_after}s")
    except RPCError as e:
        print(f"RPC failed: {e.message}, RPC ID: {e.rpc_id}")
        # Try auto-healing
        client.heal()
    except ParseError as e:
        print(f"Parse failed: {e.message}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

### Building a Stock Screener

```python
from gfinance import GoogleFinanceClient

def screen_stocks(symbols, min_price=0, max_price=float('inf'),
                  min_change_pct=-100, max_change_pct=100):
    """Simple stock screener based on price and change criteria."""
    with GoogleFinanceClient() as client:
        results = []
        for symbol, exchange in symbols:
            try:
                quote = client.quote.get(symbol, exchange)
                if (quote.price and
                    min_price <= quote.price <= max_price and
                    min_change_pct <= (quote.change_percent or 0) <= max_change_pct):
                    results.append(quote)
            except Exception:
                continue
        return results

# Find stocks under $500 that gained more than 2%
gainers = screen_stocks(
    [("AAPL", "NASDAQ"), ("TSLA", "NASDAQ"), ("NVDA", "NASDAQ"),
     ("AMD", "NASDAQ"), ("INTC", "NASDAQ")],
    min_price=0, max_price=500, min_change_pct=2.0
)
for q in gainers:
    print(f"{q.symbol}: ${q.price:.2f} ({q.change_percent:+.2f}%)")
```

### Building a Portfolio Tracker

```python
import asyncio
from gfinance.async_client import AsyncGoogleFinanceClient

class PortfolioTracker:
    def __init__(self, holdings: dict):
        """holdings = {symbol: quantity}"""
        self.holdings = holdings
        self.symbols = [(s, "NASDAQ") for s in holdings.keys()]

    async def get_value(self):
        async with AsyncGoogleFinanceClient() as client:
            quotes = await client.get_batch_quotes(self.symbols)
            total = 0
            for q in quotes:
                if q.price:
                    qty = self.holdings.get(q.symbol, 0)
                    value = q.price * qty
                    total += value
                    print(f"{q.symbol}: {qty} shares × ${q.price:.2f} = ${value:.2f}")
            print(f"\nTotal portfolio value: ${total:.2f}")
            return total

# Usage
portfolio = PortfolioTracker({"AAPL": 50, "GOOGL": 20, "MSFT": 30, "NVDA": 100})
asyncio.run(portfolio.get_value())
```

### Intraday Trading Dashboard

```python
from gfinance import GoogleFinanceClient
import time

def intraday_monitor(symbols, interval_seconds=60):
    """Monitor stocks in real-time (polling-based)."""
    with GoogleFinanceClient() as client:
        while True:
            print(f"\n--- {time.strftime('%H:%M:%S')} ---")
            for symbol, exchange in symbols:
                try:
                    quote = client.quote.realtime(symbol, exchange)
                    arrow = "▲" if (quote.change or 0) > 0 else "▼"
                    print(f"  {symbol}: ${quote.price:.2f} {arrow} {quote.change_percent:+.2f}%")
                except Exception as e:
                    print(f"  {symbol}: Error - {e}")
            time.sleep(interval_seconds)

# Run (press Ctrl+C to stop)
intraday_monitor([("AAPL", "NASDAQ"), ("TSLA", "NASDAQ"), ("NVDA", "NASDAQ")])
```

---

## 📦 Pydantic Model Export Methods

All Pydantic models in gfinance support multiple export formats:

```python
quote = client.quote.get("AAPL")

# Dictionary export
data = quote.model_dump()
# {'symbol': 'AAPL', 'price': 307.34, 'change': -3.89, ...}

# JSON string export
json_str = quote.model_dump_json()
# '{"symbol":"AAPL","price":307.34,"change":-3.89,...}'

# Selective field export
data = quote.model_dump(include={"symbol", "price", "change_percent"})
# {'symbol': 'AAPL', 'price': 307.34, 'change_percent': -1.25}

# Exclude None values
data = quote.model_dump(exclude_none=True)
# Only includes fields that have values

# DataFrame export (ChartData only, requires pandas)
chart = client.chart.data("AAPL", "NASDAQ", "1Y")
df = chart.to_dataframe()
# DataFrame with timestamp index and OHLCV columns
```

---

## 🧩 Extending gfinance

### Adding Custom Endpoints

You can add new RPC endpoints to the registry:

```python
from gfinance import GoogleFinanceClient
from gfinance.endpoints import RPCEndpoint

client = GoogleFinanceClient()

# Add a custom endpoint
client._registry._endpoints["my_custom_endpoint"] = RPCEndpoint(
    rpc_id="XyZ123",
    name="my_custom_endpoint",
    description="My custom endpoint",
    category="custom",
    payload_template="[[{asset}], 1, null]",
    entity_type="stock",
    params=["ticker"]
)

# Use it
data = client._transport.call("my_custom_endpoint", symbol="AAPL", exchange="NASDAQ")
```

### Adding Custom Extractors

Create custom data extractors for new response formats:

```python
from gfinance.parser import safe_get, recursive_extract
from gfinance.models import Quote

def extract_custom_quote(data, symbol="", exchange=""):
    """Custom extractor for a different response format."""
    quote = Quote(symbol=symbol, exchange=exchange)
    if not data or not isinstance(data, list):
        return quote

    # Navigate the response structure
    entity = data[0] if isinstance(data[0], list) else data

    # Extract using safe_get for positional data
    quote.price = safe_get(entity, [5, 0])
    quote.name = safe_get(entity, [2])

    # Use recursive extraction as fallback
    if not quote.name:
        strings = recursive_extract(entity, str)
        if strings:
            quote.name = strings[0]

    return quote
```

### Adding Custom FastAPI Routes

Add new routes to the FastAPI server:

```python
from fastapi import APIRouter
from gfinance.fastapi_app import get_client, run_sync

router = APIRouter()

@router.get("/custom/screener")
async def custom_screener(min_price: float = 0, max_price: float = 1000):
    client = get_client()
    # Custom logic here
    return {"results": []}

# In your custom app:
from gfinance.fastapi_app import create_app
app = create_app()
app.include_router(router, prefix="/api/v1/custom", tags=["Custom"])
```

---

## 🧪 Batchexecute Protocol Internals

Understanding Google's batchexecute protocol is key to maintaining and extending gfinance. This section documents the internal protocol in detail.

### XSSI Protection

Google uses Cross-Site Scripting Inclusion (XSSI) protection to prevent unauthorized cross-origin access. Every batchexecute response starts with a prefix that makes the response invalid JSON:

```
)]}'
```

This prefix must be stripped before parsing. The `strip_xssi()` function handles this:

```python
XSSI_PREFIX = ")]}'"

def strip_xssi(text: str) -> str:
    if text.startswith(XSSI_PREFIX):
        cleaned = text[len(XSSI_PREFIX):]
        return cleaned.lstrip("\r\n \t")
    return text.lstrip()
```

### Length-Prefixed Chunks

The batchexecute response format uses length-prefixed chunks:

```
<byte_length>\n<json_data>\n<next_length>\n<next_data>\n...
```

Example:

```
123
[["wrb.fr","gCvqoe","...long json string...",null,null,null,"generic"]]
456
[["wrb.fr","HacE5d","...another json string...",null,null,null,"generic"]]
```

The `parse_chunks()` function parses this format:

```python
def parse_chunks(text: str) -> List[str]:
    chunks = []
    remaining = text.strip()
    while remaining:
        nl = remaining.find("\n")
        chunk_len = int(remaining[:nl].strip())
        start = nl + 1
        end = start + chunk_len
        chunks.append(remaining[start:end])
        remaining = remaining[end:].lstrip("\r\n")
    return chunks
```

### Multi-Level JSON Unescaping

Google's responses often contain JSON strings nested inside JSON strings, sometimes up to 5 levels deep. The `unescape_json()` function iteratively parses until it reaches a non-string result:

```python
def unescape_json(escaped: Any, levels: int = 5) -> Any:
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
```

### f.req Body Structure

The batchexecute request body follows a specific format:

```
f.req=[[["RPC_ID","PAYLOAD",null,"generic"]]]&at=AUTH_TOKEN
```

Where:
- `RPC_ID` is the obfuscated function ID (e.g., `"gCvqoe"`)
- `PAYLOAD` is a JSON string containing the request parameters
- `"generic"` is the reference type
- `at` is the authentication token extracted from the session

The payload is JSON-encoded using `json.dumps()` for proper escaping of quotes and special characters:

```python
f_req_data = [[[rpc_id, payload, None, "generic"]]]
f_req_json = json.dumps(f_req_data)
body = f"f.req={f_req_json}&at={at_token}"
```

---

## 🗺️ Roadmap

- [ ] WebSocket support for real-time price streaming
- [ ] Currency conversion endpoint
- [ ] Options chain data
- [ ] Insider trading data
- [ ] Technical indicators (RSI, MACD, Bollinger Bands)
- [ ] Alert/notification system for price targets
- [ ] Multi-exchange support (NYSE, LSE, TSE, etc.)
- [ ] GraphQL API server option
- [ ] Official PyPI package publishing
- [ ] Docker image on Docker Hub
- [ ] GitHub Actions CI/CD pipeline
- [ ] Comprehensive test suite with fixtures
- [ ] Type stubs for mypy support
- [ ] Jupyter notebook examples

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository at https://github.com/maruf009sultan/gfinance
2. **Clone** your fork: `git clone https://github.com/your-username/gfinance.git`
3. **Create** a feature branch: `git checkout -b feature/my-new-feature`
4. **Install** development dependencies: `pip install -e ".[dev]"`
5. **Make** your changes and add tests
6. **Run** tests: `pytest tests/`
7. **Commit** with a descriptive message: `git commit -m "Add amazing feature"`
8. **Push** to your branch: `git push origin feature/my-new-feature`
9. **Open** a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write tests for new features
- Update documentation (this README) for significant changes
- Keep the codebase modular — new features should be in their own service module
- Use Pydantic models for all data returned from the API

---

## 📈 Marketing & SEO

### Project Keywords & Tags

These keywords and tags help users discover gfinance through search engines and package registries:

**Primary Keywords:** google finance api, stock market data, financial data python, stock quotes python, market data api, google finance scraper, stock price api, financial api python

**Secondary Keywords:** python finance library, stock market api, cryptocurrency prices python, market data scraper, ohlcv data python, financial statements api, analyst ratings python, earnings data api, historical stock prices, stock chart data

**PyPI Keywords:** google, finance, api, stocks, market, crypto, chart, financial, investment, trading, nasdaq, nyse, realtime, quotes, ohlcv, dividends, earnings, analysts

**GitHub Topics:** `python`, `google-finance`, `stock-market`, `financial-data`, `api`, `finance`, `trading`, `cryptocurrency`, `pydantic`, `fastapi`, `async`, `web-scraping`

### Search Engine Optimization

This README is optimized for search engine discoverability:

- **Descriptive headers** with relevant keywords
- **Code examples** that match common search queries (e.g., "python stock quote", "google finance api python")
- **Comparison table** that appears in searches comparing finance libraries
- **Comprehensive API documentation** that matches long-tail search queries
- **Real output examples** that demonstrate the library's capabilities

### Community & Social

- **GitHub Repository**: https://github.com/maruf009sultan/gfinance
- **Issues & Bug Reports**: https://github.com/maruf009sultan/gfinance/issues
- **Pull Requests**: https://github.com/maruf009sultan/gfinance/pulls
- **Discussions**: https://github.com/maruf009sultan/gfinance/discussions

### Package Registry SEO

When publishing to PyPI, include these in `pyproject.toml`:

```toml
[project]
name = "gfinance"
description = "Production-grade Google Finance API library with auto-healing, async support, and FastAPI server"
keywords = ["google", "finance", "api", "stocks", "market", "crypto", "chart", "financial",
            "investment", "trading", "nasdaq", "nyse", "realtime", "quotes", "ohlcv",
            "dividends", "earnings", "analysts", "pydantic", "fastapi"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: Financial and Insurance Industry",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Office/Business :: Financial :: Investment",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Framework :: FastAPI",
]
```

### GitHub Repository SEO

For maximum GitHub discoverability:

- **Repository Description**: "Production-grade Google Finance API library for Python — 36+ endpoints, auto-healing, async, FastAPI server, zero auth, Pydantic v2 models"
- **GitHub Topics**: python, google-finance, stock-market, financial-data, api, finance, trading, cryptocurrency, pydantic, fastapi, async, web-scraping, stock-quotes, market-data
- **Homepage URL**: Link to the GitHub Pages documentation (if created)
- **Wiki Pages**: Create wiki pages for common recipes and troubleshooting

### Content Marketing Ideas

- **Blog Post**: "How to Access Google Finance Data in Python — A Complete Guide"
- **Tutorial**: "Building a Real-Time Stock Dashboard with gfinance and FastAPI"
- **Video Tutorial**: "Python Stock Market API: Getting Started with gfinance"
- **Comparison Article**: "gfinance vs yfinance vs google-finance-api: Which Python Finance Library to Use?"
- **Dev.to Post**: "I Reverse-Engineered Google Finance's API — Here's What I Found"
- **Reddit Post**: r/Python, r/algotrading, r/FinancialTechnology — share the project
- **Hacker News**: Submit as "Show HN: gfinance — Production-grade Google Finance API for Python"
- **Medium Article**: "Building a Portfolio Tracker with Python and Google Finance"

---

## ⚖️ Usage Guidelines & Legal Disclaimer

### Important Legal Notice

**PLEASE READ THIS SECTION CAREFULLY BEFORE USING THIS SOFTWARE.**

### Terms of Service Compliance

This software accesses Google Finance through reverse-engineered internal APIs that are not publicly documented or intended for programmatic access. By using gfinance, you acknowledge and agree that:

- **You are solely responsible** for ensuring your use of this software complies with Google's Terms of Service (https://policies.google.com/terms) and any applicable Google Finance-specific terms
- **Google may modify, restrict, or block** access to their internal APIs at any time without notice, which may cause this software to stop functioning
- **Accessing Google's internal APIs** may constitute a violation of Google's Terms of Service, and Google may take action against accounts or IP addresses that make such accesses
- **You must not use this software** in any way that violates applicable laws, regulations, or third-party rights
- **You must respect robots.txt** and any rate-limiting or access-control mechanisms employed by Google

### Intended Use

This software is designed and intended **EXCLUSIVELY** for:

- **Personal exploration and educational purposes** — learning about financial data, API design, and web scraping techniques
- **Research and academic projects** — studying market data patterns, financial analysis, and data science
- **Non-commercial experimentation** — building personal tools and learning projects

This software is **NOT** designed, intended, or suitable for:

- **Industrial or enterprise use** — production trading systems, commercial platforms, or business-critical applications
- **High-frequency or algorithmic trading** — any automated trading system that requires reliable, low-latency market data
- **Commercial data services** — redistributing financial data as a service or product
- **Professional investment decisions** — making buy/sell/hold decisions based on data obtained through this library
- **Regulatory compliance** — any use case requiring SEC, FINRA, or other regulatory compliance
- **Heavy or sustained usage** — continuous polling, large-scale data collection, or any usage pattern that could place excessive load on Google's servers
- **Any purpose that requires guaranteed data accuracy, availability, or timeliness**

### Limitation of Liability

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.**

Specifically, the authors and contributors of gfinance:

- **Are NOT responsible** for any financial losses incurred through the use of this software
- **Are NOT responsible** for any legal consequences resulting from violations of Google's Terms of Service
- **Are NOT responsible** for any damages caused by inaccurate, delayed, or missing financial data
- **Are NOT responsible** for any action taken by Google against your account or IP address
- **Are NOT responsible** for any disruption to your business operations caused by API changes, failures, or discontinuation
- **Make NO guarantees** about the accuracy, completeness, timeliness, or reliability of any data obtained through this software
- **Make NO guarantees** about the continued availability or functionality of this software

### Data Accuracy Disclaimer

Financial data obtained through gfinance:

- **May be delayed** — Google Finance may display delayed quotes (typically 15 minutes for stocks)
- **May be inaccurate** — Data is extracted from Google's internal APIs which may contain errors or inconsistencies
- **May be incomplete** — Not all fields are available for all securities, and some data points may be missing
- **May be outdated** — There is no guarantee that data reflects the most current market conditions
- **Should NOT be used** as the sole basis for any financial, investment, or trading decision

Always verify critical financial data with official sources such as exchange feeds, SEC filings, or authorized data providers before making any investment decisions.

### Rate Limiting & Responsible Use

To use gfinance responsibly and minimize the risk of being blocked by Google:

- **Do not make excessive requests** — keep request rates reasonable (a few requests per minute is generally safe)
- **Implement caching** — cache responses locally to avoid redundant requests
- **Use batch operations** — prefer `batch_quotes()` over individual calls when fetching multiple symbols
- **Add delays between requests** — use `time.sleep()` or `asyncio.sleep()` between rapid requests
- **Respect 429 responses** — gfinance handles rate limits automatically with exponential backoff, but you should also reduce your request rate if you encounter them frequently
- **Do not scrape at scale** — avoid writing scripts that collect data for thousands of symbols continuously

### No Warranty

This software comes with absolutely no warranty. It is a reverse-engineered tool that depends on undocumented internal APIs that may change or break at any time. The authors make no commitment to maintain, update, or fix the software, and it may stop working without notice if Google modifies their infrastructure.

### Indemnification

By using this software, you agree to indemnify and hold harmless the authors and contributors from any claims, damages, losses, liabilities, and expenses (including reasonable attorney fees) arising from your use of the software, including but not limited to:

- Violations of Google's Terms of Service
- Financial losses from trading or investment decisions based on data from this software
- Legal actions from regulatory bodies or other third parties
- Damages to Google's systems or infrastructure

### Jurisdiction

This disclaimer and the software's MIT License shall be governed by and construed in accordance with applicable laws. Any disputes arising from the use of this software shall be resolved in the appropriate courts of law.

---

## 📜 License

This project is licensed under the **MIT License**:

```
MIT License

Copyright (c) 2024-2026 gfinance contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgements

- **Google Finance** — The underlying data source that makes this library possible
- **google-finance-api** — Original library providing typed Pydantic models, async support, and circuit breaker patterns
- **gfinance-beta** — Original library providing modular service architecture, Playwright auto-healing, SAPISIDHASH auth, and robust batchexecute parsing
- **Playwright** — Browser automation framework enabling auto-healing RPC discovery
- **Pydantic** — Data validation and serialization framework powering all typed models
- **FastAPI** — Modern web framework for building the REST API server
- **aiohttp** — Async HTTP client library for the async client
- **requests** — The ubiquitous HTTP library powering the sync client

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Version | 2.0.0 |
| Python Support | 3.9, 3.10, 3.11, 3.12+ |
| RPC Endpoints | 36+ |
| Pydantic Models | 15 |
| Service Modules | 9 |
| FastAPI Routes | 24+ |
| Endpoint Categories | 13 |
| Exception Types | 7 |
| Core Dependencies | 2 (requests, pydantic) |
| Optional Dependency Groups | 5 |
| Lines of Code | ~2,500+ |
| License | MIT |

---

## 📚 Source Code Reference — Complete File-by-File Analysis

This section provides a comprehensive, line-by-line analysis of every source file in the gfinance project. Each file is documented with its purpose, key classes and functions, internal logic, and integration points.

### Project Directory Structure

```
gfinance/
├── pyproject.toml               # Modern PEP 621 packaging configuration
├── run.py                       # Quick-start script with auto-dependency installation
├── README.md                    # This documentation file
└── gfinance/                    # Main Python package
    ├── __init__.py              # Public API exports (15 models + client + 7 exceptions)
    ├── client.py                # Synchronous GoogleFinanceClient (primary entry point)
    ├── async_client.py          # AsyncGoogleFinanceClient (aiohttp-based)
    ├── models.py                # 15 Pydantic v2 data models
    ├── parser.py                # Batchexecute protocol parser (XSSI, chunks, unescaping)
    ├── session.py               # Zero-auth session manager with SAPISIDHASH
    ├── transport.py             # RPC transport layer with retry logic
    ├── endpoints.py             # 36+ RPC endpoint registry with disk caching
    ├── extractors.py            # Position + recursive data extraction (10 extractors)
    ├── auto_heal.py             # Auto-healing engine (Playwright + HTML fallback)
    ├── exceptions.py            # 7 custom exception types
    ├── resilience/              # Circuit breaker + retry decorator
    │   └── __init__.py          # CircuitBreaker class and with_retry decorator
    ├── services/                # 9 service modules
    │   ├── __init__.py          # Service module exports
    │   ├── quote.py             # QuoteService — stock prices, details, stats, realtime, batch
    │   ├── market.py            # MarketService — indices, summary, movers
    │   ├── chart.py             # ChartService — OHLCV, historical, intraday
    │   ├── news.py              # NewsService — market news, ticker news
    │   ├── company.py           # CompanyService — company info, related companies
    │   ├── financials.py        # FinancialsService — statements, statistics, dividends
    │   ├── analysts.py          # AnalystsService — ratings, earnings, transcripts
    │   ├── research.py          # ResearchService — AI research queries
    │   └── search.py            # SearchService — autocomplete/symbol lookup
    ├── fastapi_app.py           # FastAPI application factory + run_sync helper
    ├── fastapi_cli.py           # CLI entry point with auto-dependency installation
    └── fastapi_routes/          # 9 modular FastAPI route files
        ├── __init__.py          # Route module exports
        ├── quote.py             # Quote REST endpoints
        ├── market.py            # Market REST endpoints
        ├── chart.py             # Chart REST endpoints
        ├── news.py              # News REST endpoints
        ├── company.py           # Company REST endpoints
        ├── financials.py        # Financials REST endpoints
        ├── analysts.py          # Analysts REST endpoints
        ├── research.py          # Research REST endpoints (POST + GET)
        └── system.py            # System REST endpoints (health, heal, endpoints)
```

### File: `pyproject.toml` — Package Configuration

The `pyproject.toml` file is the modern PEP 621 compliant packaging configuration that replaces the traditional `setup.py` / `setup.cfg` / `requirements.txt` approach. It defines the project metadata, dependencies, optional dependency groups, and build system requirements.

Key configuration details:

- **Build System**: Uses `setuptools >= 68.0` with `wheel` as the build backend. This ensures compatibility with the vast majority of Python packaging tools and CI/CD systems while using modern standards.
- **Project Name**: `gfinance` — The package name used for `pip install gfinance`
- **Version**: `2.0.0` — Follows semantic versioning (major.minor.patch)
- **Python Support**: `>= 3.9` — Supports Python 3.9, 3.10, 3.11, 3.12, and future versions
- **Core Dependencies**: Only `requests >= 2.28.0` and `pydantic >= 2.0.0` — deliberately minimal to reduce installation footprint and dependency conflicts
- **Optional Dependency Groups**: Five groups (`async`, `fastapi`, `heal`, `data`, `dev`) plus a meta-group `all` that installs everything
- **CLI Entry Point**: `gfinance-server = gfinance.fastapi_cli:main` — After installation, users can run `gfinance-server` to start the API server
- **Classifiers**: Standard PyPI classifiers for discoverability including Development Status (Production/Stable), Intended Audience (Developers), License (MIT), Python versions, and Topic (Financial/Investment)

The optional dependency groups serve specific purposes:

The `async` group installs `aiohttp >= 3.8.0` which is required for the `AsyncGoogleFinanceClient`. Without this package installed, attempting to import `AsyncGoogleFinanceClient` will raise an `ImportError`. The aiohttp library provides a fully asynchronous HTTP client that supports connection pooling, keep-alive, and concurrent requests without blocking the event loop.

The `fastapi` group installs `fastapi >= 0.100.0` and `uvicorn >= 0.20.0`. FastAPI is the web framework that powers the REST API server, while Uvicorn is the ASGI server that serves the application. These are only needed if you want to run the gfinance API server.

The `heal` group installs `playwright >= 1.30.0` for the browser-based auto-healing engine. After installing this group, you also need to run `playwright install chromium` to download the Chromium browser binary. The Playwright library enables headless browser automation for discovering RPC function IDs.

The `data` group installs `pandas >= 1.5.0` which is required for the `ChartData.to_dataframe()` method that converts chart tick data into a pandas DataFrame for analysis. This is optional because not all users need DataFrame export.

The `dev` group installs `pytest >= 7.0.0`, `pytest-asyncio >= 0.21.0`, and `httpx >= 0.24.0` for development and testing. Pytest is the test framework, pytest-asyncio adds async test support, and httpx is used for testing the FastAPI endpoints.

### File: `run.py` — Quick-Start Script

The `run.py` file is a convenience script for quickly starting the FastAPI server. It's designed to work out of the box on Arch Linux / Garuda Linux systems.

Key aspects of this file:

- **Path Setup**: Inserts the project directory into `sys.path` to ensure the gfinance package is importable regardless of the current working directory or installation state
- **Auto-Dependency Installation**: Delegates to `fastapi_cli.main()` which automatically checks and installs missing dependencies before starting the server
- **Environment Variables**: Documents the three supported environment variables (`GFINANCE_HOST`, `GFINANCE_PORT`, `GFINANCE_RELOAD`) that control server behavior
- **No Arguments Required**: Simply running `python run.py` starts the server with sensible defaults (0.0.0.0:8000 with auto-reload enabled)

This file is particularly useful during development because it handles the common case of missing dependencies gracefully — instead of failing with an import error, it offers to install them automatically.

### File: `gfinance/__init__.py` — Public API Exports

The `__init__.py` file defines the public API surface of the gfinance package. It exports all the key classes and exceptions that users need, enabling clean imports like `from gfinance import GoogleFinanceClient, Quote`.

Exported models (15 total):
- `Quote` — Real-time stock/crypto/index quote with price, change, volume
- `CompanyDetails` — Detailed company information (sector, CEO, employees)
- `ChartData` — Time-series chart data with list of ChartTick entries
- `ChartTick` — Single data point in a chart (OHLCV + change)
- `AnalystRating` — Analyst consensus and price targets
- `EarningsData` — Earnings history with EPS estimates vs. actuals
- `FinancialStatement` — Single financial statement (income/BS/CF)
- `FinancialStatements` — Complete set of financial statements
- `SearchResult` — Search autocomplete result with symbol and exchange
- `MarketIndex` — Market index entry (name, price, change)
- `MarketSummary` — Market summary with indices and sectors
- `MarketMovers` — Market movers (gainers, losers, most active)
- `NewsArticle` — News article with title, source, URL

Exported client:
- `GoogleFinanceClient` — The main synchronous client

Exported exceptions (7 total):
- `GFinanceError` — Base exception for all gfinance errors
- `SessionError` — Session acquisition or refresh failure
- `RPCError` — RPC call to batchexecute failed (includes rpc_id attribute)
- `ParseError` — Response parsing or deobfuscation failure
- `EndpointNotFoundError` — Requested endpoint/RPC function ID not found
- `AutoHealError` — Auto-healing/RPC re-discovery failure
- `RateLimitError` — Rate limit detected (includes retry_after attribute)

The `__version__` attribute provides the current version string (`"2.0.0"`), and `__author__` provides the author string.

Note that `AsyncGoogleFinanceClient` is NOT exported from the top-level package because it requires the optional `aiohttp` dependency. Users must import it directly: `from gfinance.async_client import AsyncGoogleFinanceClient`.

### File: `gfinance/client.py` — Synchronous Client

The `GoogleFinanceClient` is the primary entry point for synchronous access to Google Finance data. It follows the facade design pattern, orchestrating multiple internal components while providing a clean, simple interface.

**Constructor Parameters:**

The `__init__` method accepts six configuration parameters that control the client's behavior:

- `proxies` (Optional[Dict[str, str]]): HTTP/HTTPS proxy configuration. Pass a dictionary like `{"http": "http://proxy:8080", "https": "http://proxy:8080"}` to route all requests through a proxy server. Supports HTTP, HTTPS, and SOCKS5 proxies (for SOCKS5, install `requests[socks]`). Defaults to `None` (no proxy).

- `max_retries` (int): Maximum number of retry attempts for failed requests. The transport layer will retry up to this many times before raising an `RPCError`. Each retry uses an increasing delay based on `retry_delay`. Defaults to `3`.

- `retry_delay` (float): Base delay in seconds between retry attempts. Actual delay is `retry_delay * (attempt + 1)` for general failures, and `retry_delay * 2^(attempt+2)` for rate limits, capped at 60 seconds. Defaults to `1.0`.

- `timeout` (float): Request timeout in seconds. This is passed to both the session manager (for connection establishment) and the transport layer (for individual requests). Defaults to `30.0`.

- `auto_heal` (bool): Whether to enable automatic RPC ID re-discovery. When enabled, the client can recover from Google deployment changes that alter RPC function IDs. Defaults to `True`.

- `language` (str): The `Accept-Language` header value sent with all requests. This affects the language of company names, descriptions, and other text content in responses. Defaults to `"en-US"`.

**Internal Components:**

The constructor initializes six internal components:

1. `SessionManager`: Handles zero-auth session acquisition, token extraction (f.sid, bl, at, SAPISID), SAPISIDHASH computation, and automatic session refresh when the 30-minute TTL expires.

2. `EndpointRegistry`: Maintains the mapping of 36+ endpoint names to RPC function IDs and payload templates. Loads cached RPC IDs from disk on startup and saves updates when auto-healing discovers new IDs.

3. `RPCTransport`: The low-level transport layer that constructs and sends batchexecute POST requests with retry logic, rate limit handling, and automatic session refresh on authentication failures.

4. `CircuitBreaker`: Monitors the success/failure rate of requests and opens the circuit when failures exceed the threshold (5 by default), preventing cascading failures. The circuit automatically resets after 60 seconds.

5. `AutoHealEngine`: Re-discovers RPC function IDs using Playwright browser automation or HTML fallback parsing when Google updates their deployments.

6. **Nine Service Modules**: Each service module is initialized with the transport layer and provides domain-specific methods. The services are: `QuoteService`, `MarketService`, `ChartService`, `NewsService`, `CompanyService`, `FinancialsService`, `AnalystsService`, `ResearchService`, and `SearchService`.

**Public Methods:**

Beyond the service modules (accessed as `client.quote`, `client.market`, etc.), the client provides several utility methods:

- `heal() -> Dict[str, str]`: Manually trigger auto-healing to re-discover RPC IDs. Returns a dictionary mapping endpoint names to their new RPC IDs. This is useful when requests start failing after a Google deployment update.

- `refresh_session()`: Force-refresh the session by re-visiting Google Finance and extracting new tokens. This is useful when you suspect the session has become stale or invalid.

- `list_endpoints(category=None) -> List[RPCEndpoint]`: List all registered RPC endpoints, optionally filtered by category. Each entry includes the name, RPC ID, description, category, payload template, and entity type.

- `list_categories() -> List[str]`: List all available endpoint categories (e.g., 'analysts', 'chart', 'company', 'financials', 'market', etc.).

- `resilience_stats() -> dict`: Get the current circuit breaker statistics including success count, failure count, and whether the circuit is open.

- `close()`: Close the client and release all resources including the HTTP session. Always call this when done, or use the context manager pattern.

**Context Manager Support:**

The client supports the context manager protocol (`__enter__` / `__exit__`), which ensures proper resource cleanup:

```python
with GoogleFinanceClient() as client:
    quote = client.quote.get("AAPL")
# Session is automatically closed here
```

### File: `gfinance/async_client.py` — Asynchronous Client

The `AsyncGoogleFinanceClient` provides high-performance asynchronous access to Google Finance data using `aiohttp`. Unlike the synchronous client which delegates to service modules, the async client implements all methods directly for maximum performance and simplicity.

**Design Philosophy:**

The async client takes a different architectural approach from the sync client. Rather than using separate service modules, it implements all data fetching methods directly on the client class. This reduces overhead, simplifies the codebase, and makes it easier to implement true concurrent operations using `asyncio.gather()`.

**Constructor Parameters:**

- `timeout` (float): Request timeout in seconds for both session initialization and RPC calls. Defaults to `30.0`.
- `language` (str): Accept-Language header value. Defaults to `"en-US"`.

**Session Management:**

The async client manages its own session lifecycle:

- `_ensure_session()`: Checks if the aiohttp session exists and is not closed, and whether it has expired (30-minute TTL). If needed, creates a new session or refreshes the existing one.
- `_init_session()`: Visits Google Finance Beta and extracts the f.sid, bl, and at tokens from the HTML response. This is called automatically when the session is first needed or after expiration.
- `_is_expired()`: Returns `True` if the session has exceeded its 30-minute TTL.

**RPC Call Implementation:**

The `_call_rpc()` method is the core of the async client. It handles:

1. Session initialization/refresh
2. Endpoint lookup from the registry
3. Asset identifier construction and payload template substitution
4. Request parameter construction (rpcids, f.sid, bl, _reqid, etc.)
5. JSON body construction using `json.dumps()` for proper escaping
6. POST request with proper headers (Content-Type, X-Same-Domain, Referer)
7. Response parsing using the shared `parse_batchexecute()` function
8. RPC ID matching to find the correct response payload
9. Error handling with automatic session refresh on auth failures (400, 401, 403)

**Concurrent Batch Quotes:**

The `get_batch_quotes()` method is the key advantage of the async client. It uses `asyncio.gather()` to fetch multiple quotes concurrently:

```python
quotes = await client.get_batch_quotes([
    ("AAPL", "NASDAQ"), ("GOOGL", "NASDAQ"), ("MSFT", "NASDAQ")
])
# All three requests are sent concurrently, not sequentially
```

This provides significant performance improvement over the synchronous `batch_quotes()` method which processes requests sequentially.

**Resilience Stats:**

The `get_resilience_stats()` method returns a dictionary with success/failure counts and session health status:

```python
{
    "success": 10,        # Number of successful RPC calls
    "failure": 0,         # Number of failed RPC calls
    "session_healthy": True,  # Whether the session is not expired
    "f_sid_set": True     # Whether f.sid has been acquired
}
```

### File: `gfinance/models.py` — Pydantic Data Models

The models module defines 15 Pydantic v2 BaseModel classes that provide type safety, validation, and serialization for all data returned by the Google Finance API.

**Why Pydantic v2?**

Pydantic v2 was chosen over v1 and other alternatives for several important reasons:

1. **Performance**: Pydantic v2 is 5-50x faster than v1 thanks to its Rust-based core (`pydantic-core`). This matters when processing large financial datasets with many tick entries or complex financial statements.

2. **Type Safety**: Full type annotations with `Optional`, `List`, `Dict`, and `Field` provide IDE autocompletion, type checking with mypy, and runtime validation. Every field has a documented type.

3. **Serialization**: Built-in `.model_dump()` and `.model_dump_json()` methods support multiple export formats with fine-grained control over included/excluded fields and None handling.

4. **Validation**: Automatic type coercion and validation ensure data integrity. Invalid types are caught immediately rather than causing cryptic errors downstream.

5. **Default Values**: Every field has a sensible default (empty string, None, empty list), so partial data doesn't cause validation errors. This is crucial because Google Finance responses often have missing fields.

**Model Design Principles:**

- **Optional Fields**: Most numeric fields are `Optional[float]` or `Optional[int]` because Google Finance doesn't always return all data points. A missing P/E ratio shouldn't crash the entire application.
- **String Defaults**: Text fields default to empty strings rather than None, making it safe to access `quote.name` without None checks.
- **Computed Properties**: `ChartData` includes `latest_price`, `highest`, and `lowest` properties for convenient access to derived values.
- **DataFrame Export**: `ChartData.to_dataframe()` converts tick data to a pandas DataFrame, providing seamless integration with the data science ecosystem.
- **Nested Models**: `FinancialStatements` contains three `FinancialStatement` objects (income, balance sheet, cash flow), and `ChartData` contains a list of `ChartTick` objects.

**ChartTick Model — Deep Dive:**

The `ChartTick` model is one of the most important models because it represents individual price data points. It supports multiple data formats:

- **Full OHLCV**: When all Open, High, Low, Close, Volume data is available, all fields are populated
- **Close + Change**: When only close price and change data is available, `open` is derived as `close - change`
- **Price Only**: When only a single price is available, the `price` field is used as a fallback

The `timestamp` field uses a string format (`"YYYY-MM-DD"` or `"YYYY-MM-DD HH:MM"`) rather than a datetime object because:
1. It avoids timezone issues (Google provides timestamps in various formats)
2. It's directly serializable to JSON without custom encoders
3. It's easy to parse with pandas' `to_datetime()` when needed

### File: `gfinance/parser.py` — Batchexecute Protocol Parser

The parser module is one of the most technically complex parts of gfinance. It handles Google's proprietary batchexecute response format, which uses multiple layers of encoding and protection.

**XSSI Protection (`strip_xssi`):**

Google uses Cross-Site Scripting Inclusion (XSSI) protection to prevent unauthorized cross-origin data access. Every batchexecute response starts with the prefix `)]}'` followed by a newline. This makes the response invalid JSON, which prevents malicious websites from including it via `<script>` tags.

The `strip_xssi()` function removes this prefix and any leading whitespace/newlines. It's called as the first step in the parsing pipeline.

**Length-Prefixed Chunk Parsing (`parse_chunks`):**

Google's batchexecute responses use a length-prefixed chunk format where each chunk is preceded by its byte length:

```
123\n
[["wrb.fr","gCvqoe","...data..."]]\n
456\n
[["wrb.fr","HacE5d","...data..."]]\n
```

The `parse_chunks()` function parses this format by:
1. Finding the first newline to determine the chunk length
2. Extracting the chunk data based on the length
3. Moving to the next chunk after stripping the newline separator
4. Handling edge cases like incomplete chunks and missing length prefixes

**Multi-Level JSON Unescaping (`unescape_json`):**

Google's responses often contain JSON strings nested inside JSON strings, sometimes up to 5 levels deep. For example:

```
Level 0: "[[\"wrb.fr\",\"gCvqoe\",\"\\\"[[\\\\\"data\\\\\"]\\\"\",null,null,null,\"generic\"]]"
Level 1: [["wrb.fr","gCvqoe","\"[[\\\"data\\\"]\"",null,null,null,"generic"]]
Level 2: [[\"data\"]]
Level 3: [data]
```

The `unescape_json()` function iteratively parses JSON strings up to 5 levels deep, stopping when the result is no longer a string. This handles the full range of Google's encoding schemes.

**Recursive Extraction (`recursive_extract`):**

The `recursive_extract()` function is a powerful utility that recursively searches nested arrays and dictionaries for values of a target type. It's used as a fallback when position-based extraction fails:

```python
# Find all float values in a deeply nested response
prices = recursive_extract(data, (int, float))

# Find all string values
labels = recursive_extract(data, str)
```

The function has a `max_depth` parameter (default 50) to prevent infinite recursion on circular references, though this shouldn't occur with Google's response format.

**Safe Navigation (`safe_get`):**

The `safe_get()` function navigates nested lists by index path without raising IndexError, TypeError, or KeyError:

```python
# Safely get data[0][5][2] without worrying about missing indices
price = safe_get(data, (0, 5, 2), default=None)
```

This is essential because Google's response arrays have variable lengths and missing elements. A response for a stock might have data at index [5] while a crypto response might not, and `safe_get()` handles both cases gracefully.

**Asset Identifier Construction (`build_asset_identifier`):**

The `build_asset_identifier()` function constructs Google's internal asset identifier format:

- Stock with exchange: `[null, ["AAPL", "NASDAQ"]]`
- Crypto pair: `[null, null, ["BTC", "USDT"]]`
- Stock without exchange: `[null, ["AAPL", ""]]`

The format is determined by the presence of the exchange parameter and whether the symbol contains a hyphen (indicating a currency pair).

### File: `gfinance/session.py` — Zero-Auth Session Manager

The session module handles the complete lifecycle of Google Finance sessions, from initial acquisition through automatic refresh to proper cleanup. The key innovation is "zero-auth" — no API keys, OAuth tokens, or manual configuration is required.

**FinanceSession Dataclass:**

The `FinanceSession` dataclass holds all session tokens:

- `cookies`: Dictionary of all cookies from the Google Finance page visit
- `f_sid`: The "f.sid" parameter required in batchexecute URL query strings. This is a session identifier that Google uses to track state.
- `bl`: The "bl" parameter, which appears to be a build label or version identifier. It changes with Google's deployments.
- `at`: The "at" (XSRF token) parameter included in the request body. This provides CSRF protection.
- `sapisid`: The SAPISID cookie value used for SAPISIDHASH authentication
- `created_at`: Timestamp when the session was created, used for TTL checking

**SAPISIDHASH Authentication:**

The `to_headers()` method on `FinanceSession` computes the SAPISIDHASH authentication token that Google requires for batchexecute requests:

```
SAPISIDHASH = "{timestamp_ms}_{SHA1(timestamp_ms + ' ' + sapisid + ' ' + origin)}"
```

Where:
- `timestamp_ms` is the current time in milliseconds
- `sapisid` is the SAPISID cookie value
- `origin` is `"https://www.google.com"`

This hash is included in every request's `Authorization` header. Google validates this hash server-side to verify that the request comes from a legitimate Google Finance page visit.

**Session Acquisition:**

The `_acquire()` method performs the following steps:

1. Sends a GET request to `https://www.google.com/finance/beta`
2. Extracts `f.sid` using regex pattern `r'"FdrFJe"\s*:\s*"(-?\d+)"'`
3. Extracts `bl` using regex pattern `r'"cfb2h"\s*:\s*"([^"]+)"'`
4. Extracts `at` using regex pattern `r'"SNlM0e"\s*:\s*"([^"]+)"'`
5. Collects all cookies from the session, identifying the SAPISID cookie
6. Falls back to extracting `f.sid` from cookies if the HTML pattern doesn't match

**Session Auto-Refresh:**

Sessions have a 30-minute TTL defined by `SESSION_TTL = 1800`. The `get_session()` method automatically refreshes expired sessions:

```python
def get_session(self, force_refresh=False) -> FinanceSession:
    if force_refresh or self._finance_session is None or self._finance_session.is_expired:
        self._finance_session = self._acquire()
    return self._finance_session
```

**URL and Body Construction:**

The `build_batchexecute_url()` method constructs the full batchexecute URL with all required query parameters:

```
https://www.google.com/finance/beta/_/FinHubUi/data/batchexecute?
  rpcids=gCvqoe&
  source-path=/finance/beta&
  f.sid=1234567890&
  bl=abc123&
  hl=en-US&
  authuser=0&
  soc-app=1&
  soc-platform=1&
  soc-device=1&
  _reqid=200000&
  rt=c
```

The `build_f_req()` method constructs the f.req form body:

```
f.req=[[["gCvqoe","[[null, [\"AAPL\", \"NASDAQ\"]], 1]",null,"generic"]]]&at=XSRF_TOKEN
```

The body is JSON-encoded using `json.dumps()` to ensure proper escaping of quotes and special characters in the payload template.

### File: `gfinance/transport.py` — RPC Transport Layer

The `RPCTransport` class is the low-level transport layer responsible for sending batchexecute RPC requests and handling retries, rate limits, and session refreshes.

**Constructor Parameters:**

- `session_manager`: The `SessionManager` instance for session tokens and URL/body construction
- `registry`: The `EndpointRegistry` for looking up RPC IDs and payload templates
- `max_retries`: Maximum retry attempts (default: 3)
- `retry_delay`: Base delay between retries in seconds (default: 1.0)
- `timeout`: Request timeout in seconds (default: 30.0)

**Request Flow:**

The `call()` method is the public interface, which delegates to `_call_rpc()`. The complete request flow:

1. Look up the endpoint in the registry to get the RPC ID and payload template
2. Substitute the asset identifier: `build_asset_identifier(symbol, exchange)` replaces `{asset}` in the template
3. Substitute the ticker and exchange: `{ticker}` → `"AAPL"`, `{exchange}` → `"NASDAQ"`
4. Apply custom overrides: Any `payload_overrides` dictionary values replace matching template placeholders
5. Clean unresolved placeholders: `{entity_ids}` → `null`, `{asset_filter}` → `[]`, etc.
6. Build the batchexecute URL and request body using the session manager
7. Send the POST request with proper headers and cookies
8. Handle the response based on status code:
   - **200 OK**: Parse the response using `parse_batchexecute()` and return the matched data
   - **429 Rate Limited**: Wait with exponential backoff (delay × 2^(attempt+2), max 60s) and retry
   - **400/401/403 Auth Failure**: Refresh the session and retry with new tokens
   - **Other errors**: Raise `RPCError`
9. On success, find the response payload matching our RPC ID using `find_by_rpc_id()`
10. If no exact match, fall back to the first payload as a best-effort response

**call_multiple() Method:**

The `call_multiple()` method sends multiple RPC calls sequentially (not concurrently, for reliability). It collects results in a dictionary, with `None` for any failed calls:

```python
results = transport.call_multiple(["quote_core", "quote_stats", "quote_about"], symbol="AAPL", exchange="NASDAQ")
# results = {"quote_core": [...], "quote_stats": [...], "quote_about": [...]}
```

### File: `gfinance/endpoints.py` — RPC Endpoint Registry

The endpoint registry maps 36+ human-friendly endpoint names to Google's obfuscated RPC function IDs and payload templates. It also provides disk caching for auto-healing results.

**RPCEndpoint Dataclass:**

Each endpoint is represented by an `RPCEndpoint` dataclass with the following fields:

- `rpc_id`: The obfuscated function ID (e.g., `"gCvqoe"` for quote_core, `"FinanceHubService/ExecuteResearchQuery"` for research)
- `name`: Human-friendly name (e.g., `"quote_core"`)
- `description`: Brief description of what the endpoint returns
- `category`: Category grouping (e.g., `"quote"`, `"chart"`, `"market"`)
- `payload_template`: The JSON payload template with placeholders like `{asset}`, `{ticker}`, `{period}`
- `entity_type`: Which entity types this endpoint supports (`"all"`, `"stock"`, `"crypto"`)
- `params`: List of parameter names this endpoint accepts
- `data_service_index`: Optional index for matching endpoints during auto-healing

**Known Endpoints:**

The `KNOWN_ENDPOINTS` dictionary contains 36+ pre-discovered endpoints organized by category:

- **Navigation** (2): `page_load`, `navigation`
- **Session** (1): `feature_flags`
- **Market** (7): `market_summary`, `market_status`, `market_screener`, `market_indices`, `market_categories`, `market_regions`, `batch_quote_detailed`
- **Quote** (7): `quote_core`, `quote_details`, `quote_stats`, `quote_info`, `realtime_price`, `quote_about`, `symbol_resolve`
- **Chart** (5): `chart_data`, `chart_crypto`, `price_history`, `price_history_multi`, `stock_chart`
- **News** (2): `news`, `quote_news`
- **Company** (3): `company_info`, `related_companies`, `related_stocks`
- **Financials** (2): `financial_statements`, `dividends`
- **Analysts** (3): `analyst_ratings`, `earnings`, `earnings_transcript`
- **Watchlist** (1): `watchlist`
- **Research** (1): `research`
- **Search** (1): `search_autocomplete`
- **System** (1): `async_data`

**Disk Caching:**

The registry caches RPC ID overrides to disk at `~/.cache/gfinance/rpc_ids.json`. This ensures that auto-healing discoveries persist across application restarts. The cache is loaded on startup and updated whenever an RPC ID changes.

### File: `gfinance/extractors.py` — Data Extraction

The extractors module contains 10 specialized extraction functions that map Google's positional-array response data to typed Pydantic models. Each extractor handles the deeply nested, positional data format that Google uses.

**Extraction Strategy:**

The extractors use a dual strategy for maximum robustness:

1. **Position-Based Extraction (Primary)**: Navigates the known positions in Google's nested arrays using `safe_get()`. For example, `entity[5]` contains the price array `[price, change, change_percent]`. This is fast and accurate when the response format matches expectations.

2. **Recursive Fallback**: When position-based extraction fails or returns None, uses `recursive_extract()` to search the entire response tree for values of the expected type. This handles cases where Google changes the response format or where different entity types have different structures.

**Helper Functions:**

- `_f(data, path)`: Safe float extraction from a nested path
- `_i(data, path)`: Safe integer extraction from a nested path
- `_s(data, path)`: Safe string extraction from a nested path
- `_navigate_to_entity(data)`: Traverses deeply nested arrays to find the entity data array. The entity is identified as the innermost array that starts with a string (typically a Knowledge Graph ID like `"/m/0k8z"` for Apple).

**Extractor Functions:**

1. `extract_quote(data, symbol, exchange)` → `Quote`: Extracts price, change, name, currency, prev_close, entity_type from the response. Uses `_navigate_to_entity()` to find the entity array, then extracts fields from known positions.

2. `extract_company_details(data, symbol)` → `CompanyDetails`: Extracts sector, industry, CEO, employees, headquarters from the "about" section. Falls back to keyword-based string matching.

3. `extract_chart_data(data, symbol, exchange, period)` → `ChartData`: Extracts time-series tick data. Supports multiple tick formats (date+price, OHLCV, close+change).

4. `extract_ohlcv(data, symbol, exchange, period)` → `ChartData`: The most sophisticated extractor. Handles the `price_history_multi` format with cumulative volume, derives open from close-change, and computes per-tick volume from cumulative differences.

5. `extract_analyst_ratings(data, symbol)` → `AnalystRating`: Extracts consensus rating, price targets (low/mean/high/median), number of analysts, and ratings breakdown (strong_buy, buy, hold, sell, strong_sell).

6. `extract_earnings(data, symbol)` → `EarningsData`: Extracts next earnings date, quarterly earnings (EPS estimate, EPS actual, revenue estimate, revenue actual).

7. `extract_financial_statements(data, symbol)` → `FinancialStatements`: Extracts income statement, balance sheet, and cash flow with periods and line items.

8. `extract_search_results(data)` → `List[SearchResult]`: Extracts symbol, exchange, name, entity type, and constructs Google Finance URLs.

9. `extract_market_summary(data, region)` → `MarketSummary`: Extracts market indices (name, price, change) and sector performance data.

10. `extract_market_movers(data, category)` → `MarketMovers`: Extracts list of top gainers/losers/most active securities.

11. `extract_news(data)` → `List[NewsArticle]`: Extracts article title, source, URL, time, snippet, and image URL.

**OHLCV Extractor — Deep Dive:**

The `extract_ohlcv()` function is the most complex extractor because it handles multiple response formats from different endpoints. It tries three strategies in order:

1. **price_history_multi format**: Parses `data[0][0][3]` which contains period arrays. Each period has entries with `[[Y,M,D,h,m,null,null,[tz]], [close, change, change_pct], cum_volume]`. Open price is derived as `close - change`, and per-tick volume is computed from cumulative volume differences.

2. **Direct OHLCV array format**: Recursively searches for arrays that look like OHLCV data (nested date+price pairs, flat timestamp+OHLCV arrays, or close+change+volume tuples).

3. **Standard chart extraction**: Falls back to `extract_chart_data()` which handles simpler chart response formats.

### File: `gfinance/auto_heal.py` — Auto-Healing Engine

The auto-healing engine is one of gfinance's most innovative features. It solves the problem of Google periodically updating their deployments, which changes the obfuscated RPC function IDs and breaks API calls.

**DiscoveredEndpoint Dataclass:**

Each discovered endpoint contains:
- `rpc_id`: The discovered RPC function ID
- `data_service_key`: The data service key (e.g., "ds:2") from the HTML
- `sample_keys`: Optional list of sample data keys found in the response

**Playwright-Based Discovery:**

The `_scan_with_playwright()` method:

1. Launches headless Chromium using Playwright's async API
2. Creates a new browser context with default settings
3. Registers a response listener that captures all batchexecute responses
4. Visits three key Google Finance pages:
   - `/finance` (home page — loads market summary, navigation)
   - `/finance/quote/AAPL:NASDAQ` (quote page — loads quote, chart, news, analysts)
   - `/finance/markets` (markets page — loads indices, movers)
5. Waits for network idle and a 2-second settle time on each page
6. Closes the browser and processes the captured responses
7. Parses each response for `wrb.fr` entries to discover RPC IDs

**HTML Fallback Discovery:**

The `_heal_html()` method is used when Playwright isn't available:

1. Sends a GET request to `https://www.google.com/finance`
2. Searches for `AF_initDataCallback` patterns in the HTML
3. Extracts `ds:N` → RPC ID mappings from the data service blocks
4. Also searches for `"ds:N": ["rpcid", "RPC_ID"]` patterns
5. Matches discovered RPC IDs to known endpoints using `data_service_index`

**Endpoint Matching:**

The `_match()` method maps discovered endpoints to known endpoints:

1. **Direct RPC ID match**: If the discovered RPC ID exactly matches a known endpoint's RPC ID
2. **Data service index match**: If the discovered endpoint has a `ds:N` key, match it to endpoints with the same `data_service_index`

### File: `gfinance/exceptions.py` — Custom Exceptions

The exceptions module defines 7 custom exception types that provide granular error handling:

1. **GFinanceError**: Base exception for all gfinance errors. Has a `message` attribute. All other exceptions inherit from this class, allowing users to catch all gfinance errors with a single `except GFinanceError` handler.

2. **SessionError**: Raised when session acquisition or refresh fails. This typically indicates network issues, Google Finance being unavailable, or HTML format changes that prevent token extraction.

3. **RPCError**: Raised when an RPC call to batchexecute fails. Includes the `rpc_id` attribute for debugging which endpoint failed. This is the most common error users will encounter.

4. **ParseError**: Raised when response parsing or deobfuscation fails. This indicates that the batchexecute response format has changed in a way that gfinance can't handle.

5. **EndpointNotFoundError**: Raised when a requested endpoint or RPC function ID is not found in the registry. This typically indicates a typo in the endpoint name or an outdated registry.

6. **AutoHealError**: Raised when auto-healing/RPC re-discovery fails. This means both Playwright and HTML fallback methods failed to discover new RPC IDs.

7. **RateLimitError**: Raised when rate limiting is detected. Includes a `retry_after` attribute suggesting how long to wait before retrying. Note: in the current implementation, rate limits are handled internally with retries, so this exception is rarely raised.

### File: `gfinance/resilience/__init__.py` — Circuit Breaker & Retry

The resilience module provides two key reliability patterns: circuit breaker and retry decorator.

**CircuitBreaker Class:**

The circuit breaker implements the classic three-state pattern:

- **CLOSED** (Normal): Requests flow through. Success and failure counts are tracked. When the failure count reaches the threshold (default: 5), the circuit opens.

- **OPEN** (Blocked): All requests are rejected. This prevents cascading failures when the downstream service (Google Finance) is experiencing issues. After the reset timeout (default: 60 seconds), the circuit transitions to half-open.

- **HALF-OPEN** (Testing): One request is allowed through as a test. If it succeeds, the circuit closes and normal operation resumes. If it fails, the circuit opens again.

The circuit breaker provides these methods:

- `record_success()`: Increment success count, decrement failure count, close the circuit if it was open
- `record_failure()`: Increment failure count, open the circuit if threshold is reached
- `should_allow()`: Returns True if requests should be allowed (closed or half-open)
- `is_open`: Property that returns True if the circuit is currently open
- `get_stats()`: Returns a dictionary with success_count, failure_count, and circuit_open status

**with_retry Decorator:**

The `with_retry` decorator provides retry functionality with exponential backoff for any function:

```python
@with_retry(max_retries=3, base_delay=1.0, max_delay=30.0)
def fetch_data(symbol):
    return client.quote.get(symbol)
```

The decorator:
- Catches all exceptions and retries up to `max_retries` times
- Waits `base_delay * 2^attempt` seconds between retries, capped at `max_delay`
- Logs warnings for each retry with the attempt number and delay
- Re-raises the last exception after all retries are exhausted

### File: `gfinance/fastapi_app.py` — FastAPI Application Factory

The FastAPI application factory creates and configures the production-ready REST API server.

**Application Configuration:**

- **Title**: "gfinance API"
- **Description**: "Production-grade REST API for Google Finance data — zero auth, auto-healing."
- **Version**: "2.0.0" (matches the package version)
- **Docs URL**: `/docs` (Swagger UI)
- **ReDoc URL**: `/redoc` (ReDoc documentation)

**CORS Middleware:**

The application includes CORS middleware configured to allow all origins, methods, and headers. This is appropriate for development and personal use but should be restricted in production.

**Router Registration:**

Nine routers are registered, each with a prefix and tag:

- System routes (no prefix, tag: "System") — health, heal, endpoints
- Quote routes (`/api/v1/quote`, tag: "Quote") — quotes, details, stats, realtime
- Market routes (`/api/v1/market`, tag: "Market") — summary, indices, movers
- Chart routes (`/api/v1/chart`, tag: "Chart") — data, ohlcv, history
- News routes (`/api/v1/news`, tag: "News") — market, ticker
- Company routes (`/api/v1/company`, tag: "Company") — info, related
- Financials routes (`/api/v1/financials`, tag: "Financials") — statements, statistics, dividends
- Analysts routes (`/api/v1/analysts`, tag: "Analysts") — ratings, earnings, transcript
- Research routes (`/api/v1/research`, tag: "Research") — query (POST), quick research (GET)

**run_sync Helper:**

The `run_sync()` async function runs synchronous client methods in a thread pool to avoid blocking the event loop. This is essential because FastAPI is async, but the `GoogleFinanceClient` is synchronous:

```python
async def run_sync(func: Callable, *args, **kwargs) -> Any:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(func, *args, **kwargs))
```

**Global Error Handler:**

A global exception handler catches all `GFinanceError` exceptions and returns structured JSON responses with HTTP 502 status:

```python
@app.exception_handler(GFinanceError)
async def gfinance_error_handler(request, exc):
    return JSONResponse(status_code=502, content={"error": exc.message, "type": type(exc).__name__})
```

**Singleton Client:**

The `get_client()` function returns a singleton `GoogleFinanceClient` instance, ensuring that all requests share the same session and endpoint registry. This is important for performance because session acquisition is expensive.

### File: `gfinance/fastapi_cli.py` — CLI Entry Point

The CLI entry point provides a user-friendly way to start the FastAPI server with automatic dependency checking and installation.

**Auto-Dependency Installation:**

The `_check_and_install_deps()` function checks for the four required packages (fastapi, uvicorn, requests, pydantic) and offers to install any that are missing. This ensures that the server can start even if the user hasn't installed all dependencies.

**Server Configuration:**

The server reads three environment variables for configuration:

- `GFINANCE_HOST` (default: "0.0.0.0"): The bind address
- `GFINANCE_PORT` (default: 8000): The bind port
- `GFINANCE_RELOAD` (default: "1"): Whether to enable auto-reload on code changes

**Uvicorn Configuration:**

The server is started with:
- Factory mode (`factory=True`) because `create_app()` is a factory function
- Host and port from environment variables
- Auto-reload enabled by default (convenient for development)
- Log level set to "info"

### Service Modules — Detailed Analysis

#### `gfinance/services/quote.py` — QuoteService

The QuoteService provides five methods for accessing stock, crypto, and index quote data:

- `get(symbol, exchange)`: Uses the `quote_core` endpoint to get the primary quote data including price, change, volume, and market cap. This is the most commonly used method.

- `details(symbol, exchange)`: Uses the `quote_details` endpoint to get extended company details like sector, CEO, and employees. Returns a `CompanyDetails` model.

- `stats(symbol, exchange)`: Uses the `quote_stats` endpoint to get key financial statistics like P/E ratio, EPS, and beta. Returns a `Quote` model with the additional fields populated.

- `realtime(symbol, exchange)`: Uses the `realtime_price` endpoint for real-time price data. Falls back to `get()` if the realtime endpoint doesn't return data.

- `batch_quotes(symbols)`: Fetches quotes for multiple symbols sequentially. For concurrent fetching, use the async client's `get_batch_quotes()` method.

#### `gfinance/services/market.py` — MarketService

The MarketService provides three methods for market-wide data:

- `summary(region)`: Uses the `market_summary` endpoint with a region code (1=US, 2=Europe, 3=Asia). Returns a `MarketSummary` with market indices and sector performance.

- `indices()`: Uses the `market_indices` endpoint to get major global market indices. Returns a `MarketSummary` with the region set to "global".

- `movers(category)`: Uses the `market_screener` endpoint with a category code (1=gainers, 2=most_active, 3=losers) and count=20. Returns a `MarketMovers` with up to 20 entities.

#### `gfinance/services/chart.py` — ChartService

The ChartService is the most sophisticated service module, providing four methods for historical price data:

- `data(symbol, exchange, period, include_volume)`: The primary chart data method with intelligent endpoint selection. Tries `price_history_multi` first for best data quality, then falls back to `chart_data` or `chart_crypto`.

- `ohlcv(symbol, exchange, period)`: Alias for `data()` with `include_volume=True`. Returns Open-High-Low-Close-Volume bar data.

- `history(symbol, exchange, period)`: Alias for `ohlcv()` with a default period of "1Y" for historical analysis.

- `intraday(symbol, exchange, period)`: Alias for `data()` intended for short-period (1D, 5D) intraday data.

Valid periods: `1D`, `5D`, `1M`, `6M`, `YTD`, `1Y`, `5Y`, `MAX`

#### `gfinance/services/news.py` — NewsService

The NewsService provides two methods:

- `market()`: Uses the `news` endpoint with empty query and count=10 to get general market news.

- `ticker(symbol, exchange)`: Uses the `quote_news` endpoint to get news specific to a ticker symbol.

#### `gfinance/services/company.py` — CompanyService

The CompanyService provides two methods:

- `info(symbol, exchange)`: Uses the `company_info` endpoint to get detailed company information.

- `related(symbol, exchange)`: Uses the `related_companies` endpoint to find related/similar companies. Uses `recursive_extract()` to parse the response into a list of dictionaries.

#### `gfinance/services/financials.py` — FinancialsService

The FinancialsService provides three methods:

- `statements(symbol, exchange)`: Uses the `financial_statements` endpoint to get income statement, balance sheet, and cash flow data. Returns a `FinancialStatements` model with up to three nested `FinancialStatement` objects.

- `statistics(symbol, exchange)`: Uses the `quote_stats` endpoint to get key financial statistics. Returns a `Quote` model with additional fields populated.

- `dividends(symbol, exchange)`: Uses the `dividends` endpoint to get dividend history and yield. Returns a dictionary with symbol, yield, and history list.

#### `gfinance/services/analysts.py` — AnalystsService

The AnalystsService provides three methods:

- `ratings(symbol, exchange)`: Uses the `analyst_ratings` endpoint to get consensus ratings and price targets. Returns an `AnalystRating` model.

- `earnings(symbol, exchange)`: Uses the `earnings` endpoint to get quarterly EPS estimates vs. actuals. Returns an `EarningsData` model.

- `transcript(symbol)`: Uses the `earnings_transcript` endpoint to get full earnings call transcript text. Returns a dictionary with symbol, quarter, date, and transcript text.

#### `gfinance/services/research.py` — ResearchService

The ResearchService provides one method:

- `query(symbol, question)`: Uses the `research` endpoint (FinanceHubService/ExecuteResearchQuery) to ask an AI-powered research question about a stock. Returns a dictionary with symbol, question, answer, and sources.

#### `gfinance/services/search.py` — SearchService

The SearchService provides one method:

- `query(query)`: Uses the `search_autocomplete` endpoint to search for securities by name or symbol. Returns a list of `SearchResult` models.

### FastAPI Routes — Detailed Analysis

Each route module follows a consistent pattern:

1. Import `APIRouter` from FastAPI
2. Import `get_client` and `run_sync` from `gfinance.fastapi_app`
3. Create a router instance
4. Define async endpoint handlers that call the sync client via `run_sync()`
5. Return the model's `model_dump()` for Pydantic model responses

The `run_sync()` function is essential because FastAPI is async but the `GoogleFinanceClient` is synchronous. Without it, every client call would block the event loop and prevent the server from handling other requests.

Each route file is intentionally minimal — typically 10-30 lines — to keep the code modular and maintainable. The business logic lives in the service modules, and the route files are just thin wrappers that handle HTTP request/response mapping.

---

## 🔧 Troubleshooting Guide

### Common Issues and Solutions

#### Issue: `SessionError: Failed to fetch Google Finance page`

**Cause**: Network connectivity issues, DNS resolution failures, or Google Finance being temporarily unavailable.

**Solutions**:

1. Check your internet connection: `curl -I https://www.google.com/finance`
2. If behind a proxy, configure it: `GoogleFinanceClient(proxies={"https": "http://proxy:8080"})`
3. If Google is blocked in your region, use a VPN or proxy
4. Try refreshing the session: `client.refresh_session()`
5. Increase the timeout: `GoogleFinanceClient(timeout=60.0)`

#### Issue: `RPCError: HTTP 403`

**Cause**: The session tokens have expired or become invalid. Google may have detected automated access.

**Solutions**:

1. The transport layer should auto-refresh on 403. Try the request again.
2. Manually refresh: `client.refresh_session()`
3. Reduce request frequency to avoid detection
4. Try using a different IP address (proxy/VPN)

#### Issue: `RPCError: Failed after 3 retries`

**Cause**: Persistent RPC failures. Google may have changed their RPC function IDs.

**Solutions**:

1. Trigger auto-healing: `client.heal()`
2. Install Playwright for better healing: `pip install gfinance[heal] && playwright install chromium`
3. Clear the endpoint cache: `client._registry.clear_cache()`
4. Check if Google Finance is accessible in your browser

#### Issue: `ImportError: No module named 'aiohttp'`

**Cause**: Trying to use the async client without the aiohttp dependency.

**Solution**: `pip install gfinance[async]` or `pip install aiohttp`

#### Issue: `ImportError: No module named 'fastapi'`

**Cause**: Trying to start the FastAPI server without the fastapi dependency.

**Solution**: `pip install gfinance[fastapi]` or the auto-installer should handle this

#### Issue: Quote returns data but some fields are None

**Cause**: Google Finance doesn't always return all data points. Different exchanges and entity types have different response formats.

**Solutions**:

1. Try the `quote_stats` endpoint: `client.quote.stats("AAPL")` — it may return fields that `quote_core` doesn't
2. Try `client.quote.details("AAPL")` for company-specific fields
3. Use `client.financials.statistics("AAPL")` for P/E, EPS, beta, etc.
4. Check the `entity_type` field — crypto and currency responses have different structures

#### Issue: Chart data has no volume

**Cause**: The `price_history_multi` endpoint returns cumulative volume, and the volume computation may not work for all response formats.

**Solutions**:

1. Try a different period: some periods have better volume data
2. Use the `chart_data` endpoint directly via the transport layer
3. Volume may genuinely be unavailable for some securities (e.g., indices)

#### Issue: Search returns raw/unparsed results

**Cause**: Google's search response format can vary significantly, and the extractor may not handle all formats.

**Solutions**:

1. Try more specific search terms
2. Use the exchange parameter when getting quotes: `client.quote.get("AAPL", "NASDAQ")` instead of searching
3. Check if the raw data contains useful information in a different format

#### Issue: `AutoHealError: HTML heal failed`

**Cause**: Google's HTML format has changed, preventing the fallback parser from finding RPC IDs.

**Solutions**:

1. Install Playwright: `pip install gfinance[heal] && playwright install chromium`
2. Manually inspect the RPC IDs in your browser's Network tab and update the registry
3. Clear the cache and try again: `client._registry.clear_cache()`

---

## 🐛 Debug Mode

Enable debug logging to see detailed request/response information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from gfinance import GoogleFinanceClient

with GoogleFinanceClient() as client:
    quote = client.quote.get("AAPL")
    # You'll see detailed logs including:
    # - Session acquisition details
    # - RPC request URLs and payloads
    # - Response parsing steps
    # - Retry attempts
    # - Circuit breaker state changes
```

Key loggers to watch:

- `gfinance.session`: Session acquisition and refresh
- `gfinance.transport`: RPC requests, retries, and rate limits
- `gfinance.auto_heal`: Auto-healing discovery process
- `gfinance.resilience`: Circuit breaker state changes
- `gfinance.extractors`: Data extraction details
- `gfinance.parser`: Response parsing steps

---

## 🔄 Migration Guide

### From yfinance to gfinance

```python
# yfinance
import yfinance as yf
ticker = yf.Ticker("AAPL")
price = ticker.info.get('currentPrice')
history = ticker.history(period="1mo")

# gfinance equivalent
from gfinance import GoogleFinanceClient
with GoogleFinanceClient() as client:
    quote = client.quote.get("AAPL")
    price = quote.price
    chart = client.chart.data("AAPL", period="1M")
```

### From google-finance-api (original) to gfinance v2

```python
# Old google-finance-api
from google_finance_api import FinanceClient
client = FinanceClient()
quote = client.get_quote("AAPL")

# gfinance v2
from gfinance import GoogleFinanceClient
with GoogleFinanceClient() as client:
    quote = client.quote.get("AAPL")
```

### From gfinance-beta to gfinance v2

```python
# Old gfinance-beta
from gfinance_beta import GFinance
gf = GFinance()
quote = gf.quote("AAPL")

# gfinance v2
from gfinance import GoogleFinanceClient
with GoogleFinanceClient() as client:
    quote = client.quote.get("AAPL")
```

---

## 🏆 Best Practices

1. **Always use context managers** (`with` statement) to ensure proper resource cleanup
2. **Use the async client** for batch operations and concurrent requests
3. **Implement caching** — don't re-fetch the same data within short time intervals
4. **Handle exceptions gracefully** — catch `GFinanceError` and its subclasses
5. **Respect rate limits** — add delays between rapid requests
6. **Don't rely on all fields** — Google Finance responses are often incomplete
7. **Use DataFrame export** for data analysis — it's the most flexible format
8. **Enable auto-healing** — it prevents breakage when Google updates deployments
9. **Monitor resilience stats** — watch for increasing failure counts
10. **Log at DEBUG level** when troubleshooting — it provides detailed request/response information

---

<div align="center">

**Made with ❤️ by [maruf009sultan](https://github.com/maruf009sultan) and contributors**

**⭐ Star this repo if you find it useful! ⭐**

[⬆ Back to Top](#-gfinance)

</div>
