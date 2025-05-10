import pytest
from unittest.mock import MagicMock, patch
from io import StringIO

from src.cli_engine import CliEngine
from src.commands import commands

@pytest.fixture
def cli_engine_with_mocks():
    engine = CliEngine()
    # Setup basic commands for testing
    mock_echo_class = MagicMock()
    mock_echo_instance = MagicMock()
    mock_echo_class.return_value = mock_echo_instance

    mock_wc_class = MagicMock()
    mock_wc_instance = MagicMock()
    mock_wc_class.return_value = mock_wc_instance

    mock_cat_class = MagicMock()
    mock_cat_instance = MagicMock()
    mock_cat_class.return_value = mock_cat_instance


    commands.commands = {
        "echo": mock_echo_class,
        "wc": mock_wc_class,
        "cat": mock_cat_class,
    }
    return engine, mock_echo_instance, mock_wc_instance, mock_cat_instance


def test_single_command_no_pipe(cli_engine_with_mocks):
    """Test single command execution (no piping)"""
    cli_engine, mock_echo, _, _ = cli_engine_with_mocks
    mock_echo.execute.return_value = "hello"
    with patch('sys.stdout', new=StringIO()) as fake_out:
        return_code = cli_engine._CliEngine__execute_piped_commands([["echo", "hello"]])
        assert return_code == 0
        assert fake_out.getvalue().strip() == "hello"


def test_piped_commands_basic(cli_engine_with_mocks):
    """Test basic pipe functionality"""
    # Setup command behaviors
    cli_engine, mock_echo, mock_wc, _ = cli_engine_with_mocks
    mock_echo.execute.return_value = "hello world"
    mock_wc.execute_with_input.return_value = "1 2 12"

    return_code = cli_engine._CliEngine__execute_piped_commands([
        ["echo", "hello world"],
        ["wc"]
    ])

    assert return_code == 0
    mock_echo.execute.assert_called_once_with(["hello world"])
    mock_wc.execute_with_input.assert_called_once_with([], "hello world")


def test_piped_commands_three_commands(cli_engine_with_mocks):
    """Test pipe with three commands"""
    cli_engine, mock_echo, mock_wc, mock_cat = cli_engine_with_mocks
    mock_echo.execute.return_value = "hello"
    mock_cat.execute_with_input.return_value = "hello"
    mock_wc.execute_with_input.return_value = "1 1 6"

    return_code = cli_engine._CliEngine__execute_piped_commands([
        ["echo", "hello"],
        ["cat"],
        ["wc"]
    ])

    assert return_code == 0
    mock_echo.execute.assert_called_once_with(["hello"])
    mock_cat.execute_with_input.assert_called_once_with([], "hello")
    mock_wc.execute_with_input.assert_called_once_with([], "hello")



def test_piped_commands_no_input_handling(cli_engine_with_mocks):
    """Test pipe where middle command doesn't handle input"""
    cli_engine, mock_echo, mock_wc, _ = cli_engine_with_mocks
    mock_echo.execute.return_value = "hello"
    mock_wc.execute.return_value = "default output"

    # Remove execute_with_input to test default behavior
    del mock_wc.execute_with_input

    return_code = cli_engine._CliEngine__execute_piped_commands([
        ["echo", "hello"],
        ["wc"]
    ])

    assert return_code == 0
    mock_echo.execute.assert_called_once_with(["hello"])
    mock_wc.execute.assert_called_once_with([])


def test_empty_pipe(cli_engine_with_mocks):
    """Test empty command list"""
    cli_engine, _, _, _ = cli_engine_with_mocks
    return_code = cli_engine._CliEngine__execute_piped_commands([])
    assert return_code == 0


def test_piped_commands_with_empty_command(cli_engine_with_mocks):
    """Test pipe with empty command in middle"""
    cli_engine, mock_echo, mock_wc, _ = cli_engine_with_mocks
    mock_echo.execute.return_value = "hello"
    mock_wc.execute_with_input.return_value = "1 1 6"

    return_code = cli_engine._CliEngine__execute_piped_commands([
        ["echo", "hello"],
        [],
        ["wc"]
    ])

    assert return_code == 0
    mock_echo.execute.assert_called_once_with(["hello"])
    mock_wc.execute_with_input.assert_called_once_with([], "hello")