"""Backup tab UI with i18n support"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from typing import Optional
from gui.components import *
from gui.styles import *
from gui.i18n import t
from app.services.backup import BackupService
from app.core.config import settings


class BackupTab(ctk.CTkFrame):
    """Backup files tab with multi-language support"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BACKGROUND_COLOR, **kwargs)
        self.backup_service = BackupService()
        self._create_widgets()

    def _create_widgets(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

        # Left panel
        left = Card(container, title=t("backup_title"))
        left.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left.configure(width=400)

        ctk.CTkLabel(left, text=t("backup_mode"), font=HEADING_FONT).pack(anchor="w", padx=PADDING, pady=(10, 5))
        self.backup_mode = ctk.StringVar(value="file")
        mode_frame = ctk.CTkFrame(left, fg_color="transparent")
        mode_frame.pack(fill="x", padx=PADDING, pady=5)
        for val, txt in [("file", "backup_mode_single"), ("files", "backup_mode_multiple"), ("folder", "backup_mode_folder")]:
            ctk.CTkRadioButton(mode_frame, text=t(txt), variable=self.backup_mode, value=val, command=self._update_mode, font=NORMAL_FONT).pack(anchor="w", pady=2)

        self.source_input = FilePathInput(left, label=t("backup_source"), browse_callback=self._browse_source, mode="file")
        self.source_input.pack(fill="x", padx=PADDING, pady=10)

        self.dest_input = FilePathInput(left, label=t("backup_destination"), browse_callback=lambda m: filedialog.askdirectory(title=t("backup_destination")), mode="folder")
        self.dest_input.pack(fill="x", padx=PADDING, pady=10)
        self.dest_input.set(settings.DEFAULT_BACKUP_PATH)

        opts = ctk.CTkFrame(left, fg_color="transparent")
        opts.pack(fill="x", padx=PADDING, pady=10)
        self.preserve_structure_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(opts, text=t("backup_preserve_structure"), variable=self.preserve_structure_var, font=NORMAL_FONT).pack(anchor="w", pady=5)
        self.create_checksum_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(opts, text=t("backup_create_checksum"), variable=self.create_checksum_var, font=NORMAL_FONT).pack(anchor="w", pady=5)

        self.folder_options_frame = ctk.CTkFrame(left, fg_color="transparent")
        ctk.CTkLabel(self.folder_options_frame, text=t("backup_extensions"), font=NORMAL_FONT).pack(anchor="w", pady=(5, 2))
        self.extensions_entry = ctk.CTkEntry(self.folder_options_frame, font=NORMAL_FONT, height=35, placeholder_text=t("backup_extensions_placeholder"))
        self.extensions_entry.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(self.folder_options_frame, text=t("backup_exclude"), font=NORMAL_FONT).pack(anchor="w", pady=(5, 2))
        self.exclude_entry = ctk.CTkEntry(self.folder_options_frame, font=NORMAL_FONT, height=35, placeholder_text=t("backup_exclude_placeholder"))
        self.exclude_entry.pack(fill="x")

        StyledButton(left, text=t("btn_start_backup"), command=self._start_backup, variant="success").pack(fill="x", padx=PADDING, pady=20)

        # Right panel
        right = ctk.CTkFrame(container, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)

        info = ctk.CTkFrame(right, fg_color="transparent")
        info.pack(fill="x", pady=(0, 10))
        self.files_card = InfoCard(info, title=t("files_backed_up"), value="0", color=SUCCESS_COLOR)
        self.files_card.pack(side="left", expand=True, fill="both", padx=(0, 5))
        self.size_card = InfoCard(info, title=t("total_size"), value="0 MB", color=PRIMARY_COLOR)
        self.size_card.pack(side="left", expand=True, fill="both", padx=(0, 5))
        self.failed_card = InfoCard(info, title=t("backup_failed"), value="0", color=DANGER_COLOR)
        self.failed_card.pack(side="left", expand=True, fill="both")

        self.progress_card = ProgressCard(right)
        self.progress_card.pack(fill="x", pady=10)

        log_card = Card(right, title=t("backup_log"))
        log_card.pack(fill="both", expand=True)
        self.log_text = ctk.CTkTextbox(log_card, font=SMALL_FONT, wrap="word", height=400)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

    def _update_mode(self):
        mode = self.backup_mode.get()
        self.source_input.mode = mode
        if mode == "folder":
            self.folder_options_frame.pack(fill="x", padx=PADDING, pady=10)
        else:
            self.folder_options_frame.pack_forget()

    def _browse_source(self, mode: str) -> Optional[str]:
        if mode == "file":
            return filedialog.askopenfilename(title=t("backup_source"))
        elif mode == "files":
            files = filedialog.askopenfilenames(title=t("backup_source"))
            return ";".join(files) if files else None
        return filedialog.askdirectory(title=t("backup_source"))

    def _start_backup(self):
        if not self.source_input.get():
            messagebox.showerror(t("error"), t("msg_select_source"))
            return
        threading.Thread(target=self._perform_backup, daemon=True).start()

    def _perform_backup(self):
        try:
            mode, source = self.backup_mode.get(), self.source_input.get()
            dest = self.dest_input.get() or None
            self.log_text.delete("1.0", "end")
            self._log(t("status_backing_up") + "\n")
            self.progress_card.update_progress(0, t("status_backing_up"), "")

            if mode == "file":
                result = self.backup_service.backup_file(source, dest, self.preserve_structure_var.get(), self.create_checksum_var.get())
                if result['success']:
                    self._log(f"Done: {result['destination']}\nSize: {result['size_mb']} MB\n")
                    self.files_card.update_value("1")
                    self.size_card.update_value(f"{result['size_mb']} MB")
                    self.failed_card.update_value("0")
                else:
                    self._log(f"Error: {result.get('error', '')}\n")
                    self.failed_card.update_value("1")
            elif mode == "files":
                result = self.backup_service.backup_files(source.split(";"), dest, self.preserve_structure_var.get(), self._backup_progress)
                self.files_card.update_value(str(result['successful']))
                self.size_card.update_value(f"{result['total_size_mb']} MB")
                self.failed_card.update_value(str(result['failed']))
            else:
                exts = [e.strip() for e in self.extensions_entry.get().split(",")] if self.extensions_entry.get() else None
                excl = [e.strip() for e in self.exclude_entry.get().split(",")] if self.exclude_entry.get() else None
                result = self.backup_service.backup_folder(source, dest, exts, excl, self._backup_progress)
                if 'error' in result:
                    self._log(f"Error: {result['error']}\n")
                    self.progress_card.update_progress(0, t("status_error"), result['error'])
                    return
                self.files_card.update_value(str(result['successful']))
                self.size_card.update_value(f"{result['total_size_mb']} MB")
                self.failed_card.update_value(str(result['failed']))

            self.progress_card.update_progress(1.0, t("status_completed"), "")
            messagebox.showinfo(t("info"), t("msg_backup_success"))
        except Exception as e:
            self._log(f"Error: {str(e)}\n")
            messagebox.showerror(t("error"), t("error_backup_failed", error=str(e)))
            self.progress_card.update_progress(0, t("status_error"), str(e))

    def _backup_progress(self, current: int, total: int, file_path: str):
        self.progress_card.update_progress(current / total if total else 0, t("progress_backing_up", current=current, total=total), file_path[:50])
        self._log(f"[{current}/{total}] {file_path}\n")

    def _log(self, msg: str):
        self.log_text.insert("end", msg)
        self.log_text.see("end")

    def receive_files(self, file_paths: list):
        if not file_paths:
            return
        self.backup_mode.set("files")
        self._update_mode()
        self.source_input.set(";".join(file_paths))
        self._log(f"Received {len(file_paths)} files\n")
