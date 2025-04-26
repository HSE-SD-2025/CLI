import os
import tempfile

import pytest

from src.commands.wc_command import WcCommand


class TestWcCommand:
    @pytest.fixture
    def wc_command(self):
        return WcCommand()

    @pytest.fixture
    def temp_file(self):
        """Create a temporary file with test content"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(f"line 1{os.linesep}line 2{os.linesep}line 3{os.linesep}")
            return f.name

    def test_wc_multiple_files(self, wc_command, capsys):
        """Test wc command with multiple files"""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False
        ) as f1, tempfile.NamedTemporaryFile(mode="w", delete=False) as f2:
            f1.write("file1 content")
            f2.write("file2 content")

            result = wc_command.execute([f1.name, f2.name])
            captured = capsys.readouterr()

            assert result == 0
            assert "total" in captured.out
            assert f1.name in captured.out
            assert f2.name in captured.out

    def test_wc_nonexistent_file(self, wc_command, capsys):
        """Test wc command with a nonexistent file"""
        result = wc_command.execute(["nonexistent.txt"])
        captured = capsys.readouterr()

        assert result == 1
        assert "No such file or directory" in captured.out

    def test_wc_empty_file(self, wc_command, capsys):
        """Test wc command with an empty file"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            result = wc_command.execute([f.name])
            captured = capsys.readouterr()

            assert result == 0
            assert "0        0       0" in captured.out
            assert f.name in captured.out

    def test_wc_file_with_special_chars(self, wc_command, capsys):
        """Test wc command with a file containing special characters"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(f"line 1{os.linesep}line "
                    f"2\twith tab{os.linesep}line 3 with spaces")
            result = wc_command.execute([f.name])
            captured = capsys.readouterr()

            assert result == 0
            assert f.name in captured.out
