"""
Command Manager
"""

import subprocess
import time
from typing import Optional, List, Union, Dict

from app.core.types.models import CommandResult
from app.core.types.enums import CommandStatus
from app.core.interfaces.command import ICommand
from app.core.interfaces.console import IConsole


class CommandManager(ICommand):
    """
    Manager for executing shell commands with sudo support
    """
    def __init__(self,
                 use_sudo: bool = False,
                 sudo_user: Optional[str] = None):
        """
        Initialize the command manager

        Args:
            use_sudo: whether execute commands with sudo
            sudo_user: user to run the command as
        """
        self.use_sudo = use_sudo
        self.sudo_user = sudo_user
        self.console: IConsole = None  # Will be set DI Container

    def set_console(self,
                    console: IConsole) -> None:
        self.console = console

    def _build_command(self,
                       command: Union[str, List[str]]) -> List[str]:
        if isinstance(command, str):
            command_parts = command.split()
        else:
            command_parts = command

        if self.use_sudo:
            sudo_command = ["sudo"]
            if self.sudo_user:
                sudo_command.extend(["-u", self.sudo_user])
            return sudo_command + command_parts
        return command_parts

    def execute(self,
                command: Union[str, List[str]],
                timeout: Optional[float] = None,
                env: Optional[Dict[str, str]] = None,
                cwd: Optional[str] = None,
                shell: bool = False) -> CommandResult:
        start_time = time.time()

        try:
            command_parts = self._build_command(command)
            if self.console:
                self.console.debug(
                    f"Executing command: {' '.join(command_parts)}")

            process = subprocess.Popen(
                command_parts,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=cwd,
                env=env,
                shell=shell
            )

            try:
                stdout, stderr = process.communicate(timeout=timeout)
                execution_time = time.time() - start_time

                if process.returncode == 0:
                    status = CommandStatus.SUCCESS
                    if self.console:
                        self.console.debug(
                            f"Command {' '.join(command_parts)} "
                            f"completed successfully in {execution_time:.2f}s")
                else:
                    status = CommandStatus.FAILED
                    if self.console:
                        self.console.error(
                            f"Command {' '.join(command_parts)} "
                            f"failed with return code {process.returncode}")

                return CommandResult(
                    status=status,
                    return_code=process.returncode,
                    stdout=stdout,
                    stderr=stderr,
                    command=" ".join(command_parts),
                    execution_time=execution_time,
                    error=None if status == CommandStatus.SUCCESS else stderr
                )

            except subprocess.TimeoutExpired:
                process.kill()
                execution_time = time.time() - start_time

                if self.console:
                    self.console.error(
                        f"Command {' '.join(command_parts)} "
                        f"timed out after {timeout}s")

                return CommandResult(
                    status=CommandStatus.TIMEOUT,
                    return_code=-1,
                    stdout="",
                    stderr="",
                    command=" ".join(command_parts),
                    execution_time=execution_time,
                    error="Command timed out"
                )
            
        except Exception as e:
            execution_time = time.time() - start_time

            if self.console:
                self.console.error(
                    f"Command {' '.join(command_parts)} "
                    f"failed with error: {str(e)}")

            return CommandResult(
                status=CommandStatus.FAILED,
                return_code=-1,
                stdout="",
                stderr=str(e),
                command=" ".join(command_parts),
                execution_time=execution_time,
                error=str(e)
            )

    def execute_sudo(self,
                     command: Union[str, List[str]],
                     sudo_user: Optional[str] = None,
                     **kwargs) -> CommandResult:
        original_sudo = self.use_sudo
        original_user = self.sudo_user

        try:
            self.use_sudo = True
            self.sudo_user = sudo_user
            return self.execute(command, **kwargs)
        finally:
            self.use_sudo = original_sudo
            self.sudo_user = original_user
