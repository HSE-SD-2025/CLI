import os
import tempfile

import pytest

from src.commands.cat_command import CatCommand


class TestCatCommand:
    @pytest.fixture
    def cat_command(self):
        return CatCommand()

    @pytest.fixture
    def temp_file(self):
        """Create a temporary file with test content"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("line 1\nline 2\nline 3")
            return f.name

    @pytest.fixture
    def temp_file_second(self):
        """Create a temporary file with test content"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("line 1\nline 2\nline 3")
            return f.name

    def test_cat_empty_args(self, cat_command, capsys, monkeypatch):
        """Test cat command with no arguments (should read from stdin)"""
        input_text = "test line 1\ntest line 2"
        monkeypatch.setattr('sys.stdin', iter(input_text.split('\n')))

        result = cat_command.execute([])
        captured = capsys.readouterr()

        assert result == 0
        assert captured.out == input_text + "\n"

    def test_cat_single_file(self, cat_command, capsys, temp_file):
        """Test cat command with a single file"""
        result = cat_command.execute([temp_file])
        captured = capsys.readouterr()

        assert result == 0
        assert captured.out == "line 1\nline 2\nline 3"

    def test_cat_multiple_files(self, temp_file, temp_file_second, cat_command, capsys):
        """Test cat command with multiple files"""

        result = cat_command.execute([temp_file,temp_file_second])
        captured = capsys.readouterr()

        assert result == 0
        assert captured.out == "line 1\nline 2\nline 3\nline 1\nline 2\nline 3\n"



def test_cat_nonexistent_file(cat_command, capsys):
    """Test cat command with a nonexistent file"""
    result = cat_command.execute(["nonexistent.txt"])
    captured = capsys.readouterr()

    assert result == 1
    assert "No such file or directory" in captured.err


def test_cat_permission_error(cat_command, capsys):
    """Test cat command with a file that has no read permissions"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test content")
        os.chmod(f.name, 0o000)

        result = cat_command.execute([f.name])
        captured = capsys.readouterr()

        assert result == 1
        assert "Permission denied" in captured.err

        os.chmod(f.name, 0o644)
        os.unlink(f.name)
