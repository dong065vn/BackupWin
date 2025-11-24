"""File consolidation service for gathering multiple files into one folder"""
import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Callable, Literal
from datetime import datetime
from app.core.logger import app_logger


class FileConsolidationService:
    """Service for consolidating multiple files from different locations into a single folder"""

    def __init__(self):
        self.logger = app_logger

    def consolidate_files(
        self,
        source_files: List[str],
        destination_folder: str,
        operation: Literal["copy", "move"] = "copy",
        duplicate_handling: Literal["skip", "rename", "overwrite"] = "rename",
        preserve_structure: bool = False,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> Dict:
        """
        Consolidate multiple files from different locations into a single destination folder

        Args:
            source_files: List of source file paths to consolidate
            destination_folder: Destination folder path
            operation: "copy" to keep originals, "move" to remove originals
            duplicate_handling: How to handle duplicate file names ("skip", "rename", "overwrite")
            preserve_structure: Whether to preserve original folder structure
            progress_callback: Callback function(current, total, filename) for progress updates

        Returns:
            Dict with consolidation results and statistics
        """
        try:
            # Validate inputs
            validation_result = self._validate_files(source_files)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": validation_result["error"],
                    "invalid_files": validation_result.get("invalid_files", [])
                }

            # Create destination folder
            dest_path = Path(destination_folder)
            dest_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Destination folder ready: {dest_path}")

            # Calculate total size
            total_size = self._calculate_total_size(source_files)

            # Initialize results
            results = {
                "success": True,
                "operation": operation,
                "total_files": len(source_files),
                "successful": 0,
                "failed": 0,
                "skipped": 0,
                "renamed": 0,
                "overwritten": 0,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "files": [],
                "errors": [],
                "completed_at": None
            }

            # Process each file
            processed_files = []  # Track for rollback if needed

            for idx, source_file in enumerate(source_files, 1):
                try:
                    source_path = Path(source_file)

                    # Determine destination path
                    if preserve_structure:
                        # Preserve folder structure
                        # Extract relative path from root drive
                        try:
                            # Get the drive and relative path
                            drive = source_path.drive
                            relative = source_path.relative_to(drive + os.sep)
                            dest_file_path = dest_path / relative
                        except (ValueError, AttributeError):
                            # If can't determine relative path, use parent folder name
                            dest_file_path = dest_path / source_path.parent.name / source_path.name
                    else:
                        # Flat structure - all files in root of destination
                        dest_file_path = dest_path / source_path.name

                    # Handle duplicate file names
                    final_dest_path, action = self._handle_duplicate(
                        dest_file_path,
                        duplicate_handling,
                        source_path
                    )

                    if action == "skip":
                        results["skipped"] += 1
                        results["files"].append({
                            "source": str(source_path),
                            "destination": str(dest_file_path),
                            "action": "skipped",
                            "reason": "File already exists"
                        })
                        self.logger.info(f"Skipped (already exists): {source_path.name}")

                        if progress_callback:
                            progress_callback(idx, len(source_files), f"Skipped: {source_path.name}")
                        continue

                    # Create parent directory if needed
                    final_dest_path.parent.mkdir(parents=True, exist_ok=True)

                    # Perform operation
                    if operation == "copy":
                        shutil.copy2(source_path, final_dest_path)
                        operation_text = "Copied"
                    else:  # move
                        shutil.move(str(source_path), str(final_dest_path))
                        operation_text = "Moved"

                    # Track successful operation
                    processed_files.append({
                        "source": str(source_path),
                        "destination": str(final_dest_path),
                        "operation": operation
                    })

                    # Update statistics
                    results["successful"] += 1
                    if action == "rename":
                        results["renamed"] += 1
                    elif action == "overwrite":
                        results["overwritten"] += 1

                    # Get file size
                    file_size = final_dest_path.stat().st_size

                    results["files"].append({
                        "source": str(source_path),
                        "destination": str(final_dest_path),
                        "action": action,
                        "operation": operation,
                        "size_mb": round(file_size / (1024 * 1024), 2)
                    })

                    self.logger.info(f"{operation_text}: {source_path} -> {final_dest_path}")

                    if progress_callback:
                        progress_callback(idx, len(source_files), f"{operation_text}: {source_path.name}")

                except Exception as e:
                    results["failed"] += 1
                    error_msg = f"Failed to process {source_file}: {str(e)}"
                    results["errors"].append({
                        "file": source_file,
                        "error": str(e)
                    })
                    self.logger.error(error_msg)

                    if progress_callback:
                        progress_callback(idx, len(source_files), f"Error: {Path(source_file).name}")

            results["completed_at"] = datetime.now().isoformat()

            # Log summary
            self.logger.info(
                f"Consolidation completed: {results['successful']} successful, "
                f"{results['failed']} failed, {results['skipped']} skipped"
            )

            return results

        except Exception as e:
            self.logger.error(f"Error during consolidation: {e}")
            return {
                "success": False,
                "error": str(e),
                "total_files": len(source_files) if source_files else 0
            }

    def _validate_files(self, source_files: List[str]) -> Dict:
        """
        Validate that all source files exist and are accessible

        Args:
            source_files: List of source file paths

        Returns:
            Dict with validation results
        """
        if not source_files:
            return {
                "valid": False,
                "error": "No source files provided"
            }

        invalid_files = []

        for file_path in source_files:
            path = Path(file_path)

            if not path.exists():
                invalid_files.append({
                    "path": file_path,
                    "reason": "File does not exist"
                })
            elif not path.is_file():
                invalid_files.append({
                    "path": file_path,
                    "reason": "Path is not a file"
                })
            elif not os.access(path, os.R_OK):
                invalid_files.append({
                    "path": file_path,
                    "reason": "File is not readable"
                })

        if invalid_files:
            return {
                "valid": False,
                "error": f"Found {len(invalid_files)} invalid file(s)",
                "invalid_files": invalid_files
            }

        return {"valid": True}

    def _handle_duplicate(
        self,
        dest_path: Path,
        duplicate_handling: str,
        source_path: Path
    ) -> tuple[Path, str]:
        """
        Handle duplicate file names in destination

        Args:
            dest_path: Intended destination path
            duplicate_handling: Strategy ("skip", "rename", "overwrite")
            source_path: Source file path

        Returns:
            Tuple of (final_path, action_taken)
        """
        if not dest_path.exists():
            return dest_path, "new"

        # File already exists, handle based on strategy
        if duplicate_handling == "skip":
            return dest_path, "skip"

        elif duplicate_handling == "overwrite":
            return dest_path, "overwrite"

        elif duplicate_handling == "rename":
            # Find unique name by adding (1), (2), etc.
            counter = 1
            stem = dest_path.stem
            suffix = dest_path.suffix
            parent = dest_path.parent

            while True:
                new_name = f"{stem} ({counter}){suffix}"
                new_path = parent / new_name

                if not new_path.exists():
                    return new_path, "rename"

                counter += 1

                # Safety check to prevent infinite loop
                if counter > 9999:
                    raise Exception("Too many duplicate files")

        return dest_path, "unknown"

    def _calculate_total_size(self, source_files: List[str]) -> int:
        """
        Calculate total size of all source files

        Args:
            source_files: List of source file paths

        Returns:
            Total size in bytes
        """
        total_size = 0

        for file_path in source_files:
            try:
                path = Path(file_path)
                if path.exists() and path.is_file():
                    total_size += path.stat().st_size
            except Exception as e:
                self.logger.warning(f"Could not get size for {file_path}: {e}")

        return total_size

    def get_consolidation_preview(
        self,
        source_files: List[str],
        destination_folder: str,
        preserve_structure: bool = False,
        duplicate_handling: str = "rename"
    ) -> Dict:
        """
        Preview consolidation without actually performing it (dry run)

        Args:
            source_files: List of source file paths
            destination_folder: Destination folder path
            preserve_structure: Whether to preserve folder structure
            duplicate_handling: How duplicates would be handled

        Returns:
            Dict with preview information
        """
        try:
            dest_path = Path(destination_folder)
            preview = {
                "total_files": len(source_files),
                "total_size_mb": 0.0,
                "conflicts": 0,
                "files": []
            }

            total_size = self._calculate_total_size(source_files)
            preview["total_size_mb"] = round(total_size / (1024 * 1024), 2)

            # Simulate destination paths
            dest_names = {}

            for source_file in source_files:
                source_path = Path(source_file)

                if not source_path.exists():
                    continue

                # Determine destination
                if preserve_structure:
                    try:
                        drive = source_path.drive
                        relative = source_path.relative_to(drive + os.sep)
                        dest_file_path = dest_path / relative
                    except (ValueError, AttributeError):
                        dest_file_path = dest_path / source_path.parent.name / source_path.name
                else:
                    dest_file_path = dest_path / source_path.name

                # Check for conflicts
                conflict = str(dest_file_path) in dest_names or dest_file_path.exists()

                if conflict:
                    preview["conflicts"] += 1

                dest_names[str(dest_file_path)] = True

                file_size = source_path.stat().st_size
                preview["files"].append({
                    "source": str(source_path),
                    "destination": str(dest_file_path),
                    "size_mb": round(file_size / (1024 * 1024), 2),
                    "has_conflict": conflict
                })

            return preview

        except Exception as e:
            self.logger.error(f"Error generating preview: {e}")
            return {
                "error": str(e),
                "total_files": len(source_files)
            }
