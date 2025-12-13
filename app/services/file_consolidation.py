"""File consolidation service"""
import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Callable, Literal
from datetime import datetime
from app.core.logger import app_logger


class FileConsolidationService:
    """Service for consolidating files into a single folder"""

    def __init__(self):
        self.logger = app_logger

    def consolidate_files(self, source_files: List[str], destination_folder: str,
                          operation: Literal["copy", "move"] = "copy",
                          duplicate_handling: Literal["skip", "rename", "overwrite"] = "rename",
                          preserve_structure: bool = False,
                          progress_callback: Optional[Callable[[int, int, str], None]] = None) -> Dict:
        """Consolidate multiple files into a single destination folder"""
        try:
            validation = self._validate_files(source_files)
            if not validation["valid"]:
                return {"success": False, "error": validation["error"], "invalid_files": validation.get("invalid_files", [])}

            dest = Path(destination_folder)
            dest.mkdir(parents=True, exist_ok=True)
            total_size = self._calculate_total_size(source_files)

            results = {"success": True, "operation": operation, "total_files": len(source_files),
                      "successful": 0, "failed": 0, "skipped": 0, "renamed": 0, "overwritten": 0,
                      "total_size_mb": round(total_size / 1048576, 2), "files": [], "errors": [], "completed_at": None}

            for i, src_file in enumerate(source_files, 1):
                try:
                    src = Path(src_file)
                    if preserve_structure:
                        try:
                            rel = src.relative_to(src.drive + os.sep)
                            dest_path = dest / rel
                        except (ValueError, AttributeError):
                            dest_path = dest / src.parent.name / src.name
                    else:
                        dest_path = dest / src.name

                    final_path, action = self._handle_duplicate(dest_path, duplicate_handling)
                    if action == "skip":
                        results["skipped"] += 1
                        results["files"].append({"source": str(src), "destination": str(dest_path), "action": "skipped"})
                        if progress_callback:
                            progress_callback(i, len(source_files), f"Skipped: {src.name}")
                        continue

                    final_path.parent.mkdir(parents=True, exist_ok=True)
                    if operation == "copy":
                        shutil.copy2(src, final_path)
                    else:
                        shutil.move(str(src), str(final_path))

                    results["successful"] += 1
                    if action == "rename":
                        results["renamed"] += 1
                    elif action == "overwrite":
                        results["overwritten"] += 1

                    results["files"].append({"source": str(src), "destination": str(final_path), "action": action,
                                            "operation": operation, "size_mb": round(final_path.stat().st_size / 1048576, 2)})
                    if progress_callback:
                        progress_callback(i, len(source_files), f"{operation.title()}d: {src.name}")

                except Exception as e:
                    results["failed"] += 1
                    results["errors"].append({"file": src_file, "error": str(e)})
                    if progress_callback:
                        progress_callback(i, len(source_files), f"Error: {Path(src_file).name}")

            results["completed_at"] = datetime.now().isoformat(sep=' ')
            return results
        except Exception as e:
            self.logger.error(f"Consolidation error: {e}")
            return {"success": False, "error": str(e), "total_files": len(source_files) if source_files else 0}

    def _validate_files(self, files: List[str]) -> Dict:
        if not files:
            return {"valid": False, "error": "No files provided"}
        invalid = []
        for f in files:
            p = Path(f)
            if not p.exists():
                invalid.append({"path": f, "reason": "Not found"})
            elif not p.is_file():
                invalid.append({"path": f, "reason": "Not a file"})
            elif not os.access(p, os.R_OK):
                invalid.append({"path": f, "reason": "Not readable"})
        return {"valid": False, "error": f"{len(invalid)} invalid file(s)", "invalid_files": invalid} if invalid else {"valid": True}

    def _handle_duplicate(self, dest: Path, handling: str) -> tuple:
        if not dest.exists():
            return dest, "new"
        if handling == "skip":
            return dest, "skip"
        if handling == "overwrite":
            return dest, "overwrite"
        counter = 1
        while True:
            new_path = dest.parent / f"{dest.stem} ({counter}){dest.suffix}"
            if not new_path.exists():
                return new_path, "rename"
            counter += 1
            if counter > 9999:
                raise Exception("Too many duplicates")

    def _calculate_total_size(self, files: List[str]) -> int:
        total = 0
        for f in files:
            try:
                p = Path(f)
                if p.exists() and p.is_file():
                    total += p.stat().st_size
            except:
                pass
        return total

    def get_consolidation_preview(self, source_files: List[str], destination_folder: str,
                                   preserve_structure: bool = False, duplicate_handling: str = "rename") -> Dict:
        """Preview consolidation without performing it"""
        try:
            dest = Path(destination_folder)
            preview = {"total_files": len(source_files), "total_size_mb": round(self._calculate_total_size(source_files) / 1048576, 2),
                      "conflicts": 0, "files": []}
            dest_names = {}

            for f in source_files:
                src = Path(f)
                if not src.exists():
                    continue
                if preserve_structure:
                    try:
                        rel = src.relative_to(src.drive + os.sep)
                        dest_path = dest / rel
                    except (ValueError, AttributeError):
                        dest_path = dest / src.parent.name / src.name
                else:
                    dest_path = dest / src.name

                conflict = str(dest_path) in dest_names or dest_path.exists()
                if conflict:
                    preview["conflicts"] += 1
                dest_names[str(dest_path)] = True
                preview["files"].append({"source": str(src), "destination": str(dest_path),
                                        "size_mb": round(src.stat().st_size / 1048576, 2), "has_conflict": conflict})
            return preview
        except Exception as e:
            return {"error": str(e), "total_files": len(source_files)}
