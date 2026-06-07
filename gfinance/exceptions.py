"""Custom exception hierarchy for gfinance."""


class GFinanceError(Exception):
    """Base exception for all gfinance errors."""
    def __init__(self, message: str = "", *args, **kwargs):
        self.message = message
        super().__init__(message, *args, **kwargs)


class SessionError(GFinanceError):
    """Session acquisition or refresh failed."""
    pass


class RPCError(GFinanceError):
    """RPC call to batchexecute failed."""
    def __init__(self, message: str = "RPC call failed", rpc_id: str = None, **kwargs):
        self.rpc_id = rpc_id
        detail = f"{message} (rpc_id={rpc_id})" if rpc_id else message
        super().__init__(detail, **kwargs)


class ParseError(GFinanceError):
    """Response parsing or deobfuscation failed."""
    pass


class EndpointNotFoundError(GFinanceError):
    """Requested endpoint / RPC function ID not found."""
    def __init__(self, message: str = "Endpoint not found", endpoint: str = None, **kwargs):
        self.endpoint = endpoint
        detail = f"{message}: {endpoint}" if endpoint else message
        super().__init__(detail, **kwargs)


class AutoHealError(GFinanceError):
    """Auto-healing / RPC re-discovery failed."""
    pass


class RateLimitError(GFinanceError):
    """Rate limit detected — need to back off."""
    def __init__(self, message: str = "Rate limited", retry_after: float = None, **kwargs):
        self.retry_after = retry_after
        super().__init__(message, **kwargs)
