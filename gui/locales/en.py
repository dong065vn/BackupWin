"""English language translations"""

en = {
    # Window titles
    "app_title": "BackupWin - File Backup & Search",
    "app_subtitle": "Windows File Backup Solution",

    # Tabs
    "tab_search": "Search Files",
    "tab_backup": "Backup Files",
    "tab_restore": "Restore & Manage",

    # Common buttons
    "btn_browse": "Browse",
    "btn_search": "Search",
    "btn_backup": "Backup",
    "btn_restore": "Restore",
    "btn_delete": "Delete",
    "btn_cancel": "Cancel",
    "btn_ok": "OK",
    "btn_refresh": "Refresh",
    "btn_open_folder": "Open Folder",
    "btn_about": "About",

    # Search Tab
    "search_title": "Search Options",
    "search_path": "Search Path:",
    "search_pattern": "File Pattern:",
    "search_pattern_placeholder": "e.g., *.pdf, test_*",
    "search_extension": "File Extension:",
    "search_extension_placeholder": "e.g., .pdf, .docx (optional)",
    "search_recursive": "Search in subdirectories",
    "search_case_sensitive": "Case sensitive",
    "search_max_results": "Max Results:",
    "search_max_results_placeholder": "Leave empty for unlimited",
    "btn_search_all_drives": "Search All Drives",
    "btn_get_drives": "Get Available Drives",

    # Search Results
    "search_results": "Search Results",
    "files_found": "Files Found",
    "total_size": "Total Size",
    "col_file_name": "File Name",
    "col_path": "Path",
    "col_size": "Size (MB)",
    "col_modified": "Modified",

    # Backup Tab
    "backup_title": "Backup Options",
    "backup_mode": "Backup Mode:",
    "backup_mode_single": "Single File",
    "backup_mode_multiple": "Multiple Files",
    "backup_mode_folder": "Entire Folder",
    "backup_source": "Source:",
    "backup_destination": "Destination (optional):",
    "backup_preserve_structure": "Preserve directory structure",
    "backup_create_checksum": "Create checksum (MD5)",
    "backup_extensions": "File Extensions (comma-separated):",
    "backup_extensions_placeholder": "e.g., .pdf,.docx,.xlsx",
    "backup_exclude": "Exclude Patterns (comma-separated):",
    "backup_exclude_placeholder": "e.g., *.tmp,__pycache__",
    "btn_start_backup": "Start Backup",

    # Backup Stats
    "files_backed_up": "Files Backed Up",
    "backup_failed": "Failed",
    "backup_log": "Backup Log",

    # Restore Tab
    "restore_title": "Restore Options",
    "restore_backup_file": "Backup File:",
    "restore_destination": "Restore Destination:",
    "restore_verify_checksum": "Verify checksum",
    "btn_restore_file": "Restore File",
    "restore_management": "Backup Management",
    "restore_filter_date": "Filter by Date:",
    "restore_filter_placeholder": "YYYYMMDD (optional)",
    "available_backups": "Available Backups",
    "total_backup_size": "Total Backup Size",
    "btn_open_backup_folder": "Open Backup Folder",

    # Status messages
    "status_ready": "Ready",
    "status_searching": "Searching...",
    "status_backing_up": "Backing up...",
    "status_restoring": "Restoring...",
    "status_completed": "Completed!",
    "status_error": "Error",

    # Dialog messages
    "msg_select_path": "Please select a search path!",
    "msg_select_source": "Please select source to backup!",
    "msg_select_backup": "Please select a backup file!",
    "msg_select_destination": "Please select restore destination!",
    "msg_search_all_drives": "This will search all available drives. This may take a while.",
    "msg_confirm_delete": "Are you sure you want to delete this backup?\n\n{path}\n\nThis action cannot be undone!",
    "msg_confirm_restore": "Restore file from:\n{backup}\n\nTo:\n{destination}",
    "msg_backup_success": "Backup completed successfully!",
    "msg_restore_success": "File restored successfully!\n\nDestination: {destination}",
    "msg_delete_success": "Backup deleted successfully!",

    # Error messages
    "error": "Error",
    "error_search_failed": "Search failed: {error}",
    "error_backup_failed": "Backup failed: {error}",
    "error_restore_failed": "Restore failed: {error}",
    "error_delete_failed": "Delete failed: {error}",
    "error_load_backups": "Failed to load backups: {error}",
    "error_get_drives": "Failed to get drives: {error}",

    # Info messages
    "info": "Information",
    "info_drives_found": "Found {count} drives:\n\n{drives}",
    "info_no_backups": "No backups found",
    "msg_restart_language": "Please restart the application for language changes to take effect.",

    # Progress messages
    "progress_found_files": "Found {count} files",
    "progress_backing_up": "Backing up... ({current}/{total})",
    "progress_current_file": "Current: {file}...",

    # Footer
    "footer_version": "Version 1.0.0",
    "footer_status": "Ready",
    "footer_copyright": "© 2025 BackupWin - All rights reserved",

    # About dialog
    "about_title": "About BackupWin",
    "about_text": """
BackupWin - File Backup & Search Application
Version 1.0.0

A comprehensive Windows file backup and search solution
built with Python and CustomTkinter.

Features:
• Search files across all drives and folders
• Backup single files, multiple files, or entire folders
• Checksum verification for data integrity
• Restore files from backups
• Manage and organize backups

Developed with:
• Python 3.8+
• CustomTkinter for modern UI
• FastAPI for REST API backend
• PostgreSQL for data persistence

© 2025 BackupWin - All rights reserved
""",

    # Language
    "language": "Language:",
    "lang_english": "English",
    "lang_vietnamese": "Tiếng Việt",

    # Consolidate Tab
    "tab_consolidate": "Consolidate Files",
    "consolidate_title": "Consolidation Options",
    "consolidate_operation": "Operation Mode:",
    "consolidate_copy": "Copy files (keep originals)",
    "consolidate_move": "Move files (remove originals)",
    "consolidate_destination": "Destination Folder:",
    "consolidate_duplicate_handling": "Duplicate Handling:",
    "consolidate_skip": "Skip duplicates",
    "consolidate_rename": "Rename with suffix",
    "consolidate_overwrite": "Overwrite existing",
    "consolidate_preserve_structure": "Preserve folder structure",
    "consolidate_file_list": "File List",
    "btn_add_file": "➕ Add File",
    "btn_add_files": "➕ Add Multiple Files",
    "btn_add_from_folder": "📁 Add From Folder",
    "btn_remove_selected": "Remove Selected",
    "btn_clear_all": "Clear All",
    "btn_start_consolidate": "Start Consolidation",
    "btn_preview": "Preview",
    "consolidate_total_files": "Total: {count} files",
    "consolidate_total_size": "Size: {size}",
    "consolidate_successful": "Successful",
    "consolidate_skipped": "Skipped",
    "consolidate_failed": "Failed",

    # Consolidate Status
    "status_consolidating": "Consolidating...",
    "progress_consolidating": "Consolidating... ({current}/{total})",

    # Consolidate Messages
    "msg_no_files_selected": "Please add files to consolidate!",
    "msg_no_files_in_folder": "No files found in the selected folder.",
    "msg_files_added": "{count} file(s) added to the list.",
    "msg_error_reading_folder": "Error reading folder: {error}",
    "msg_use_remove_button": "Use the X button next to each file to remove it.",
    "msg_confirm_clear_all": "Are you sure you want to clear all {count} file(s) from the list?",
    "msg_preview_info": "Preview:\n\nTotal Files: {count}\nTotal Size: {size} MB\nPotential Conflicts: {conflicts}\n\nNote: Conflicts will be handled based on your duplicate handling setting.",
    "msg_confirm_consolidate": "Consolidate {count} file(s)?\n\nOperation: {operation}\nDestination: {destination}\n\nThis will {operation} all files to the destination folder.",
    "msg_consolidation_complete": "Consolidation completed!\n\nSuccessful: {successful}\nSkipped: {skipped}\nFailed: {failed}\nTotal Size: {size} MB",
    "preview_title": "Consolidation Preview",
    "confirm": "Confirm",
    "warning": "Warning",
    "success": "Success",

    # Duplicate Finder Tab
    "tab_duplicate_finder": "Find Duplicates",
    "duplicate_scan_options": "Scan Options",
    "duplicate_scan_paths": "Folders to Scan:",
    "duplicate_no_paths": "No folders selected",
    "btn_add_folder": "Add Folder",
    "btn_clear_paths": "Clear All",
    "duplicate_comparison_method": "Comparison Method:",
    "duplicate_method_quick": "Quick (Size then Hash) - Fastest",
    "duplicate_method_hash": "Hash (MD5) - Most Accurate",
    "duplicate_method_size_name": "Size + Name - Fast but less accurate",
    "duplicate_options": "Options:",
    "duplicate_min_size": "Minimum File Size (bytes):",
    "duplicate_file_types": "File Types (comma-separated):",
    "duplicate_file_types_placeholder": "e.g., .jpg,.png,.pdf (leave empty for all)",
    "duplicate_recursive": "Scan subdirectories",
    "btn_start_scan": "Start Scan",

    # Duplicate Results
    "duplicate_files_scanned": "Files Scanned",
    "duplicate_groups_found": "Duplicate Groups",
    "duplicate_space_wasted": "Space Wasted",
    "duplicate_results": "Scan Results",
    "duplicate_no_results": "No scan results yet. Click 'Start Scan' to begin.",
    "duplicate_no_duplicates_found": "✓ No duplicate files found! Your storage is clean.",
    "duplicate_copies": "copies",
    "duplicate_each": "each",
    "duplicate_wasted": "wasted",
    "duplicate_files_in_group": "Files in this group:",
    "btn_delete_duplicates": "Delete Duplicates",
    "btn_move_duplicates": "Move Duplicates",

    # Duplicate Messages
    "duplicate_no_paths_selected": "Please add at least one folder to scan!",
    "duplicate_invalid_size": "Invalid minimum file size. Please enter a number.",
    "duplicate_path_already_added": "This path is already in the scan list.",
    "duplicate_select_folder": "Select Folder to Scan",
    "duplicate_select_move_folder": "Select Destination for Duplicates",
    "status_scanning": "Scanning for duplicates...",
    "progress_scanning": "Scanning... ({current}/{total} files)",
    "duplicate_scan_complete": "Scan completed!\n\nDuplicate Groups: {groups}\nTotal Duplicates: {duplicates}\nSpace Wasted: {space} MB",
    "duplicate_confirm_delete": "Delete {count} duplicate file(s)?\n\nThe original file will be kept:\n{kept}\n\nThis action cannot be undone!",
    "duplicate_delete_success": "Deleted: {deleted}\nFailed: {failed}",
    "duplicate_move_success": "Moved: {moved}\nFailed: {failed}\n\nTo: {destination}",
}
