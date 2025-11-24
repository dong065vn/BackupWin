# BackupWin

A comprehensive Windows file backup and search application with both Desktop GUI and RESTful API.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

## 🎯 Features at a Glance

- 🖥️ **Beautiful Desktop GUI** - User-friendly interface built with CustomTkinter
- 🔍 **Smart File Search** - Find files across all drives with pattern matching
- 💾 **Reliable Backup** - Backup files with MD5 checksum verification
- ♻️ **Easy Restore** - Restore files and manage backups effortlessly
- 🌐 **REST API** - Full-featured API for automation and integration
- 📊 **PostgreSQL Database** - Track all backup operations and history

## 🚀 Quick Start

### ⚡ Super Quick Start (Easiest!)

**For English:**
- **Double-click** `run_gui_english.bat`

**For Vietnamese (Tiếng Việt):**
- **Double-click** `run_gui_vietnamese.bat`

**First time setup:**
1. **Double-click** `QUICK_START.bat`
2. Choose option 1 (Install and Run)
3. Wait for installation and the GUI will open automatically!

### Option 2: API Server (For Developers)

**Prerequisites:**
- Python 3.8 or higher
- PostgreSQL database
- Windows operating system

**Installation:**

1. Clone or download the project

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows Command Prompt
venv\Scripts\activate

# Windows PowerShell
venv\Scripts\Activate.ps1

# Git Bash
source venv/Scripts/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure environment:
```bash
# Copy example environment file
copy .env.example .env

# Edit .env file with your settings
notepad .env
```

6. Start the API server:
```bash
python main.py
```

7. Open API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Features

### File Search
- Search files across all Windows drives
- Pattern matching with wildcards (*, ?)
- Filter by file extension
- Recursive and non-recursive search
- Calculate folder sizes

### Backup Operations
- Backup single or multiple files
- Backup entire folders with filters
- Checksum verification (MD5)
- Preserve directory structure
- Custom backup destinations
- Restore files from backups
- List and manage backups

### API
- RESTful API with FastAPI
- Automatic API documentation (Swagger)
- Request/response validation
- CORS support
- Comprehensive error handling

## API Examples

### Get Available Drives
```bash
curl http://localhost:8000/api/v1/drives
```

### Search for Files
```bash
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d "{\"search_path\": \"C:\\\\\", \"file_pattern\": \"*.pdf\", \"max_results\": 10}"
```

### Backup a File
```bash
curl -X POST http://localhost:8000/api/v1/backup/file \
  -H "Content-Type: application/json" \
  -d "{\"source_file\": \"C:\\\\important.pdf\"}"
```

### Backup a Folder
```bash
curl -X POST http://localhost:8000/api/v1/backup/folder \
  -H "Content-Type: application/json" \
  -d "{\"source_folder\": \"C:\\\\MyDocuments\", \"file_extensions\": [\".pdf\", \".docx\"]}"
```

### List Backups
```bash
curl http://localhost:8000/api/v1/backups
```

## Testing

Run tests with pytest:
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_backup.py

# Run with coverage
pytest --cov=app
```

## Project Structure

```
BackupWin/
├── app/                    # Main application package
│   ├── api/               # API routes
│   ├── core/              # Configuration, database, logging
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   └── services/          # Business logic
├── tests/                 # Test suite
├── logs/                  # Application logs
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
└── .env                  # Environment configuration
```

## Configuration

Edit `.env` file to configure:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/backupwin_db

# API
API_HOST=0.0.0.0
API_PORT=8000

# Backup
DEFAULT_BACKUP_PATH=C:\Backups

# Logging
LOG_LEVEL=INFO
```

## 📚 Documentation

- [📖 GUI_USER_GUIDE.md](GUI_USER_GUIDE.md) - Complete user guide for desktop application
- [📘 PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Detailed technical documentation
- [📋 BACKUP_FEATURE_TASK.md](BACKUP_FEATURE_TASK.md) - Feature implementation details
- [🌐 API Docs](http://localhost:8000/docs) - Interactive API documentation (when server running)

## 🖥️ Desktop Application Guide

### Main Features

#### 1. 🔍 Search Files Tab
- Search in specific folders or across all drives
- Use wildcards: `*.pdf`, `report_*`, `test_?.txt`
- Filter by file extension
- View file details (name, path, size, date)
- Export search results

#### 2. 💾 Backup Files Tab
**Three Backup Modes:**
- **Single File** - Backup one file
- **Multiple Files** - Backup several files at once
- **Entire Folder** - Backup complete folders with filters

**Features:**
- Preserve directory structure
- MD5 checksum verification
- Custom backup destinations
- Progress tracking
- Detailed backup logs

#### 3. ♻️ Restore & Manage Tab
- View all available backups
- Restore files with integrity verification
- Manage backups (open folder, delete)
- Filter backups by date
- See backup statistics

### Building Standalone Executable

Create a portable .exe file that runs without Python:

```bash
# Run the build script
build_exe.bat
```

The executable will be created in `dist\BackupWin.exe`

**Advantages:**
- No Python installation required
- Single file distribution
- Faster startup time
- Can be run from USB drive

## 🔧 Available Scripts

| Script | Description |
|--------|-------------|
| `QUICK_START.bat` | Quick start menu with all options |
| `run_gui_english.bat` | Launch GUI in English |
| `run_gui_vietnamese.bat` | Launch GUI in Vietnamese (Tiếng Việt) |

## ❗ Troubleshooting

### "ModuleNotFoundError: No module named 'customtkinter'"

**Solution:**
1. Run `install_gui_deps.bat`
2. Wait for installation to complete
3. Run `run_gui.bat` again

### Python not found
**Solution:**
1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. During installation, **CHECK** ☑ "Add Python to PATH"
3. Restart your computer
4. Run `install_gui_deps.bat`

### Application won't start
**Solution:**
1. Delete the `venv` folder
2. Run `install_gui_deps.bat`
3. Run `run_gui.bat`

### Build executable fails
**Solution:**
```bash
# Clean and rebuild
rmdir /s /q build
rmdir /s /q dist
pip install --upgrade pyinstaller
build_exe.bat
```

### Database connection error (API only)
- Ensure PostgreSQL is installed and running
- Verify DATABASE_URL in .env file
- Create the database if it doesn't exist
- **Note:** GUI app works WITHOUT database

### Permission errors during search
- Some system folders require administrator access
- The application will skip inaccessible files
- Run as administrator if needed

## License

This project is provided as-is for educational and personal use.

## Support

For issues, questions, or contributions, please refer to the project documentation.
