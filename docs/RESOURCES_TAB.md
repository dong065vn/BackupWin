# Resources Tab - Module Tài Nguyên

## Tổng Quan
Module "Tài Nguyên" (Resources) là một tính năng mới được thêm vào BackupWin để quản lý và truy cập nhanh các công cụ và phần mềm hữu ích được tích hợp sẵn trong ứng dụng.

## Cấu Trúc Thư Mục

Module tích hợp 3 folder chính:

### 1. **Cài Đặt Phần Mềm** (`Cai dat phan mem`)
- **Mô tả**: Công cụ cài đặt phần mềm tự động
- **Nội dung**: Chứa file `Cai dat phan mem.exe` (1.18 MB)
- **Chức năng**: Tự động cài đặt các phần mềm cần thiết

### 2. **Office & Công Cụ** (`OFFICE, WINRAR, IDM`)
- **Mô tả**: Microsoft Office, WinRAR, IDM và các công cụ khác
- **Nội dung**:
  - `7z.dll`, `7z.exe` - 7-Zip compression tools
  - `Main.bat` - Batch script chính
  - `O10OSPP.VBS`, `O16OSPP.VBS` - Office activation scripts
  - `rarreg.key` - WinRAR registration key
  - `SLERROR.XML` - Office licensing error definitions

### 3. **Công Cụ Sao Lưu** (`Sao luu du lieu`)
- **Mô tả**: Công cụ sao lưu dữ liệu chuyên dụng
- **Nội dung**: Chứa file `Sao luu du lieu.exe` (1.37 MB)
- **Chức năng**: Công cụ sao lưu dữ liệu độc lập

## Tính Năng

### 1. **Hiển Thị Thông Tin File**
- Tên file với icon 📄
- Dung lượng file (MB)
- Đường dẫn file

### 2. **Thao Tác Với File**

#### a) **Mở Vị Trí** (Open Location)
- Mở folder chứa file trong File Explorer
- Phím tắt: Click vào nút "Mở Vị Trí"

#### b) **Chạy File** (Run File)
- Chỉ hiển thị cho file `.exe` và `.bat`
- Có xác nhận trước khi chạy
- Thông báo khi chạy thành công
- Xử lý lỗi chi tiết

#### c) **Copy Lên Desktop** (Copy to Desktop)
- Copy file ra Desktop
- Tự động đổi tên nếu file đã tồn tại
- Thông báo khi copy thành công

### 3. **Đa Ngôn Ngữ** (Multi-language Support)
- Tiếng Việt (Vietnamese)
- Tiếng Anh (English)

## Sử Dụng

### Bước 1: Mở Tab Resources
1. Khởi động BackupWin
2. Click vào tab "📦 Tài Nguyên" (hoặc "📦 Resources" nếu dùng tiếng Anh)

### Bước 2: Chọn Danh Mục
Chọn một trong 3 danh mục từ dropdown:
- Cài Đặt Phần Mềm
- Office & Công Cụ
- Công Cụ Sao Lưu

### Bước 3: Thao Tác Với File
Mỗi file sẽ hiển thị các nút:
- **Mở Vị Trí**: Mở folder chứa file
- **Chạy File**: Chạy file executable (chỉ .exe, .bat)
- **Copy Lên Desktop**: Copy file ra Desktop

## Cấu Trúc Code

### File Chính
- `gui/resources_tab_i18n.py` - Tab Resources với hỗ trợ đa ngôn ngữ

### Translations
**Vietnamese** (`gui/locales/vi.py`):
```python
"tab_resources": "Tài Nguyên"
"resources_title": "Quản Lý Tài Nguyên"
"resources_software_installer": "Cài Đặt Phần Mềm"
# ... và nhiều translations khác
```

**English** (`gui/locales/en.py`):
```python
"tab_resources": "Resources"
"resources_title": "Resource Management"
"resources_software_installer": "Software Installer"
# ... and more translations
```

### Build Configuration
Trong `build_exe.spec`:
```python
datas=[
    ('.env.example', '.'),
    ('Cai dat phan mem', 'Cai dat phan mem'),
    ('OFFICE, WINRAR, IDM', 'OFFICE, WINRAR, IDM'),
    ('Sao luu du lieu', 'Sao luu du lieu'),
],
hiddenimports=[
    # ...
    'gui.resources_tab_i18n',
    # ...
]
```

## Xử Lý Lỗi

### 1. Folder Không Tồn Tại
```
⚠️ Folder not found: [folder_name]
```

### 2. Folder Trống
```
📂 No files in this folder
```

### 3. Lỗi Đọc Folder
```
Error reading folder: [error details]
```

### 4. Lỗi Chạy File
```
Lỗi khi chạy file: [error details]
```

### 5. Lỗi Copy File
```
Lỗi khi copy file: [error details]
```

## Security & Best Practices

### 1. **Xác Nhận Trước Khi Chạy**
- Luôn hiển thị dialog xác nhận trước khi chạy file executable
- Tránh chạy file không mong muốn

### 2. **Xử Lý File Trùng**
- Tự động đổi tên file khi copy nếu đã tồn tại
- Format: `filename_1.exe`, `filename_2.exe`, ...

### 3. **Error Handling**
- Try-catch cho tất cả các thao tác file
- Hiển thị thông báo lỗi chi tiết cho user

## Tương Lai

### Tính Năng Có Thể Thêm
1. **Tìm Kiếm File**: Tìm kiếm nhanh file trong các danh mục
2. **Favorites**: Đánh dấu file yêu thích để truy cập nhanh
3. **File Info**: Hiển thị thông tin chi tiết hơn (ngày tạo, checksum, ...)
4. **Custom Categories**: Cho phép người dùng thêm danh mục tùy chỉnh
5. **Cloud Sync**: Đồng bộ resources với cloud storage

## Technical Details

### Dependencies
- `customtkinter` - Modern UI framework
- `pathlib` - Path manipulation
- `shutil` - File operations
- `subprocess` - Process execution
- `os` - OS operations

### Class Structure
```python
class ResourcesTab(ctk.CTkFrame):
    def __init__(self, parent)
    def _create_widgets(self)
    def _on_category_change(self, choice)
    def _load_category(self)
    def _create_file_card(self, parent, file_path, folder_path)
    def _open_folder(self, folder_path)
    def _run_file(self, file_path)
    def _copy_to_desktop(self, file_path)
```

## Changelog

### Version 1.0.0 (2025-11-29)
- ✨ Tính năng mới: Module Resources
- 📦 Tích hợp 3 folders: Cài đặt phần mềm, Office & Công cụ, Công cụ sao lưu
- 🌍 Hỗ trợ đa ngôn ngữ (Vietnamese/English)
- 🎨 UI hiện đại với card-based layout
- 🚀 Build vào EXE file với PyInstaller

## License
© 2025 BackupWin - All rights reserved
