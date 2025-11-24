"""Duplicate file finder service for identifying and managing duplicate files"""
import os
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Callable, Literal
from collections import defaultdict
from datetime import datetime
from app.core.logger import app_logger


class DuplicateFinderService:
    """Service for finding and managing duplicate files"""

    def __init__(self):
        self.logger = app_logger

    def scan_for_duplicates(
        self,
        scan_paths: List[str],
        comparison_method: Literal["hash", "size_name", "quick"] = "hash",
        min_file_size: int = 0,  # bytes
        file_extensions: Optional[List[str]] = None,
        recursive: bool = True,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> Dict:
        """
        Scan for duplicate files in specified paths

        Args:
            scan_paths: List of folder paths to scan
            comparison_method: Method to compare files
                - "hash": Compare by MD5 hash (accurate, slower)
                - "size_name": Compare by size + name (fast, less accurate)
                - "quick": Compare by size only first, then hash duplicates
            min_file_size: Minimum file size to consider (in bytes)
            file_extensions: List of extensions to include (e.g., ['.jpg', '.png'])
            recursive: Whether to scan subdirectories
            progress_callback: Callback function(current, total, filename)

        Returns:
            Dict with duplicate groups and statistics
        """
        try:
            self.logger.info(f"Starting duplicate scan in {len(scan_paths)} path(s)")

            # Collect all files
            all_files = []
            for scan_path in scan_paths:
                files = self._collect_files(
                    scan_path,
                    min_file_size=min_file_size,
                    file_extensions=file_extensions,
                    recursive=recursive
                )
                all_files.extend(files)

            self.logger.info(f"Found {len(all_files)} files to scan")

            if not all_files:
                return {
                    "success": True,
                    "total_files_scanned": 0,
                    "duplicate_groups": [],
                    "total_duplicates": 0,
                    "space_wasted_bytes": 0,
                    "space_wasted_mb": 0.0
                }

            # Find duplicates based on method
            if comparison_method == "hash":
                duplicate_groups = self._find_duplicates_by_hash(
                    all_files, progress_callback
                )
            elif comparison_method == "size_name":
                duplicate_groups = self._find_duplicates_by_size_name(
                    all_files, progress_callback
                )
            else:  # quick
                duplicate_groups = self._find_duplicates_quick(
                    all_files, progress_callback
                )

            # Calculate statistics
            total_duplicates = sum(len(group["files"]) - 1 for group in duplicate_groups)
            space_wasted = sum(group["wasted_space"] for group in duplicate_groups)

            result = {
                "success": True,
                "total_files_scanned": len(all_files),
                "duplicate_groups": duplicate_groups,
                "total_duplicates": total_duplicates,
                "space_wasted_bytes": space_wasted,
                "space_wasted_mb": round(space_wasted / (1024 * 1024), 2),
                "scanned_at": datetime.now().isoformat()
            }

            self.logger.info(
                f"Scan complete: {len(duplicate_groups)} duplicate groups, "
                f"{total_duplicates} duplicate files, "
                f"{result['space_wasted_mb']} MB wasted"
            )

            return result

        except Exception as e:
            self.logger.error(f"Error during duplicate scan: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _collect_files(
        self,
        path: str,
        min_file_size: int,
        file_extensions: Optional[List[str]],
        recursive: bool
    ) -> List[Path]:
        """Collect all files matching criteria"""
        files = []
        path_obj = Path(path)

        try:
            if recursive:
                pattern = "**/*"
            else:
                pattern = "*"

            for file_path in path_obj.glob(pattern):
                if not file_path.is_file():
                    continue

                # Check file size
                try:
                    size = file_path.stat().st_size
                    if size < min_file_size:
                        continue
                except:
                    continue

                # Check extension
                if file_extensions:
                    if file_path.suffix.lower() not in [ext.lower() for ext in file_extensions]:
                        continue

                files.append(file_path)

        except Exception as e:
            self.logger.warning(f"Error collecting files from {path}: {e}")

        return files

    def _find_duplicates_by_hash(
        self,
        files: List[Path],
        progress_callback: Optional[Callable] = None
    ) -> List[Dict]:
        """Find duplicates by comparing MD5 hashes"""
        hash_map = defaultdict(list)
        total = len(files)

        for idx, file_path in enumerate(files, 1):
            try:
                file_hash = self._calculate_hash(file_path)
                file_size = file_path.stat().st_size

                hash_map[file_hash].append({
                    "path": str(file_path.absolute()),
                    "name": file_path.name,
                    "size": file_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })

                if progress_callback:
                    progress_callback(idx, total, file_path.name)

            except Exception as e:
                self.logger.warning(f"Error processing {file_path}: {e}")

        # Filter out unique files (only keep groups with 2+ files)
        duplicate_groups = []
        for file_hash, file_list in hash_map.items():
            if len(file_list) >= 2:
                # Sort by modification date (oldest first)
                file_list.sort(key=lambda x: x["modified"])

                file_size = file_list[0]["size"]
                wasted_space = file_size * (len(file_list) - 1)

                duplicate_groups.append({
                    "hash": file_hash,
                    "count": len(file_list),
                    "file_size": file_size,
                    "file_size_mb": round(file_size / (1024 * 1024), 3),
                    "wasted_space": wasted_space,
                    "wasted_space_mb": round(wasted_space / (1024 * 1024), 2),
                    "files": file_list
                })

        # Sort by wasted space (largest first)
        duplicate_groups.sort(key=lambda x: x["wasted_space"], reverse=True)

        return duplicate_groups

    def _find_duplicates_by_size_name(
        self,
        files: List[Path],
        progress_callback: Optional[Callable] = None
    ) -> List[Dict]:
        """Find duplicates by comparing size and name (faster but less accurate)"""
        size_name_map = defaultdict(list)
        total = len(files)

        for idx, file_path in enumerate(files, 1):
            try:
                file_size = file_path.stat().st_size
                file_name = file_path.name.lower()
                key = f"{file_size}_{file_name}"

                size_name_map[key].append({
                    "path": str(file_path.absolute()),
                    "name": file_path.name,
                    "size": file_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })

                if progress_callback:
                    progress_callback(idx, total, file_path.name)

            except Exception as e:
                self.logger.warning(f"Error processing {file_path}: {e}")

        # Filter out unique files
        duplicate_groups = []
        for key, file_list in size_name_map.items():
            if len(file_list) >= 2:
                file_list.sort(key=lambda x: x["modified"])

                file_size = file_list[0]["size"]
                wasted_space = file_size * (len(file_list) - 1)

                duplicate_groups.append({
                    "hash": key,
                    "count": len(file_list),
                    "file_size": file_size,
                    "file_size_mb": round(file_size / (1024 * 1024), 3),
                    "wasted_space": wasted_space,
                    "wasted_space_mb": round(wasted_space / (1024 * 1024), 2),
                    "files": file_list
                })

        duplicate_groups.sort(key=lambda x: x["wasted_space"], reverse=True)

        return duplicate_groups

    def _find_duplicates_quick(
        self,
        files: List[Path],
        progress_callback: Optional[Callable] = None
    ) -> List[Dict]:
        """Quick method: Group by size first, then hash only potential duplicates"""
        # Step 1: Group by size
        size_map = defaultdict(list)

        for file_path in files:
            try:
                file_size = file_path.stat().st_size
                size_map[file_size].append(file_path)
            except Exception as e:
                self.logger.warning(f"Error processing {file_path}: {e}")

        # Step 2: For sizes with multiple files, calculate hash
        potential_duplicates = []
        for size, file_list in size_map.items():
            if len(file_list) >= 2:
                potential_duplicates.extend(file_list)

        # Step 3: Calculate hash only for potential duplicates
        return self._find_duplicates_by_hash(potential_duplicates, progress_callback)

    def _calculate_hash(self, file_path: Path, algorithm: str = "md5") -> str:
        """Calculate file hash"""
        if algorithm == "md5":
            hash_obj = hashlib.md5()
        elif algorithm == "sha256":
            hash_obj = hashlib.sha256()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        try:
            with open(file_path, "rb") as f:
                # Read in chunks for memory efficiency
                for chunk in iter(lambda: f.read(8192), b""):
                    hash_obj.update(chunk)

            return hash_obj.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating hash for {file_path}: {e}")
            raise

    def delete_duplicates(
        self,
        duplicate_group: Dict,
        keep_index: int = 0,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Delete duplicate files, keeping one copy

        Args:
            duplicate_group: Duplicate group dict from scan results
            keep_index: Index of file to keep (default: 0 = oldest)
            progress_callback: Callback for progress updates

        Returns:
            Dict with operation results
        """
        try:
            files = duplicate_group["files"]
            total = len(files) - 1  # Don't count the kept file
            deleted = 0
            errors = []

            for idx, file_info in enumerate(files):
                if idx == keep_index:
                    continue  # Skip the file we want to keep

                try:
                    file_path = Path(file_info["path"])
                    if file_path.exists():
                        file_path.unlink()
                        deleted += 1
                        self.logger.info(f"Deleted duplicate: {file_path}")

                    if progress_callback:
                        progress_callback(deleted, total, file_info["name"])

                except Exception as e:
                    error_msg = f"Failed to delete {file_info['path']}: {str(e)}"
                    errors.append(error_msg)
                    self.logger.error(error_msg)

            return {
                "success": True,
                "deleted": deleted,
                "failed": len(errors),
                "errors": errors,
                "kept_file": files[keep_index]["path"]
            }

        except Exception as e:
            self.logger.error(f"Error deleting duplicates: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def move_duplicates(
        self,
        duplicate_group: Dict,
        destination_folder: str,
        keep_index: int = 0,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Move duplicate files to a folder, keeping one copy

        Args:
            duplicate_group: Duplicate group dict from scan results
            destination_folder: Where to move duplicates
            keep_index: Index of file to keep (default: 0 = oldest)
            progress_callback: Callback for progress updates

        Returns:
            Dict with operation results
        """
        try:
            import shutil

            dest_path = Path(destination_folder)
            dest_path.mkdir(parents=True, exist_ok=True)

            files = duplicate_group["files"]
            total = len(files) - 1
            moved = 0
            errors = []

            for idx, file_info in enumerate(files):
                if idx == keep_index:
                    continue

                try:
                    source = Path(file_info["path"])
                    if not source.exists():
                        continue

                    # Handle filename conflicts in destination
                    dest_file = dest_path / source.name
                    counter = 1
                    while dest_file.exists():
                        stem = source.stem
                        suffix = source.suffix
                        dest_file = dest_path / f"{stem}_{counter}{suffix}"
                        counter += 1

                    shutil.move(str(source), str(dest_file))
                    moved += 1
                    self.logger.info(f"Moved duplicate: {source} -> {dest_file}")

                    if progress_callback:
                        progress_callback(moved, total, file_info["name"])

                except Exception as e:
                    error_msg = f"Failed to move {file_info['path']}: {str(e)}"
                    errors.append(error_msg)
                    self.logger.error(error_msg)

            return {
                "success": True,
                "moved": moved,
                "failed": len(errors),
                "errors": errors,
                "kept_file": files[keep_index]["path"],
                "destination": str(dest_path)
            }

        except Exception as e:
            self.logger.error(f"Error moving duplicates: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def auto_select_best_file(self, files: List[Dict]) -> int:
        """
        Automatically select the best file to keep based on criteria:
        1. Shortest path (likely original location)
        2. Oldest modification time
        3. First in list

        Returns:
            Index of best file to keep
        """
        if not files:
            return 0

        # Score each file
        scored_files = []
        for idx, file_info in enumerate(files):
            path_length = len(file_info["path"])
            # Shorter path = higher score
            path_score = 1000 - path_length

            # Older file = higher score (convert to timestamp)
            mod_time = datetime.fromisoformat(file_info["modified"]).timestamp()
            time_score = -mod_time  # Negative so older is higher

            total_score = path_score + time_score
            scored_files.append((idx, total_score))

        # Sort by score (highest first)
        scored_files.sort(key=lambda x: x[1], reverse=True)

        return scored_files[0][0]
