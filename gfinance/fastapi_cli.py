"""CLI entry point — run the FastAPI server.

Usage:
    python -m gfinance.fastapi_cli          # from anywhere
    python gfinance/fastapi_cli.py           # from project root
    python run.py                            # from project root (convenience)
    gfinance-server                          # if installed via pip

On Arch Linux / Garuda:
    pacman -S python python-pip
    pip install fastapi uvicorn requests pydantic
    python gfinance/fastapi_cli.py
"""

import sys
import os


def _check_and_install_deps():
    """Auto-check and offer to install missing dependencies."""
    missing = []
    for pkg, import_name in [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("requests", "requests"),
        ("pydantic", "pydantic"),
    ]:
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"[gfinance] Missing dependencies: {', '.join(missing)}")
        print(f"[gfinance] Installing: pip install {' '.join(missing)}")
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print(f"[gfinance] Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print(f"[gfinance] Failed to auto-install. Please run manually:")
            print(f"  pip install {' '.join(missing)}")
            sys.exit(1)


def main():
    _check_and_install_deps()

    import uvicorn

    # Determine host and port from environment or defaults
    host = os.environ.get("GFINANCE_HOST", "0.0.0.0")
    port = int(os.environ.get("GFINANCE_PORT", "8000"))
    reload = os.environ.get("GFINANCE_RELOAD", "1").lower() in ("1", "true", "yes")

    print(f"[gfinance] Starting server on {host}:{port}")
    print(f"[gfinance] API docs: http://{host}:{port}/docs")
    print(f"[gfinance] ReDoc:    http://{host}:{port}/redoc")
    print(f"[gfinance] Press Ctrl+C to stop")

    uvicorn.run(
        "gfinance.fastapi_app:create_app",
        factory=True,
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()
