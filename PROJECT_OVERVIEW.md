# BackupWin - Windows File Backup Application

## Project Overview

BackupWin is a comprehensive Windows file backup and search application built with Python. It provides robust functionality for backing up files, searching across drives and folders, and managing backup operations through a RESTful API.

## Project Structure

```
BackupWin/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py              # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Application configuration
│   │   ├── database.py            # Database connection & session
│   │   └── logger.py              # Logging configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── backup.py              # Database models (BackupJob, BackupFile, etc.)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── backup.py              # Pydantic schemas for API requests/responses
│   └── services/
│       ├── __init__.py
│       ├── backup.py              # Backup service implementation
│       ├── file_search.py         # File search service implementation
│       ├── file_consolidation.py  # File consolidation service implementation
│       └── duplicate_finder.py    # Duplicate file finder service implementation
├── gui/
│   ├── __init__.py
│   ├── components.py              # Reusable GUI components with i18n
│   ├── styles.py                  # UI styling constants
│   ├── i18n.py                    # Internationalization manager
│   ├── locales/
│   │   ├── __init__.py
│   │   ├── en.py                  # English translations
│   │   └── vi.py                  # Vietnamese translations
│   ├── search_tab_i18n.py         # Search tab with i18n support
│   ├── backup_tab_i18n.py         # Backup tab with i18n support
│   ├── consolidate_tab_i18n.py    # Consolidate tab with i18n support
│   ├── duplicate_finder_tab_i18n.py # Duplicate finder tab with i18n support
│   └── restore_tab_i18n.py        # Restore tab with i18n support
├── tests/
│   ├── __init__.py
│   ├── test_api.py                # API endpoint tests
│   ├── test_backup.py             # Backup service tests
│   └── test_file_search.py        # File search service tests
├── migrations/                    # Database migrations
├── logs/                          # Application logs directory
├── venv/                          # Virtual environment (not committed)
├── .env                           # Environment variables (not committed)
├── .env.example                   # Example environment configuration
├── .language_config.json          # Language preference storage (auto-generated)
├── .gitignore                     # Git ignore rules
├── CLAUDE.md                      # Project instructions for AI agents
├── PROJECT_OVERVIEW.md            # This file - Detailed technical documentation
├── README.md                      # English README
├── README_VI.md                   # Vietnamese README
├── QUICK_START.bat                # Quick start menu with installation options
├── run_gui_english.bat            # Launch GUI in English (main launcher)
├── run_gui_vietnamese.bat         # Launch GUI in Vietnamese (main launcher)
├── build_exe.spec                 # PyInstaller spec for building executable
├── gui_app_i18n.py                # GUI application with i18n (main entry)
├── main.py                        # FastAPI application entry point
├── requirements.txt               # Python dependencies (full)
├── requirements-dev.txt           # Development dependencies
└── requirements-gui.txt           # GUI-only dependencies
```

### Directory Explanations:

- **app/**: Main application package containing all core functionality
  - **api/**: REST API endpoints and routing
  - **core/**: Core utilities (config, database, logging)
  - **models/**: SQLAlchemy database models
  - **schemas/**: Pydantic models for data validation
  - **services/**: Business logic for backup and file search operations

- **gui/**: Desktop GUI application with multi-language support
  - **components.py**: Reusable UI components (Card, Button, InfoCard, etc.)
  - **styles.py**: UI styling constants and color schemes
  - **i18n.py**: Internationalization system for language switching
  - **locales/**: Translation files for supported languages (English, Vietnamese)
  - **search_tab_i18n.py**: File search interface with i18n
  - **backup_tab_i18n.py**: Backup interface with i18n
  - **consolidate_tab_i18n.py**: File consolidation interface with i18n
  - **duplicate_finder_tab_i18n.py**: Duplicate file finder interface with i18n
  - **restore_tab_i18n.py**: Restore and manage interface with i18n

- **migrations/**: Database migration scripts
  - SQL files for schema updates and data migrations

- **tests/**: Comprehensive test suite using pytest
- **logs/**: Application log files (auto-created)
- **venv/**: Python virtual environment (excluded from git)

## Features

### 1. File Search Capabilities
- **Search in specific folders**: Find files in any directory with pattern matching
- **Search across all drives**: Automatically detect and search all available drives on Windows
- **Pattern matching**: Support for wildcard patterns (*, ?) for flexible file searching
- **Extension filtering**: Filter files by specific extensions (e.g., .txt, .pdf, .docx)
- **Recursive search**: Option to search in subdirectories
- **Folder size calculation**: Calculate total size of folders with file count
- **Get available drives**: List all accessible drives on the system

### 2. Backup Operations
- **Single file backup**: Backup individual files with checksum verification
- **Multiple files backup**: Batch backup multiple files at once
- **Folder backup**: Backup entire folders with filtering options
- **Preserve structure**: Maintain original folder structure in backups
- **Checksum verification**: MD5 hash verification for data integrity
- **Timestamped backups**: Automatic timestamping for backup organization
- **Custom destinations**: Specify custom backup locations or use default
- **File restoration**: Restore files from backups with integrity verification
- **Backup management**: List, view, and delete backups

### 3. File Consolidation
- **Gather multiple files**: Consolidate files from different locations into one folder
- **Flexible operation modes**: Copy (keep originals) or Move (remove originals)
- **Smart duplicate handling**: Skip, rename with suffix, or overwrite existing files
- **Preserve structure option**: Maintain original folder hierarchy or create flat structure
- **Interactive file list**: Add files individually, in bulk, or from entire folders
- **Preview before action**: See what will happen before consolidating
- **Progress tracking**: Real-time progress updates during consolidation
- **Detailed reporting**: Statistics on successful, skipped, and failed operations

### 4. Duplicate File Finder
- **Intelligent scanning**: Find duplicate files using multiple comparison methods
- **Multiple algorithms**: Hash (MD5), Size+Name, or Quick (hybrid) comparison
- **Flexible filters**: Filter by minimum file size, file types, and recursive scanning
- **Grouped results**: Duplicates organized in groups with statistics
- **Space analysis**: Calculate wasted disk space from duplicates
- **Batch actions**: Delete or move duplicate files while keeping originals
- **Smart selection**: Auto-select best file to keep based on path and date
- **Expandable groups**: View all files in each duplicate group before taking action

### 5. Database Storage
- **Backup job tracking**: Store backup job metadata and status
- **File tracking**: Track individual files within backup jobs
- **Search history**: Log search operations for analytics
- **Backup scheduling**: Support for scheduled backup operations (schema ready)

### 6. RESTful API
- **FastAPI framework**: High-performance async API
- **Swagger documentation**: Auto-generated API documentation at `/docs`
- **CORS support**: Cross-origin resource sharing enabled
- **Streaming support**: Built-in support for long-running operations
- **Error handling**: Comprehensive error handling with detailed messages
- **Request validation**: Automatic request validation using Pydantic

### 7. Logging & Monitoring
- **Structured logging**: Using Loguru for beautiful, informative logs
- **File and console output**: Logs to both file and console
- **Log rotation**: Automatic log rotation (10MB) with 7-day retention
- **Compression**: Old logs automatically compressed to save space
- **Log levels**: Configurable log levels (DEBUG, INFO, WARNING, ERROR)

### 8. Desktop GUI Application
- **Modern UI**: Built with CustomTkinter for a modern, clean interface
- **Multi-language Support**: Full internationalization (i18n) system
  - English and Vietnamese languages fully supported
  - Language preference saved and persisted
  - All UI elements translate dynamically
- **Five Main Tabs**:
  - **Search Tab**: Interactive file search with pattern matching and filters
  - **Backup Tab**: Three backup modes (single file, multiple files, folder)
  - **Consolidate Tab**: Gather and organize files from multiple locations
  - **Duplicate Finder Tab**: Find and manage duplicate files to save disk space
  - **Restore Tab**: View, manage, and restore backups with verification
- **Quick Start Menu**: Easy-to-use batch file menu system
- **Standalone Executable**: Build standalone .exe with PyInstaller
- **Real-time Progress**: Progress bars and status updates for long operations
- **Responsive Design**: Adaptive layout with scrollable content areas

## Dependencies

### Core Dependencies
- **FastAPI** (0.115.0): Modern web framework for building APIs
- **Uvicorn** (0.32.0): Lightning-fast ASGI server
- **Pydantic** (2.9.2): Data validation using Python type hints
- **SQLAlchemy** (2.0.36): SQL toolkit and ORM
- **PostgreSQL** (psycopg2-binary 2.9.10): Database driver
- **Loguru** (0.7.3): Beautiful and powerful logging

### Utility Dependencies
- **python-dotenv** (1.0.1): Environment variable management
- **aiofiles** (24.1.0): Async file operations
- **watchdog** (6.0.0): File system event monitoring
- **python-magic-bin** (0.4.14): File type detection (Windows)
- **tqdm** (4.67.0): Progress bars for long operations

### Cloud Storage (Optional)
- **boto3** (1.35.65): AWS SDK for Cloudflare R2 integration

### Testing
- **pytest** (8.3.4): Testing framework
- **pytest-asyncio** (0.24.0): Async test support
- **httpx** (0.28.1): HTTP client for testing API endpoints

### GUI Dependencies
- **customtkinter** (5.2.2): Modern UI framework for desktop application
- **pillow** (10.4.0): Image processing for GUI icons and graphics
- **pyinstaller** (6.11.1): Build standalone executables

## API Routes

### Search Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/drives` | Get all available drives on system |
| POST | `/api/v1/search` | Search files in specific path |
| POST | `/api/v1/search/all-drives` | Search across all drives |
| GET | `/api/v1/folder-size` | Calculate folder size |

### Backup Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/backup/file` | Backup single file |
| POST | `/api/v1/backup/files` | Backup multiple files |
| POST | `/api/v1/backup/folder` | Backup entire folder |
| POST | `/api/v1/restore` | Restore file from backup |
| GET | `/api/v1/backups` | List all backups |
| DELETE | `/api/v1/backups` | Delete specific backup |

### System Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API info |
| GET | `/api/v1/health` | Health check endpoint |
| GET | `/docs` | Swagger API documentation |
| GET | `/redoc` | ReDoc API documentation |

## Environment Configuration

Create a `.env` file based on `.env.example`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/backupwin_db

# API
API_HOST=0.0.0.0
API_PORT=8000

# Backup
DEFAULT_BACKUP_PATH=C:\Backups
MAX_BACKUP_SIZE_GB=100

# Logging
LOG_LEVEL=INFO
LOG_FILE=server.log

# Cloudflare R2 (Optional)
R2_ACCOUNT_ID=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET_NAME=
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database server (optional for GUI-only usage)
- Windows operating system

### Quick Start (GUI Application)

1. **Run Quick Start Menu**:
   ```bash
   QUICK_START.bat
   ```

   Choose from the menu:
   - Option 1: Install dependencies and run GUI (first time)
   - Option 2: Run GUI in English
   - Option 3: Run GUI in Vietnamese
   - Option 4: Build standalone executable
   - Option 5: Test dependencies

2. **Or run directly**:
   ```bash
   # English version
   run_gui_english.bat

   # Vietnamese version
   run_gui_vietnamese.bat
   ```

### Setup Steps (Full Application with API)

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**:
   ```bash
   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   # For GUI only
   pip install -r requirements-gui.txt

   # For full application with API
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Update database connection and other settings

5. **Initialize database** (for API):
   ```bash
   # Database tables will be created automatically on first run
   python main.py
   ```

6. **Run application**:
   ```bash
   # GUI application
   python gui_app_i18n.py

   # API server
   python main.py
   ```

7. **Access API documentation** (if running API):
   - Open browser to `http://localhost:8000/docs`

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_backup.py

# Run with verbose output
pytest -v
```

## Usage Examples

### Search for Files

```python
import requests

# Search in specific folder
response = requests.post("http://localhost:8000/api/v1/search", json={
    "search_path": "C:\\Users",
    "file_pattern": "*.pdf",
    "recursive": True,
    "max_results": 100
})

print(response.json())
```

### Backup Files

```python
import requests

# Backup single file
response = requests.post("http://localhost:8000/api/v1/backup/file", json={
    "source_file": "C:\\important_document.pdf",
    "create_checksum": True
})

print(response.json())

# Backup entire folder
response = requests.post("http://localhost:8000/api/v1/backup/folder", json={
    "source_folder": "C:\\MyDocuments",
    "file_extensions": [".docx", ".pdf", ".xlsx"],
    "exclude_patterns": ["*.tmp", "__pycache__"]
})

print(response.json())
```

## Security Considerations

- Database credentials should be stored securely in `.env` file
- `.env` file is excluded from git via `.gitignore`
- API runs with CORS enabled (configure appropriately for production)
- File paths are validated to prevent directory traversal attacks
- Backup deletion restricted to backup base path
- All operations include comprehensive error handling

## Logging

Logs are written to:
- **Console**: Colored, formatted output for development
- **File**: `server.log` with rotation (10MB max, 7-day retention)

Log format includes:
- Timestamp
- Log level
- Module/function/line information
- Message content

## Future Enhancements

- [ ] Cloudflare R2 cloud backup integration
- [ ] Scheduled backup jobs (cron-based)
- [ ] Incremental backups (only changed files)
- [ ] Backup compression (zip/tar.gz)
- [ ] Email notifications for backup completion
- [ ] Web-based UI for backup management
- [ ] Backup encryption
- [ ] Multi-user support with authentication
- [ ] Backup versioning and history
- [ ] Network drive support

## Changelog

### Version 2.1.0 (Optimization - Removed Smart Classification)

**Changes Made:**
- Removed Smart File Classification feature to optimize and simplify the application
- Cleaned up codebase by removing unused classification-related files
- Reduced dependencies by removing 6 libraries (mutagen, PyPDF2, python-docx, openpyxl, filetype, send2trash)
- Simplified GUI from 6 tabs to 5 tabs
- Improved application performance and reduced memory footprint

**Files Removed:**
- `app/api/classification_routes.py`: Classification API endpoints
- `app/models/classification.py`: Classification database models
- `app/models/tag.py`: Tag models
- `app/models/organization.py`: Organization models
- `app/schemas/classification.py`: Classification schemas
- `app/schemas/tag.py`: Tag schemas
- `app/schemas/organization.py`: Organization schemas
- `app/services/file_classifier.py`: File classification service
- `app/services/content_analyzer.py`: Content analysis service
- `app/services/tag_manager.py`: Tag management service
- `app/services/file_organizer.py`: File organization service
- `app/services/classification_scanner.py`: Classification scanner
- `app/services/classification_report.py`: Classification reporting
- `gui/classification_tab_i18n.py`: Smart Classification GUI tab
- `migrations/001_add_classification_tables.sql`: Classification database migration

**Files Modified:**
- `main.py`: Removed classification router import and registration
- `gui_app_i18n.py`: Removed classification tab from GUI
- `gui/locales/en.py`: Removed classification-related translations
- `gui/locales/vi.py`: Removed classification-related translations
- `requirements.txt`: Removed 6 unnecessary dependencies
- `PROJECT_OVERVIEW.md`: Updated documentation to reflect changes

**Benefits:**
- Smaller application footprint
- Faster startup time
- Reduced complexity
- Easier maintenance
- Focus on core backup and search functionality

**Version**: 2.1.0
**Date**: 2025-11-08
**Status**: ✅ Completed & Tested

---

### Version 2.0.0 (Modern UI Redesign - Figma-Inspired Interface)

**Features Added:**
- Complete UI/UX redesign with modern Figma-inspired design
- Professional header with integrated tab navigation
- Custom tab system with smooth hover effects and animations
- Active tab indicator with 3px colored underline
- 8px grid system for consistent spacing
- Modern color palette with Primary Blue (#2563eb) and professional grays
- Enhanced typography scale with Segoe UI font family
- Icon + Text tab design for better UX
- Smooth content switching between tabs
- Modernized footer with cleaner styling
- Professional hover states and visual feedback

**New Components:**
- `gui/tab_header.py`: Modern tab navigation system (350+ lines)
  - `TabButton`: Individual tab with hover and active states
  - `TabHeader`: Main header component with title, tabs, and controls
  - `TabContent`: Content container with smooth switching

**Files Modified:**
- `gui_app_i18n.py`: Complete refactor to use new TabHeader component
  - Replaced `CTkTabview` with custom `TabHeader` and `TabContent`
  - Implemented `_create_modern_interface()` method
  - Added `_on_tab_change()` callback handler
  - Modernized footer styling
- `gui/styles.py`: Enhanced design system (200+ lines)
  - Added comprehensive tab design tokens
  - Documented 8px grid system
  - Added professional color palette
  - Typography scale documentation
  - Border radius system
  - Tab state colors and transitions

**Design System:**
- **8px Grid System**: SPACE_XXS (4px) to SPACE_XXL (48px)
- **Color Tokens**: Primary, Secondary, Status, Text, Background, Border
- **Typography**: Display (32px) to Tiny (10px) scale
- **Border Radius**: sm (6px) to xl (16px)
- **Tab States**: Active, Inactive, Hover with smooth transitions
- **Professional Icons**: 🔍 Search, 💾 Backup, 📁 Consolidate, 🔄 Duplicates, 🏷️ Classify, ⚙️ Restore

**User Experience Improvements:**
- Instant visual feedback on tab hover
- Clear active tab indication
- Hand cursor on interactive elements
- Clean, uncluttered interface
- Professional polish with pixel-perfect alignment
- Consistent spacing following design system

**Documentation:**
- `UI_REDESIGN.md`: Complete redesign documentation with technical details
- Comprehensive design system documentation
- Component architecture explanation
- Migration notes and testing verification

**Breaking Changes:**
- Removed dependency on `CTkTabview`
- Custom tab implementation (backward compatible with tab content)

**Version**: 2.0.0
**Date**: 2025-11-08
**Status**: ✅ Completed & Tested

---

### Version 1.4.0 (Duplicate File Finder)

**Features Added:**
- Duplicate File Finder functionality
- New "Find Duplicates" tab in GUI
- Multiple comparison methods (Hash, Size+Name, Quick hybrid)
- Smart filtering options (min size, file types, recursive scanning)
- Grouped duplicate display with expandable details
- Batch operations: Delete or move duplicates
- Space waste analysis and statistics
- Auto-select best file to keep
- Real-time progress tracking
- Full i18n support (English/Vietnamese)

**Files Created:**
- `app/services/duplicate_finder.py`: Core duplicate finding service (450+ lines)
- `gui/duplicate_finder_tab_i18n.py`: GUI tab with i18n support (600+ lines)

**Files Modified:**
- `gui_app_i18n.py`: Added Duplicate Finder tab
- `gui/locales/en.py`: Added 40+ English translation keys
- `gui/locales/vi.py`: Added 40+ Vietnamese translation keys
- `PROJECT_OVERVIEW.md`: Updated with new feature documentation

**Use Cases:**
- Clean up photo collections with duplicates
- Find duplicate downloads and documents
- Reclaim wasted disk space
- Organize messy file structures
- Identify redundant backups

**Performance:**
- Quick mode: 2-3x faster than full hash
- Hash mode: 100% accurate duplicate detection
- Handles thousands of files efficiently
- Memory-efficient streaming hash calculation

### Version 1.3.0 (File Consolidation Feature)

**Features Added:**
- File Consolidation functionality
- New "Consolidate Files" tab in GUI
- Gather multiple files from different locations into one folder
- Flexible operation modes: Copy or Move
- Smart duplicate handling: Skip, Rename, or Overwrite
- Preserve folder structure option
- Interactive file list management (add/remove files)
- Preview consolidation before executing
- Real-time progress tracking
- Detailed statistics and reporting

**Files Created:**
- `app/services/file_consolidation.py`: Core consolidation service
- `gui/consolidate_tab_i18n.py`: GUI tab with i18n support

**Files Modified:**
- `gui_app_i18n.py`: Added Consolidate tab
- `gui/locales/en.py`: Added English translations (40+ keys)
- `gui/locales/vi.py`: Added Vietnamese translations (40+ keys)
- `PROJECT_OVERVIEW.md`: Updated with new feature documentation

**Use Cases:**
- Organizing scattered project files into one location
- Collecting photos/documents from multiple drives
- Consolidating downloads from different folders
- Preparing files for archiving or sharing

### Version 1.2.0 (i18n Complete)

**Features Added:**
- Full internationalization (i18n) system
- English and Vietnamese language support
- Language preference persistence
- All UI components translated (100+ translation keys)
- Language selector in GUI header
- Language-specific launcher scripts

**Files Modified:**
- `gui_app_i18n.py`: Updated to use i18n tab components
- `gui/components.py`: Added i18n support for Browse button
- `gui/search_tab_i18n.py`: Complete i18n integration
- `gui/backup_tab_i18n.py`: Complete i18n integration
- `gui/restore_tab_i18n.py`: Complete i18n integration

### Version 1.1.0 (GUI Application)

**Features Added:**
- Desktop GUI application with CustomTkinter
- Modern, responsive UI design
- Three main tabs: Search, Backup, Restore
- Real-time progress tracking
- Visual backup management
- Standalone executable build support
- Quick start menu system
- Automatic dependency checking

**Files Created:**
- GUI application structure
- Reusable UI components
- Styling system
- Batch scripts for Windows
- GUI-specific requirements file

### Version 1.0.0 (Initial Release)

**Features Implemented:**
- File search functionality across drives and folders
- Single file, multiple files, and folder backup
- Database schema for tracking backups
- RESTful API with FastAPI
- Comprehensive error handling and logging
- Test suite with pytest
- API documentation with Swagger
- Checksum verification for data integrity
- Backup restoration functionality
- Folder size calculation

**Files Created:**
- Core application structure
- Database models and schemas
- Service layer (backup & file search)
- API endpoints
- Configuration management
- Test suite
- Documentation

---

**Last Updated**: 2025-11-08
**Version**: 2.1.0
**Status**: Production Ready
