import pytest
import os
from src.commands.pwd_command import PwdCommand
from src.file_system import FileSystem


class TestPwdCommand:
    @pytest.fixture
    def file_system(self):
        return FileSystem()

    @pytest.fixture
    def pwd_command(self, file_system):
        return PwdCommand(file_system)

    def test_pwd_basic(self, pwd_command, capsys):
        """Test pwd command basic functionality"""
        result = pwd_command.execute([])
        captured = capsys.readouterr()

        assert result == 0
        assert captured.out == os.getcwd() + "\n"

    def test_pwd_with_args(self, pwd_command, capsys):
        """Test pwd command with arguments (should ignore them)"""
        result = pwd_command.execute(["some", "args"])
        captured = capsys.readouterr()

        assert result == 0
        assert captured.out == os.getcwd() + "\n"

    def test_pwd_in_different_directory(
        self, file_system, pwd_command, capsys, tmp_path
    ):
        """Test pwd command in a different directory"""
        original_dir = os.getcwd()
        try:
            file_system.set_current_dir(tmp_path)
            result = pwd_command.execute([])
            captured = capsys.readouterr()

            assert result == 0
            assert captured.out == str(tmp_path) + "\n"
        finally:
            file_system.set_current_dir(original_dir)
