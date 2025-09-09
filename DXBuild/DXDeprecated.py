import warnings, functools
from datetime import datetime
from typing import(
    List,
    Tuple
)

def deprecated(version: str = "", reason: str = ""):
    """Decorator used to mark methods or classes that have been deprecated."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"Function {func.__name__} is deprecated"
                + (f" since version {version}" if version else "")
                + (f": {reason}" if reason else ""),
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator

