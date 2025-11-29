# BackupWin - File Backup & Management Tool

> Ứng dụng sao lưu và quản lý file chuyên nghiệp cho Windows

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-Proprietary-red)

## 📋 Tổng Quan

BackupWin là ứng dụng desktop chuyên nghiệp cho Windows, cung cấp giải pháp toàn diện cho việc sao lưu, tìm kiếm, và quản lý file. Với giao diện hiện đại và nhiều tính năng mạnh mẽ, BackupWin giúp bạn quản lý dữ liệu một cách dễ dàng và hiệu quả.

### ✨ Tính Năng Chính

- **🔍 Tìm Kiếm File** - Tìm kiếm nhanh trên toàn bộ ổ đĩa
- **💾 Sao Lưu** - Sao lưu file/folder với nhiều tùy chọn
- **📁 Gộp File** - Tổng hợp file từ nhiều nguồn
- **🔄 Tìm File Trùng** - Phát hiện và xóa file trùng lặp
- **🗂️ Sắp Xếp File** - Tự động phân loại file theo danh mục
- **📦 Tài Nguyên** - Quản lý công cụ và phần mềm tích hợp
- **⚙️ Khôi Phục** - Khôi phục và quản lý bản sao lưu

### 🌍 Đa Ngôn Ngữ

- Tiếng Việt
- English

## 🚀 Cài Đặt & Sử Dụng

### Cách 1: Chạy File EXE (Đơn Giản)

1. Tải file `BackupWin.exe` (26 MB)
2. Double-click để chạy
3. Không cần cài đặt Python hay dependencies

### Cách 2: Chạy Từ Source Code (Developer)

**Yêu cầu:**
- Python 3.8 trở lên
- Windows 10/11

**Các bước:**

```bash
# 1. Clone repository
git clone <repository-url>
cd BackupWin

# 2. Tạo virtual environment
python -m venv venv

# 3. Kích hoạt virtual environment
venv\Scripts\activate

# 4. Cài đặt dependencies
pip install -r requirements.txt

# 5. Chạy ứng dụng
python gui_app_i18n.py
```

## 📦 Build EXE

Để build file EXE từ source code:

```bash
# Kích hoạt virtual environment
venv\Scripts\activate

# Build EXE
pyinstaller build_exe.spec --clean --noconfirm

# File output: dist/BackupWin.exe
```

## 🎯 Hướng Dẫn Sử Dụng

### 1. Tìm Kiếm File

1. Mở tab **"🔍 Tìm Kiếm File"**
2. Chọn đường dẫn tìm kiếm hoặc tìm trên tất cả ổ đĩa
3. Nhập pattern tìm kiếm (VD: `*.pdf`, `report_*`)
4. Click **"Tìm Kiếm"**
5. Kết quả hiển thị với tên, đường dẫn, kích thước
6. Có thể gửi kết quả sang các module khác

### 2. Sao Lưu File

1. Mở tab **"💾 Sao Lưu File"**
2. Chọn chế độ: File đơn / Nhiều file / Toàn bộ thư mục
3. Chọn nguồn cần sao lưu
4. Chọn đích (hoặc để mặc định)
5. Tùy chọn: Giữ cấu trúc, tạo checksum
6. Click **"Bắt Đầu Sao Lưu"**

### 3. Gộp File

1. Mở tab **"📁 Gộp File"**
2. Thêm file từ nhiều nguồn khác nhau
3. Chọn thư mục đích
4. Chọn chế độ: Copy hoặc Move
5. Xử lý file trùng: Skip / Rename / Overwrite
6. Click **"Bắt Đầu Gộp File"**

### 4. Tìm File Trùng

1. Mở tab **"🔄 Tìm File Trùng"**
2. Thêm các thư mục cần quét
3. Chọn phương pháp so sánh
4. Click **"Bắt Đầu Quét"**
5. Xem kết quả với nhóm file trùng
6. Xóa hoặc di chuyển file trùng

### 5. Sắp Xếp File

1. Mở tab **"🗂️ Sắp Xếp File"**
2. Chọn thư mục nguồn
3. Chọn thư mục đích
4. Chọn chế độ: Copy / Move / Delete
5. Click **"Bắt Đầu Sắp Xếp"**
6. File tự động phân loại vào các thư mục

### 6. Tài Nguyên

1. Mở tab **"📦 Tài Nguyên"**
2. Chọn danh mục:
   - **Cài Đặt Phần Mềm** - Công cụ cài đặt tự động
   - **Office & Công Cụ** - 7-Zip, Office scripts, WinRAR key
   - **Công Cụ Sao Lưu** - Backup utility
3. Mỗi file có 3 thao tác:
   - 📂 Mở vị trí
   - ▶️ Chạy file (.exe, .bat)
   - 📋 Copy lên Desktop

### 7. Khôi Phục & Quản Lý

1. Mở tab **"⚙️ Khôi Phục & Quản Lý"**
2. Xem danh sách bản sao lưu
3. Chọn bản cần khôi phục
4. Chọn vị trí khôi phục
5. Click **"Khôi Phục File"**

## 📂 Cấu Trúc Dự Án

```
BackupWin/
├── app/                          # Backend logic
│   ├── core/                     # Core modules
│   │   ├── config.py            # Configuration
│   │   └── logger.py            # Logging
│   └── services/                # Business logic
│       ├── backup.py            # Backup service
│       ├── file_search.py       # Search service
│       ├── file_consolidation.py # Consolidation
│       ├── duplicate_finder.py  # Duplicate detection
│       └── file_organizer.py    # File organization
│
├── gui/                          # Frontend GUI
│   ├── locales/                 # Translations
│   │   ├── en.py               # English
│   │   └── vi.py               # Vietnamese
│   ├── backup_tab_i18n.py      # Backup tab
│   ├── consolidate_tab_i18n.py # Consolidate tab
│   ├── duplicate_finder_tab_i18n.py # Duplicate tab
│   ├── organizer_tab_i18n.py   # Organizer tab
│   ├── resources_tab_i18n.py   # Resources tab
│   ├── restore_tab_i18n.py     # Restore tab
│   ├── search_tab_i18n.py      # Search tab
│   ├── components.py            # Reusable components
│   ├── i18n.py                  # i18n handler
│   ├── styles.py                # UI styles
│   └── tab_header.py            # Tab header
│
├── config/                       # Configuration files
│   └── file_categories.json    # File categories
│
├── Cai dat phan mem/            # Software installer
│   └── Cai dat phan mem.exe
│
├── OFFICE, WINRAR, IDM/         # Office tools
│   ├── 7z.dll, 7z.exe
│   ├── Main.bat
│   ├── O10OSPP.VBS, O16OSPP.VBS
│   ├── rarreg.key
│   └── SLERROR.XML
│
├── Sao luu du lieu/             # Backup utility
│   └── Sao luu du lieu.exe
│
├── dist/                         # Build output
│   └── BackupWin.exe            # Executable (26 MB)
│
├── .env.example                  # Environment template
├── build_exe.spec               # PyInstaller spec
├── gui_app_i18n.py              # Main entry point
├── requirements.txt             # Dependencies
└── README.md                     # This file
```

## 🛠️ Dependencies

### Core
- **Python 3.8+**
- **customtkinter** - Modern UI framework
- **Pillow** - Image processing
- **pydantic** - Data validation

### Services
- **loguru** - Advanced logging
- **send2trash** - Safe file deletion
- **python-dotenv** - Environment management

### Build
- **pyinstaller** - EXE builder

Xem file `requirements.txt` để biết chi tiết đầy đủ.

## 📊 Thông Tin Build

### BackupWin.exe (26 MB)

```
Composition:
├── Python Runtime       14 MB  (54%)
├── Dependencies         8 MB   (31%)
├── Resource Files       4 MB   (15%)
└── Application Code     500 KB
```

### Resource Files (9 files - 4.05 MB)

**Cai dat phan mem/** (1 file - 1.13 MB)
- Cai dat phan mem.exe

**OFFICE, WINRAR, IDM/** (7 files - 1.62 MB)
- 7z.dll, 7z.exe
- Main.bat
- O10OSPP.VBS, O16OSPP.VBS
- rarreg.key
- SLERROR.XML

**Sao luu du lieu/** (1 file - 1.30 MB)
- Sao luu du lieu.exe

## 🔧 Configuration

### File Categories (config/file_categories.json)

File Organizer tự động phân loại file theo các danh mục:

- **Documents** - PDF, Word, Excel, PowerPoint
- **Images** - JPG, PNG, GIF, SVG
- **Videos** - MP4, AVI, MKV
- **Music** - MP3, WAV, FLAC
- **Archives** - ZIP, RAR, 7Z
- **Code Projects** - Auto-detect project folders
- **Others** - Các file khác

### Environment Variables (.env)

```env
DATABASE_URL=             # PostgreSQL connection (optional)
OPENROUTER_API_KEY=      # AI features (future)
```

## 🎨 UI Features

### Modern Design
- Clean Figma-inspired interface
- Professional card-based layout
- Smooth tab transitions
- Optimized for 7 tabs without overlap

### Responsive
- Auto-adjust to screen size
- Even tab distribution
- Compact spacing

### Dark/Light Mode
- Currently: Light mode
- Easy to extend for dark mode

## 🔐 Security

### Best Practices
- ✅ Safe file deletion (trash bin)
- ✅ Checksum verification (MD5)
- ✅ Confirmation dialogs for destructive actions
- ✅ No automatic file execution
- ✅ Temp files auto-cleanup on exit

### Resource Files
- Extracted to temp folder at runtime
- Read-only access
- Auto-delete when app closes
- No persistent modification

## 🐛 Troubleshooting

### Ứng dụng không chạy
**Giải pháp:**
1. Kiểm tra Windows version (Windows 10/11)
2. Disable antivirus tạm thời
3. Chạy as Administrator
4. Download lại file EXE

### File không tìm thấy trong Resources
**Giải pháp:**
1. Restart ứng dụng
2. Check folder tồn tại trong build
3. Rebuild từ source code

### Lỗi "Module not found"
**Giải pháp (Source code):**
```bash
pip install -r requirements.txt --force-reinstall
```

### Build lỗi
**Giải pháp:**
```bash
# Clean và rebuild
rm -rf build dist
pyinstaller build_exe.spec --clean --noconfirm
```

## 📝 Development

### Coding Standards
- Python 3.8+ syntax
- Type hints encouraged
- Docstrings for functions
- Error handling required

### Adding New Features

1. **Backend Service** - Thêm vào `app/services/`
2. **GUI Tab** - Thêm vào `gui/`
3. **Translations** - Update `gui/locales/vi.py` và `en.py`
4. **Integration** - Import trong `gui_app_i18n.py`

### Testing

```bash
# Run from source
python gui_app_i18n.py

# Test specific module
python -m app.services.backup

# Build and test
pyinstaller build_exe.spec --clean
./dist/BackupWin.exe
```

## 🔄 Version History

### v1.0.0 (2025-11-29)
- ✨ Initial release
- ✅ 7 functional modules
- ✅ Multi-language support
- ✅ 9 resource files integrated
- ✅ Modern optimized UI
- ✅ Complete documentation

## 📞 Support

Nếu gặp vấn đề hoặc cần hỗ trợ:
1. Check Troubleshooting section
2. Review logs trong `logs/app.log`
3. Contact developer

## 📄 License

© 2025 BackupWin - All rights reserved.

Proprietary software - Unauthorized distribution prohibited.

---

**BackupWin** - Your Complete File Management Solution 🚀
