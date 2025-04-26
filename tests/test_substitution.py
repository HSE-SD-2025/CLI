from unittest.mock import patch

import pytest

from src.cli_engine import CliEngine
from src.commands.echo_command import EchoCommand


class TestCliEngineEnv:
    def test_env_substitution_with_assignment(self):
        """Test environment variable substitution with assignment"""
        cli = CliEngine()
        cli._CliEngine__parse_command("TEST_VAR=hello")
        assert cli.env["TEST_VAR"] == "hello"

    def test_env_substitution_with_empty_assignment(self):
        """Test that empty assignment raises an error"""
        cli = CliEngine()
        with pytest.raises(Exception):
            cli._CliEngine__parse_command("=value")
        with pytest.raises(Exception):
            cli._CliEngine__parse_command("VARNAME=")

class TestCliEngineSubstitution:
    @pytest.fixture
    def cli(self):
        return CliEngine()

    def test_env_substitution_with_assignment(self, cli):
        """Test environment variable substitution with assignment"""
        with pytest.raises(Exception):
            cli._CliEngine__parse_command("=value")
        with pytest.raises(Exception):
            cli._CliEngine__parse_command("VARNAME=")

    def test_echo_with_multiple_vars(self, cli, capfd):
        """Test echo with multiple environment variables"""
        cli.env["FIRST"] = "hello"
        cli.env["SECOND"] = "world"

        parsed_commands = cli._CliEngine__parse_commands('echo $FIRST $SECOND')
        return_code = cli._CliEngine__execute_piped_commands(parsed_commands)
        captured = capfd.readouterr()

        assert return_code == 0
        assert captured.out == "hello world 0"

    def test_echo_with_unset_vars(self, cli, capfd):
        """Test echo with unset environment variables"""
        cli.env["SET_VAR"] = "hello"
        parsed_commands = cli._CliEngine__parse_commands('echo $SET_VAR $UNSET2')
        return_code = cli._CliEngine__execute_piped_commands(parsed_commands)
        captured = capfd.readouterr()
        assert return_code == 0
        assert captured.out == "hello 0"

    def test_echo_with_mixed_vars(self, cli, capfd):
        """Test echo with mix of set and unset variables"""
        cli.env["SET_VAR"] = "hello"
        parsed_commands = cli._CliEngine__parse_commands('echo $UNSET1 $UNSET2')
        return_code = cli._CliEngine__execute_piped_commands(parsed_commands)
        captured = capfd.readouterr()
        assert return_code == 0
        assert captured.out == "0"
