"""Duplicate file finder service"""
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

    def scan_for_duplicates(self, scan_paths: List[str], comparison_method: Literal["hash", "size_name", "quick"] = "hash",
                            min_file_size: int = 0, file_extensions: Optional[List[str]] = None,
                            recursive: bool = True, progress_callback: Optional[Callable[[int, int, str], None]] = None) -> Dict:
        """Scan for duplicate files"""
        try:
            files = []
            for p in scan_paths:
                files.extend(self._collect_files(p, min_file_size, file_extensions, recursive))

            if not files:
                return {"success": True, "total_files_scanned": 0, "duplicate_groups": [], "total_duplicates": 0, "space_wasted_bytes": 0, "space_wasted_mb": 0.0}

            if comparison_method == "hash":
                groups = self._find_by_hash(files, progress_callback)
            elif comparison_method == "size_name":
                groups = self._find_by_size_name(files, progress_callback)
            else:
                groups = self._find_quick(files, progress_callback)

            total_dups = sum(len(g["files"]) - 1 for g in groups)
            wasted = sum(g["wasted_space"] for g in groups)

            return {"success": True, "total_files_scanned": len(files), "duplicate_groups": groups,
                    "total_duplicates": total_dups, "space_wasted_bytes": wasted,
                    "space_wasted_mb": round(wasted / 1048576, 2), "scanned_at": datetime.now().isoformat(sep=' ')}
        except Exception as e:
            self.logger.error(f"Scan error: {e}")
            return {"success": False, "error": str(e)}

    def _collect_files(self, path: str, min_size: int, extensions: Optional[List[str]], recursive: bool) -> List[Path]:
        files = []
        try:
            for f in Path(path).glob("**/*" if recursive else "*"):
                if not f.is_file():
                    continue
                try:
                    if f.stat().st_size < min_size:
                        continue
                except:
                    continue
                if extensions and f.suffix.lower() not in [e.lower() for e in extensions]:
                    continue
                files.append(f)
        except Exception as e:
            self.logger.warning(f"Collect error {path}: {e}")
        return files

    def _find_by_hash(self, files: List[Path], progress_callback: Optional[Callable] = None) -> List[Dict]:
        hash_map = defaultdict(list)
        for i, f in enumerate(files, 1):
            try:
                h = self._calculate_hash(f)
                s = f.stat()
                hash_map[h].append({"path": str(f.absolute()), "name": f.name, "size": s.st_size,
                                   "modified": datetime.fromtimestamp(s.st_mtime).isoformat(sep=' ')})
                if progress_callback:
                    progress_callback(i, len(files), f.name)
            except Exception as e:
                self.logger.warning(f"Hash error {f}: {e}")

        groups = []
        for h, flist in hash_map.items():
            if len(flist) >= 2:
                flist.sort(key=lambda x: x["modified"])
                size = flist[0]["size"]
                wasted = size * (len(flist) - 1)
                groups.append({"hash": h, "count": len(flist), "file_size": size, "file_size_mb": round(size / 1048576, 3),
                              "wasted_space": wasted, "wasted_space_mb": round(wasted / 1048576, 2), "files": flist})
        return sorted(groups, key=lambda x: x["wasted_space"], reverse=True)

    def _find_by_size_name(self, files: List[Path], progress_callback: Optional[Callable] = None) -> List[Dict]:
        size_map = defaultdict(list)
        for i, f in enumerate(files, 1):
            try:
                s = f.stat()
                key = f"{s.st_size}_{f.name.lower()}"
                size_map[key].append({"path": str(f.absolute()), "name": f.name, "size": s.st_size,
                                     "modified": datetime.fromtimestamp(s.st_mtime).isoformat(sep=' ')})
                if progress_callback:
                    progress_callback(i, len(files), f.name)
            except Exception as e:
                self.logger.warning(f"Size/name error {f}: {e}")

        groups = []
        for key, flist in size_map.items():
            if len(flist) >= 2:
                flist.sort(key=lambda x: x["modified"])
                size = flist[0]["size"]
                wasted = size * (len(flist) - 1)
                groups.append({"hash": key, "count": len(flist), "file_size": size, "file_size_mb": round(size / 1048576, 3),
                              "wasted_space": wasted, "wasted_space_mb": round(wasted / 1048576, 2), "files": flist})
        return sorted(groups, key=lambda x: x["wasted_space"], reverse=True)

    def _find_quick(self, files: List[Path], progress_callback: Optional[Callable] = None) -> List[Dict]:
        size_map = defaultdict(list)
        for f in files:
            try:
                size_map[f.stat().st_size].append(f)
            except:
                pass
        potential = [f for flist in size_map.values() if len(flist) >= 2 for f in flist]
        return self._find_by_hash(potential, progress_callback)

    def _calculate_hash(self, file_path: Path) -> str:
        h = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def delete_duplicates(self, group: Dict, keep_index: int = 0) -> Dict:
        """Delete duplicate files, keeping one"""
        try:
            files, deleted, errors = group["files"], 0, []
            for i, f in enumerate(files):
                if i == keep_index:
                    continue
                try:
                    p = Path(f["path"])
                    if p.exists():
                        p.unlink()
                        deleted += 1
                except Exception as e:
                    errors.append(f"Failed {f['path']}: {e}")
            return {"success": True, "deleted": deleted, "failed": len(errors), "errors": errors, "kept_file": files[keep_index]["path"]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def move_duplicates(self, group: Dict, destination: str, keep_index: int = 0) -> Dict:
        """Move duplicate files to a folder"""
        try:
            import shutil
            dest = Path(destination)
            dest.mkdir(parents=True, exist_ok=True)
            files, moved, errors = group["files"], 0, []

            for i, f in enumerate(files):
                if i == keep_index:
                    continue
                try:
                    src = Path(f["path"])
                    if not src.exists():
                        continue
                    target = dest / src.name
                    counter = 1
                    while target.exists():
                        target = dest / f"{src.stem}_{counter}{src.suffix}"
                        counter += 1
                    shutil.move(str(src), str(target))
                    moved += 1
                except Exception as e:
                    errors.append(f"Failed {f['path']}: {e}")

            return {"success": True, "moved": moved, "failed": len(errors), "errors": errors,
                    "kept_file": files[keep_index]["path"], "destination": str(dest)}
        except Exception as e:
            return {"success": False, "error": str(e)}
