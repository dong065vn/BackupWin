"""Consolidate files tab UI with i18n support"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from typing import List, Dict
from pathlib import Path
from gui.components import *
from gui.styles import *
from gui.i18n import t
from app.services.file_consolidation import FileConsolidationService


class ConsolidateTab(ctk.CTkFrame):
    """Consolidate files tab with multi-language support"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BACKGROUND_COLOR, **kwargs)

        self.consolidation_service = FileConsolidationService()
        self.file_list: List[str] = []  # Track added files

        self._create_widgets()

    def _create_widgets(self):
        """Create all widgets for consolidate tab"""

        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

        # Left panel - Options
        left_panel = Card(container, title=t("consolidate_title"))
        left_panel.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left_panel.configure(width=400)

        # Operation mode selection
        mode_label = ctk.CTkLabel(left_panel, text=t("consolidate_operation"), font=HEADING_FONT)
        mode_label.pack(anchor="w", padx=PADDING, pady=(10, 5))

        self.operation_mode = ctk.StringVar(value="copy")

        mode_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        mode_frame.pack(fill="x", padx=PADDING, pady=5)

        ctk.CTkRadioButton(
            mode_frame,
            text=t("consolidate_copy"),
            variable=self.operation_mode,
            value="copy",
            font=NORMAL_FONT
        ).pack(anchor="w", pady=2)

        ctk.CTkRadioButton(
            mode_frame,
            text=t("consolidate_move"),
            variable=self.operation_mode,
            value="move",
            font=NORMAL_FONT
        ).pack(anchor="w", pady=2)

        # Destination folder
        self.dest_input = FilePathInput(
            left_panel,
            label=t("consolidate_destination"),
            browse_callback=self._browse_dest,
            mode="folder"
        )
        self.dest_input.pack(fill="x", padx=PADDING, pady=10)

        # Duplicate handling
        duplicate_label = ctk.CTkLabel(
            left_panel,
            text=t("consolidate_duplicate_handling"),
            font=HEADING_FONT
        )
        duplicate_label.pack(anchor="w", padx=PADDING, pady=(10, 5))

        self.duplicate_handling = ctk.StringVar(value="rename")

        duplicate_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        duplicate_frame.pack(fill="x", padx=PADDING, pady=5)

        ctk.CTkRadioButton(
            duplicate_frame,
            text=t("consolidate_skip"),
            variable=self.duplicate_handling,
            value="skip",
            font=NORMAL_FONT
        ).pack(anchor="w", pady=2)

        ctk.CTkRadioButton(
            duplicate_frame,
            text=t("consolidate_rename"),
            variable=self.duplicate_handling,
            value="rename",
            font=NORMAL_FONT
        ).pack(anchor="w", pady=2)

        ctk.CTkRadioButton(
            duplicate_frame,
            text=t("consolidate_overwrite"),
            variable=self.duplicate_handling,
            value="overwrite",
            font=NORMAL_FONT
        ).pack(anchor="w", pady=2)

        # Preserve structure option
        self.preserve_structure_var = ctk.BooleanVar(value=False)
        preserve_cb = ctk.CTkCheckBox(
            left_panel,
            text=t("consolidate_preserve_structure"),
            variable=self.preserve_structure_var,
            font=NORMAL_FONT
        )
        preserve_cb.pack(anchor="w", padx=PADDING, pady=10)

        # Preview button
        StyledButton(
            left_panel,
            text=t("btn_preview"),
            command=self._show_preview,
            variant="primary"
        ).pack(fill="x", padx=PADDING, pady=(10, 5))

        # Start consolidation button
        StyledButton(
            left_panel,
            text=t("btn_start_consolidate"),
            command=self._start_consolidation,
            variant="success"
        ).pack(fill="x", padx=PADDING, pady=(5, 20))

        # Right panel - File list
        right_panel = ctk.CTkFrame(container, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True)

        # File list card
        file_list_card = Card(right_panel, title=t("consolidate_file_list"))
        file_list_card.pack(fill="both", expand=True)

        # Add file buttons
        button_frame = ctk.CTkFrame(file_list_card, fg_color="transparent")
        button_frame.pack(fill="x", padx=PADDING, pady=10)

        StyledButton(
            button_frame,
            text=t("btn_add_file"),
            command=self._add_single_file,
            variant="primary"
        ).pack(side="left", padx=5)

        StyledButton(
            button_frame,
            text=t("btn_add_files"),
            command=self._add_multiple_files,
            variant="primary"
        ).pack(side="left", padx=5)

        StyledButton(
            button_frame,
            text=t("btn_add_from_folder"),
            command=self._add_from_folder,
            variant="primary"
        ).pack(side="left", padx=5)

        # File list display (scrollable)
        self.file_list_frame = ctk.CTkScrollableFrame(
            file_list_card,
            fg_color=BACKGROUND_COLOR,
            height=300
        )
        self.file_list_frame.pack(fill="both", expand=True, padx=PADDING, pady=10)

        # File list info
        info_frame = ctk.CTkFrame(file_list_card, fg_color="transparent")
        info_frame.pack(fill="x", padx=PADDING, pady=10)

        self.file_count_label = ctk.CTkLabel(
            info_frame,
            text=t("consolidate_total_files", count=0),
            font=NORMAL_FONT
        )
        self.file_count_label.pack(side="left", padx=5)

        self.file_size_label = ctk.CTkLabel(
            info_frame,
            text=t("consolidate_total_size", size="0 MB"),
            font=NORMAL_FONT
        )
        self.file_size_label.pack(side="left", padx=5)

        # Remove buttons
        remove_frame = ctk.CTkFrame(file_list_card, fg_color="transparent")
        remove_frame.pack(fill="x", padx=PADDING, pady=(0, 10))

        StyledButton(
            remove_frame,
            text=t("btn_remove_selected"),
            command=self._remove_selected,
            variant="danger"
        ).pack(side="left", padx=5)

        StyledButton(
            remove_frame,
            text=t("btn_clear_all"),
            command=self._clear_all,
            variant="danger"
        ).pack(side="left", padx=5)

        # Progress and status area
        status_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        status_frame.pack(fill="x", pady=10)

        # Info cards
        info_card_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        info_card_frame.pack(fill="x", pady=(0, 10))

        self.successful_card = InfoCard(
            info_card_frame,
            title=t("consolidate_successful"),
            value="0",
            color=SUCCESS_COLOR
        )
        self.successful_card.pack(side="left", expand=True, fill="x", padx=5)

        self.skipped_card = InfoCard(
            info_card_frame,
            title=t("consolidate_skipped"),
            value="0",
            color=WARNING_COLOR
        )
        self.skipped_card.pack(side="left", expand=True, fill="x", padx=5)

        self.failed_card = InfoCard(
            info_card_frame,
            title=t("consolidate_failed"),
            value="0",
            color=DANGER_COLOR
        )
        self.failed_card.pack(side="left", expand=True, fill="x", padx=5)

        # Progress card
        self.progress_card = ProgressCard(status_frame)
        self.progress_card.pack(fill="x")

    def _add_single_file(self):
        """Add a single file to the list"""
        file_path = filedialog.askopenfilename(title=t("btn_add_file"))
        if file_path:
            self._add_file_to_list(file_path)

    def _add_multiple_files(self):
        """Add multiple files to the list"""
        file_paths = filedialog.askopenfilenames(title=t("btn_add_files"))
        for file_path in file_paths:
            self._add_file_to_list(file_path)

    def _add_from_folder(self):
        """Add all files from a folder (non-recursive)"""
        folder_path = filedialog.askdirectory(title=t("btn_add_from_folder"))
        if folder_path:
            try:
                folder = Path(folder_path)
                files = [str(f) for f in folder.iterdir() if f.is_file()]

                if not files:
                    messagebox.showinfo(t("info"), t("msg_no_files_in_folder"))
                    return

                for file_path in files:
                    self._add_file_to_list(file_path)

                messagebox.showinfo(
                    t("info"),
                    t("msg_files_added", count=len(files))
                )
            except Exception as e:
                messagebox.showerror(t("error"), t("msg_error_reading_folder", error=str(e)))

    def _add_file_to_list(self, file_path: str):
        """Add a file to the internal list and update UI"""
        if file_path in self.file_list:
            return  # Already in list

        self.file_list.append(file_path)
        self._refresh_file_list_display()

    def _refresh_file_list_display(self):
        """Refresh the file list display"""
        # Clear existing widgets
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()

        # Add file items
        total_size = 0
        for idx, file_path in enumerate(self.file_list):
            file_item = FileListItem(
                self.file_list_frame,
                file_path=file_path,
                index=idx,
                remove_callback=self._remove_file_by_index
            )
            file_item.pack(fill="x", pady=2)

            # Calculate size
            try:
                total_size += Path(file_path).stat().st_size
            except:
                pass

        # Update info labels
        self.file_count_label.configure(
            text=t("consolidate_total_files", count=len(self.file_list))
        )
        size_mb = round(total_size / (1024 * 1024), 2)
        self.file_size_label.configure(
            text=t("consolidate_total_size", size=f"{size_mb} MB")
        )

    def _remove_file_by_index(self, index: int):
        """Remove a file by its index"""
        if 0 <= index < len(self.file_list):
            del self.file_list[index]
            self._refresh_file_list_display()

    def _remove_selected(self):
        """Remove selected files (for future enhancement with checkboxes)"""
        # For now, just show a message
        messagebox.showinfo(
            t("info"),
            t("msg_use_remove_button")
        )

    def _clear_all(self):
        """Clear all files from the list"""
        if not self.file_list:
            return

        confirm = messagebox.askyesno(
            t("confirm"),
            t("msg_confirm_clear_all", count=len(self.file_list))
        )

        if confirm:
            self.file_list.clear()
            self._refresh_file_list_display()
            # Reset stats
            self.successful_card.update_value("0")
            self.skipped_card.update_value("0")
            self.failed_card.update_value("0")
            self.progress_card.update_progress(0, t("status_ready"), "")

    def _browse_dest(self, mode: str) -> str:
        """Browse for destination folder"""
        return filedialog.askdirectory(title=t("consolidate_destination"))

    def _show_preview(self):
        """Show preview of consolidation"""
        if not self.file_list:
            messagebox.showwarning(t("warning"), t("msg_no_files_selected"))
            return

        destination = self.dest_input.get()
        if not destination:
            messagebox.showwarning(t("warning"), t("msg_select_destination"))
            return

        # Get preview from service
        try:
            preserve = self.preserve_structure_var.get()
            duplicate = self.duplicate_handling.get()

            preview = self.consolidation_service.get_consolidation_preview(
                source_files=self.file_list,
                destination_folder=destination,
                preserve_structure=preserve,
                duplicate_handling=duplicate
            )

            if "error" in preview:
                messagebox.showerror(t("error"), preview["error"])
                return

            # Show preview dialog
            preview_msg = t("msg_preview_info",
                count=preview["total_files"],
                size=preview["total_size_mb"],
                conflicts=preview["conflicts"]
            )

            messagebox.showinfo(t("preview_title"), preview_msg)

        except Exception as e:
            messagebox.showerror(t("error"), str(e))

    def _start_consolidation(self):
        """Start consolidation process"""
        if not self.file_list:
            messagebox.showwarning(t("warning"), t("msg_no_files_selected"))
            return

        destination = self.dest_input.get()
        if not destination:
            messagebox.showwarning(t("warning"), t("msg_select_destination"))
            return

        # Confirm operation
        operation = self.operation_mode.get()
        confirm_msg = t("msg_confirm_consolidate",
            count=len(self.file_list),
            operation=t(f"consolidate_{operation}"),
            destination=destination
        )

        if not messagebox.askyesno(t("confirm"), confirm_msg):
            return

        # Run consolidation in background thread
        thread = threading.Thread(target=self._perform_consolidation, daemon=True)
        thread.start()

    def _perform_consolidation(self):
        """Perform the actual consolidation"""
        try:
            operation = self.operation_mode.get()
            destination = self.dest_input.get()
            duplicate = self.duplicate_handling.get()
            preserve = self.preserve_structure_var.get()

            # Reset stats
            self.successful_card.update_value("0")
            self.skipped_card.update_value("0")
            self.failed_card.update_value("0")
            self.progress_card.update_progress(0, t("status_consolidating"), "")

            # Perform consolidation
            result = self.consolidation_service.consolidate_files(
                source_files=self.file_list,
                destination_folder=destination,
                operation=operation,
                duplicate_handling=duplicate,
                preserve_structure=preserve,
                progress_callback=self._consolidation_progress
            )

            if not result["success"]:
                messagebox.showerror(t("error"), result.get("error", "Unknown error"))
                self.progress_card.update_progress(0, t("status_error"), result.get("error", ""))
                return

            # Update stats
            self.successful_card.update_value(str(result["successful"]))
            self.skipped_card.update_value(str(result["skipped"]))
            self.failed_card.update_value(str(result["failed"]))
            self.progress_card.update_progress(1.0, t("status_completed"), "")

            # Show summary
            summary = t("msg_consolidation_complete",
                successful=result["successful"],
                skipped=result["skipped"],
                failed=result["failed"],
                size=result["total_size_mb"]
            )

            messagebox.showinfo(t("success"), summary)

        except Exception as e:
            messagebox.showerror(t("error"), str(e))
            self.progress_card.update_progress(0, t("status_error"), str(e))

    def _consolidation_progress(self, current: int, total: int, filename: str):
        """Progress callback for consolidation"""
        progress = current / total if total > 0 else 0
        self.progress_card.update_progress(
            progress,
            t("progress_consolidating", current=current, total=total),
            filename
        )


class FileListItem(ctk.CTkFrame):
    """Individual file item in the list"""

    def __init__(self, parent, file_path: str, index: int, remove_callback, **kwargs):
        super().__init__(parent, fg_color=CARD_BACKGROUND, corner_radius=5, **kwargs)

        self.file_path = file_path
        self.index = index
        self.remove_callback = remove_callback

        # File info
        path = Path(file_path)
        file_name = path.name
        file_dir = str(path.parent)

        try:
            file_size = path.stat().st_size
            size_mb = round(file_size / (1024 * 1024), 3)
            size_text = f"{size_mb} MB" if size_mb >= 0.001 else f"{file_size} bytes"
        except:
            size_text = "Unknown"

        # Main content
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        # File name
        name_label = ctk.CTkLabel(
            content_frame,
            text=file_name,
            font=NORMAL_FONT,
            anchor="w"
        )
        name_label.pack(anchor="w")

        # File path and size
        info_label = ctk.CTkLabel(
            content_frame,
            text=f"{file_dir} | {size_text}",
            font=SMALL_FONT,
            text_color=TEXT_LIGHT_COLOR,
            anchor="w"
        )
        info_label.pack(anchor="w")

        # Remove button
        remove_btn = ctk.CTkButton(
            self,
            text="✕",
            command=self._remove,
            width=30,
            height=30,
            fg_color=DANGER_COLOR,
            hover_color=DANGER_COLOR,
            font=("Arial", 14, "bold")
        )
        remove_btn.pack(side="right", padx=5)

    def _remove(self):
        """Handle remove button click"""
        self.remove_callback(self.index)
