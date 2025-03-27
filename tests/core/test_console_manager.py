"""
Tests for ConsoleManager
"""

import pytest
from rich.console import Console
from unittest.mock import patch

from app.core.console_manager import ConsoleManager
from app.core.types.enums import ConsoleLevel


@pytest.fixture
def console_manager():
    """Fixture for creating ConsoleManager instance"""
    return ConsoleManager(app_name="TestApp")


@pytest.fixture
def console_manager_debug():
    """Fixture for creating ConsoleManager instance with debug mode"""
    return ConsoleManager(app_name="TestApp", debug=True)


def test_console_manager_initialization():
    """Test ConsoleManager initialization"""
    manager = ConsoleManager(app_name="TestApp")
    assert manager.app_name == "TestApp"
    assert manager.debug_mode is False
    assert isinstance(manager.console, Console)

    # Test with empty app_name
    manager = ConsoleManager(app_name="")
    assert manager.app_name == "App"


@patch('rich.console.Console.print')
def test_log_without_module_prefix(mock_print, console_manager):
    """Test logging without module prefix"""
    console_manager._log("Test message", ConsoleLevel.INFO)
    mock_print.assert_called_once_with(
        "[white] [TestApp] Test message [/white]"
    )


@patch('rich.console.Console.print')
def test_log_with_module_prefix(mock_print, console_manager):
    """Test logging with module prefix"""
    console_manager._log("Test message", ConsoleLevel.INFO, "test_module")
    mock_print.assert_called_once_with(
        "[white] [TestApp] [test_module] Test message [/white]"
    )


@patch('rich.console.Console.print')
def test_info_logging(mock_print, console_manager):
    """Test info level logging"""
    console_manager.info("Test message")
    mock_print.assert_called_once_with(
        "[white] [TestApp] Test message [/white]"
    )


@patch('rich.console.Console.print')
def test_debug_logging_disabled(mock_print, console_manager):
    """Test debug logging when disabled"""
    console_manager.debug("Test message")
    mock_print.assert_not_called()


@patch('rich.console.Console.print')
def test_debug_logging_enabled(mock_print, console_manager_debug):
    """Test debug logging when enabled"""
    console_manager_debug.debug("Test message")
    mock_print.assert_called_once_with(
        "[blue] [TestApp] Test message [/blue]"
    )


@patch('rich.console.Console.print')
def test_warning_logging(mock_print, console_manager):
    """Test warning level logging"""
    console_manager.warning("Test message")
    mock_print.assert_called_once_with(
        "[yellow] [TestApp] Test message [/yellow]"
    )


@patch('rich.console.Console.print')
def test_error_logging(mock_print, console_manager):
    """Test error level logging"""
    console_manager.error("Test message")
    mock_print.assert_called_once_with(
        "[red] [TestApp] Test message [/red]"
    )


@patch('rich.console.Console.print')
def test_critical_logging(mock_print, console_manager):
    """Test critical level logging"""
    console_manager.critical("Test message")
    mock_print.assert_called_once_with(
        "[bold red] [TestApp] Test message [/bold red]"
    ) 