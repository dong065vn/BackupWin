"""Vietnamese language translations"""

vi = {
    # Window titles
    "app_title": "BackupWin - Sao Lưu & Tìm Kiếm File",
    "app_subtitle": "Giải Pháp Sao Lưu File Cho Windows",

    # Tabs
    "tab_search": "Tìm Kiếm File",
    "tab_backup": "Sao Lưu File",
    "tab_restore": "Khôi Phục & Quản Lý",

    # Common buttons
    "btn_browse": "Duyệt",
    "btn_search": "Tìm Kiếm",
    "btn_backup": "Sao Lưu",
    "btn_restore": "Khôi Phục",
    "btn_delete": "Xóa",
    "btn_cancel": "Hủy",
    "btn_ok": "Đồng Ý",
    "btn_refresh": "Làm Mới",
    "btn_open_folder": "Mở Thư Mục",
    "btn_about": "Giới Thiệu",

    # Search Tab
    "search_title": "Tùy Chọn Tìm Kiếm",
    "search_path": "Đường Dẫn Tìm Kiếm:",
    "search_pattern": "Mẫu File:",
    "search_pattern_placeholder": "VD: *.pdf, test_*",
    "search_extension": "Phần Mở Rộng:",
    "search_extension_placeholder": "VD: .pdf, .docx (tùy chọn)",
    "search_recursive": "Tìm trong thư mục con",
    "search_case_sensitive": "Phân biệt chữ hoa/thường",
    "search_max_results": "Số Kết Quả Tối Đa:",
    "search_max_results_placeholder": "Để trống = không giới hạn",
    "btn_search_all_drives": "Tìm Trên Tất Cả Ổ Đĩa",
    "btn_get_drives": "Xem Các Ổ Đĩa",

    # Search Results
    "search_results": "Kết Quả Tìm Kiếm",
    "files_found": "File Tìm Thấy",
    "total_size": "Tổng Dung Lượng",
    "col_file_name": "Tên File",
    "col_path": "Đường Dẫn",
    "col_size": "Dung Lượng (MB)",
    "col_modified": "Ngày Sửa",

    # Backup Tab
    "backup_title": "Tùy Chọn Sao Lưu",
    "backup_mode": "Chế Độ Sao Lưu:",
    "backup_mode_single": "File Đơn",
    "backup_mode_multiple": "Nhiều File",
    "backup_mode_folder": "Toàn Bộ Thư Mục",
    "backup_source": "Nguồn:",
    "backup_destination": "Đích (tùy chọn):",
    "backup_preserve_structure": "Giữ nguyên cấu trúc thư mục",
    "backup_create_checksum": "Tạo mã kiểm tra (MD5)",
    "backup_extensions": "Phần Mở Rộng File (phân cách bằng dấu phẩy):",
    "backup_extensions_placeholder": "VD: .pdf,.docx,.xlsx",
    "backup_exclude": "Loại Trừ (phân cách bằng dấu phẩy):",
    "backup_exclude_placeholder": "VD: *.tmp,__pycache__",
    "btn_start_backup": "Bắt Đầu Sao Lưu",

    # Backup Stats
    "files_backed_up": "File Đã Sao Lưu",
    "backup_failed": "Thất Bại",
    "backup_log": "Nhật Ký Sao Lưu",

    # Restore Tab
    "restore_title": "Tùy Chọn Khôi Phục",
    "restore_backup_file": "File Sao Lưu:",
    "restore_destination": "Đích Khôi Phục:",
    "restore_verify_checksum": "Xác minh mã kiểm tra",
    "btn_restore_file": "Khôi Phục File",
    "restore_management": "Quản Lý Sao Lưu",
    "restore_filter_date": "Lọc Theo Ngày:",
    "restore_filter_placeholder": "YYYYMMDD (tùy chọn)",
    "available_backups": "Bản Sao Lưu Khả Dụng",
    "total_backup_size": "Tổng Dung Lượng Sao Lưu",
    "btn_open_backup_folder": "Mở Thư Mục Sao Lưu",

    # Status messages
    "status_ready": "Sẵn Sàng",
    "status_searching": "Đang Tìm Kiếm...",
    "status_backing_up": "Đang Sao Lưu...",
    "status_restoring": "Đang Khôi Phục...",
    "status_completed": "Hoàn Thành!",
    "status_error": "Lỗi",

    # Dialog messages
    "msg_select_path": "Vui lòng chọn đường dẫn tìm kiếm!",
    "msg_select_source": "Vui lòng chọn nguồn để sao lưu!",
    "msg_select_backup": "Vui lòng chọn file sao lưu!",
    "msg_select_destination": "Vui lòng chọn đích khôi phục!",
    "msg_search_all_drives": "Tìm kiếm trên tất cả các ổ đĩa. Có thể mất một chút thời gian.",
    "msg_confirm_delete": "Bạn có chắc muốn xóa bản sao lưu này?\n\n{path}\n\nHành động này không thể hoàn tác!",
    "msg_confirm_restore": "Khôi phục file từ:\n{backup}\n\nĐến:\n{destination}",
    "msg_backup_success": "Sao lưu hoàn tất thành công!",
    "msg_restore_success": "File đã được khôi phục thành công!\n\nĐích: {destination}",
    "msg_delete_success": "Đã xóa bản sao lưu thành công!",

    # Error messages
    "error": "Lỗi",
    "error_search_failed": "Tìm kiếm thất bại: {error}",
    "error_backup_failed": "Sao lưu thất bại: {error}",
    "error_restore_failed": "Khôi phục thất bại: {error}",
    "error_delete_failed": "Xóa thất bại: {error}",
    "error_load_backups": "Không thể tải danh sách sao lưu: {error}",
    "error_get_drives": "Không thể lấy danh sách ổ đĩa: {error}",

    # Info messages
    "info": "Thông Báo",
    "info_drives_found": "Tìm thấy {count} ổ đĩa:\n\n{drives}",
    "info_no_backups": "Không tìm thấy bản sao lưu",
    "msg_restart_language": "Vui lòng khởi động lại ứng dụng để thay đổi ngôn ngữ có hiệu lực.",

    # Progress messages
    "progress_found_files": "Đã tìm thấy {count} file",
    "progress_backing_up": "Đang sao lưu... ({current}/{total})",
    "progress_current_file": "Hiện tại: {file}...",

    # Footer
    "footer_version": "Phiên bản 1.0.0",
    "footer_status": "Sẵn Sàng",
    "footer_copyright": "© 2025 BackupWin - Bản quyền đã được bảo hộ",

    # About dialog
    "about_title": "Giới Thiệu BackupWin",
    "about_text": """
BackupWin - Ứng Dụng Sao Lưu & Tìm Kiếm File
Phiên bản 1.0.0

Giải pháp sao lưu file toàn diện cho Windows
được xây dựng bằng Python và CustomTkinter.

Tính năng:
• Tìm kiếm file trên tất cả ổ đĩa và thư mục
• Sao lưu file đơn, nhiều file hoặc toàn bộ thư mục
• Xác minh tính toàn vẹn bằng mã kiểm tra
• Khôi phục file từ bản sao lưu
• Quản lý và tổ chức các bản sao lưu

Phát triển bằng:
• Python 3.8+
• CustomTkinter cho giao diện hiện đại
• FastAPI cho REST API backend
• PostgreSQL để lưu trữ dữ liệu

© 2025 BackupWin - Bản quyền đã được bảo hộ
""",

    # Language
    "language": "Ngôn Ngữ:",
    "lang_english": "English",
    "lang_vietnamese": "Tiếng Việt",

    # Consolidate Tab
    "tab_consolidate": "Gộp File",
    "consolidate_title": "Tùy Chọn Gộp File",
    "consolidate_operation": "Chế Độ:",
    "consolidate_copy": "Copy file (giữ file gốc)",
    "consolidate_move": "Di chuyển file (xóa file gốc)",
    "consolidate_destination": "Thư Mục Đích:",
    "consolidate_duplicate_handling": "Xử Lý File Trùng Tên:",
    "consolidate_skip": "Bỏ qua file trùng",
    "consolidate_rename": "Đổi tên tự động",
    "consolidate_overwrite": "Ghi đè file cũ",
    "consolidate_preserve_structure": "Giữ cấu trúc thư mục",
    "consolidate_file_list": "Danh Sách File",
    "btn_add_file": "➕ Thêm File",
    "btn_add_files": "➕ Thêm Nhiều File",
    "btn_add_from_folder": "📁 Thêm Từ Thư Mục",
    "btn_remove_selected": "Xóa File Đã Chọn",
    "btn_clear_all": "Xóa Tất Cả",
    "btn_start_consolidate": "Bắt Đầu Gộp File",
    "btn_preview": "Xem Trước",
    "consolidate_total_files": "Tổng: {count} file",
    "consolidate_total_size": "Dung lượng: {size}",
    "consolidate_successful": "Thành Công",
    "consolidate_skipped": "Đã Bỏ Qua",
    "consolidate_failed": "Thất Bại",

    # Consolidate Status
    "status_consolidating": "Đang Gộp File...",
    "progress_consolidating": "Đang gộp file... ({current}/{total})",

    # Consolidate Messages
    "msg_no_files_selected": "Vui lòng thêm file để gộp!",
    "msg_no_files_in_folder": "Không tìm thấy file nào trong thư mục đã chọn.",
    "msg_files_added": "Đã thêm {count} file vào danh sách.",
    "msg_error_reading_folder": "Lỗi đọc thư mục: {error}",
    "msg_use_remove_button": "Sử dụng nút X bên cạnh mỗi file để xóa.",
    "msg_confirm_clear_all": "Bạn có chắc muốn xóa tất cả {count} file khỏi danh sách?",
    "msg_preview_info": "Xem trước:\n\nTổng File: {count}\nTổng Dung Lượng: {size} MB\nFile Có Thể Trùng: {conflicts}\n\nLưu ý: File trùng sẽ được xử lý dựa trên cài đặt xử lý file trùng của bạn.",
    "msg_confirm_consolidate": "Gộp {count} file?\n\nThao tác: {operation}\nĐích: {destination}\n\nThao tác này sẽ {operation} tất cả file vào thư mục đích.",
    "msg_consolidation_complete": "Gộp file hoàn tất!\n\nThành công: {successful}\nĐã bỏ qua: {skipped}\nThất bại: {failed}\nTổng dung lượng: {size} MB",
    "preview_title": "Xem Trước Gộp File",
    "confirm": "Xác Nhận",
    "warning": "Cảnh Báo",
    "success": "Thành Công",

    # Duplicate Finder Tab
    "tab_duplicate_finder": "Tìm File Trùng",
    "duplicate_scan_options": "Tùy Chọn Quét",
    "duplicate_scan_paths": "Thư Mục Quét:",
    "duplicate_no_paths": "Chưa chọn thư mục nào",
    "btn_add_folder": "Thêm Thư Mục",
    "btn_clear_paths": "Xóa Tất Cả",
    "duplicate_comparison_method": "Phương Pháp So Sánh:",
    "duplicate_method_quick": "Nhanh (Kích thước rồi Hash) - Nhanh nhất",
    "duplicate_method_hash": "Hash (MD5) - Chính xác nhất",
    "duplicate_method_size_name": "Kích thước + Tên - Nhanh nhưng kém chính xác",
    "duplicate_options": "Tùy Chọn:",
    "duplicate_min_size": "Kích Thước Tối Thiểu (bytes):",
    "duplicate_file_types": "Loại File (phân cách bằng dấu phẩy):",
    "duplicate_file_types_placeholder": "VD: .jpg,.png,.pdf (để trống = tất cả)",
    "duplicate_recursive": "Quét thư mục con",
    "btn_start_scan": "Bắt Đầu Quét",

    # Duplicate Results
    "duplicate_files_scanned": "File Đã Quét",
    "duplicate_groups_found": "Nhóm File Trùng",
    "duplicate_space_wasted": "Dung Lượng Lãng Phí",
    "duplicate_results": "Kết Quả Quét",
    "duplicate_no_results": "Chưa có kết quả. Nhấn 'Bắt Đầu Quét' để bắt đầu.",
    "duplicate_no_duplicates_found": "✓ Không tìm thấy file trùng lặp! Ổ đĩa của bạn sạch sẽ.",
    "duplicate_copies": "bản sao",
    "duplicate_each": "mỗi file",
    "duplicate_wasted": "lãng phí",
    "duplicate_files_in_group": "File trong nhóm này:",
    "btn_delete_duplicates": "Xóa File Trùng",
    "btn_move_duplicates": "Di Chuyển File Trùng",

    # Duplicate Messages
    "duplicate_no_paths_selected": "Vui lòng thêm ít nhất một thư mục để quét!",
    "duplicate_invalid_size": "Kích thước tối thiểu không hợp lệ. Vui lòng nhập số.",
    "duplicate_path_already_added": "Thư mục này đã có trong danh sách quét.",
    "duplicate_select_folder": "Chọn Thư Mục Để Quét",
    "duplicate_select_move_folder": "Chọn Thư Mục Đích Cho File Trùng",
    "status_scanning": "Đang quét file trùng...",
    "progress_scanning": "Đang quét... ({current}/{total} file)",
    "duplicate_scan_complete": "Quét hoàn tất!\n\nNhóm file trùng: {groups}\nTổng file trùng: {duplicates}\nDung lượng lãng phí: {space} MB",
    "duplicate_confirm_delete": "Xóa {count} file trùng?\n\nFile gốc sẽ được giữ lại:\n{kept}\n\nHành động này không thể hoàn tác!",
    "duplicate_delete_success": "Đã xóa: {deleted}\nThất bại: {failed}",
    "duplicate_move_success": "Đã di chuyển: {moved}\nThất bại: {failed}\n\nĐến: {destination}",

    # File Organizer Tab
    "tab_organizer": "Sắp Xếp File",
    "organizer_title": "Tùy Chọn Sắp Xếp File",
    "organizer_source": "Thư Mục Nguồn:",
    "organizer_destination": "Thư Mục Đích:",
    "organizer_options": "Tùy Chọn Sắp Xếp:",
    "organizer_mode": "Chế Độ Thao Tác:",
    "organizer_mode_copy": "Sao Chép (Giữ file gốc)",
    "organizer_mode_move": "Di Chuyển (Xóa file gốc)",
    "organizer_mode_delete": "Sao Chép rồi Xóa (Gửi vào thùng rác)",
    "organizer_recursive": "Quét cả thư mục con",
    "btn_organize": "Bắt Đầu Sắp Xếp",

    # Organizer Stats
    "organizer_organized": "File Đã Sắp Xếp",
    "organizer_failed": "Thất Bại",
    "organizer_categories": "Danh Mục Đã Dùng",
    "organizer_log": "Nhật Ký Sắp Xếp",
    "organizer_categories_breakdown": "Chi Tiết Theo Danh Mục",
    "files": "file",

    # Organizer Status
    "status_organizing": "Đang sắp xếp file...",
    "progress_organizing": "Đang sắp xếp... ({current}/{total})",

    # Organizer Messages
    "msg_confirm_organize": "Sắp xếp file?\n\nChế độ: {mode}\nNguồn: {source}\nĐích: {dest}\n\nĐiều này sẽ sắp xếp tất cả file vào các thư mục theo danh mục.",
    "msg_organize_success": "Sắp xếp file hoàn tất thành công!",
    "error_organize_failed": "Sắp xếp thất bại: {error}",
}
