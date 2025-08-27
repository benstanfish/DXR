import warnings, functools
from datetime import datetime

_NL = '\n'

_RESET = '\033[0m'
_BOLD = '\033[1m'
_FAINT = '\033[2m'
_ITALIC = '\033[3m'
_UNDERLINE = '\033[4m'

_RED = '\033[31m'
_GREEN = '\033[32m'
_YELLOW = '\033[33m'
_BLUE = '\033[34m'
_MAGENTA = '\033[35m'
_CYAN = '\033[36M'

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


def timestamp(format_string: str=r'%Y%m%d_%H%M%S') -> str:
    """Returns a timestamp, default format: YYYYMMDD_HHMMSS"""
    return datetime.now().strftime(format_string)
    