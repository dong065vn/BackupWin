"""
PLFSmart - Professional File Organizer
Core logic for file classification and organization
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from send2trash import send2trash


class FileOrganizer:
    """Main class for organizing files based on categories"""

    def __init__(self, config_path: str = None):
        """
        Initialize FileOrganizer with configuration

        Args:
            config_path: Path to JSON configuration file
        """
        if config_path is None:
            # Get the application's base path (works for both source and exe)
            if getattr(sys, 'frozen', False):
                # Running as compiled exe
                if hasattr(sys, '_MEIPASS'):
                    # Running from PyInstaller bundle
                    base_path = sys._MEIPASS
                else:
                    base_path = os.path.dirname(sys.executable)
            else:
                # Running from source
                base_path = os.path.dirname(os.path.dirname(__file__))
            
            config_path = os.path.join(base_path, 'config', 'file_categories.json')

        self.config_path = config_path
        self.categories = self._load_config()
        self.stats = {
            'total_files': 0,
            'organized_files': 0,
            'failed_files': 0,
            'skipped_files': 0,
            'categories_used': {}
        }

    def _load_config(self) -> Dict:
        """Load category configuration from JSON file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.project_indicators = data.get('project_indicators', [])
                return data.get('categories', {})
        except Exception as e:
            raise Exception(f"Failed to load configuration: {str(e)}")

    def _is_code_project_directory(self, directory: str) -> bool:
        """
        Check if a directory contains indicators of a code project

        Args:
            directory: Path to directory to check

        Returns:
            True if directory appears to be a code project
        """
        dir_path = Path(directory)
        if not dir_path.is_dir():
            return False

        # Check for project indicator files/folders
        for indicator in self.project_indicators:
            indicator_path = dir_path / indicator
            if indicator_path.exists():
                return True

        # Check for common project structure patterns
        common_project_folders = ['src', 'lib', 'test', 'tests', 'dist', 'build']
        code_file_count = 0
        project_folder_count = 0

        try:
            for item in dir_path.iterdir():
                if item.is_dir() and item.name in common_project_folders:
                    project_folder_count += 1
                elif item.is_file() and item.suffix.lower() in ['.py', '.js', '.java', '.cpp', '.c', '.go', '.rs', '.ts', '.jsx', '.tsx']:
                    code_file_count += 1
        except PermissionError:
            return False

        # If has 2+ project folders or 5+ code files, likely a project
        return project_folder_count >= 2 or code_file_count >= 5

    def get_file_category(self, file_path: str, source_dir: str = None) -> str:
        """
        Intelligently determine the category of a file

        Args:
            file_path: Path to the file
            source_dir: Source directory for context-aware classification

        Returns:
            Category name
        """
        file_path_obj = Path(file_path)
        ext = file_path_obj.suffix.lower()

        # Check if file is part of a code project
        if source_dir and ext in ['.py', '.js', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.ts', '.jsx', '.tsx', '.vue', '.html', '.css', '.scss', '.sass', '.less', '.json', '.xml', '.yaml', '.yml']:
            parent_dir = file_path_obj.parent
            # Check current directory and parent directories
            current = parent_dir
            for _ in range(3):  # Check up to 3 levels up
                if self._is_code_project_directory(str(current)):
                    return 'Code_Projects'
                if current.parent == current:  # Reached root
                    break
                current = current.parent

        # Standard extension-based classification
        for category, info in self.categories.items():
            if ext in info.get('extensions', []):
                return category

        return 'Others'

    def scan_directory(self, directory: str, recursive: bool = False) -> List[str]:
        """
        Scan directory for files to organize

        Args:
            directory: Directory path to scan
            recursive: Whether to scan subdirectories

        Returns:
            List of file paths
        """
        files = []
        directory = Path(directory)

        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        if recursive:
            for root, _, filenames in os.walk(directory):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
        else:
            for item in directory.iterdir():
                if item.is_file():
                    files.append(str(item))

        self.stats['total_files'] = len(files)
        return files

    def create_category_folders(self, destination: str) -> Dict[str, str]:
        """
        Create category folders in destination directory

        Args:
            destination: Base destination directory

        Returns:
            Dictionary mapping categories to folder paths
        """
        destination = Path(destination)
        category_paths = {}

        for category, info in self.categories.items():
            folder_name = info['folder']
            folder_path = destination / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)
            category_paths[category] = str(folder_path)

        return category_paths

    def organize_files(
        self,
        source_dir: str,
        destination_dir: str,
        mode: str = 'move',  # 'move', 'copy', or 'delete'
        recursive: bool = False,
        progress_callback: Optional[callable] = None
    ) -> Tuple[int, int, List[str]]:
        """
        Organize files from source to destination

        Args:
            source_dir: Source directory containing files
            destination_dir: Destination directory for organized files
            mode: Operation mode ('move', 'copy', 'delete')
            recursive: Scan subdirectories
            progress_callback: Callback function for progress updates

        Returns:
            Tuple of (successful, failed, error_messages)
        """
        # Reset stats
        self.stats = {
            'total_files': 0,
            'organized_files': 0,
            'failed_files': 0,
            'skipped_files': 0,
            'categories_used': {}
        }

        errors = []

        # Scan files
        try:
            files = self.scan_directory(source_dir, recursive)
        except Exception as e:
            return 0, 0, [f"Failed to scan directory: {str(e)}"]

        # Create category folders
        try:
            category_paths = self.create_category_folders(destination_dir)
        except Exception as e:
            return 0, 0, [f"Failed to create category folders: {str(e)}"]

        # Group files by their parent directory for smart project detection
        processed_projects = set()

        # Process each file
        for idx, file_path in enumerate(files):
            try:
                # Get category with smart detection
                category = self.get_file_category(file_path, source_dir)

                # For Code_Projects, organize by project folder
                if category == 'Code_Projects':
                    file_path_obj = Path(file_path)
                    parent_dir = file_path_obj.parent

                    # Find the project root
                    current = parent_dir
                    project_root = None
                    for _ in range(3):
                        if self._is_code_project_directory(str(current)):
                            project_root = current
                            break
                        if current.parent == current:
                            break
                        current = current.parent

                    # If we found a project root and haven't processed it yet
                    if project_root and str(project_root) not in processed_projects:
                        processed_projects.add(str(project_root))

                        # Copy/move entire project directory
                        project_name = project_root.name
                        dest_folder = category_paths[category]
                        project_dest = os.path.join(dest_folder, project_name)

                        # Handle duplicate project names
                        if os.path.exists(project_dest):
                            counter = 1
                            while os.path.exists(project_dest):
                                project_dest = os.path.join(dest_folder, f"{project_name}_{counter}")
                                counter += 1

                        # Copy the entire project
                        if mode == 'move':
                            shutil.move(str(project_root), project_dest)
                        elif mode == 'copy':
                            shutil.copytree(str(project_root), project_dest)
                        elif mode == 'delete':
                            shutil.copytree(str(project_root), project_dest)
                            send2trash(str(project_root))

                        # Count files in project
                        project_file_count = sum(1 for _ in Path(project_dest).rglob('*') if _.is_file())
                        self.stats['organized_files'] += project_file_count
                        self.stats['categories_used'][category] = \
                            self.stats['categories_used'].get(category, 0) + project_file_count

                        # Skip individual file processing for project files
                        continue
                    elif str(project_root) in processed_projects:
                        # Already processed as part of project, skip
                        continue

                dest_folder = category_paths[category]

                # Get file name
                file_name = Path(file_path).name
                dest_path = os.path.join(dest_folder, file_name)

                # Handle duplicate file names
                if os.path.exists(dest_path):
                    base_name = Path(file_name).stem
                    extension = Path(file_name).suffix
                    counter = 1
                    while os.path.exists(dest_path):
                        new_name = f"{base_name}_{counter}{extension}"
                        dest_path = os.path.join(dest_folder, new_name)
                        counter += 1

                # Perform operation
                if mode == 'move':
                    shutil.move(file_path, dest_path)
                elif mode == 'copy':
                    shutil.copy2(file_path, dest_path)
                elif mode == 'delete':
                    # First copy, then delete original
                    shutil.copy2(file_path, dest_path)
                    send2trash(file_path)

                # Update stats
                self.stats['organized_files'] += 1
                self.stats['categories_used'][category] = \
                    self.stats['categories_used'].get(category, 0) + 1

            except Exception as e:
                self.stats['failed_files'] += 1
                errors.append(f"Failed to process {file_path}: {str(e)}")

            # Progress callback
            if progress_callback:
                progress = ((idx + 1) / len(files)) * 100
                progress_callback(progress, file_path)

        return self.stats['organized_files'], self.stats['failed_files'], errors

    def get_stats(self) -> Dict:
        """Get current organization statistics"""
        return self.stats.copy()

    def generate_report(self) -> str:
        """Generate a detailed report of the organization process"""
        report = []
        report.append("=" * 60)
        report.append("PLFSmart - File Organization Report")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        report.append(f"Total files scanned: {self.stats['total_files']}")
        report.append(f"Successfully organized: {self.stats['organized_files']}")
        report.append(f"Failed: {self.stats['failed_files']}")
        report.append(f"Skipped: {self.stats['skipped_files']}")
        report.append("")
        report.append("Files per category:")
        report.append("-" * 60)

        for category, count in sorted(self.stats['categories_used'].items()):
            report.append(f"  {category}: {count} files")

        report.append("=" * 60)
        return "\n".join(report)
