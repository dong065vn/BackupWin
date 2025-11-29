# Resource Files Manifest - BackupWin EXE

## Tổng Quan
Document này liệt kê tất cả các files được tích hợp vào BackupWin.exe

## Files Được Đóng Gói

### 📦 Tổng Số
- **Folders:** 3
- **Files:** 9
- **Tổng dung lượng:** 4.05 MB

---

## Chi Tiết Từng Folder

### 1️⃣ Cai dat phan mem/

**Số files:** 1
**Dung lượng:** 1.13 MB

| File | Kích thước | Loại | Mô tả |
|------|-----------|------|-------|
| `Cai dat phan mem.exe` | 1.13 MB | Executable | Công cụ cài đặt phần mềm tự động |

**Truy cập trong app:**
- Resources tab → Cài Đặt Phần Mềm
- Có thể chạy trực tiếp từ GUI

---

### 2️⃣ OFFICE, WINRAR, IDM/

**Số files:** 7
**Dung lượng:** 1.62 MB

| File | Kích thước | Loại | Mô tả |
|------|-----------|------|-------|
| `7z.dll` | 1.11 MB | DLL | 7-Zip compression library |
| `7z.exe` | 0.32 MB | Executable | 7-Zip command line tool |
| `Main.bat` | 0.01 MB | Batch Script | Script chính để kích hoạt Office |
| `O10OSPP.VBS` | 0.05 MB | VBScript | Office 2010 activation script |
| `O16OSPP.VBS` | 0.09 MB | VBScript | Office 2016 activation script |
| `rarreg.key` | 0.00 MB | Key File | WinRAR registration key |
| `SLERROR.XML` | 0.03 MB | XML | Office licensing error definitions |

**Truy cập trong app:**
- Resources tab → Office & Công Cụ
- Main.bat có thể chạy để kích hoạt Office
- 7z.exe có thể dùng để nén/giải nén

---

### 3️⃣ Sao luu du lieu/

**Số files:** 1
**Dung lượng:** 1.30 MB

| File | Kích thước | Loại | Mô tả |
|------|-----------|------|-------|
| `Sao luu du lieu.exe` | 1.30 MB | Executable | Công cụ sao lưu dữ liệu chuyên dụng |

**Truy cập trong app:**
- Resources tab → Công Cụ Sao Lưu
- Có thể chạy độc lập

---

## PyInstaller Configuration

### build_exe.spec
```python
datas=[
    ('.env.example', '.'),
    ('config/file_categories.json', 'config'),
    ('Cai dat phan mem', 'Cai dat phan mem'),      # ← 1 file
    ('OFFICE, WINRAR, IDM', 'OFFICE, WINRAR, IDM'), # ← 7 files
    ('Sao luu du lieu', 'Sao luu du lieu'),         # ← 1 file
],
```

## Cách Hoạt Động

### 1. Build Time
```
PyInstaller đọc build_exe.spec
    ↓
Copy tất cả 9 files từ 3 folders
    ↓
Compress và đóng gói vào BackupWin.exe
    ↓
Tạo archive PKG
    ↓
Nhúng vào EXE final
```

### 2. Runtime
```
User chạy BackupWin.exe
    ↓
PyInstaller bootloader khởi động
    ↓
Extract PKG archive vào temp folder (_MEIxxxxxx)
    ↓
All 9 files available tại sys._MEIPASS/<folder>/<file>
    ↓
Application truy cập files qua Path API
```

### 3. Access Pattern

**Trong Code:**
```python
from pathlib import Path
import sys

# Get base path
if getattr(sys, 'frozen', False):
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).parent

# Access resource file
resource_file = base_path / "OFFICE, WINRAR, IDM" / "Main.bat"
```

**Trong Resources Tab:**
```python
# gui/resources_tab_i18n.py
folder_name = "OFFICE, WINRAR, IDM"
folder_path = Path(folder_name)

for file in folder_path.iterdir():
    if file.is_file():
        # Display file in GUI
        # Allow user to run/copy
```

## Verification

### Check Files in Running EXE

```python
import sys
from pathlib import Path

if hasattr(sys, '_MEIPASS'):
    temp_dir = Path(sys._MEIPASS)
    print(f"Temp extract location: {temp_dir}")

    # Check each folder
    for folder in ['Cai dat phan mem', 'OFFICE, WINRAR, IDM', 'Sao luu du lieu']:
        folder_path = temp_dir / folder
        if folder_path.exists():
            print(f"\n{folder}:")
            for file in folder_path.iterdir():
                print(f"  ✓ {file.name}")
```

### Expected Output When EXE Runs
```
Temp extract location: C:\Users\xxx\AppData\Local\Temp\_MEI123456

Cai dat phan mem:
  ✓ Cai dat phan mem.exe

OFFICE, WINRAR, IDM:
  ✓ 7z.dll
  ✓ 7z.exe
  ✓ Main.bat
  ✓ O10OSPP.VBS
  ✓ O16OSPP.VBS
  ✓ rarreg.key
  ✓ SLERROR.XML

Sao luu du lieu:
  ✓ Sao luu du lieu.exe
```

## User Access via GUI

### Resources Tab Features

Mỗi file trong 3 folders có thể:

1. **📂 Mở Vị Trí** - Mở folder chứa file trong Explorer
2. **▶️ Chạy File** - Chạy trực tiếp .exe và .bat files
3. **📋 Copy Lên Desktop** - Copy file ra Desktop để dùng

### Example: Running Main.bat

```
User clicks Resources tab
    → Select "Office & Công Cụ"
    → See Main.bat in list
    → Click "Chạy File"
    → Confirmation dialog
    → Main.bat executes from temp location
    → Office activation script runs
```

## File Types Breakdown

| Loại File | Số lượng | Tổng KB | % |
|-----------|----------|---------|---|
| .exe | 3 | 3,700 | 91% |
| .dll | 1 | 1,136 | 28% |
| .vbs | 2 | 143 | 3.5% |
| .bat | 1 | 14 | 0.3% |
| .key | 1 | 0.5 | 0.01% |
| .xml | 1 | 35 | 0.9% |
| **Total** | **9** | **4,050** | **100%** |

## Security Notes

⚠️ **Important:**
- Tất cả files được extract vào temp folder khi chạy
- Temp folder tự động xóa khi đóng app
- Files không thể modify trong EXE (read-only)
- Không lưu persistent data trong temp location

✅ **Safe Practices:**
- .exe files chỉ chạy khi user click "Chạy File"
- Có confirmation dialog trước khi execute
- Log tất cả file operations
- Check file integrity trước khi run

## Build Statistics

### Final EXE Breakdown
```
BackupWin.exe (26 MB)
├── Python Runtime         (~14 MB)
├── Dependencies           (~8 MB)
├── Application Code       (~500 KB)
└── Resource Files         (4.05 MB)
    ├── Cai dat phan mem/  (1.13 MB)
    ├── OFFICE, WINRAR, IDM/ (1.62 MB)
    └── Sao luu du lieu/   (1.30 MB)
```

### Compression Ratio
- **Uncompressed:** ~30 MB
- **Compressed (UPX):** 26 MB
- **Ratio:** ~87%

## Troubleshooting

### Files Not Found
**Triệu chứng:** ResourceNotFound error
**Giải pháp:**
1. Verify files exist trong source folders
2. Check build_exe.spec datas section
3. Rebuild với --clean flag

### Cannot Execute .exe
**Triệu chứng:** Permission denied khi chạy file
**Giải pháp:**
1. Files trong temp có thể bị block bởi antivirus
2. Copy file ra desktop trước khi chạy
3. Add exception trong antivirus

### File Missing After Close
**Triệu chứng:** File không tìm thấy sau khi đóng app
**Giải pháp:**
- Temp files tự động xóa (expected behavior)
- Sử dụng "Copy Lên Desktop" để persistent storage

## Version History

### v1.0.0 (2025-11-29)
✅ Initial integration of 9 resource files
✅ 3 folders with full file listing
✅ Resources tab access implementation
✅ Complete documentation

---

**Tất cả 9 files đã được tích hợp hoàn chỉnh vào BackupWin.exe!** ✓
