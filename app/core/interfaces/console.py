"""
Console interface for the application
"""

from abc import ABC, abstractmethod
from typing import Optional
from app.core.types.enums import ConsoleLevel


class IConsole(ABC):

    @abstractmethod
    def log(self,
            message: str,
            level: ConsoleLevel = ConsoleLevel.INFO,
            module_prefix: Optional[str] = None):
        """
        Log a message to the console

        Args:
            message (str): The message to log
            level (ConsoleLevel): The level of the message
            module_prefix (Optional[str]): The prefix of the module
        """
        pass
