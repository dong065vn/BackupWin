"""File search service for Windows"""
import os
import re
import string
from pathlib import Path
from typing import List, Optional, Dict, Generator
from datetime import datetime
from app.core.logger import app_logger


class FileSearchService:
    """Service for searching files in Windows drives and folders"""

    def __init__(self):
        self.logger = app_logger

    def get_available_drives(self) -> List[str]:
        """Get all available drives on Windows system"""
        try:
            drives = [f"{letter}:" for letter in string.ascii_uppercase if os.path.exists(f"{letter}:")]
            self.logger.info(f"Found {len(drives)} drives: {drives}")
            return drives
        except Exception as e:
            self.logger.error(f"Error getting drives: {e}")
            return []

    def search_files(self, search_path: str, file_pattern: str = "*", file_extension: Optional[str] = None,
                     recursive: bool = True, max_results: Optional[int] = None, case_sensitive: bool = False) -> Generator[Dict, None, None]:
        """Search for files in specified path"""
        try:
            path = Path(search_path)
            if not path.exists():
                self.logger.error(f"Path not found: {search_path}")
                return

            self.logger.info(f"Searching: {search_path}, pattern: {file_pattern}, ext: {file_extension}")
            regex = self._wildcard_to_regex(file_pattern, case_sensitive)
            count = 0

            for item in (path.rglob("*") if recursive else path.glob("*")):
                try:
                    if not item.is_file():
                        continue
                    if file_extension and not item.name.lower().endswith(file_extension.lower()):
                        continue
                    if not regex.match(item.name):
                        continue

                    stats = item.stat()
                    yield {
                        "path": str(item.absolute()),
                        "name": item.name,
                        "size": stats.st_size,
                        "size_mb": round(stats.st_size / 1048576, 2),
                        "created": datetime.fromtimestamp(stats.st_ctime).isoformat(sep=' '),
                        "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(sep=' '),
                        "extension": item.suffix
                    }
                    count += 1
                    if max_results and count >= max_results:
                        break
                except (PermissionError, OSError):
                    continue

            self.logger.info(f"Found {count} files")
        except Exception as e:
            self.logger.error(f"Search error: {e}")
            raise

    def search_in_multiple_drives(self, file_pattern: str = "*", file_extension: Optional[str] = None,
                                   exclude_drives: Optional[List[str]] = None, max_results_per_drive: int = 100) -> Generator[Dict, None, None]:
        """Search across all available drives"""
        drives = [d for d in self.get_available_drives() if not exclude_drives or d not in exclude_drives]
        for drive in drives:
            self.logger.info(f"Searching drive: {drive}")
            try:
                for f in self.search_files(f"{drive}\\", file_pattern, file_extension, True, max_results_per_drive):
                    f["drive"] = drive
                    yield f
            except Exception as e:
                self.logger.error(f"Error on {drive}: {e}")

    def _wildcard_to_regex(self, pattern: str, case_sensitive: bool = False) -> re.Pattern:
        """Convert wildcard pattern to regex"""
        pattern = re.escape(pattern).replace(r"\*", ".*").replace(r"\?", ".")
        return re.compile(f"^{pattern}$", 0 if case_sensitive else re.IGNORECASE)

    def get_folder_size(self, folder_path: str) -> Dict:
        """Calculate total size of a folder"""
        try:
            path = Path(folder_path)
            if not path.exists():
                raise ValueError(f"Folder not found: {folder_path}")
            total, count = 0, 0
            for item in path.rglob("*"):
                if item.is_file():
                    try:
                        total += item.stat().st_size
                        count += 1
                    except (PermissionError, OSError):
                        continue
            return {"path": folder_path, "total_size_bytes": total, "total_size_mb": round(total / 1048576, 2), "total_size_gb": round(total / 1073741824, 2), "file_count": count}
        except Exception as e:
            self.logger.error(f"Folder size error: {e}")
            raise
