# Build Integration - Folders Included in EXE

## Tổng Quan

Document này mô tả tất cả các folders và resources được tích hợp vào file EXE của BackupWin.

## Folders Được Tích Hợp

### 1. Resource Folders (User Resources)

Ba folders chứa các công cụ và phần mềm hữu ích:

#### **Cai dat phan mem/**
- **Kích thước:** 1.2 MB
- **Nội dung:** Công cụ cài đặt phần mềm tự động
  - `Cai dat phan mem.exe` (1.18 MB)
- **Đường dẫn trong EXE:** `_internal/Cai dat phan mem/`

#### **OFFICE, WINRAR, IDM/**
- **Kích thước:** 1.7 MB
- **Nội dung:** Microsoft Office tools, WinRAR, IDM
  - `7z.dll`, `7z.exe` - 7-Zip compression tools
  - `Main.bat` - Batch script chính
  - `O10OSPP.VBS` - Office 2010 activation script
  - `O16OSPP.VBS` - Office 2016 activation script
  - `rarreg.key` - WinRAR registration key
  - `SLERROR.XML` - Office licensing error definitions
- **Đường dẫn trong EXE:** `_internal/OFFICE, WINRAR, IDM/`

#### **Sao luu du lieu/**
- **Kích thước:** 1.4 MB
- **Nội dung:** Công cụ sao lưu dữ liệu
  - `Sao luu du lieu.exe` (1.37 MB)
- **Đường dẫn trong EXE:** `_internal/Sao luu du lieu/`

**Tổng dung lượng resources:** ~4.3 MB

### 2. Configuration Files

#### **config/file_categories.json**
- **Kích thước:** ~3 KB
- **Mục đích:** Cấu hình categories cho File Organizer
- **Đường dẫn trong EXE:** `_internal/config/file_categories.json`

#### **.env.example**
- **Kích thước:** ~400 bytes
- **Mục đích:** Template cho environment variables
- **Đường dẫn trong EXE:** `_internal/.env.example`

## PyInstaller Configuration

### build_exe.spec - Data Section

```python
datas=[
    ('.env.example', '.'),
    ('config/file_categories.json', 'config'),
    ('Cai dat phan mem', 'Cai dat phan mem'),
    ('OFFICE, WINRAR, IDM', 'OFFICE, WINRAR, IDM'),
    ('Sao luu du lieu', 'Sao luu du lieu'),
],
```

### Cách Thức Hoạt Động

1. **Build Time:**
   - PyInstaller đọc `datas` section
   - Copy tất cả folders/files vào archive
   - Nén và đóng gói vào single EXE

2. **Runtime:**
   - EXE extract resources vào temp folder `_MEI*`
   - Ứng dụng truy cập qua `sys._MEIPASS`
   - Resources có sẵn cho toàn bộ session

## Truy Cập Resources Trong Code

### File Organizer Config

```python
# app/services/file_organizer.py
if getattr(sys, 'frozen', False):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS  # PyInstaller temp folder
    else:
        base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

config_path = os.path.join(base_path, 'config', 'file_categories.json')
```

### Resources Tab

```python
# gui/resources_tab_i18n.py
resource_folders = {
    "software_installer": "Cai dat phan mem",
    "office_tools": "OFFICE, WINRAR, IDM",
    "backup_tools": "Sao luu du lieu"
}

folder_path = Path(folder_name)  # Tương đối từ working directory
```

## Build Process

### Command
```bash
pyinstaller build_exe.spec --clean --noconfirm
```

### Output
```
dist/BackupWin.exe  # 26 MB (bao gồm tất cả resources)
```

### Breakdown
- Python runtime + dependencies: ~22 MB
- Resources folders: ~4.3 MB
- Application code: ~500 KB
- **Total:** ~26 MB

## Verification

### Kiểm Tra Resources Có Được Include

```python
import sys
import os
from pathlib import Path

if hasattr(sys, '_MEIPASS'):
    base = Path(sys._MEIPASS)
    print("Resources location:", base)
    print("\nFolders:")
    for folder in ['Cai dat phan mem', 'OFFICE, WINRAR, IDM', 'Sao luu du lieu']:
        folder_path = base / folder
        print(f"  - {folder}: {'✓' if folder_path.exists() else '✗'}")
```

### Test Commands

```bash
# Test from source
python gui_app_i18n.py

# Test EXE
./dist/BackupWin.exe

# Verify resources in Resources tab
# Navigate to "Tài Nguyên" tab and check all 3 categories
```

## Thêm Folders Mới

### Bước 1: Thêm Vào build_exe.spec

```python
datas=[
    ('.env.example', '.'),
    ('config/file_categories.json', 'config'),
    ('Cai dat phan mem', 'Cai dat phan mem'),
    ('OFFICE, WINRAR, IDM', 'OFFICE, WINRAR, IDM'),
    ('Sao luu du lieu', 'Sao luu du lieu'),
    ('New Folder', 'New Folder'),  # ← Thêm folder mới
],
```

### Bước 2: Update Resources Tab (nếu cần)

```python
# gui/resources_tab_i18n.py
self.resource_folders = {
    "software_installer": "Cai dat phan mem",
    "office_tools": "OFFICE, WINRAR, IDM",
    "backup_tools": "Sao luu du lieu",
    "new_category": "New Folder",  # ← Thêm category mới
}
```

### Bước 3: Thêm Translations

```python
# gui/locales/vi.py
"resources_new_category": "Danh Mục Mới",
"resources_new_category_desc": "Mô tả folder mới",

# gui/locales/en.py
"resources_new_category": "New Category",
"resources_new_category_desc": "Description of new folder",
```

### Bước 4: Rebuild

```bash
pyinstaller build_exe.spec --clean --noconfirm
```

## Best Practices

1. **Tổ Chức Folders:**
   - Tên folder rõ ràng, có ý nghĩa
   - Tránh ký tự đặc biệt trong tên
   - Sử dụng spaces hoặc underscores

2. **Kích Thước:**
   - Kiểm tra kích thước trước khi thêm
   - Folders quá lớn (>100MB) nên cân nhắc
   - Tổng EXE không nên >50MB

3. **Security:**
   - Không include files nhạy cảm
   - Không include passwords/keys thật
   - Sử dụng .gitignore cho sensitive files

4. **Testing:**
   - Test từ source trước
   - Build và test EXE
   - Verify resources accessible trong EXE

## Troubleshooting

### Folder Không Tìm Thấy

**Triệu chứng:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'Folder Name'
```

**Giải pháp:**
1. Kiểm tra folder có trong `datas` section
2. Rebuild với `--clean` flag
3. Verify đường dẫn tương đối đúng

### Resources Không Load

**Triệu chứng:**
```
⚠️ Folder not found: Folder Name
```

**Giải pháp:**
1. Kiểm tra `sys._MEIPASS` path
2. Verify folder structure trong temp
3. Check permissions

### Build Size Quá Lớn

**Triệu chứng:**
- EXE file >100MB
- Build time quá lâu

**Giải pháp:**
1. Review folders size
2. Xóa files không cần thiết
3. Compress files trước khi include
4. Sử dụng external download cho large files

## Version History

### v1.0.0 (2025-11-29)
- ✅ Tích hợp 3 resource folders
- ✅ Config file integration
- ✅ Resources Tab implementation
- ✅ Full documentation

## License

© 2025 BackupWin - All rights reserved
