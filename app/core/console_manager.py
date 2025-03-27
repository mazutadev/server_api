"""
Console manager for the application
"""

from rich import Console
from typing import Optional

from app.core.interfaces.console import IConsole
from app.core.types.enums import ConsoleLevel


class ConsoleManager(IConsole):
    """
    Console manager for the application
    """

    def __init__(self, app_name: str, debug: bool = False):
        """
        Initialize the console manager
        """
        self.console = Console()
        self.app_name = app_name if app_name else "App"
        self.debug = debug

    def _log(self,
             message: str,
             level: ConsoleLevel,
             module_prefix: Optional[str] = None) -> None:

        prefix = f"[{module_prefix}]" if module_prefix else ""
        self.console.print(f"[{level.value}] [{self.app_name}] "
                           f"{prefix} {message} [/{level.value}] ")

    def info(self,
             message: str,
             module_prefix: Optional[str] = None) -> None:
        self._log(message, ConsoleLevel.INFO, module_prefix)

    def debug(self,
              message: str,
              module_prefix: Optional[str] = None) -> None:
        if self.debug:
            self._log(message, ConsoleLevel.DEBUG, module_prefix)

    def warning(self,
                message: str,
                module_prefix: Optional[str] = None) -> None:
        self._log(message, ConsoleLevel.WARNING, module_prefix)

    def error(self,
              message: str,
              module_prefix: Optional[str] = None) -> None:
        self._log(message, ConsoleLevel.ERROR, module_prefix)

    def critical(self,
                 message: str,
                 module_prefix: Optional[str] = None) -> None:
        self._log(message, ConsoleLevel.CRITICAL, module_prefix)
