class InvariantViolationError(RuntimeError):
    """
    Raised when a core system invariant is violated.
    This indicates database corruption or a serious logic bug.
    """
    def __init__(self, message: str, *, context: dict | None = None):
        super().__init__(message)
        self.context = context or {}
