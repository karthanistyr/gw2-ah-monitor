import traceback

def format_exception(exception):
    """Formats an exception's trace for printing"""
    return "".join(
        traceback.format_exception(
            etype=exception.__class__,
            value=exception,
            tb=exception.__traceback__
            )
        )

class ApplicationError(Exception):
    def __init__(self, message):
        super().__init__(message)
