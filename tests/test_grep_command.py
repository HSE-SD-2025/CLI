import pytest
import tempfile
from src.commands.grep_command import GrepCommand
from src.file_system import FileSystem


class TestGrepCommand:
    @pytest.fixture
    def grep_command(self):
        return GrepCommand(FileSystem())

    @pytest.fixture
    def temp_file(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Hello World\nThis is a test\nAnother line\n")
            return f.name

    def test_basic_search(self, grep_command, capsys, temp_file):
        result = grep_command.execute(["Hello", temp_file])
        captured = capsys.readouterr()
        assert result == 0
        assert "Hello World" in captured.out

    def test_word_boundary(self, grep_command, capsys, temp_file):
        result = grep_command.execute(["-w", "Hello", temp_file])
        captured = capsys.readouterr()
        assert result == 0
        assert "Hello World" in captured.out

        result = grep_command.execute(["-w", "Hell", temp_file])
        captured = capsys.readouterr()
        assert result == 1
        assert captured.out == ""

    def test_case_insensitive(self, grep_command, capsys, temp_file):
        result = grep_command.execute(["-i", "hello", temp_file])
        captured = capsys.readouterr()
        assert result == 0
        assert "Hello World" in captured.out

    def test_after_context(self, grep_command, capsys, temp_file):
        result = grep_command.execute(["-A", "1", "test", temp_file])
        captured = capsys.readouterr()
        assert result == 0
        assert "This is a test" in captured.out
        assert "Another line" in captured.out

    def test_nonexistent_file(self, grep_command, capsys):
        result = grep_command.execute(["pattern", "nonexistent.txt"])
        captured = capsys.readouterr()
        assert result == 1
        assert "No such file or directory" in captured.err

    def test_regex_pattern(self, grep_command, capsys, temp_file):
        result = grep_command.execute(["^Hello", temp_file])
        captured = capsys.readouterr()
        assert result == 0
        assert "Hello World" in captured.out
