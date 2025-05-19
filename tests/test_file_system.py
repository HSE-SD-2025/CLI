import pytest
from unittest.mock import patch
from src.file_system import FileSystem


class TestFileSystem:
    @pytest.fixture
    def file_system(self):
        with patch("os.getcwd", return_value="/mock/current/dir"):
            return FileSystem()

    def test_get_current_dir(self, file_system):
        """Test get_current_dir"""
        current_dir = file_system.get_current_dir()
        assert current_dir == "/mock/current/dir"

    def test_resolve_absolute_path(self, file_system):
        """Test resolve for an absolute path"""
        absolute_path = "/absolute/path"
        resolved_path = file_system.resolve(absolute_path)
        assert resolved_path == absolute_path

    def test_resolve_relative_path(self, file_system):
        """Test resolve for a relative path"""
        relative_path = "relative/path"
        resolved_path = file_system.resolve(relative_path)
        assert resolved_path == "/mock/current/dir/relative/path"
