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
