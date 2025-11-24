"""File search service for Windows"""
import os
import re
from pathlib import Path
from typing import List, Optional, Dict, Generator
from datetime import datetime
from app.core.logger import app_logger


class FileSearchService:
    """Service for searching files in Windows drives and folders"""

    def __init__(self):
        self.logger = app_logger

    def get_available_drives(self) -> List[str]:
        """
        Get all available drives on Windows system

        Returns:
            List of drive letters (e.g., ['C:', 'D:', 'E:'])
        """
        try:
            import string
            drives = []
            for letter in string.ascii_uppercase:
                drive = f"{letter}:"
                if os.path.exists(drive):
                    drives.append(drive)
            self.logger.info(f"Found {len(drives)} available drives: {drives}")
            return drives
        except Exception as e:
            self.logger.error(f"Error getting available drives: {e}")
            return []

    def search_files(
        self,
        search_path: str,
        file_pattern: Optional[str] = "*",
        file_extension: Optional[str] = None,
        recursive: bool = True,
        max_results: Optional[int] = None,
        case_sensitive: bool = False
    ) -> Generator[Dict, None, None]:
        """
        Search for files in specified path

        Args:
            search_path: Path to search (can be drive letter or folder)
            file_pattern: Pattern to match filename (supports wildcards)
            file_extension: File extension filter (e.g., '.txt', '.pdf')
            recursive: Search in subdirectories
            max_results: Maximum number of results to return
            case_sensitive: Case sensitive search

        Yields:
            Dict containing file information
        """
        try:
            search_path_obj = Path(search_path)
            if not search_path_obj.exists():
                self.logger.error(f"Search path does not exist: {search_path}")
                return

            self.logger.info(f"Searching files in: {search_path}")
            self.logger.info(f"Pattern: {file_pattern}, Extension: {file_extension}, Recursive: {recursive}")

            # Convert wildcard pattern to regex
            regex_pattern = self._wildcard_to_regex(file_pattern, case_sensitive)
            count = 0

            # Choose search method based on recursive flag
            if recursive:
                search_method = search_path_obj.rglob("*")
            else:
                search_method = search_path_obj.glob("*")

            for item in search_method:
                try:
                    # Skip directories
                    if not item.is_file():
                        continue

                    # Check extension filter
                    if file_extension and not item.name.lower().endswith(file_extension.lower()):
                        continue

                    # Check pattern match
                    if not regex_pattern.match(item.name):
                        continue

                    # Get file stats
                    stats = item.stat()

                    file_info = {
                        "path": str(item.absolute()),
                        "name": item.name,
                        "size": stats.st_size,
                        "size_mb": round(stats.st_size / (1024 * 1024), 2),
                        "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                        "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                        "extension": item.suffix
                    }

                    yield file_info
                    count += 1

                    # Check max results limit
                    if max_results and count >= max_results:
                        self.logger.info(f"Reached max results limit: {max_results}")
                        break

                except (PermissionError, OSError) as e:
                    # Skip files/folders we don't have permission to access
                    self.logger.debug(f"Skipping {item}: {e}")
                    continue

            self.logger.info(f"Search completed. Found {count} files.")

        except Exception as e:
            self.logger.error(f"Error searching files: {e}")
            raise

    def search_in_multiple_drives(
        self,
        file_pattern: Optional[str] = "*",
        file_extension: Optional[str] = None,
        exclude_drives: Optional[List[str]] = None,
        max_results_per_drive: Optional[int] = 100
    ) -> Generator[Dict, None, None]:
        """
        Search for files across all available drives

        Args:
            file_pattern: Pattern to match filename
            file_extension: File extension filter
            exclude_drives: List of drives to exclude (e.g., ['A:', 'B:'])
            max_results_per_drive: Maximum results per drive

        Yields:
            Dict containing file information with drive letter
        """
        drives = self.get_available_drives()

        if exclude_drives:
            drives = [d for d in drives if d not in exclude_drives]

        for drive in drives:
            self.logger.info(f"Searching in drive: {drive}")
            try:
                for file_info in self.search_files(
                    search_path=f"{drive}\\",
                    file_pattern=file_pattern,
                    file_extension=file_extension,
                    recursive=True,
                    max_results=max_results_per_drive
                ):
                    file_info["drive"] = drive
                    yield file_info
            except Exception as e:
                self.logger.error(f"Error searching drive {drive}: {e}")
                continue

    def _wildcard_to_regex(self, pattern: str, case_sensitive: bool = False) -> re.Pattern:
        """
        Convert wildcard pattern to regex pattern

        Args:
            pattern: Wildcard pattern (e.g., "*.txt", "test_*")
            case_sensitive: Case sensitive matching

        Returns:
            Compiled regex pattern
        """
        # Escape special regex characters except * and ?
        pattern = re.escape(pattern)
        # Convert wildcard * to regex .*
        pattern = pattern.replace(r"\*", ".*")
        # Convert wildcard ? to regex .
        pattern = pattern.replace(r"\?", ".")
        # Match full string
        pattern = f"^{pattern}$"

        flags = 0 if case_sensitive else re.IGNORECASE
        return re.compile(pattern, flags)

    def get_folder_size(self, folder_path: str) -> Dict:
        """
        Calculate total size of a folder

        Args:
            folder_path: Path to folder

        Returns:
            Dict with size information
        """
        try:
            total_size = 0
            file_count = 0
            folder_path_obj = Path(folder_path)

            if not folder_path_obj.exists():
                raise ValueError(f"Folder does not exist: {folder_path}")

            for item in folder_path_obj.rglob("*"):
                if item.is_file():
                    try:
                        total_size += item.stat().st_size
                        file_count += 1
                    except (PermissionError, OSError):
                        continue

            return {
                "path": folder_path,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "total_size_gb": round(total_size / (1024 * 1024 * 1024), 2),
                "file_count": file_count
            }
        except Exception as e:
            self.logger.error(f"Error calculating folder size: {e}")
            raise
