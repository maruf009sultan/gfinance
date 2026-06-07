# 🏦 gfinance v2.0.0

**Production-Grade Google Finance API Library** — reverse-engineered, auto-healing, zero-auth, Arch-Linux-tested.

The **best of both worlds**: merges `google-finance-api` (typed models, async, resilience) with `gfinance-beta` (modular services, Playwright auto-heal, robust parsing, SAPISIDHASH auth) into one battle-tested library.

## ✨ Features

| Feature | Details |
|---------|---------|
| 🔥 **26+ RPC Endpoints** | Quotes, charts, news, financials, analysts, AI research, dividends, watchlist... |
| 🩹 **Auto-Healing** | Playwright + HTML fallback re-discovers RPC IDs when Google updates deployments |
| 🔄 **Async + Sync** | Both `GoogleFinanceClient` (sync) and `AsyncGoogleFinanceClient` (aiohttp) |
| 🛡️ **Circuit Breaker** | Prevents cascading failures; auto-opens/closes based on success rate |
| 🧱 **Typed Models** | Pydantic v2 models with `.model_dump()`, `.to_json()`, DataFrame export |
| 🚀 **FastAPI Server** | Modular route files, Swagger UI, CORS, `run_sync` for non-blocking |
| 🔐 **Zero Auth** | No API keys — sessions auto-generated with SAPISIDHASH |
| 📦 **Modern Packaging** | `pyproject.toml` only (no `setup.py`), PEP 621 compliant |
| 🐧 **Arch-Tested** | Tested on Linux (Arch/Garuda compatible) |

## 📦 Installation

```bash
# Core library only (minimal)
pip install -e .

# With FastAPI server
pip install -e ".[fastapi]"

# With async support
pip install -e ".[async]"

# With auto-healing (Playwright)
pip install -e ".[heal]"
playwright install chromium

# Everything
pip install -e ".[all]"
```

## 🚀 Quick Start

### Python Library

```python
from gfinance import GoogleFinanceClient

# Sync client (context manager)
with GoogleFinanceClient() as client:
    # Stock quote
    quote = client.quote.get("AAPL", "NASDAQ")
    print(f"AAPL: ${quote.price} ({quote.change_percent:.2f}%)")
    print(f"Name: {quote.name}, Currency: {quote.currency}")

    # Search
    results = client.search.query("Bitcoin")
    for r in results:
        print(f"{r.symbol} - {r.name}")

    # Market summary
    summary = client.market.summary("us")
    for idx in summary.indices:
        print(f"{idx.name}: {idx.price}")

    # Company info
    info = client.company.info("TSLA", "NASDAQ")
    print(f"Sector: {info.sector}, CEO: {info.ceo}")

    # Financial statements
    stmts = client.financials.statements("AAPL", "NASDAQ")
    print(f"Income stmt periods: {stmts.income_statement.periods if stmts.income_statement else 'N/A'}")
```

### Async Client

```python
import asyncio
from gfinance import AsyncGoogleFinanceClient

async def main():
    async with AsyncGoogleFinanceClient() as client:
        # Single quote
        quote = await client.get_quote("AAPL", "NASDAQ")
        print(f"AAPL: ${quote.price}")

        # Concurrent batch quotes
        quotes = await client.get_batch_quotes([
            ("AAPL", "NASDAQ"), ("GOOGL", "NASDAQ"), ("MSFT", "NASDAQ")
        ])
        for q in quotes:
            print(f"{q.symbol}: ${q.price}")

asyncio.run(main())
```

### FastAPI Server

```bash
# Start the server
gfinance-server
# Or: uvicorn gfinance.fastapi_app:create_app --factory --host 0.0.0.0 --port 8000
```

Then visit **http://localhost:8000/docs** for Swagger UI.

#### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check + resilience stats |
| GET | `/api/v1/quote/{symbol}` | Real-time stock quote |
| GET | `/api/v1/quote/{symbol}/details` | Company details |
| GET | `/api/v1/quote/{symbol}/stats` | Key statistics |
| GET | `/api/v1/quote/{symbol}/realtime` | Real-time price |
| GET | `/api/v1/market/summary` | Market summary |
| GET | `/api/v1/market/indices` | Major indices |
| GET | `/api/v1/market/movers` | Market movers |
| GET | `/api/v1/chart/{symbol}` | Chart data |
| GET | `/api/v1/news/market` | Market news |
| GET | `/api/v1/news/{symbol}` | Ticker news |
| GET | `/api/v1/company/{symbol}/info` | Company info |
| GET | `/api/v1/company/{symbol}/related` | Related companies |
| GET | `/api/v1/financials/{symbol}/statements` | Financial statements |
| GET | `/api/v1/financials/{symbol}/statistics` | Key statistics |
| GET | `/api/v1/financials/{symbol}/dividends` | Dividend data |
| GET | `/api/v1/analysts/{symbol}/ratings` | Analyst ratings |
| GET | `/api/v1/analysts/{symbol}/earnings` | Earnings data |
| GET | `/api/v1/analysts/{symbol}/transcript` | Earnings transcript |
| POST | `/api/v1/research/query` | AI research query |
| GET | `/api/v1/research/{symbol}` | Quick research |
| POST | `/api/v1/heal` | Trigger auto-heal |
| GET | `/api/v1/endpoints` | List all RPC endpoints |
| GET | `/api/v1/categories` | List endpoint categories |

## 🏗️ Architecture

```
gfinance/
├── gfinance/
│   ├── __init__.py              # Public API exports
│   ├── client.py                # Sync client (main entry point)
│   ├── async_client.py          # Async client (aiohttp)
│   ├── models.py                # 15 Pydantic v2 models
│   ├── parser.py                # Batchexecute protocol parser
│   ├── session.py               # Zero-auth session manager (SAPISIDHASH)
│   ├── transport.py             # RPC transport with retries
│   ├── endpoints.py             # 26+ RPC endpoint registry
│   ├── extractors.py            # Position + recursive data extraction
│   ├── auto_heal.py             # Playwright + HTML fallback healing
│   ├── exceptions.py            # 7 custom exception types
│   ├── resilience/              # Circuit breaker + retry decorator
│   ├── services/                # 9 service modules
│   │   ├── quote.py, market.py, chart.py, news.py
│   │   ├── company.py, financials.py, analysts.py
│   │   ├── research.py, search.py
│   ├── fastapi_app.py           # App factory + run_sync helper
│   ├── fastapi_cli.py           # CLI entry point
│   └── fastapi_routes/          # 9 modular route files
├── pyproject.toml               # Modern PEP 621 packaging
└── README.md
```

## ⚙️ Configuration

```python
client = GoogleFinanceClient(
    proxies={"http": "http://proxy:8080", "https": "http://proxy:8080"},
    max_retries=3,
    retry_delay=1.0,
    timeout=30.0,
    auto_heal=True,
    language="en-US",
)
```

## ⚠️ Disclaimer

This is an **unofficial** library that accesses Google Finance through reverse-engineered internal APIs. Not affiliated with Google. Use responsibly.

## 📜 License

MIT
