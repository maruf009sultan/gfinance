"""
Resilience module — circuit breaker, retry decorator, health monitoring.
"""

import time
import logging
from typing import Optional, Callable, Any
from functools import wraps

logger = logging.getLogger(__name__)


class CircuitBreaker:
    """Prevents cascading failures by blocking requests when failure count is high."""

    def __init__(self, failure_threshold: int = 5, reset_timeout: float = 60.0):
        self._failure_count = 0
        self._success_count = 0
        self._open = False
        self._open_since: Optional[float] = None
        self._threshold = failure_threshold
        self._reset_timeout = reset_timeout

    def record_success(self):
        self._success_count += 1
        self._failure_count = max(0, self._failure_count - 1)
        if self._open:
            self._open = False
            logger.info("Circuit breaker closed")

    def record_failure(self):
        self._failure_count += 1
        if self._failure_count >= self._threshold and not self._open:
            self._open = True
            self._open_since = time.time()
            logger.warning("Circuit breaker opened — too many failures")

    def should_allow(self) -> bool:
        if not self._open:
            return True
        if self._open_since and (time.time() - self._open_since) > self._reset_timeout:
            logger.info("Circuit breaker half-open — allowing test request")
            return True
        return False

    @property
    def is_open(self) -> bool:
        return self._open

    def get_stats(self) -> dict:
        return {
            "success_count": self._success_count,
            "failure_count": self._failure_count,
            "circuit_open": self._open,
        }


def with_retry(max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 30.0):
    """Decorator: retry with exponential backoff."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_error = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries:
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        logger.warning("Attempt %d/%d failed: %s — retry in %.1fs",
                                       attempt + 1, max_retries + 1, e, delay)
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator
