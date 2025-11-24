# BackupWin - Phiên Bản Tiếng Việt

Ứng dụng sao lưu và tìm kiếm file toàn diện cho Windows với giao diện Desktop và REST API.

![Version](https://img.shields.io/badge/phiên_bản-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Platform](https://img.shields.io/badge/nền_tảng-Windows-lightgrey)

## 🎯 Tính Năng Nổi Bật

- 🖥️ **Giao Diện Desktop Đẹp** - Interface thân thiện xây dựng bằng CustomTkinter
- 🔍 **Tìm Kiếm File Thông Minh** - Tìm file trên tất cả ổ đĩa với pattern matching
- 💾 **Sao Lưu Tin Cậy** - Sao lưu file với xác minh checksum MD5
- ♻️ **Khôi Phục Dễ Dàng** - Khôi phục file và quản lý backup đơn giản
- 🌐 **REST API** - API đầy đủ tính năng cho tự động hóa
- 📊 **PostgreSQL Database** - Theo dõi tất cả thao tác sao lưu
- 🌍 **Đa Ngôn Ngữ** - Hỗ trợ Tiếng Việt và Tiếng Anh

## 🚀 Bắt Đầu Nhanh

### ⚡ Siêu Nhanh (Dễ Nhất!)

**Tiếng Anh:**
- **Click đúp** vào `run_gui_english.bat`

**Tiếng Việt:**
- **Click đúp** vào `run_gui_vietnamese.bat`

**Lần đầu sử dụng:**
1. **Click đúp** vào `QUICK_START.bat`
2. Chọn tùy chọn 1 (Cài đặt và Chạy)
3. Đợi cài đặt hoàn tất và ứng dụng sẽ tự động mở!

### Lựa Chọn 2: API Server (Cho Lập Trình Viên)

**Yêu Cầu:**
- Python 3.8 trở lên
- PostgreSQL database
- Windows operating system

**Cài Đặt:**

1. Clone hoặc download project

2. Tạo virtual environment:
```bash
python -m venv venv
```

3. Kích hoạt virtual environment:
```bash
# Windows Command Prompt
venv\Scripts\activate

# Windows PowerShell
venv\Scripts\Activate.ps1

# Git Bash
source venv/Scripts/activate
```

4. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

5. Cấu hình environment:
```bash
# Copy file mẫu
copy .env.example .env

# Chỉnh sửa file .env
notepad .env
```

6. Khởi động API server:
```bash
python main.py
```

7. Mở API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🌍 Chuyển Đổi Ngôn Ngữ

### Cách 1: Chạy Trực Tiếp Với Ngôn Ngữ Mong Muốn

```bash
# Tiếng Việt
run_gui_vietnamese.bat

# Tiếng Anh
run_gui_english.bat
```

### Cách 2: Thay Đổi Trong Ứng Dụng

1. Khởi động ứng dụng
2. Nhìn góc trên bên phải header
3. Click dropdown "Ngôn Ngữ:" / "Language:"
4. Chọn ngôn ngữ mong muốn
5. Khởi động lại ứng dụng

## 📚 Tài Liệu

- [📖 GUI_USER_GUIDE.md](GUI_USER_GUIDE.md) - Hướng dẫn đầy đủ (Tiếng Anh)
- [📘 PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Tài liệu kỹ thuật
- [📋 BACKUP_FEATURE_TASK.md](BACKUP_FEATURE_TASK.md) - Chi tiết triển khai
- [🌐 API Docs](http://localhost:8000/docs) - API documentation (khi server chạy)

## 🖥️ Hướng Dẫn Ứng Dụng Desktop

### Tính Năng Chính

#### 1. 🔍 Tab Tìm Kiếm File
- Tìm kiếm trong thư mục cụ thể hoặc tất cả ổ đĩa
- Sử dụng wildcards: `*.pdf`, `report_*`, `test_?.txt`
- Lọc theo phần mở rộng file
- Xem chi tiết file (tên, đường dẫn, dung lượng, ngày)

#### 2. 💾 Tab Sao Lưu File
**Ba Chế Độ Sao Lưu:**
- **File Đơn** - Sao lưu một file
- **Nhiều File** - Sao lưu nhiều file cùng lúc
- **Toàn Bộ Thư Mục** - Sao lưu toàn bộ thư mục với bộ lọc

**Tính Năng:**
- Giữ nguyên cấu trúc thư mục
- Xác minh MD5 checksum
- Tùy chỉnh đích sao lưu
- Theo dõi tiến trình
- Nhật ký sao lưu chi tiết

#### 3. ♻️ Tab Khôi Phục & Quản Lý
- Xem tất cả bản sao lưu khả dụng
- Khôi phục file với xác minh tính toàn vẹn
- Quản lý backup (mở thư mục, xóa)
- Lọc backup theo ngày
- Xem thống kê backup

### Build File Thực Thi Độc Lập

Tạo file .exe portable chạy mà không cần Python:

```bash
# Chạy script build
build_exe.bat
```

File thực thi sẽ được tạo trong `dist\BackupWin.exe`

**Ưu Điểm:**
- Không cần cài đặt Python
- Phân phối single file
- Khởi động nhanh hơn
- Có thể chạy từ USB drive

## 🔧 Các Script Khả Dụng

| Script | Mô Tả |
|--------|-------|
| `QUICK_START.bat` | Menu nhanh (dễ nhất) |
| `setup.bat` | Cài đặt tất cả dependencies |
| `install_gui_deps.bat` | Cài đặt GUI dependencies |
| `run_gui_vietnamese.bat` | Chạy phiên bản Tiếng Việt |
| `run_gui_english.bat` | Chạy phiên bản Tiếng Anh |
| `run_dev.bat` | Khởi động API server |
| `run_tests.bat` | Chạy tests |
| `build_exe.bat` | Build executable |
| `test_dependencies.bat` | Kiểm tra dependencies |

## ❗ Khắc Phục Sự Cố

### "ModuleNotFoundError: No module named 'customtkinter'"

**Giải pháp:**
```bash
install_gui_deps.bat
```

### Không tìm thấy Python

**Giải pháp:**
1. Download Python 3.8+ từ [python.org](https://www.python.org/downloads/)
2. Khi cài đặt, **TÍCH** ☑ "Add Python to PATH"
3. Khởi động lại máy tính
4. Chạy `install_gui_deps.bat`

### Ứng dụng không khởi động

**Giải pháp:**
1. Xóa thư mục `venv`
2. Chạy `install_gui_deps.bat`
3. Chạy `run_gui_vietnamese.bat`

### Build executable thất bại

**Giải pháp:**
```bash
# Dọn dẹp và build lại
rmdir /s /q build
rmdir /s /q dist
pip install --upgrade pyinstaller
build_exe.bat
```

### Lỗi kết nối database (chỉ API)
- Đảm bảo PostgreSQL đã cài đặt và đang chạy
- Kiểm tra DATABASE_URL trong file .env
- Tạo database nếu chưa tồn tại
- **Lưu ý:** GUI app hoạt động KHÔNG CẦN database

### Lỗi permission khi tìm kiếm
- Một số thư mục hệ thống yêu cầu quyền administrator
- Ứng dụng sẽ bỏ qua các file không truy cập được
- Chạy với quyền administrator nếu cần

## 📖 Ví Dụ Sử Dụng

### Tìm Kiếm File

```python
import requests

# Tìm trong thư mục cụ thể
response = requests.post("http://localhost:8000/api/v1/search", json={
    "search_path": "C:\\Users",
    "file_pattern": "*.pdf",
    "recursive": True,
    "max_results": 100
})

print(response.json())
```

### Sao Lưu File

```python
import requests

# Sao lưu file đơn
response = requests.post("http://localhost:8000/api/v1/backup/file", json={
    "source_file": "C:\\tai_lieu_quan_trong.pdf",
    "create_checksum": True
})

print(response.json())

# Sao lưu toàn bộ thư mục
response = requests.post("http://localhost:8000/api/v1/backup/folder", json={
    "source_folder": "C:\\Tai_Lieu",
    "file_extensions": [".docx", ".pdf", ".xlsx"],
    "exclude_patterns": ["*.tmp", "__pycache__"]
})

print(response.json())
```

## 🎓 Bước Tiếp Theo

### Cho Người Dùng
1. Đọc `GUI_USER_GUIDE.md` - Hướng dẫn đầy đủ
2. Cấu hình file `.env` - Đặt vị trí backup tùy chỉnh
3. Tạo backup đầu tiên - Làm theo hướng dẫn
4. Khám phá tất cả tính năng - Tìm kiếm, backup, khôi phục

### Cho Lập Trình Viên
1. Đọc `PROJECT_OVERVIEW.md` - Tài liệu kỹ thuật
2. Đọc `BACKUP_FEATURE_TASK.md` - Chi tiết triển khai
3. Chạy tests - `run_tests.bat`
4. Khởi động API server - `run_dev.bat`

## 🌟 Tính Năng Đa Ngôn Ngữ

### Cấu Trúc I18n

```
gui/
├── locales/
│   ├── en.py          # Bản dịch Tiếng Anh
│   ├── vi.py          # Bản dịch Tiếng Việt
│   └── __init__.py
└── i18n.py            # I18n manager
```

### Thêm Ngôn Ngữ Mới

1. Tạo file mới trong `gui/locales/` (ví dụ: `fr.py` cho Tiếng Pháp)
2. Copy cấu trúc từ `en.py` hoặc `vi.py`
3. Dịch tất cả các string
4. Thêm vào `gui/i18n.py`:
```python
from gui.locales.fr import fr

SUPPORTED_LANGUAGES = {
    'en': 'English',
    'vi': 'Tiếng Việt',
    'fr': 'Français'  # Thêm dòng này
}

TRANSLATIONS = {
    'en': en,
    'vi': vi,
    'fr': fr  # Thêm dòng này
}
```

## 💡 Tips & Tricks

### Tìm Kiếm Hiệu Quả
- Tìm trong thư mục cụ thể thay vì tất cả ổ đĩa
- Sử dụng bộ lọc extension
- Giới hạn số kết quả tối đa

### Quản Lý Backup
- Tạo backup định kỳ cho dữ liệu quan trọng
- Xóa backup cũ để tiết kiệm dung lượng
- Giữ nhiều phiên bản backup

### Tối Ưu Hiệu Suất
- Sử dụng phiên bản source (không phải executable) để khởi động nhanh hơn
- Đóng các ứng dụng khác khi backup dung lượng lớn
- Sử dụng SSD thay vì HDD

## 📞 Nhận Trợ Giúp

### Tài Liệu Ưu Tiên
1. `START_HERE.txt` - Tham khảo nhanh
2. `GUI_USER_GUIDE.md` - Hướng dẫn đầy đủ
3. `INSTALLATION_GUIDE.md` - Trợ giúp cài đặt
4. `FIX_NOTES.md` - Các vấn đề đã biết
5. `README.md` - Tổng quan

### Log Files
- `server.log` - Application logs
- Kiểm tra file này đầu tiên khi gặp sự cố
- Nằm trong thư mục gốc của project

### Testing Tools
- `test_dependencies.bat` - Kiểm tra cài đặt
- `QUICK_START.bat` option 4 - Kiểm tra nhanh

## 📄 Giấy Phép

Project này được cung cấp miễn phí cho mục đích giáo dục và sử dụng cá nhân.

## 🙏 Hỗ Trợ

Để biết các vấn đề, câu hỏi, hoặc đóng góp, vui lòng tham khảo tài liệu của project.

---

**Phiên bản:** 1.0.0
**Cập nhật lần cuối:** 2025-01-07
**Nền tảng:** Windows 7+
**Giấy phép:** Miễn phí cho sử dụng cá nhân
**Tình trạng:** ✅ Sẵn Sàng Sử Dụng
