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
        """Create all widgets for backup tab"""

        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

        # Left panel - Backup options
        left_panel = Card(container, title=t("backup_title"))
        left_panel.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left_panel.configure(width=400)

        # Backup mode selection
        mode_label = ctk.CTkLabel(left_panel, text=t("backup_mode"), font=HEADING_FONT)
        mode_label.pack(anchor="w", padx=PADDING, pady=(10, 5))

        self.backup_mode = ctk.StringVar(value="file")

        mode_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        mode_frame.pack(fill="x", padx=PADDING, pady=5)

        ctk.CTkRadioButton(
            mode_frame,
            text=t("backup_mode_single"),
            variable=self.backup_mode,
            value="file",
            command=self._update_mode,
            font=NORMAL_FONT
        ).pack(anchor="w", pady=2)

        ctk.CTkRadioButton(
            mode_frame,
            text=t("backup_mode_multiple"),
            variable=self.backup_mode,
            value="files",
            command=self._update_mode,
            font=NORMAL_FONT
        ).pack(anchor="w", pady=2)

        ctk.CTkRadioButton(
            mode_frame,
            text=t("backup_mode_folder"),
            variable=self.backup_mode,
            value="folder",
            command=self._update_mode,
            font=NORMAL_FONT
        ).pack(anchor="w", pady=2)

        # Source path
        self.source_input = FilePathInput(
            left_panel,
            label=t("backup_source"),
            browse_callback=self._browse_source,
            mode="file"
        )
        self.source_input.pack(fill="x", padx=PADDING, pady=10)

        # Destination path (optional)
        self.dest_input = FilePathInput(
            left_panel,
            label=t("backup_destination"),
            browse_callback=self._browse_dest,
            mode="folder"
        )
        self.dest_input.pack(fill="x", padx=PADDING, pady=10)
        self.dest_input.set(settings.DEFAULT_BACKUP_PATH)

        # Options
        options_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        options_frame.pack(fill="x", padx=PADDING, pady=10)

        # Preserve structure
        self.preserve_structure_var = ctk.BooleanVar(value=True)
        preserve_cb = ctk.CTkCheckBox(
            options_frame,
            text=t("backup_preserve_structure"),
            variable=self.preserve_structure_var,
            font=NORMAL_FONT
        )
        preserve_cb.pack(anchor="w", pady=5)

        # Create checksum
        self.create_checksum_var = ctk.BooleanVar(value=True)
        checksum_cb = ctk.CTkCheckBox(
            options_frame,
            text=t("backup_create_checksum"),
            variable=self.create_checksum_var,
            font=NORMAL_FONT
        )
        checksum_cb.pack(anchor="w", pady=5)

        # Folder options (only for folder mode)
        self.folder_options_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        self.folder_options_frame.pack(fill="x", padx=PADDING, pady=10)
        self.folder_options_frame.pack_forget()  # Hide initially

        ext_label = ctk.CTkLabel(
            self.folder_options_frame,
            text=t("backup_extensions"),
            font=NORMAL_FONT
        )
        ext_label.pack(anchor="w", pady=(5, 2))

        self.extensions_entry = ctk.CTkEntry(
            self.folder_options_frame,
            font=NORMAL_FONT,
            height=35,
            placeholder_text=t("backup_extensions_placeholder")
        )
        self.extensions_entry.pack(fill="x", pady=(0, 10))

        exclude_label = ctk.CTkLabel(
            self.folder_options_frame,
            text=t("backup_exclude"),
            font=NORMAL_FONT
        )
        exclude_label.pack(anchor="w", pady=(5, 2))

        self.exclude_entry = ctk.CTkEntry(
            self.folder_options_frame,
            font=NORMAL_FONT,
            height=35,
            placeholder_text=t("backup_exclude_placeholder")
        )
        self.exclude_entry.pack(fill="x")

        # Backup button
        StyledButton(
            left_panel,
            text=t("btn_start_backup"),
            command=self._start_backup,
            variant="success"
        ).pack(fill="x", padx=PADDING, pady=20)

        # Right panel - Status and results
        right_panel = ctk.CTkFrame(container, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True)

        # Info cards
        info_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        info_frame.pack(fill="x", pady=(0, 10))

        self.files_card = InfoCard(
            info_frame,
            title=t("files_backed_up"),
            value="0",
            color=SUCCESS_COLOR
        )
        self.files_card.pack(side="left", expand=True, fill="x", padx=5)

        self.size_card = InfoCard(
            info_frame,
            title=t("total_size"),
            value="0 MB",
            color=PRIMARY_COLOR
        )
        self.size_card.pack(side="left", expand=True, fill="x", padx=5)

        self.failed_card = InfoCard(
            info_frame,
            title=t("backup_failed"),
            value="0",
            color=DANGER_COLOR
        )
        self.failed_card.pack(side="left", expand=True, fill="x", padx=5)

        # Progress
        self.progress_card = ProgressCard(right_panel)
        self.progress_card.pack(fill="x", pady=10)

        # Log/Results area
        log_card = Card(right_panel, title=t("backup_log"))
        log_card.pack(fill="both", expand=True)

        self.log_text = ctk.CTkTextbox(
            log_card,
            font=SMALL_FONT,
            wrap="word",
            height=400
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

    def _update_mode(self):
        """Update UI based on selected mode"""
        mode = self.backup_mode.get()

        if mode == "file":
            self.source_input.mode = "file"
            self.folder_options_frame.pack_forget()
        elif mode == "files":
            self.source_input.mode = "files"
            self.folder_options_frame.pack_forget()
        elif mode == "folder":
            self.source_input.mode = "folder"
            self.folder_options_frame.pack(fill="x", padx=PADDING, pady=10)

    def _browse_source(self, mode: str) -> Optional[str]:
        """Browse for source"""
        if mode == "file":
            return filedialog.askopenfilename(title=t("backup_source"))
        elif mode == "files":
            files = filedialog.askopenfilenames(title=t("backup_source"))
            return ";".join(files) if files else None
        elif mode == "folder":
            return filedialog.askdirectory(title=t("backup_source"))
        return None

    def _browse_dest(self, mode: str) -> Optional[str]:
        """Browse for destination"""
        return filedialog.askdirectory(title=t("backup_destination"))

    def _start_backup(self):
        """Start backup process"""
        source = self.source_input.get()

        if not source:
            messagebox.showerror(t("error"), t("msg_select_source"))
            return

        # Run backup in background thread
        thread = threading.Thread(target=self._perform_backup, daemon=True)
        thread.start()

    def _perform_backup(self):
        """Perform the actual backup"""
        try:
            mode = self.backup_mode.get()
            source = self.source_input.get()
            destination = self.dest_input.get() or None
            preserve = self.preserve_structure_var.get()
            checksum = self.create_checksum_var.get()

            # Clear log
            self.log_text.delete("1.0", "end")
            self._log(t("status_backing_up") + "\n")

            # Update progress
            self.progress_card.update_progress(0, t("status_backing_up"), "")

            result = None

            if mode == "file":
                # Single file backup
                self._log(f"{t('backup_source')}: {source}\n")
                result = self.backup_service.backup_file(
                    source_file=source,
                    destination_folder=destination,
                    preserve_structure=preserve,
                    create_checksum=checksum
                )

                if result['success']:
                    self._log(f"✓ {t('status_completed')}\n")
                    self._log(f"{t('backup_destination')}: {result['destination']}\n")
                    self._log(f"{t('total_size')}: {result['size_mb']} MB\n")
                    if checksum:
                        self._log(f"Checksum: {result['checksum']}\n")

                    # Update stats
                    self.files_card.update_value("1")
                    self.size_card.update_value(f"{result['size_mb']} MB")
                    self.failed_card.update_value("0")
                    self.progress_card.update_progress(1.0, t("status_completed"), "")
                else:
                    self._log(f"✗ {t('error_backup_failed', error=result.get('error', ''))}\n")
                    self.failed_card.update_value("1")
                    self.progress_card.update_progress(0, t("status_error"), result.get('error', ''))

            elif mode == "files":
                # Multiple files backup
                files = source.split(";")
                self._log(f"{t('progress_backing_up', current=0, total=len(files))}\n")

                result = self.backup_service.backup_files(
                    source_files=files,
                    destination_folder=destination,
                    preserve_structure=preserve,
                    progress_callback=self._backup_progress
                )

                # Update stats
                self.files_card.update_value(str(result['successful']))
                self.size_card.update_value(f"{result['total_size_mb']} MB")
                self.failed_card.update_value(str(result['failed']))

                # Log results
                self._log(f"\n{t('status_completed')}:\n")
                self._log(f"{t('files_backed_up')}: {result['successful']}\n")
                self._log(f"{t('backup_failed')}: {result['failed']}\n")
                self._log(f"{t('total_size')}: {result['total_size_mb']} MB\n")

                if result['failed'] > 0:
                    self._log(f"\n{t('error')}:\n")
                    for error in result['errors']:
                        self._log(f"✗ {error['source']}: {error.get('error', 'Unknown error')}\n")

                self.progress_card.update_progress(1.0, t("status_completed"), "")

            elif mode == "folder":
                # Folder backup
                self._log(f"{t('backup_source')}: {source}\n")

                # Get folder options
                extensions = self.extensions_entry.get()
                exclude = self.exclude_entry.get()

                extensions_list = [e.strip() for e in extensions.split(",")] if extensions else None
                exclude_list = [e.strip() for e in exclude.split(",")] if exclude else None

                result = self.backup_service.backup_folder(
                    source_folder=source,
                    destination_folder=destination,
                    file_extensions=extensions_list,
                    exclude_patterns=exclude_list,
                    progress_callback=self._backup_progress
                )

                if 'error' in result:
                    self._log(f"✗ {t('error_backup_failed', error=result['error'])}\n")
                    self.progress_card.update_progress(0, t("status_error"), result['error'])
                    return

                # Update stats
                self.files_card.update_value(str(result['successful']))
                self.size_card.update_value(f"{result['total_size_mb']} MB")
                self.failed_card.update_value(str(result['failed']))

                # Log results
                self._log(f"\n{t('status_completed')}:\n")
                self._log(f"{t('files_backed_up')}: {result['successful']}\n")
                self._log(f"{t('backup_failed')}: {result['failed']}\n")
                self._log(f"{t('total_size')}: {result['total_size_mb']} MB\n")

                self.progress_card.update_progress(1.0, t("status_completed"), "")

            messagebox.showinfo(t("info"), t("msg_backup_success"))

        except Exception as e:
            self._log(f"\n✗ {t('error')}: {str(e)}\n")
            messagebox.showerror(t("error"), t("error_backup_failed", error=str(e)))
            self.progress_card.update_progress(0, t("status_error"), str(e))

    def _backup_progress(self, current: int, total: int, file_path: str):
        """Progress callback for backup"""
        progress = current / total if total > 0 else 0
        self.progress_card.update_progress(
            progress,
            t("progress_backing_up", current=current, total=total),
            t("progress_current_file", file=file_path[:50])
        )
        self._log(f"[{current}/{total}] {file_path}\n")

    def _log(self, message: str):
        """Add message to log"""
        self.log_text.insert("end", message)
        self.log_text.see("end")
