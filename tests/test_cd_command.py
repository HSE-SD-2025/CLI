import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from src.commands.cd_command import CdCommand
from src.file_system import FileSystem


class TestCdCommand:
    @pytest.fixture
    def cd_command(self):
        file_system = MagicMock(spec=FileSystem)
        command = CdCommand(file_system)
        return command

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing"""
        with tempfile.TemporaryDirectory() as tmpdirname:
            yield tmpdirname

    def test_cd_valid_directory(self, cd_command, capsys, temp_dir):
        """Test cd with valid directory"""
        cd_command.file_system.resolve.return_value = temp_dir

        with patch("os.path.isdir", return_value=True):
            result = cd_command.execute([temp_dir])

        assert result == 0
        cd_command.file_system.current_dir = os.path.abspath(temp_dir)

    def test_cd_nonexistent_directory(self, cd_command, capsys):
        """Test cd with non-existent directory"""
        test_path = "/nonexistent/path"
        cd_command.file_system.resolve.return_value = test_path

        with patch("os.path.exists", return_value=False):
            result = cd_command.execute([test_path])
        captured = capsys.readouterr()

        assert result == 1
        assert "No such file or directory" in captured.err

    def test_cd_not_a_directory(self, cd_command, capsys):
        """Test cd with file path (not directory)"""
        test_file = "/some/file.txt"
        cd_command.file_system.resolve.return_value = test_file

        with patch("os.path.exists", return_value=True), \
                patch("os.path.isdir", return_value=False):
            result = cd_command.execute([test_file])
        captured = capsys.readouterr()

        assert result == 1
        assert "Not a directory" in captured.err

    def test_cd_too_many_arguments(self, cd_command, capsys):
        """Test cd with multiple arguments"""
        result = cd_command.execute(["dir1", "dir2"])
        captured = capsys.readouterr()

        assert result == 1
        assert "too many arguments" in captured.err

    def test_cd_relative_path(self, cd_command, capsys, temp_dir):
        """Test cd with relative path"""
        rel_path = "subdir"
        abs_path = os.path.join(temp_dir, rel_path)
        os.mkdir(abs_path)

        cd_command.file_system.resolve.return_value = abs_path
        cd_command.file_system.current_dir = temp_dir

        with patch("os.path.isdir", return_value=True):
            result = cd_command.execute([rel_path])

        assert result == 0
        cd_command.file_system.current_dir = abs_path

    def test_cd_permission_error(self, cd_command, capsys):
        """Test cd with directory that has permission denied"""
        test_dir = "/restricted"
        cd_command.file_system.resolve.return_value = test_dir

        with patch("os.path.exists", return_value=True), \
                patch("os.path.isdir", return_value=True), \
                patch("os.path.abspath", side_effect=PermissionError("Permission denied")):
            result = cd_command.execute([test_dir])
        captured = capsys.readouterr()

        assert result == 1
        assert "Permission denied" in captured.err