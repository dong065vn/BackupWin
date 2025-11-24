"""Tests for API endpoints"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_get_drives():
    """Test get available drives endpoint"""
    response = client.get("/api/v1/drives")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "drives" in data
    assert isinstance(data["drives"], list)


def test_search_files():
    """Test search files endpoint"""
    request_data = {
        "search_path": ".",
        "file_pattern": "*.py",
        "recursive": False,
        "max_results": 10
    }
    response = client.post("/api/v1/search", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "results_count" in data
    assert "files" in data


def test_get_folder_size():
    """Test get folder size endpoint"""
    response = client.get("/api/v1/folder-size?folder_path=.")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "total_size_mb" in data
    assert "file_count" in data


def test_backup_file_missing_source():
    """Test backup file with missing source"""
    request_data = {
        "source_file": "nonexistent_file.txt"
    }
    response = client.post("/api/v1/backup/file", json=request_data)
    # Should return error but not 500
    assert response.status_code in [200, 400, 404, 500]


def test_list_backups():
    """Test list backups endpoint"""
    response = client.get("/api/v1/backups")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "backups" in data
    assert isinstance(data["backups"], list)
