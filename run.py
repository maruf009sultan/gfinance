#!/usr/bin/env python3
"""
gfinance — Quick-start FastAPI server.

Just run:
    python run.py

This will auto-check dependencies, install missing ones, and start the server.
Works on Arch Linux / Garuda out of the box.

Environment variables:
    GFINANCE_HOST  — bind address (default: 0.0.0.0)
    GFINANCE_PORT  — bind port (default: 8000)
    GFINANCE_RELOAD — auto-reload on code changes (default: 1)
"""

import sys
import os

# Ensure the package is importable from the project directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gfinance.fastapi_cli import main

if __name__ == "__main__":
    main()
