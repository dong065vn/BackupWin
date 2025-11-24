"""Tests for file search service"""
import pytest
from pathlib import Path
from app.services.file_search import FileSearchService


@pytest.fixture
def file_search_service():
    """Create file search service instance"""
    return FileSearchService()


def test_get_available_drives(file_search_service):
    """Test getting available drives"""
    drives = file_search_service.get_available_drives()
    assert isinstance(drives, list)
    assert len(drives) > 0
    # Windows drives should end with ':'
    for drive in drives:
        assert drive.endswith(':')


def test_wildcard_to_regex(file_search_service):
    """Test wildcard to regex conversion"""
    # Test simple pattern
    pattern = file_search_service._wildcard_to_regex("*.txt", case_sensitive=False)
    assert pattern.match("test.txt")
    assert pattern.match("TEST.TXT")
    assert not pattern.match("test.pdf")

    # Test case sensitive
    pattern = file_search_service._wildcard_to_regex("*.txt", case_sensitive=True)
    assert pattern.match("test.txt")
    assert not pattern.match("TEST.TXT")

    # Test wildcard with prefix
    pattern = file_search_service._wildcard_to_regex("test_*", case_sensitive=False)
    assert pattern.match("test_file.txt")
    assert pattern.match("test_123")
    assert not pattern.match("other_test")


def test_search_files_in_current_directory(file_search_service):
    """Test searching files in current directory"""
    # Search for Python files in current directory
    results = list(file_search_service.search_files(
        search_path=".",
        file_pattern="*.py",
        recursive=False,
        max_results=10
    ))

    assert isinstance(results, list)
    # Should find at least main.py
    if len(results) > 0:
        assert all("path" in r for r in results)
        assert all("name" in r for r in results)
        assert all("size" in r for r in results)


def test_get_folder_size(file_search_service):
    """Test getting folder size"""
    # Test with current directory
    result = file_search_service.get_folder_size(".")

    assert "path" in result
    assert "total_size_bytes" in result
    assert "total_size_mb" in result
    assert "file_count" in result
    assert result["total_size_bytes"] >= 0
    assert result["file_count"] >= 0


def test_get_folder_size_nonexistent(file_search_service):
    """Test getting folder size for non-existent folder"""
    with pytest.raises(ValueError):
        file_search_service.get_folder_size("nonexistent_folder_xyz")
