from enum import StrEnum

class Escapes(StrEnum):
    """Enum for ANSI escape codes used to style console output."""

    NL = '\n'

    Reset = '\033[0m'
    Bold = '\033[1m'
    Faint = '\033[2m'
    Italic = '\033[3m'
    Underline = '\033[4m'

    Red = '\033[31m'
    Green = '\033[32m'
    Yellow = '\033[33m'
    Blue = '\033[34m'
    Magenta = '\033[35m'
    Cyan = '\033[36M'