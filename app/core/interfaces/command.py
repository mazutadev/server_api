"""
Interface for commands
"""

from abc import ABC, abstractmethod
from typing import Optional, Union, List, Dict

from app.core.types.models import CommandResult
from app.core.interfaces.console import IConsole


class ICommand(ABC):
    """
    Interface for command_manager
    """

    @abstractmethod
    def set_console(self, console: IConsole) -> None:
        """
        Set the console manager for the command

        Args:
            console: IConsole
        """
        pass

    @abstractmethod
    def _build_command(self,
                       command: Union[str, List[str]] = None) -> List[str]:
        """
        Build the command with sudo if needed

        Args:
            command: command to execute

        Returns:
            List of command parts
        """
        pass

    @abstractmethod
    def execute(self,
                command: Union[str, List[str]],
                timeout: Optional[float] = None,
                env: Optional[Dict[str, str]] = None,
                cwd: Optional[str] = None,
                shell: bool = False) -> CommandResult:
        """
        Execute the command and return results

        Args:
            command: command to execute
            timeout: timeout for the command
            env: environment variables
            cwd: working directory

        Returns:
            CommandResult object with the results of the command
        """
        pass

    @abstractmethod
    def execute_sudo(self,
                     command: Union[str, List[str]],
                     sudo_user: Optional[str] = None,
                     **kwargs) -> CommandResult:
        """
        Execute the command with sudo

        Args:
            command: command to execute
            sudo_user: user to run the command as
            kwargs: Additional arguments for the execute method

        Returns:
            CommandResult object with the results of the command
        """
        pass
