"""
Console interface for the application
"""

from abc import ABC, abstractmethod
from typing import Optional
from app.core.types.enums import ConsoleLevel


class IConsole(ABC):

    @abstractmethod
    def _log(self,
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

    @abstractmethod
    def info(self, message: str,
             module_prefix: Optional[str] = None):
        """
        Log an info message to the console

        Args:
            message (str): The message to log
            module_prefix (Optional[str]): The prefix of the module
        """
        pass

    @abstractmethod
    def debug(self, message: str,
              module_prefix: Optional[str] = None):
        """
        Log a debug message to the console

        Args:
            message (str): The message to log
            module_prefix (Optional[str]): The prefix of the module
        """
        pass

    @abstractmethod
    def warning(self, message: str,
                module_prefix: Optional[str] = None):
        """
        Log a warning message to the console

        Args:
            message (str): The message to log
            module_prefix (Optional[str]): The prefix of the module
        """
        pass

    @abstractmethod
    def error(self, message: str,
              module_prefix: Optional[str] = None):
        """
        Log an error message to the console

        Args:
            message (str): The message to log
            module_prefix (Optional[str]): The prefix of the module
        """
        pass

    @abstractmethod
    def critical(self, message: str,
                 module_prefix: Optional[str] = None):
        """
        Log a critical message to the console

        Args:
            message (str): The message to log
            module_prefix (Optional[str]): The prefix of the module
        """
        pass
