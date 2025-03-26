import pytest
from unittest.mock import MagicMock, patch
from io import StringIO

from src.cli_engine import CliEngine
from src.commands import commands


@pytest.fixture
def cli_engine():
    engine = CliEngine()
    # Setup basic commands for testing
    commands.commands = {
        "echo": MagicMock(),
        "wc": MagicMock(),
        "cat": MagicMock(),
    }
    return engine


def test_single_command_no_pipe(cli_engine):
    """Test single command execution (no piping)"""
    commands.commands["echo"].execute.return_value = "hello"

    with patch('sys.stdout', new=StringIO()) as fake_out:
        return_code = cli_engine._CliEngine__execute_piped_commands([["echo", "hello"]])
        assert return_code == 0
        assert fake_out.getvalue().strip() == "hello"


def test_piped_commands_basic(cli_engine):
    """Test basic pipe functionality"""
    # Setup command behaviors
    commands.commands["echo"].execute.return_value = "hello world"
    commands.commands["wc"].execute_with_input.return_value = "1 2 12"

    return_code = cli_engine._CliEngine__execute_piped_commands([
        ["echo", "hello world"],
        ["wc"]
    ])

    assert return_code == 0
    commands.commands["echo"].execute.assert_called_once_with(["hello world"])
    commands.commands["wc"].execute_with_input.assert_called_once_with([], "hello world")


def test_piped_commands_three_commands(cli_engine):
    """Test pipe with three commands"""
    commands.commands["echo"].execute.return_value = "hello"
    commands.commands["cat"].execute_with_input.return_value = "hello"
    commands.commands["wc"].execute_with_input.return_value = "1 1 6"

    return_code = cli_engine._CliEngine__execute_piped_commands([
        ["echo", "hello"],
        ["cat"],
        ["wc"]
    ])

    assert return_code == 0
    commands.commands["echo"].execute.assert_called_once_with(["hello"])
    commands.commands["cat"].execute_with_input.assert_called_once_with([], "hello")
    commands.commands["wc"].execute_with_input.assert_called_once_with([], "hello")



def test_piped_commands_no_input_handling(cli_engine):
    """Test pipe where middle command doesn't handle input"""
    commands.commands["echo"].execute.return_value = "hello"
    commands.commands["wc"].execute.return_value = "default output"

    # Remove execute_with_input to test default behavior
    del commands.commands["wc"].execute_with_input

    return_code = cli_engine._CliEngine__execute_piped_commands([
        ["echo", "hello"],
        ["wc"]
    ])

    assert return_code == 0
    commands.commands["echo"].execute.assert_called_once_with(["hello"])
    commands.commands["wc"].execute.assert_called_once_with([])


def test_empty_pipe(cli_engine):
    """Test empty command list"""
    return_code = cli_engine._CliEngine__execute_piped_commands([])
    assert return_code == 0


def test_piped_commands_with_empty_command(cli_engine):
    """Test pipe with empty command in middle"""
    commands.commands["echo"].execute.return_value = "hello"
    commands.commands["wc"].execute_with_input.return_value = "1 1 6"

    return_code = cli_engine._CliEngine__execute_piped_commands([
        ["echo", "hello"],
        [],
        ["wc"]
    ])

    assert return_code == 0
    commands.commands["echo"].execute.assert_called_once_with(["hello"])
    commands.commands["wc"].execute_with_input.assert_called_once_with([], "hello")