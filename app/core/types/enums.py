"""
Enum for core types
"""

from enum import Enum


"""
ENUMS FOR CONSOLE
"""


class ConsoleLevel(Enum):
    """
    Enum for core console levels
    """
    INFO: str = "white"
    DEBUG: str = "blue"
    WARNING: str = "yellow"
    ERROR: str = "red"
    CRITICAL: str = "bold red"


"""
ENUMS FOR COMMANDS
"""


class CommandStatus(Enum):
    """
    Enum for command status
    """
    SUCCESS: str = "success"
    FAILED: str = "failed"
    SKIPPED: str = "skipped"
    RUNNING: str = "running"
    CANCELLED: str = "cancelled"
    PENDING: str = "pending"
    INTERRUPTED: str = "interrupted"
    TIMEOUT: str = "timeout"
