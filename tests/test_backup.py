"""Tests for backup service"""
import pytest
import tempfile
import shutil
from pathlib import Path
from app.services.backup import BackupService


@pytest.fixture
def backup_service():
    """Create backup service with temporary directory"""
    temp_dir = tempfile.mkdtemp()
    service = BackupService(backup_base_path=temp_dir)
    yield service
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def test_file():
    """Create a temporary test file"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    temp_file.write("Test content for backup")
    temp_file.close()
    yield temp_file.name
    # Cleanup
    Path(temp_file.name).unlink(missing_ok=True)


def test_backup_file(backup_service, test_file):
    """Test backing up a single file"""
    result = backup_service.backup_file(
        source_file=test_file,
        create_checksum=True
    )

    assert result["success"] is True
    assert "source" in result
    assert "destination" in result
    assert "checksum" in result
    assert Path(result["destination"]).exists()


def test_backup_file_nonexistent(backup_service):
    """Test backing up non-existent file"""
    result = backup_service.backup_file(
        source_file="nonexistent_file.txt"
    )

    assert result["success"] is False
    assert "error" in result


def test_backup_multiple_files(backup_service, test_file):
    """Test backing up multiple files"""
    # Create another test file
    temp_file2 = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    temp_file2.write("Second test file")
    temp_file2.close()

    try:
        result = backup_service.backup_files(
            source_files=[test_file, temp_file2.name]
        )

        assert "total_files" in result
        assert result["total_files"] == 2
        assert result["successful"] >= 0
        assert result["failed"] >= 0

    finally:
        Path(temp_file2.name).unlink(missing_ok=True)


def test_calculate_checksum(backup_service, test_file):
    """Test checksum calculation"""
    checksum = backup_service._calculate_checksum(Path(test_file))
    assert isinstance(checksum, str)
    assert len(checksum) > 0

    # Same file should have same checksum
    checksum2 = backup_service._calculate_checksum(Path(test_file))
    assert checksum == checksum2


def test_list_backups(backup_service, test_file):
    """Test listing backups"""
    # Create a backup first
    backup_service.backup_file(source_file=test_file)

    # List backups
    backups = backup_service.list_backups()
    assert isinstance(backups, list)
    assert len(backups) > 0


def test_restore_file(backup_service, test_file):
    """Test restoring a file"""
    # Backup the file first
    backup_result = backup_service.backup_file(source_file=test_file)
    assert backup_result["success"] is True

    # Create temporary destination for restoration
    temp_restore = tempfile.mktemp(suffix='.txt')

    try:
        # Restore the file
        restore_result = backup_service.restore_file(
            backup_file=backup_result["destination"],
            destination=temp_restore,
            verify_checksum=True
        )

        assert restore_result["success"] is True
        assert Path(temp_restore).exists()

        # Verify content
        with open(test_file, 'r') as f1, open(temp_restore, 'r') as f2:
            assert f1.read() == f2.read()

    finally:
        Path(temp_restore).unlink(missing_ok=True)
