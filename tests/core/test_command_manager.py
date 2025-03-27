"""
Tests for CommandManager
"""

import pytest
from unittest.mock import patch, MagicMock, call
import subprocess

from app.core.command_manager import CommandManager
from app.core.types.enums import CommandStatus
from app.core.types.models import CommandResult


@pytest.fixture
def command_manager():
    """Fixture for creating CommandManager instance"""
    return CommandManager()


@pytest.fixture
def command_manager_sudo():
    """Fixture for creating CommandManager instance with sudo"""
    return CommandManager(use_sudo=True, sudo_user="test_user")


@pytest.fixture
def mock_console():
    """Fixture for creating mock console"""
    return MagicMock()


def test_command_manager_initialization():
    """Test CommandManager initialization"""
    manager = CommandManager()
    assert manager.use_sudo is False
    assert manager.sudo_user is None
    assert manager.console is None

    manager = CommandManager(use_sudo=True, sudo_user="test_user")
    assert manager.use_sudo is True
    assert manager.sudo_user == "test_user"
    assert manager.console is None


def test_set_console(command_manager, mock_console):
    """Test setting console"""
    command_manager.set_console(mock_console)
    assert command_manager.console == mock_console


def test_build_command_without_sudo(command_manager):
    """Test building command without sudo"""
    command = "ls -la"
    result = command_manager._build_command(command)
    assert result == ["ls", "-la"]

    command = ["ls", "-la"]
    result = command_manager._build_command(command)
    assert result == ["ls", "-la"]


def test_build_command_with_sudo(command_manager_sudo):
    """Test building command with sudo"""
    command = "ls -la"
    result = command_manager_sudo._build_command(command)
    assert result == ["sudo", "-u", "test_user", "ls", "-la"]

    command = ["ls", "-la"]
    result = command_manager_sudo._build_command(command)
    assert result == ["sudo", "-u", "test_user", "ls", "-la"]


@patch('subprocess.Popen')
def test_execute_success(mock_popen, command_manager, mock_console):
    """Test successful command execution"""
    # Setup mock
    mock_process = MagicMock()
    mock_process.communicate.return_value = ("stdout", "stderr")
    mock_process.returncode = 0
    mock_popen.return_value = mock_process

    # Setup console
    command_manager.set_console(mock_console)

    # Execute command
    result = command_manager.execute("echo test")

    # Verify result
    assert isinstance(result, CommandResult)
    assert result.status == CommandStatus.SUCCESS
    assert result.return_code == 0
    assert result.stdout == "stdout"
    assert result.stderr == "stderr"
    assert result.command == "echo test"
    assert result.execution_time >= 0
    assert result.error is None

    # Verify console calls
    execution_time = result.execution_time
    success_msg = (
        "Command echo test completed successfully "
        f"in {execution_time:.2f}s"
    )
    mock_console.debug.assert_has_calls([
        call("Executing command: echo test"),
        call(success_msg)
    ])


@patch('subprocess.Popen')
def test_execute_failure(mock_popen, command_manager, mock_console):
    """Test failed command execution"""
    # Setup mock
    mock_process = MagicMock()
    mock_process.communicate.return_value = ("", "error message")
    mock_process.returncode = 1
    mock_popen.return_value = mock_process

    # Setup console
    command_manager.set_console(mock_console)

    # Execute command
    result = command_manager.execute("invalid_command")

    # Verify result
    assert isinstance(result, CommandResult)
    assert result.status == CommandStatus.FAILED
    assert result.return_code == 1
    assert result.stdout == ""
    assert result.stderr == "error message"
    assert result.command == "invalid_command"
    assert result.execution_time >= 0
    assert result.error == "error message"

    # Verify console calls
    mock_console.debug.assert_called_with("Executing command: invalid_command")
    mock_console.error.assert_called_once()


@patch('subprocess.Popen')
def test_execute_timeout(mock_popen, command_manager, mock_console):
    """Test command timeout"""
    # Setup mock
    mock_process = MagicMock()
    mock_process.communicate.side_effect = subprocess.TimeoutExpired("sleep 10", 1)
    mock_popen.return_value = mock_process

    # Setup console
    command_manager.set_console(mock_console)

    # Execute command
    result = command_manager.execute("sleep 10", timeout=1)

    # Verify result
    assert isinstance(result, CommandResult)
    assert result.status == CommandStatus.TIMEOUT
    assert result.return_code == -1
    assert result.stdout == ""
    assert result.stderr == ""
    assert result.command == "sleep 10"
    assert result.execution_time >= 0
    assert result.error == "Command timed out"

    # Verify console calls
    mock_console.debug.assert_called_with("Executing command: sleep 10")
    mock_console.error.assert_called_once()


@patch('subprocess.Popen')
def test_execute_sudo(mock_popen, command_manager):
    """Test command execution with sudo"""
    # Setup mock
    mock_process = MagicMock()
    mock_process.communicate.return_value = ("stdout", "stderr")
    mock_process.returncode = 0
    mock_popen.return_value = mock_process

    # Execute command
    result = command_manager.execute_sudo("ls -la", sudo_user="test_user")

    # Verify result
    assert isinstance(result, CommandResult)
    assert result.status == CommandStatus.SUCCESS
    assert result.return_code == 0
    assert result.stdout == "stdout"
    assert result.stderr == "stderr"
    assert result.command == "sudo -u test_user ls -la"
    assert result.execution_time >= 0
    assert result.error is None

    # Verify sudo state was restored
    assert command_manager.use_sudo is False
    assert command_manager.sudo_user is None 