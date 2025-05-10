import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from src.commands.ls_command import LsCommand
from src.file_system import FileSystem


class TestLsCommand:
    @pytest.fixture
    def ls_command(self):
        file_system = MagicMock(spec=FileSystem)
        command = LsCommand(file_system)
        return command

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary dir with test content"""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(os.path.join(tmpdirname, "file1.txt"), "w") as f:
                f.write("file 1 content")
            os.mkdir(os.path.join(tmpdirname, "dir1"))
            with open(os.path.join(tmpdirname, "file2.txt"), "w") as f:
                f.write("file 2 content")
            yield tmpdirname

    @pytest.fixture
    def temp_file(self):
        """Create a temporary file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("some content")
            return f.name

    def test_ls_current_directory(self, ls_command, capsys, temp_dir):
        """Test ls without args (cur dir)"""
        ls_command.file_system.get_current_dir.return_value = temp_dir

        with patch("os.listdir", return_value=["file1.txt", "dir1", "file2.txt"]):
            result = ls_command.execute([])
        captured = capsys.readouterr()

        assert result == 0
        assert "file1.txt" in captured.out
        assert "file2.txt" in captured.out
        assert "dir1" in captured.out

    def test_ls_nonexistent_path(self, ls_command, capsys):
        """Test ls with incorrect path"""
        ls_command.file_system.resolve.return_value = "/non/existing/path"

        with patch("os.path.exists", return_value=False):
            result = ls_command.execute(["/non/existing/path"])
        captured = capsys.readouterr()

        assert result == 1
        assert "No such file or directory" in captured.err

    def test_ls_directory(self, ls_command, capsys, temp_dir):
        """Test ls for given dir"""
        ls_command.file_system.resolve.return_value = temp_dir

        with patch("os.path.isdir", return_value=True), patch("os.listdir", return_value=["file1.txt", "dir1"]):
            result = ls_command.execute([temp_dir])
        captured = capsys.readouterr()

        assert result == 0
        assert "file1.txt" in captured.out
        assert "dir1" in captured.out

    def test_ls_file(self, ls_command, capsys, temp_file):
        """Test ls for a single file"""
        ls_command.file_system.resolve.return_value = temp_file

        with patch("os.path.isdir", return_value=False):
            result = ls_command.execute([temp_file])
        captured = capsys.readouterr()

        assert result == 0
        assert temp_file in captured.out

    def test_ls_multiple_arguments(self, ls_command, capsys):
        """Test ls with multiple files"""
        result = ls_command.execute(["/tmp/path1/", "/tmp/path2"])
        captured = capsys.readouterr()

        assert result == 1
        assert "support only 1 file" in captured.err
