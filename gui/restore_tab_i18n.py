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
    """Restore and manage backups tab with multi-language support"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BACKGROUND_COLOR, **kwargs)

        self.backup_service = BackupService()
        self.backups_list = []

        self._create_widgets()
        self._refresh_backups()

    def _create_widgets(self):
        """Create all widgets for restore tab"""

        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

        # Left panel - Restore options
        left_panel = Card(container, title=t("restore_title"))
        left_panel.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left_panel.configure(width=400)

        # Backup file
        self.backup_file_input = FilePathInput(
            left_panel,
            label=t("restore_backup_file"),
            browse_callback=self._browse_backup_file,
            mode="file"
        )
        self.backup_file_input.pack(fill="x", padx=PADDING, pady=10)

        # Destination
        self.restore_dest_input = FilePathInput(
            left_panel,
            label=t("restore_destination"),
            browse_callback=self._browse_restore_dest,
            mode="file"
        )
        self.restore_dest_input.pack(fill="x", padx=PADDING, pady=10)

        # Options
        options_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        options_frame.pack(fill="x", padx=PADDING, pady=10)

        self.verify_checksum_var = ctk.BooleanVar(value=True)
        checksum_cb = ctk.CTkCheckBox(
            options_frame,
            text=t("restore_verify_checksum"),
            variable=self.verify_checksum_var,
            font=NORMAL_FONT
        )
        checksum_cb.pack(anchor="w", pady=5)

        # Restore button
        StyledButton(
            left_panel,
            text=t("btn_restore_file"),
            command=self._restore_file,
            variant="success"
        ).pack(fill="x", padx=PADDING, pady=10)

        # Divider
        divider = ctk.CTkFrame(left_panel, height=2, fg_color=BORDER_COLOR)
        divider.pack(fill="x", padx=PADDING, pady=20)

        # Backup management
        mgmt_label = ctk.CTkLabel(
            left_panel,
            text=t("restore_management"),
            font=HEADING_FONT,
            text_color=PRIMARY_COLOR
        )
        mgmt_label.pack(anchor="w", padx=PADDING, pady=(10, 5))

        # Filter by date
        date_label = ctk.CTkLabel(left_panel, text=t("restore_filter_date"), font=NORMAL_FONT)
        date_label.pack(anchor="w", padx=PADDING, pady=(10, 5))

        self.date_filter_entry = ctk.CTkEntry(
            left_panel,
            font=NORMAL_FONT,
            height=35,
            placeholder_text=t("restore_filter_placeholder")
        )
        self.date_filter_entry.pack(fill="x", padx=PADDING)

        # Management buttons
        btn_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=PADDING, pady=20)

        StyledButton(
            btn_frame,
            text=t("btn_refresh"),
            command=self._refresh_backups,
            variant="primary"
        ).pack(fill="x", pady=5)

        StyledButton(
            btn_frame,
            text=t("btn_open_backup_folder"),
            command=self._open_backup_folder,
            variant="primary"
        ).pack(fill="x", pady=5)

        # Right panel - Backups list
        right_panel = ctk.CTkFrame(container, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True)

        # Info card
        info_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        info_frame.pack(fill="x", pady=(0, 10))

        self.backups_count_card = InfoCard(
            info_frame,
            title=t("available_backups"),
            value="0",
            color=PRIMARY_COLOR
        )
        self.backups_count_card.pack(side="left", expand=True, fill="x", padx=5)

        self.total_backup_size_card = InfoCard(
            info_frame,
            title=t("total_backup_size"),
            value="0 MB",
            color=SUCCESS_COLOR
        )
        self.total_backup_size_card.pack(side="left", expand=True, fill="x", padx=5)

        # Backups list
        backups_card = Card(right_panel, title=t("available_backups"))
        backups_card.pack(fill="both", expand=True)

        # Scrollable frame for backups
        self.backups_scroll = ctk.CTkScrollableFrame(
            backups_card,
            fg_color="transparent"
        )
        self.backups_scroll.pack(fill="both", expand=True, padx=10, pady=10)

    def _browse_backup_file(self, mode: str) -> Optional[str]:
        """Browse for backup file"""
        file = filedialog.askopenfilename(
            title=t("restore_backup_file"),
            initialdir=self.backup_service.backup_base_path
        )
        return file if file else None

    def _browse_restore_dest(self, mode: str) -> Optional[str]:
        """Browse for restore destination"""
        file = filedialog.asksaveasfilename(title=t("restore_destination"))
        return file if file else None

    def _restore_file(self):
        """Restore a file from backup"""
        backup_file = self.backup_file_input.get()
        destination = self.restore_dest_input.get()

        if not backup_file:
            messagebox.showerror(t("error"), t("msg_select_backup"))
            return

        if not destination:
            messagebox.showerror(t("error"), t("msg_select_destination"))
            return

        # Confirm
        if not messagebox.askyesno(
            t("info"),
            t("msg_confirm_restore", backup=backup_file, destination=destination)
        ):
            return

        # Run restore in background
        thread = threading.Thread(
            target=self._perform_restore,
            args=(backup_file, destination),
            daemon=True
        )
        thread.start()

    def _perform_restore(self, backup_file: str, destination: str):
        """Perform the actual restore"""
        try:
            verify = self.verify_checksum_var.get()

            result = self.backup_service.restore_file(
                backup_file=backup_file,
                destination=destination,
                verify_checksum=verify
            )

            if result['success']:
                messagebox.showinfo(
                    t("info"),
                    t("msg_restore_success", destination=result['destination'])
                )
            else:
                messagebox.showerror(
                    t("error"),
                    t("error_restore_failed", error=result.get('error', 'Unknown error'))
                )

        except Exception as e:
            messagebox.showerror(t("error"), t("error_restore_failed", error=str(e)))

    def _refresh_backups(self):
        """Refresh backups list"""
        thread = threading.Thread(target=self._load_backups, daemon=True)
        thread.start()

    def _load_backups(self):
        """Load backups from service"""
        try:
            # Get filter
            date_filter = self.date_filter_entry.get() or None

            # Load backups
            self.backups_list = self.backup_service.list_backups(backup_date=date_filter)

            # Clear existing widgets
            for widget in self.backups_scroll.winfo_children():
                widget.destroy()

            if not self.backups_list:
                no_backups_label = ctk.CTkLabel(
                    self.backups_scroll,
                    text=t("info_no_backups"),
                    font=NORMAL_FONT,
                    text_color=TEXT_COLOR
                )
                no_backups_label.pack(pady=50)
                self.backups_count_card.update_value("0")
                self.total_backup_size_card.update_value("0 MB")
                return

            # Calculate total size
            total_size = sum(b['size_mb'] for b in self.backups_list)

            # Update info cards
            self.backups_count_card.update_value(str(len(self.backups_list)))
            self.total_backup_size_card.update_value(f"{total_size:.2f} MB")

            # Add backup cards
            for backup in self.backups_list:
                self._create_backup_card(backup)

        except Exception as e:
            messagebox.showerror(t("error"), t("error_load_backups", error=str(e)))

    def _create_backup_card(self, backup: dict):
        """Create a card for each backup"""
        card = ctk.CTkFrame(
            self.backups_scroll,
            fg_color=CARD_BACKGROUND,
            corner_radius=8,
            border_width=1,
            border_color=BORDER_COLOR
        )
        card.pack(fill="x", pady=5)

        # Content frame
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=10)

        # Title
        title_label = ctk.CTkLabel(
            content,
            text=backup['name'],
            font=(FONT_FAMILY, 14, "bold"),
            text_color=PRIMARY_COLOR,
            anchor="w"
        )
        title_label.pack(fill="x")

        # Info
        info_text = f"{t('files_found')}: {backup['file_count']} | {t('total_size')}: {backup['size_mb']} MB | {backup['created'][:19]}"
        info_label = ctk.CTkLabel(
            content,
            text=info_text,
            font=SMALL_FONT,
            text_color=TEXT_COLOR,
            anchor="w"
        )
        info_label.pack(fill="x", pady=(5, 0))

        # Path
        path_label = ctk.CTkLabel(
            content,
            text=f"Path: {backup['path']}",
            font=SMALL_FONT,
            text_color=TEXT_COLOR,
            anchor="w"
        )
        path_label.pack(fill="x", pady=(2, 10))

        # Buttons frame
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x")

        # Open button
        open_btn = ctk.CTkButton(
            btn_frame,
            text=t("btn_open_folder"),
            command=lambda p=backup['path']: self._open_folder(p),
            font=SMALL_FONT,
            height=30,
            width=100,
            fg_color=PRIMARY_COLOR
        )
        open_btn.pack(side="left", padx=(0, 5))

        # Delete button
        delete_btn = ctk.CTkButton(
            btn_frame,
            text=t("btn_delete"),
            command=lambda p=backup['path']: self._delete_backup(p),
            font=SMALL_FONT,
            height=30,
            width=100,
            fg_color=DANGER_COLOR
        )
        delete_btn.pack(side="left")

    def _open_folder(self, path: str):
        """Open backup folder in file explorer"""
        try:
            import os
            os.startfile(path)
        except Exception as e:
            messagebox.showerror(t("error"), t("error", error=str(e)))

    def _delete_backup(self, path: str):
        """Delete a backup"""
        if not messagebox.askyesno(
            t("info"),
            t("msg_confirm_delete", path=path)
        ):
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
        """Open main backup folder"""
        try:
            import os
            os.startfile(str(self.backup_service.backup_base_path))
        except Exception as e:
            messagebox.showerror(t("error"), t("error", error=str(e)))
