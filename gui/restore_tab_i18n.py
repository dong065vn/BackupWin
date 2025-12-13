"""Restore and manage backups tab UI with i18n support"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from typing import Optional
from gui.components import *
from gui.styles import *
from gui.i18n import t
from app.services.backup import BackupService


class RestoreTab(ctk.CTkFrame):
    """Restore and manage backups tab"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BACKGROUND_COLOR, **kwargs)
        self.backup_service = BackupService()
        self.backups_list = []
        self._create_widgets()
        self._refresh_backups()

    def _create_widgets(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

        # Left panel
        left = Card(container, title=t("restore_title"))
        left.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left.configure(width=400)

        self.backup_file_input = FilePathInput(left, label=t("restore_backup_file"), 
            browse_callback=lambda m: filedialog.askopenfilename(title=t("restore_backup_file"), initialdir=self.backup_service.backup_base_path), mode="file")
        self.backup_file_input.pack(fill="x", padx=PADDING, pady=10)

        self.restore_dest_input = FilePathInput(left, label=t("restore_destination"),
            browse_callback=lambda m: filedialog.asksaveasfilename(title=t("restore_destination")), mode="file")
        self.restore_dest_input.pack(fill="x", padx=PADDING, pady=10)

        opts = ctk.CTkFrame(left, fg_color="transparent")
        opts.pack(fill="x", padx=PADDING, pady=10)
        self.verify_checksum_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(opts, text=t("restore_verify_checksum"), variable=self.verify_checksum_var, font=NORMAL_FONT).pack(anchor="w", pady=5)

        StyledButton(left, text=t("btn_restore_file"), command=self._restore_file, variant="success").pack(fill="x", padx=PADDING, pady=10)

        ctk.CTkFrame(left, height=2, fg_color=BORDER_COLOR).pack(fill="x", padx=PADDING, pady=20)

        ctk.CTkLabel(left, text=t("restore_management"), font=HEADING_FONT, text_color=PRIMARY_COLOR).pack(anchor="w", padx=PADDING, pady=(10, 5))
        ctk.CTkLabel(left, text=t("restore_filter_date"), font=NORMAL_FONT).pack(anchor="w", padx=PADDING, pady=(10, 5))
        self.date_filter_entry = ctk.CTkEntry(left, font=NORMAL_FONT, height=35, placeholder_text=t("restore_filter_placeholder"))
        self.date_filter_entry.pack(fill="x", padx=PADDING)

        btns = ctk.CTkFrame(left, fg_color="transparent")
        btns.pack(fill="x", padx=PADDING, pady=20)
        StyledButton(btns, text=t("btn_refresh"), command=self._refresh_backups, variant="primary").pack(fill="x", pady=5)
        StyledButton(btns, text=t("btn_open_backup_folder"), command=self._open_backup_folder, variant="primary").pack(fill="x", pady=5)

        # Right panel
        right = ctk.CTkFrame(container, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)

        info = ctk.CTkFrame(right, fg_color="transparent")
        info.pack(fill="x", pady=(0, 10))
        self.backups_count_card = InfoCard(info, title=t("available_backups"), value="0", color=PRIMARY_COLOR)
        self.backups_count_card.pack(side="left", expand=True, fill="both", padx=(0, 5))
        self.total_backup_size_card = InfoCard(info, title=t("total_backup_size"), value="0 MB", color=SUCCESS_COLOR)
        self.total_backup_size_card.pack(side="left", expand=True, fill="both")

        backups_card = Card(right, title=t("available_backups"))
        backups_card.pack(fill="both", expand=True)
        self.backups_scroll = ctk.CTkScrollableFrame(backups_card, fg_color="transparent")
        self.backups_scroll.pack(fill="both", expand=True, padx=10, pady=10)

    def _restore_file(self):
        backup, dest = self.backup_file_input.get(), self.restore_dest_input.get()
        if not backup:
            messagebox.showerror(t("error"), t("msg_select_backup"))
            return
        if not dest:
            messagebox.showerror(t("error"), t("msg_select_destination"))
            return
        if not messagebox.askyesno(t("info"), t("msg_confirm_restore", backup=backup, destination=dest)):
            return
        threading.Thread(target=self._perform_restore, args=(backup, dest), daemon=True).start()

    def _perform_restore(self, backup: str, dest: str):
        try:
            result = self.backup_service.restore_file(backup, dest, self.verify_checksum_var.get())
            if result['success']:
                messagebox.showinfo(t("info"), t("msg_restore_success", destination=result['destination']))
            else:
                messagebox.showerror(t("error"), t("error_restore_failed", error=result.get('error', 'Unknown')))
        except Exception as e:
            messagebox.showerror(t("error"), t("error_restore_failed", error=str(e)))

    def _refresh_backups(self):
        threading.Thread(target=self._load_backups, daemon=True).start()

    def _load_backups(self):
        try:
            self.backups_list = self.backup_service.list_backups(self.date_filter_entry.get() or None)
            for w in self.backups_scroll.winfo_children():
                w.destroy()

            if not self.backups_list:
                ctk.CTkLabel(self.backups_scroll, text=t("info_no_backups"), font=NORMAL_FONT, text_color=TEXT_COLOR).pack(pady=50)
                self.backups_count_card.update_value("0")
                self.total_backup_size_card.update_value("0 MB")
                return

            total = sum(b['size_mb'] for b in self.backups_list)
            self.backups_count_card.update_value(str(len(self.backups_list)))
            self.total_backup_size_card.update_value(f"{total:.2f} MB")

            for b in self.backups_list:
                self._create_backup_card(b)
        except Exception as e:
            messagebox.showerror(t("error"), t("error_load_backups", error=str(e)))

    def _create_backup_card(self, backup: dict):
        card = ctk.CTkFrame(self.backups_scroll, fg_color=CARD_BACKGROUND, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        card.pack(fill="x", pady=5)
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=10)

        ctk.CTkLabel(content, text=backup['name'], font=(FONT_FAMILY, 14, "bold"), text_color=PRIMARY_COLOR, anchor="w").pack(fill="x")
        ctk.CTkLabel(content, text=f"Files: {backup['file_count']} | Size: {backup['size_mb']} MB | {backup['created'][:19]}", font=SMALL_FONT, text_color=TEXT_COLOR, anchor="w").pack(fill="x", pady=(5, 0))
        ctk.CTkLabel(content, text=f"Path: {backup['path']}", font=SMALL_FONT, text_color=TEXT_COLOR, anchor="w").pack(fill="x", pady=(2, 10))

        btns = ctk.CTkFrame(content, fg_color="transparent")
        btns.pack(fill="x")
        ctk.CTkButton(btns, text=t("btn_open_folder"), command=lambda p=backup['path']: self._open_folder(p), font=SMALL_FONT, height=30, width=100, fg_color=PRIMARY_COLOR).pack(side="left", padx=(0, 5))
        ctk.CTkButton(btns, text=t("btn_delete"), command=lambda p=backup['path']: self._delete_backup(p), font=SMALL_FONT, height=30, width=100, fg_color=DANGER_COLOR).pack(side="left")

    def _open_folder(self, path: str):
        try:
            import os
            os.startfile(path)
        except Exception as e:
            messagebox.showerror(t("error"), str(e))

    def _delete_backup(self, path: str):
        if not messagebox.askyesno(t("info"), t("msg_confirm_delete", path=path)):
            return
        try:
            result = self.backup_service.delete_backup(path)
            if result['success']:
                messagebox.showinfo(t("info"), t("msg_delete_success"))
                self._refresh_backups()
            else:
                messagebox.showerror(t("error"), t("error_delete_failed", error=result.get('error')))
        except Exception as e:
            messagebox.showerror(t("error"), t("error_delete_failed", error=str(e)))

    def _open_backup_folder(self):
        try:
            import os
            os.startfile(str(self.backup_service.backup_base_path))
        except Exception as e:
            messagebox.showerror(t("error"), str(e))
