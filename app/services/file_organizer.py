"""File Organizer - Core logic for file classification"""
import os
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from send2trash import send2trash


class FileOrganizer:
    """Main class for organizing files based on categories"""

    PROJECT_INDICATORS = ["package.json", "requirements.txt", "pom.xml", "build.gradle", "Cargo.toml", "go.mod", ".git", "node_modules", "venv", "env"]

    def __init__(self, config_path: str = None):
        if config_path is None:
            if getattr(sys, 'frozen', False):
                base = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
            else:
                base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            config_path = os.path.join(base, 'config', 'file_categories.json')

        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.project_indicators = data.get('project_indicators', self.PROJECT_INDICATORS)
            self.categories = data.get('categories', {})

        self.stats = {'total_files': 0, 'organized_files': 0, 'failed_files': 0, 'skipped_files': 0, 'categories_used': {}}

    def _is_code_project(self, directory: str) -> bool:
        d = Path(directory)
        if not d.is_dir():
            return False
        for ind in self.project_indicators:
            if (d / ind).exists():
                return True
        try:
            code_exts = ['.py', '.js', '.java', '.cpp', '.c', '.go', '.rs', '.ts', '.jsx', '.tsx']
            proj_folders = ['src', 'lib', 'test', 'tests', 'dist', 'build']
            code_count = sum(1 for f in d.iterdir() if f.is_file() and f.suffix.lower() in code_exts)
            folder_count = sum(1 for f in d.iterdir() if f.is_dir() and f.name in proj_folders)
            return folder_count >= 2 or code_count >= 5
        except PermissionError:
            return False

    def get_file_category(self, file_path: str, source_dir: str = None) -> str:
        f = Path(file_path)
        ext = f.suffix.lower()
        code_exts = ['.py', '.js', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.ts', '.jsx', '.tsx', '.vue', '.html', '.css', '.scss', '.sass', '.less', '.json', '.xml', '.yaml', '.yml']

        if source_dir and ext in code_exts:
            current = f.parent
            for _ in range(3):
                if self._is_code_project(str(current)):
                    return 'Code_Projects'
                if current.parent == current:
                    break
                current = current.parent

        for cat, info in self.categories.items():
            if ext in info.get('extensions', []):
                return cat
        return 'Others'

    def scan_directory(self, directory: str, recursive: bool = False) -> List[str]:
        d = Path(directory)
        if not d.exists():
            raise FileNotFoundError(f"Not found: {directory}")
        files = [str(f) for f in (d.rglob("*") if recursive else d.iterdir()) if f.is_file()]
        self.stats['total_files'] = len(files)
        return files

    def create_category_folders(self, destination: str) -> Dict[str, str]:
        dest = Path(destination)
        paths = {}
        for cat, info in self.categories.items():
            folder = dest / info['folder']
            folder.mkdir(parents=True, exist_ok=True)
            paths[cat] = str(folder)
        return paths

    def organize_files(self, source_dir: str, destination_dir: str, mode: str = 'move',
                       recursive: bool = False, progress_callback: Optional[callable] = None) -> Tuple[int, int, List[str]]:
        self.stats = {'total_files': 0, 'organized_files': 0, 'failed_files': 0, 'skipped_files': 0, 'categories_used': {}}
        errors = []

        try:
            files = self.scan_directory(source_dir, recursive)
        except Exception as e:
            return 0, 0, [f"Scan failed: {e}"]

        try:
            cat_paths = self.create_category_folders(destination_dir)
        except Exception as e:
            return 0, 0, [f"Create folders failed: {e}"]

        processed_projects = set()

        for i, file_path in enumerate(files):
            try:
                cat = self.get_file_category(file_path, source_dir)
                f = Path(file_path)

                if cat == 'Code_Projects':
                    current = f.parent
                    project_root = None
                    for _ in range(3):
                        if self._is_code_project(str(current)):
                            project_root = current
                            break
                        if current.parent == current:
                            break
                        current = current.parent

                    if project_root and str(project_root) not in processed_projects:
                        processed_projects.add(str(project_root))
                        dest_folder = cat_paths[cat]
                        proj_dest = os.path.join(dest_folder, project_root.name)
                        counter = 1
                        while os.path.exists(proj_dest):
                            proj_dest = os.path.join(dest_folder, f"{project_root.name}_{counter}")
                            counter += 1

                        if mode == 'move':
                            shutil.move(str(project_root), proj_dest)
                        elif mode == 'copy':
                            shutil.copytree(str(project_root), proj_dest)
                        else:
                            shutil.copytree(str(project_root), proj_dest)
                            send2trash(str(project_root))

                        count = sum(1 for _ in Path(proj_dest).rglob('*') if _.is_file())
                        self.stats['organized_files'] += count
                        self.stats['categories_used'][cat] = self.stats['categories_used'].get(cat, 0) + count
                        continue
                    elif str(project_root) in processed_projects:
                        continue

                dest_folder = cat_paths[cat]
                dest_path = os.path.join(dest_folder, f.name)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(dest_folder, f"{f.stem}_{counter}{f.suffix}")
                    counter += 1

                if mode == 'move':
                    shutil.move(file_path, dest_path)
                elif mode == 'copy':
                    shutil.copy2(file_path, dest_path)
                else:
                    shutil.copy2(file_path, dest_path)
                    send2trash(file_path)

                self.stats['organized_files'] += 1
                self.stats['categories_used'][cat] = self.stats['categories_used'].get(cat, 0) + 1

            except Exception as e:
                self.stats['failed_files'] += 1
                errors.append(f"Failed {file_path}: {e}")

            if progress_callback:
                progress_callback(((i + 1) / len(files)) * 100, file_path)

        return self.stats['organized_files'], self.stats['failed_files'], errors

    def get_stats(self) -> Dict:
        return self.stats.copy()

    def generate_report(self) -> str:
        lines = ["=" * 60, "File Organization Report", "=" * 60,
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Total: {self.stats['total_files']}", f"Organized: {self.stats['organized_files']}",
                f"Failed: {self.stats['failed_files']}", "", "Categories:", "-" * 60]
        for cat, count in sorted(self.stats['categories_used'].items()):
            lines.append(f"  {cat}: {count}")
        lines.append("=" * 60)
        return "\n".join(lines)
