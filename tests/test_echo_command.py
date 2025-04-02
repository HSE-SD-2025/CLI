import pytest
from io import StringIO
import sys
from src.commands.echo_command import EchoCommand

class TestEchoCommand:
    @pytest.fixture
    def echo_command(self):
        return EchoCommand()

    def test_echo_empty_args(self, echo_command, capsys):
        """Test echo command with no arguments"""
        result = echo_command.execute([])
        captured = capsys.readouterr()
        assert result == 0
        assert captured.out == "\n"

    def test_echo_single_arg(self, echo_command, capsys):
        """Test echo command with a single argument"""
        result = echo_command.execute(["hello"])
        captured = capsys.readouterr()
        assert result == 0
        assert captured.out == "hello\n"

    def test_echo_multiple_args(self, echo_command, capsys):
        """Test echo command with multiple arguments"""
        result = echo_command.execute(["hello", "world", "test"])
        captured = capsys.readouterr()
        assert result == 0
        assert captured.out == "hello world test\n"

    def test_echo_special_chars(self, echo_command, capsys):
        """Test echo command with special characters"""
        result = echo_command.execute(["hello\n", "world\t", "test!"])
        captured = capsys.readouterr()
        assert result == 0
        assert captured.out == "hello\n world\t test!\n"