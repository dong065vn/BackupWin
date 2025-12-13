"""Backup service for Windows files"""
import shutil
import hashlib
from pathlib import Path
from typing import List, Optional, Dict, Callable
from datetime import datetime
from app.core.logger import app_logger
from app.core.config import settings


class BackupService:
    """Service for backing up files"""

    def __init__(self, backup_base_path: Optional[str] = None):
        self.logger = app_logger
        self.backup_base_path = Path(backup_base_path or settings.DEFAULT_BACKUP_PATH)
        self.backup_base_path.mkdir(parents=True, exist_ok=True)

    def backup_file(self, source_file: str, destination_folder: Optional[str] = None,
                    preserve_structure: bool = True, create_checksum: bool = True) -> Dict:
        """Backup a single file"""
        try:
            src = Path(source_file)
            if not src.exists() or not src.is_file():
                raise FileNotFoundError(f"Source not found: {source_file}")

            dest_base = Path(destination_folder) if destination_folder else self.backup_base_path / datetime.now().strftime("%Y%m%d_%H%M%S")
            dest_folder = dest_base / src.parent.name if preserve_structure else dest_base
            dest_folder.mkdir(parents=True, exist_ok=True)
            dest_file = dest_folder / src.name

            src_checksum = self._calculate_checksum(src) if create_checksum else None
            shutil.copy2(src, dest_file)

            if create_checksum and src_checksum != self._calculate_checksum(dest_file):
                raise Exception("Checksum mismatch!")

            stats = dest_file.stat()
            return {"success": True, "source": str(src.absolute()), "destination": str(dest_file.absolute()),
                    "size_bytes": stats.st_size, "size_mb": round(stats.st_size / 1048576, 2),
                    "checksum": src_checksum, "backed_up_at": datetime.now().isoformat(sep=' ')}
        except Exception as e:
            self.logger.error(f"Backup error {source_file}: {e}")
            return {"success": False, "source": source_file, "error": str(e)}

    def backup_files(self, source_files: List[str], destination_folder: Optional[str] = None,
                     preserve_structure: bool = True, progress_callback: Optional[Callable] = None) -> Dict:
        """Backup multiple files"""
        results = {"total_files": len(source_files), "successful": 0, "failed": 0, "total_size_mb": 0.0, "files": [], "errors": []}
        dest = destination_folder or str(self.backup_base_path / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

        for i, f in enumerate(source_files, 1):
            result = self.backup_file(f, dest, preserve_structure)
            if result["success"]:
                results["successful"] += 1
                results["total_size_mb"] += result["size_mb"]
                results["files"].append(result)
            else:
                results["failed"] += 1
                results["errors"].append(result)
            if progress_callback:
                progress_callback(i, len(source_files), f)

        results["total_size_mb"] = round(results["total_size_mb"], 2)
        return results

    def backup_folder(self, source_folder: str, destination_folder: Optional[str] = None,
                      file_extensions: Optional[List[str]] = None, exclude_patterns: Optional[List[str]] = None,
                      progress_callback: Optional[Callable] = None) -> Dict:
        """Backup entire folder"""
        try:
            src = Path(source_folder)
            if not src.exists() or not src.is_dir():
                raise FileNotFoundError(f"Folder not found: {source_folder}")

            files = [str(f.absolute()) for f in src.rglob("*") if f.is_file()
                     and (not file_extensions or any(f.name.endswith(ext) for ext in file_extensions))
                     and (not exclude_patterns or not any(f.match(p) for p in exclude_patterns))]

            return self.backup_files(files, destination_folder, True, progress_callback)
        except Exception as e:
            self.logger.error(f"Folder backup error: {e}")
            return {"success": False, "source": source_folder, "error": str(e)}

    def restore_file(self, backup_file: str, destination: str, verify_checksum: bool = True) -> Dict:
        """Restore a file from backup"""
        try:
            src = Path(backup_file)
            if not src.exists():
                raise FileNotFoundError(f"Backup not found: {backup_file}")

            dest = Path(destination)
            dest.parent.mkdir(parents=True, exist_ok=True)
            checksum = self._calculate_checksum(src) if verify_checksum else None
            shutil.copy2(src, dest)

            if verify_checksum and checksum != self._calculate_checksum(dest):
                raise Exception("Checksum mismatch!")

            return {"success": True, "backup_file": str(src.absolute()), "destination": str(dest.absolute()),
                    "checksum": checksum, "restored_at": datetime.now().isoformat(sep=' ')}
        except Exception as e:
            self.logger.error(f"Restore error: {e}")
            return {"success": False, "backup_file": backup_file, "error": str(e)}

    def list_backups(self, backup_date: Optional[str] = None) -> List[Dict]:
        """List available backups"""
        try:
            backups = []
            for folder in self.backup_base_path.iterdir():
                if not folder.is_dir() or (backup_date and not folder.name.startswith(backup_date)):
                    continue
                files = list(folder.rglob("*"))
                size = sum(f.stat().st_size for f in files if f.is_file())
                backups.append({"path": str(folder.absolute()), "name": folder.name,
                               "file_count": sum(1 for f in files if f.is_file()),
                               "size_bytes": size, "size_mb": round(size / 1048576, 2),
                               "created": datetime.fromtimestamp(folder.stat().st_ctime).isoformat(sep=' ')})
            return sorted(backups, key=lambda x: x["created"], reverse=True)
        except Exception as e:
            self.logger.error(f"List backups error: {e}")
            return []

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate MD5 checksum"""
        h = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def delete_backup(self, backup_path: str) -> Dict:
        """Delete a backup folder"""
        try:
            folder = Path(backup_path)
            if not folder.exists():
                raise FileNotFoundError(f"Not found: {backup_path}")
            if self.backup_base_path not in folder.parents:
                raise ValueError("Cannot delete outside backup directory")
            shutil.rmtree(folder)
            return {"success": True, "deleted_path": backup_path, "deleted_at": datetime.now().isoformat(sep=' ')}
        except Exception as e:
            self.logger.error(f"Delete error: {e}")
            return {"success": False, "path": backup_path, "error": str(e)}
