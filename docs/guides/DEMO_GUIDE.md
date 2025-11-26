# 🎬 DEMO - Hướng dẫn Test Tính Năng Cross-Module Integration

## 🚀 Cách Test Nhanh (5 phút)

### Bước 1: Khởi động ứng dụng
```bash
cd c:\Project\BackupWin
python gui_app_i18n.py
```

---

### Bước 2: Test Send to Backup

#### **Scenario**: Tìm file và backup ngay

**Các bước thực hiện:**

1. **Tab Search Files** (Tab đầu tiên - icon 🔍)
   - Ở "Search Path": Click `Browse` → Chọn thư mục bất kỳ (VD: `D:/Documents`)
   - Ở "File Pattern": Để mặc định `*`
   - Ở "Max Results": Để `100`
   - Click nút **"Search"** (màu xanh)

2. **Xem kết quả**
   - Sau vài giây, sẽ thấy danh sách file trong bảng "Search Results"
   - VD: Tìm được 17 files, tổng 45.2 MB

3. **Test Send to Backup**
   - Scroll xuống dưới bảng kết quả
   - Click nút **"📤 Send to Backup"** (nút đầu tiên, màu xanh)

4. **Quan sát kết quả**
   - ✅ Hiện popup: "17 file(s) sent to Backup Files!"
   - ✅ Click OK
   - ✅ **Tự động chuyển sang tab "Backup Files"** (tab thứ 2 - icon 💾)
   - ✅ Ở "Backup Mode" → tự động chọn "Multiple files"
   - ✅ Trong khung "Organization Log" → thấy:
     ```
     Info: 17 file(s) sent to Backup Files!
       1. D:/Documents/file1.pdf
       2. D:/Documents/file2.docx
       3. D:/Documents/file3.xlsx
       4. D:/Documents/file4.txt
       5. D:/Documents/file5.png
       ... and 12 more files
     ```

5. **Thực hiện Backup** (optional)
   - Ở "Destination Folder": Click `Browse` → Chọn nơi lưu backup (VD: `E:/Backups`)
   - Click nút **"Start Backup"** (màu xanh lá)
   - Xem progress bar và log chi tiết
   - Kết quả: "Backup completed successfully!"

**✅ PASS** nếu thấy:
- Tab tự động chuyển
- Danh sách file hiện trong log
- Backup mode = "Multiple files"

---

### Bước 3: Test Send to Consolidate

#### **Scenario**: Tìm file rải rác và gom vào 1 chỗ

**Các bước thực hiện:**

1. **Quay lại Tab Search** (Click vào tab "Search Files" - icon 🔍)

2. **Tìm kiếm lại**
   - Có thể tìm kiếm mới hoặc dùng kết quả cũ
   - VD: Tìm file PDF: Extension = `.pdf`
   - Click "Search"

3. **Test Send to Consolidate**
   - Click nút **"📤 Send to Consolidate"** (nút giữa, màu xanh lá)

4. **Quan sát kết quả**
   - ✅ Hiện popup: "5 file(s) sent to Consolidate Files!"
   - ✅ Click OK
   - ✅ **Tự động chuyển sang tab "Consolidate Files"** (tab thứ 3 - icon 📁)
   - ✅ Thấy popup: "5 file(s) added to the list."
   - ✅ Trong "File List" → thấy 5 file, mỗi file có:
     ```
     📄 file1.pdf          2.5 MB    [X]
     📄 file2.pdf          1.2 MB    [X]
     📄 file3.pdf          3.8 MB    [X]
     📄 file4.pdf          0.9 MB    [X]
     📄 file5.pdf          1.5 MB    [X]

     Total: 5 files
     Size: 9.9 MB
     ```

5. **Thực hiện Consolidation** (optional)
   - Chọn "Operation Mode": Copy files
   - Ở "Destination Folder": Click `Browse` → Chọn thư mục đích
   - Click "Start Consolidation"
   - Xem progress và kết quả

**✅ PASS** nếu thấy:
- Tab tự động chuyển
- File hiện trong File List
- Đếm đúng số file và size

---

### Bước 4: Test Send to Organizer

#### **Scenario 1**: File từ cùng 1 thư mục (Easy case)

**Các bước thực hiện:**

1. **Quay lại Tab Search**

2. **Tìm trong 1 thư mục cụ thể**
   - Search Path: Chọn 1 thư mục cụ thể (VD: `D:/Downloads`)
   - Recursive: ☐ Bỏ check (chỉ tìm trong thư mục đó, không tìm con)
   - Click "Search"

3. **Test Send to Organizer**
   - Click nút **"📤 Send to Organizer"** (nút thứ 3, màu xanh)

4. **Quan sát kết quả**
   - ✅ Hiện popup: "8 file(s) sent to Organize Files!"
   - ✅ Click OK
   - ✅ **Tự động chuyển sang tab "Organize Files"** (tab thứ 5 - icon 🗂️)
   - ✅ Trong "Organization Log" → thấy:
     ```
     Info: Set source folder to D:/Downloads
     Contains 8 file(s) from search
     ```
   - ✅ Ở "Source Folder" → tự động điền: `D:/Downloads`

#### **Scenario 2**: File từ nhiều thư mục (Complex case)

**Các bước thực hiện:**

1. **Quay lại Tab Search**

2. **Tìm trong nhiều thư mục**
   - Search Path: Chọn thư mục gốc (VD: `D:/`)
   - Recursive: ☑ Check (tìm trong tất cả thư mục con)
   - Pattern: Tìm file cụ thể (VD: `*.jpg`)
   - Max Results: 20
   - Click "Search"

3. **Test Send to Organizer**
   - Click nút **"📤 Send to Organizer"**

4. **Quan sát kết quả**
   - ✅ Hiện popup: "15 file(s) sent to Organize Files!"
   - ✅ Click OK
   - ✅ **Tự động chuyển sang tab "Organize Files"**
   - ✅ Hiện popup cảnh báo:
     ```
     Files are from 8 different folders.

     File Organizer works on entire folders.
     Please select a source folder manually.
     ```
   - ✅ Trong log → thấy:
     ```
     Info: Received 15 files from 8 folders
     ```
   - ✅ "Source Folder" → KHÔNG tự động điền (vì nhiều folder)

**✅ PASS** nếu thấy:
- **Case 1** (1 folder): Source folder tự động điền
- **Case 2** (nhiều folder): Hiện cảnh báo, không auto-fill

---

## 🎯 Quick Verification Checklist

Test tất cả 3 chức năng trong **5 phút**:

### ✅ Send to Backup
- [ ] Click nút → hiện popup xác nhận
- [ ] Tab tự động chuyển sang Backup
- [ ] File paths hiện trong log
- [ ] Backup mode = "Multiple files"

### ✅ Send to Consolidate
- [ ] Click nút → hiện popup xác nhận
- [ ] Tab tự động chuyển sang Consolidate
- [ ] File hiện trong File List
- [ ] Total files và Size đúng

### ✅ Send to Organizer
- [ ] Click nút → hiện popup xác nhận
- [ ] Tab tự động chuyển sang Organizer
- [ ] **Nếu 1 folder**: Source folder tự động điền
- [ ] **Nếu nhiều folder**: Hiện cảnh báo

---

## 📹 Visual Demo (Text-based)

### Demo Flow: Search → Backup

```
┌─────────────────────────────────────────────┐
│ 🔍 Search Files                             │
├─────────────────────────────────────────────┤
│ Search Path: [D:/Documents        ] [📁]   │
│ Pattern:     [*                   ]        │
│ Max Results: [100                 ]        │
│                                             │
│ [🔍 Search]                                 │
└─────────────────────────────────────────────┘
         │
         │ (User clicks Search)
         ▼
┌─────────────────────────────────────────────┐
│ Search Results                              │
├─────────────────────────────────────────────┤
│ Files Found: 17    Total Size: 45.2 MB     │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │Name      │Path           │Size │Modified││
│ │file1.pdf │D:/Docs/...    │2.5MB│2025... ││
│ │file2.doc │D:/Docs/...    │1.2MB│2025... ││
│ │...       │...            │...  │...     ││
│ └─────────────────────────────────────────┘ │
│                                             │
│ [📤 Send to Backup] [📤 Send to Consolidate]│
│                     [📤 Send to Organizer]  │
└─────────────────────────────────────────────┘
         │
         │ (User clicks Send to Backup)
         ▼
┌─────────────────────────────────────────────┐
│ ℹ️ Info                                     │
│ 17 file(s) sent to Backup Files!           │
│                          [OK]               │
└─────────────────────────────────────────────┘
         │
         │ (User clicks OK)
         ▼
┌─────────────────────────────────────────────┐
│ 💾 Backup Files ◄── AUTOMATICALLY SWITCHED  │
├─────────────────────────────────────────────┤
│ Backup Mode:                                │
│ ○ Single file                               │
│ ⦿ Multiple files  ◄── AUTO SELECTED        │
│ ○ Folder                                    │
│                                             │
│ Source: [17 files selected]                │
│ Destination: [              ] [📁]         │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ Organization Log                        │ │
│ │                                         │ │
│ │ Info: 17 file(s) sent to Backup Files! │ │
│ │   1. D:/Documents/file1.pdf             │ │
│ │   2. D:/Documents/file2.docx            │ │
│ │   3. D:/Documents/file3.xlsx            │ │
│ │   4. D:/Documents/file4.txt             │ │
│ │   5. D:/Documents/file5.png             │ │
│ │   ... and 12 more files                 │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ [Start Backup]                              │
└─────────────────────────────────────────────┘
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "No files found" warning khi click Send
**Nguyên nhân**: Chưa search hoặc search không có kết quả
**Giải pháp**: Thực hiện search trước khi click Send

### Issue 2: Tab không tự động chuyển
**Nguyên nhân**: Callback chưa được setup
**Giải pháp**: Restart ứng dụng, kiểm tra code trong `_setup_tab_connections()`

### Issue 3: File không hiện trong destination tab
**Nguyên nhân**: Lỗi trong `receive_files()` method
**Giải pháp**: Kiểm tra log file `server.log` để xem lỗi chi tiết

---

## 📊 Expected Results Summary

| Action | Expected Result |
|--------|----------------|
| Click "Send to Backup" | ✅ Switch to Backup tab<br>✅ Mode = Multiple files<br>✅ Files in log |
| Click "Send to Consolidate" | ✅ Switch to Consolidate tab<br>✅ Files in File List<br>✅ Total count updated |
| Click "Send to Organizer"<br>(1 folder) | ✅ Switch to Organizer tab<br>✅ Source folder auto-filled<br>✅ Log shows folder |
| Click "Send to Organizer"<br>(multi folder) | ✅ Switch to Organizer tab<br>✅ Warning popup<br>✅ Source NOT filled |

---

## 🎉 Success Criteria

Tính năng **HOẠT ĐỘNG TốT** nếu:

1. ✅ Tất cả 3 nút "Send to" đều hiển thị
2. ✅ Click vào bất kỳ nút nào → tab tự động chuyển
3. ✅ File data được truyền sang tab đích
4. ✅ UI cập nhật đúng (log, file list, count, size...)
5. ✅ Hiển thị popup thông báo rõ ràng
6. ✅ Không có lỗi trong console/log

---

**Ready to test?** Chạy ngay:
```bash
python gui_app_i18n.py
```

Good luck! 🚀
