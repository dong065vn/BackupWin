"""Backup service for Windows files"""
import os
import shutil
import hashlib
from pathlib import Path
from typing import List, Optional, Dict, Callable
from datetime import datetime
from app.core.logger import app_logger
from app.core.config import settings


class BackupService:
    """Service for backing up files to local or cloud storage"""

    def __init__(self, backup_base_path: Optional[str] = None):
        self.logger = app_logger
        self.backup_base_path = Path(backup_base_path or settings.DEFAULT_BACKUP_PATH)
        self._ensure_backup_directory()

    def _ensure_backup_directory(self):
        """Create backup directory if it doesn't exist"""
        try:
            self.backup_base_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Backup directory ready: {self.backup_base_path}")
        except Exception as e:
            self.logger.error(f"Error creating backup directory: {e}")
            raise

    def backup_file(
        self,
        source_file: str,
        destination_folder: Optional[str] = None,
        preserve_structure: bool = True,
        create_checksum: bool = True
    ) -> Dict:
        """
        Backup a single file

        Args:
            source_file: Path to source file
            destination_folder: Custom destination folder (optional)
            preserve_structure: Preserve original folder structure
            create_checksum: Create MD5 checksum for verification

        Returns:
            Dict with backup information
        """
        try:
            source_path = Path(source_file)
            if not source_path.exists():
                raise FileNotFoundError(f"Source file not found: {source_file}")

            if not source_path.is_file():
                raise ValueError(f"Source is not a file: {source_file}")

            # Determine destination path
            if destination_folder:
                dest_base = Path(destination_folder)
                dest_base.mkdir(parents=True, exist_ok=True)
            else:
                # Create timestamped backup folder
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                dest_base = self.backup_base_path / timestamp

            if preserve_structure:
                # Preserve directory structure
                relative_path = source_path.parent
                dest_folder = dest_base / relative_path.name
            else:
                dest_folder = dest_base

            dest_folder.mkdir(parents=True, exist_ok=True)
            dest_file = dest_folder / source_path.name

            # Calculate source checksum if requested
            source_checksum = None
            if create_checksum:
                source_checksum = self._calculate_checksum(source_path)

            # Copy file
            self.logger.info(f"Backing up: {source_file} -> {dest_file}")
            shutil.copy2(source_path, dest_file)

            # Verify checksum
            dest_checksum = None
            if create_checksum:
                dest_checksum = self._calculate_checksum(dest_file)
                if source_checksum != dest_checksum:
                    raise Exception("Checksum mismatch! Backup may be corrupted.")

            # Get file stats
            stats = dest_file.stat()

            return {
                "success": True,
                "source": str(source_path.absolute()),
                "destination": str(dest_file.absolute()),
                "size_bytes": stats.st_size,
                "size_mb": round(stats.st_size / (1024 * 1024), 2),
                "checksum": dest_checksum,
                "backed_up_at": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error backing up file {source_file}: {e}")
            return {
                "success": False,
                "source": source_file,
                "error": str(e)
            }

    def backup_files(
        self,
        source_files: List[str],
        destination_folder: Optional[str] = None,
        preserve_structure: bool = True,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Backup multiple files

        Args:
            source_files: List of source file paths
            destination_folder: Custom destination folder (optional)
            preserve_structure: Preserve original folder structure
            progress_callback: Callback function for progress updates

        Returns:
            Dict with backup summary
        """
        results = {
            "total_files": len(source_files),
            "successful": 0,
            "failed": 0,
            "total_size_mb": 0.0,
            "files": [],
            "errors": []
        }

        # Create single timestamped backup folder for batch
        if not destination_folder:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            destination_folder = str(self.backup_base_path / f"backup_{timestamp}")

        for idx, source_file in enumerate(source_files, 1):
            result = self.backup_file(
                source_file=source_file,
                destination_folder=destination_folder,
                preserve_structure=preserve_structure
            )

            if result["success"]:
                results["successful"] += 1
                results["total_size_mb"] += result["size_mb"]
                results["files"].append(result)
            else:
                results["failed"] += 1
                results["errors"].append(result)

            # Call progress callback if provided
            if progress_callback:
                progress_callback(idx, len(source_files), source_file)

            self.logger.info(f"Progress: {idx}/{len(source_files)} files processed")

        results["total_size_mb"] = round(results["total_size_mb"], 2)
        self.logger.info(f"Backup completed: {results['successful']} successful, {results['failed']} failed")

        return results

    def backup_folder(
        self,
        source_folder: str,
        destination_folder: Optional[str] = None,
        file_extensions: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Backup entire folder

        Args:
            source_folder: Path to source folder
            destination_folder: Custom destination folder (optional)
            file_extensions: Only backup files with these extensions
            exclude_patterns: Patterns to exclude (e.g., ['*.tmp', '__pycache__'])
            progress_callback: Callback function for progress updates

        Returns:
            Dict with backup summary
        """
        try:
            source_path = Path(source_folder)
            if not source_path.exists():
                raise FileNotFoundError(f"Source folder not found: {source_folder}")

            if not source_path.is_dir():
                raise ValueError(f"Source is not a folder: {source_folder}")

            # Collect files to backup
            files_to_backup = []
            for item in source_path.rglob("*"):
                if not item.is_file():
                    continue

                # Check extension filter
                if file_extensions:
                    if not any(item.name.endswith(ext) for ext in file_extensions):
                        continue

                # Check exclude patterns
                if exclude_patterns:
                    if any(item.match(pattern) for pattern in exclude_patterns):
                        continue

                files_to_backup.append(str(item.absolute()))

            self.logger.info(f"Found {len(files_to_backup)} files to backup in {source_folder}")

            # Backup files
            return self.backup_files(
                source_files=files_to_backup,
                destination_folder=destination_folder,
                preserve_structure=True,
                progress_callback=progress_callback
            )

        except Exception as e:
            self.logger.error(f"Error backing up folder {source_folder}: {e}")
            return {
                "success": False,
                "source": source_folder,
                "error": str(e)
            }

    def restore_file(self, backup_file: str, destination: str, verify_checksum: bool = True) -> Dict:
        """
        Restore a file from backup

        Args:
            backup_file: Path to backup file
            destination: Destination path for restoration
            verify_checksum: Verify file integrity

        Returns:
            Dict with restoration information
        """
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup file not found: {backup_file}")

            dest_path = Path(destination)
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Calculate backup checksum
            backup_checksum = None
            if verify_checksum:
                backup_checksum = self._calculate_checksum(backup_path)

            # Restore file
            self.logger.info(f"Restoring: {backup_file} -> {destination}")
            shutil.copy2(backup_path, dest_path)

            # Verify restored file
            if verify_checksum:
                restored_checksum = self._calculate_checksum(dest_path)
                if backup_checksum != restored_checksum:
                    raise Exception("Checksum mismatch! Restored file may be corrupted.")

            return {
                "success": True,
                "backup_file": str(backup_path.absolute()),
                "destination": str(dest_path.absolute()),
                "checksum": backup_checksum,
                "restored_at": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error restoring file {backup_file}: {e}")
            return {
                "success": False,
                "backup_file": backup_file,
                "error": str(e)
            }

    def list_backups(self, backup_date: Optional[str] = None) -> List[Dict]:
        """
        List available backups

        Args:
            backup_date: Filter by date (format: YYYYMMDD)

        Returns:
            List of backup information
        """
        try:
            backups = []
            for backup_folder in self.backup_base_path.iterdir():
                if not backup_folder.is_dir():
                    continue

                # Filter by date if specified
                if backup_date and not backup_folder.name.startswith(backup_date):
                    continue

                # Get folder stats
                file_count = sum(1 for _ in backup_folder.rglob("*") if _.is_file())
                folder_size = sum(f.stat().st_size for f in backup_folder.rglob("*") if f.is_file())

                backups.append({
                    "path": str(backup_folder.absolute()),
                    "name": backup_folder.name,
                    "file_count": file_count,
                    "size_bytes": folder_size,
                    "size_mb": round(folder_size / (1024 * 1024), 2),
                    "created": datetime.fromtimestamp(backup_folder.stat().st_ctime).isoformat()
                })

            return sorted(backups, key=lambda x: x["created"], reverse=True)

        except Exception as e:
            self.logger.error(f"Error listing backups: {e}")
            return []

    def _calculate_checksum(self, file_path: Path, algorithm: str = "md5") -> str:
        """
        Calculate file checksum

        Args:
            file_path: Path to file
            algorithm: Hash algorithm (md5, sha256)

        Returns:
            Checksum string
        """
        try:
            hash_func = hashlib.new(algorithm)
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating checksum: {e}")
            raise

    def delete_backup(self, backup_path: str) -> Dict:
        """
        Delete a backup folder

        Args:
            backup_path: Path to backup folder

        Returns:
            Dict with deletion status
        """
        try:
            backup_folder = Path(backup_path)
            if not backup_folder.exists():
                raise FileNotFoundError(f"Backup folder not found: {backup_path}")

            # Safety check: ensure it's within backup base path
            if self.backup_base_path not in backup_folder.parents:
                raise ValueError("Cannot delete folder outside backup directory")

            shutil.rmtree(backup_folder)
            self.logger.info(f"Deleted backup: {backup_path}")

            return {
                "success": True,
                "deleted_path": backup_path,
                "deleted_at": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error deleting backup {backup_path}: {e}")
            return {
                "success": False,
                "path": backup_path,
                "error": str(e)
            }
