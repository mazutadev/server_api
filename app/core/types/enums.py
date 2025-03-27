"""
Enum for core types
"""

from enum import Enum
from typing import List, Dict, Any, Optional


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
