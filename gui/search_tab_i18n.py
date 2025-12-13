"""Search tab UI with i18n support"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from typing import Optional
from gui.components import *
from gui.styles import *
from gui.i18n import t
from app.services.file_search import FileSearchService


class SearchTab(ctk.CTkFrame):
    """Search files tab with multi-language support"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BACKGROUND_COLOR, **kwargs)
        self.search_service = FileSearchService()
        self.search_results = []
        self.on_send_to_backup = self.on_send_to_consolidate = self.on_send_to_organizer = None
        self._create_widgets()

    def _create_widgets(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

        # Left panel
        left = Card(container, title=t("search_title"))
        left.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left.configure(width=400)

        self.path_input = FilePathInput(left, label=t("search_path"), browse_callback=lambda m: filedialog.askdirectory(title=t("search_path")), mode="folder")
        self.path_input.pack(fill="x", padx=PADDING, pady=10)

        ctk.CTkLabel(left, text=t("search_pattern"), font=NORMAL_FONT).pack(anchor="w", padx=PADDING, pady=(10, 5))
        self.pattern_entry = ctk.CTkEntry(left, font=NORMAL_FONT, height=35, placeholder_text=t("search_pattern_placeholder"))
        self.pattern_entry.pack(fill="x", padx=PADDING)
        self.pattern_entry.insert(0, "*")

        ctk.CTkLabel(left, text=t("search_extension"), font=NORMAL_FONT).pack(anchor="w", padx=PADDING, pady=(10, 5))
        self.ext_entry = ctk.CTkEntry(left, font=NORMAL_FONT, height=35, placeholder_text=t("search_extension_placeholder"))
        self.ext_entry.pack(fill="x", padx=PADDING)

        opts = ctk.CTkFrame(left, fg_color="transparent")
        opts.pack(fill="x", padx=PADDING, pady=10)
        self.recursive_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(opts, text=t("search_recursive"), variable=self.recursive_var, font=NORMAL_FONT).pack(anchor="w", pady=5)
        self.case_sensitive_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(opts, text=t("search_case_sensitive"), variable=self.case_sensitive_var, font=NORMAL_FONT).pack(anchor="w", pady=5)

        ctk.CTkLabel(left, text=t("search_max_results"), font=NORMAL_FONT).pack(anchor="w", padx=PADDING, pady=(10, 5))
        self.max_results_entry = ctk.CTkEntry(left, font=NORMAL_FONT, height=35, placeholder_text=t("search_max_results_placeholder"))
        self.max_results_entry.pack(fill="x", padx=PADDING)
        self.max_results_entry.insert(0, "100")

        btns = ctk.CTkFrame(left, fg_color="transparent")
        btns.pack(fill="x", padx=PADDING, pady=20)
        StyledButton(btns, text=t("btn_search"), command=self._start_search, variant="primary").pack(fill="x", pady=5)
        StyledButton(btns, text=t("btn_search_all_drives"), command=self._search_all_drives, variant="success").pack(fill="x", pady=5)
        StyledButton(btns, text=t("btn_get_drives"), command=self._show_drives, variant="primary").pack(fill="x", pady=5)

        # Right panel
        right = ctk.CTkFrame(container, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)

        info = ctk.CTkFrame(right, fg_color="transparent")
        info.pack(fill="x", pady=(0, 10))
        self.results_count_card = InfoCard(info, title=t("files_found"), value="0", color=PRIMARY_COLOR)
        self.results_count_card.pack(side="left", expand=True, fill="both", padx=(0, 5))
        self.total_size_card = InfoCard(info, title=t("total_size"), value="0 MB", color=SUCCESS_COLOR)
        self.total_size_card.pack(side="left", expand=True, fill="both", padx=(0, 5))

        self.progress_card = ProgressCard(right)
        self.progress_card.pack(fill="x", pady=10)

        action_card = Card(right, title="⚡ Quick Actions")
        action_card.pack(fill="x", pady=(0, 10))
        action_frame = ctk.CTkFrame(action_card, fg_color="transparent")
        action_frame.pack(fill="x", padx=10, pady=10)
        StyledButton(action_frame, text=t("btn_send_to_backup"), command=self._send_to_backup, variant="primary").pack(side="left", padx=(0, 10))
        StyledButton(action_frame, text=t("btn_send_to_consolidate"), command=self._send_to_consolidate, variant="success").pack(side="left", padx=(0, 10))
        StyledButton(action_frame, text=t("btn_send_to_organizer"), command=self._send_to_organizer, variant="primary").pack(side="left")

        results_card = Card(right, title=t("search_results"))
        results_card.pack(fill="both", expand=True)
        self.results_table = ResultsTable(results_card, columns=[t("col_file_name"), t("col_path"), t("col_size"), t("col_modified")], height=350)
        self.results_table.pack(fill="both", expand=True, padx=10, pady=10)

    def _start_search(self):
        if not self.path_input.get():
            messagebox.showerror(t("error"), t("msg_select_path"))
            return
        threading.Thread(target=self._perform_search, daemon=True).start()

    def _perform_search(self):
        try:
            self.results_table.clear()
            self.search_results = []
            self.progress_card.update_progress(0, t("status_searching"), "")
            
            max_results = int(self.max_results_entry.get()) if self.max_results_entry.get() else None
            count, total_size = 0, 0

            for f in self.search_service.search_files(
                search_path=self.path_input.get(), file_pattern=self.pattern_entry.get() or "*",
                file_extension=self.ext_entry.get() or None, recursive=self.recursive_var.get(),
                max_results=max_results, case_sensitive=self.case_sensitive_var.get()
            ):
                self.search_results.append(f)
                count += 1
                total_size += f['size']
                self.results_table.add_row([f['name'], f['path'][:50] + "..." if len(f['path']) > 50 else f['path'], f['size_mb'], f['modified'][:19]])
                if max_results:
                    self.progress_card.update_progress(count / max_results, t("progress_found_files", count=count), f"{total_size / 1048576:.2f} MB")

            self.results_count_card.update_value(str(count))
            self.total_size_card.update_value(f"{total_size / 1048576:.2f} MB")
            self.progress_card.update_progress(1.0, t("status_completed"), t("progress_found_files", count=count))
        except Exception as e:
            messagebox.showerror(t("error"), t("error_search_failed", error=str(e)))
            self.progress_card.update_progress(0, t("status_error"), str(e))

    def _search_all_drives(self):
        messagebox.showinfo(t("info"), t("msg_search_all_drives"))
        self.path_input.set("All Drives")
        threading.Thread(target=self._perform_all_drives_search, daemon=True).start()

    def _perform_all_drives_search(self):
        try:
            self.results_table.clear()
            self.search_results = []
            self.progress_card.update_progress(0, t("status_searching"), "")
            count, total_size = 0, 0

            for f in self.search_service.search_in_multiple_drives(
                file_pattern=self.pattern_entry.get() or "*", file_extension=self.ext_entry.get() or None, max_results_per_drive=50
            ):
                self.search_results.append(f)
                count += 1
                total_size += f['size']
                self.results_table.add_row([f['name'], f"{f['drive']} - {f['path'][:40]}...", f['size_mb'], f['modified'][:19]])

            self.results_count_card.update_value(str(count))
            self.total_size_card.update_value(f"{total_size / 1048576:.2f} MB")
            self.progress_card.update_progress(1.0, t("status_completed"), t("progress_found_files", count=count))
        except Exception as e:
            messagebox.showerror(t("error"), t("error_search_failed", error=str(e)))

    def _show_drives(self):
        try:
            drives = self.search_service.get_available_drives()
            messagebox.showinfo(t("info"), t("info_drives_found", count=len(drives), drives="\n".join(drives)))
        except Exception as e:
            messagebox.showerror(t("error"), t("error_get_drives", error=str(e)))

    def _send_to_backup(self):
        self._send_results(self.on_send_to_backup, t("tab_backup"))

    def _send_to_consolidate(self):
        self._send_results(self.on_send_to_consolidate, t("tab_consolidate"))

    def _send_to_organizer(self):
        self._send_results(self.on_send_to_organizer, t("tab_organizer"))

    def _send_results(self, callback, module):
        if not self.search_results:
            messagebox.showwarning(t("warning"), t("msg_no_search_results"))
            return
        if callback:
            paths = [r['path'] for r in self.search_results]
            callback(paths)
            messagebox.showinfo(t("info"), t("msg_files_sent", count=len(paths), module=module))
