from enum import StrEnum


class FlashCategory(StrEnum):
    """Category for flask flash messages"""

    SUCCESS = "green"
    """Success message"""

    INFO = "blue"
    """Information message"""

    WARNING = "yellow"
    """Warning message"""

    ERROR = "red"
    """Error message"""
