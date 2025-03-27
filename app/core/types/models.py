"""
Models for the core types
"""

from dataclasses import dataclass
from typing import Optional

from app.core.types.enums import CommandStatus


"""
MODELS FOR COMMANDS
"""


@dataclass
class CommandResult:
    """
    Result of a command
    """
    status: CommandStatus
    return_code: int
    command: str
    stdout: str
    stderr: str
    execution_time: float
    error: Optional[str] = None
