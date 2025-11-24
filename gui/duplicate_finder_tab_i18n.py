"""Duplicate Finder tab UI with i18n support"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from typing import List, Dict, Optional
from pathlib import Path
from gui.components import *
from gui.styles import *
from gui.i18n import t
from app.services.duplicate_finder import DuplicateFinderService


class DuplicateFinderTab(ctk.CTkFrame):
    """Duplicate Finder tab with multi-language support"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BACKGROUND_COLOR, **kwargs)

        self.duplicate_service = DuplicateFinderService()
        self.scan_paths: List[str] = []
        self.duplicate_groups: List[Dict] = []

        self._create_widgets()

    def _create_widgets(self):
        """Create all widgets for duplicate finder tab"""

        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

        # Left panel - Scan options
        left_panel = Card(container, title=t("duplicate_scan_options"))
        left_panel.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left_panel.configure(width=400)

        # Scan paths section
        paths_label = ctk.CTkLabel(left_panel, text=t("duplicate_scan_paths"), font=HEADING_FONT)
        paths_label.pack(anchor="w", padx=PADDING, pady=(10, 5))

        # Paths list display
        self.paths_frame = ctk.CTkFrame(left_panel, fg_color=BACKGROUND_COLOR, height=100)
        self.paths_frame.pack(fill="x", padx=PADDING, pady=5)

        self.paths_label = ctk.CTkLabel(
            self.paths_frame,
            text=t("duplicate_no_paths"),
            font=SMALL_FONT,
            text_color=TEXT_LIGHT_COLOR
        )
        self.paths_label.pack(pady=10)

        # Path buttons
        path_buttons = ctk.CTkFrame(left_panel, fg_color="transparent")
        path_buttons.pack(fill="x", padx=PADDING, pady=5)

        StyledButton(
            path_buttons,
            text=t("btn_add_folder"),
            command=self._add_scan_path,
            variant="primary"
        ).pack(side="left", padx=(0, 5))

        StyledButton(
            path_buttons,
            text=t("btn_clear_paths"),
            command=self._clear_paths,
            variant="danger"
        ).pack(side="left")

        # Comparison method
        method_label = ctk.CTkLabel(
            left_panel,
            text=t("duplicate_comparison_method"),
            font=HEADING_FONT
        )
        method_label.pack(anchor="w", padx=PADDING, pady=(15, 5))

        self.comparison_method = ctk.StringVar(value="quick")

        method_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        method_frame.pack(fill="x", padx=PADDING, pady=5)

        ctk.CTkRadioButton(
            method_frame,
            text=t("duplicate_method_quick"),
            variable=self.comparison_method,
            value="quick",
            font=NORMAL_FONT
        ).pack(anchor="w", pady=2)

        ctk.CTkRadioButton(
            method_frame,
            text=t("duplicate_method_hash"),
            variable=self.comparison_method,
            value="hash",
            font=NORMAL_FONT
        ).pack(anchor="w", pady=2)

        ctk.CTkRadioButton(
            method_frame,
            text=t("duplicate_method_size_name"),
            variable=self.comparison_method,
            value="size_name",
            font=NORMAL_FONT
        ).pack(anchor="w", pady=2)

        # Options
        options_label = ctk.CTkLabel(left_panel, text=t("duplicate_options"), font=HEADING_FONT)
        options_label.pack(anchor="w", padx=PADDING, pady=(15, 5))

        # Min file size
        size_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        size_frame.pack(fill="x", padx=PADDING, pady=5)

        size_label = ctk.CTkLabel(
            size_frame,
            text=t("duplicate_min_size"),
            font=NORMAL_FONT
        )
        size_label.pack(anchor="w", pady=(0, 2))

        self.min_size_entry = ctk.CTkEntry(
            size_frame,
            font=NORMAL_FONT,
            height=35,
            placeholder_text="0"
        )
        self.min_size_entry.pack(fill="x")
        self.min_size_entry.insert(0, "0")

        # File extensions
        ext_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        ext_frame.pack(fill="x", padx=PADDING, pady=5)

        ext_label = ctk.CTkLabel(
            ext_frame,
            text=t("duplicate_file_types"),
            font=NORMAL_FONT
        )
        ext_label.pack(anchor="w", pady=(0, 2))

        self.extensions_entry = ctk.CTkEntry(
            ext_frame,
            font=NORMAL_FONT,
            height=35,
            placeholder_text=t("duplicate_file_types_placeholder")
        )
        self.extensions_entry.pack(fill="x")

        # Recursive scan
        self.recursive_var = ctk.BooleanVar(value=True)
        recursive_cb = ctk.CTkCheckBox(
            left_panel,
            text=t("duplicate_recursive"),
            variable=self.recursive_var,
            font=NORMAL_FONT
        )
        recursive_cb.pack(anchor="w", padx=PADDING, pady=10)

        # Scan button
        StyledButton(
            left_panel,
            text=t("btn_start_scan"),
            command=self._start_scan,
            variant="success"
        ).pack(fill="x", padx=PADDING, pady=20)

        # Right panel - Results
        right_panel = ctk.CTkFrame(container, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True)

        # Statistics cards
        stats_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 10))

        self.files_scanned_card = InfoCard(
            stats_frame,
            title=t("duplicate_files_scanned"),
            value="0",
            color=PRIMARY_COLOR
        )
        self.files_scanned_card.pack(side="left", expand=True, fill="x", padx=5)

        self.groups_card = InfoCard(
            stats_frame,
            title=t("duplicate_groups_found"),
            value="0",
            color=WARNING_COLOR
        )
        self.groups_card.pack(side="left", expand=True, fill="x", padx=5)

        self.wasted_space_card = InfoCard(
            stats_frame,
            title=t("duplicate_space_wasted"),
            value="0 MB",
            color=DANGER_COLOR
        )
        self.wasted_space_card.pack(side="left", expand=True, fill="x", padx=5)

        # Progress
        self.progress_card = ProgressCard(right_panel)
        self.progress_card.pack(fill="x", pady=10)

        # Results area
        results_card = Card(right_panel, title=t("duplicate_results"))
        results_card.pack(fill="both", expand=True)

        # Scrollable results frame
        self.results_frame = ctk.CTkScrollableFrame(
            results_card,
            fg_color=BACKGROUND_COLOR
        )
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Initial message
        self.no_results_label = ctk.CTkLabel(
            self.results_frame,
            text=t("duplicate_no_results"),
            font=NORMAL_FONT,
            text_color=TEXT_LIGHT_COLOR
        )
        self.no_results_label.pack(pady=50)

    def _add_scan_path(self):
        """Add a folder to scan"""
        folder = filedialog.askdirectory(title=t("duplicate_select_folder"))
        if folder:
            if folder not in self.scan_paths:
                self.scan_paths.append(folder)
                self._update_paths_display()
            else:
                messagebox.showinfo(t("info"), t("duplicate_path_already_added"))

    def _clear_paths(self):
        """Clear all scan paths"""
        if self.scan_paths:
            self.scan_paths.clear()
            self._update_paths_display()

    def _update_paths_display(self):
        """Update the display of scan paths"""
        for widget in self.paths_frame.winfo_children():
            widget.destroy()

        if not self.scan_paths:
            self.paths_label = ctk.CTkLabel(
                self.paths_frame,
                text=t("duplicate_no_paths"),
                font=SMALL_FONT,
                text_color=TEXT_LIGHT_COLOR
            )
            self.paths_label.pack(pady=10)
        else:
            for idx, path in enumerate(self.scan_paths):
                path_item = ctk.CTkFrame(self.paths_frame, fg_color=CARD_BACKGROUND)
                path_item.pack(fill="x", pady=2, padx=5)

                path_label = ctk.CTkLabel(
                    path_item,
                    text=path,
                    font=SMALL_FONT,
                    anchor="w"
                )
                path_label.pack(side="left", fill="x", expand=True, padx=5, pady=3)

                remove_btn = ctk.CTkButton(
                    path_item,
                    text="✕",
                    width=25,
                    height=25,
                    command=lambda i=idx: self._remove_path(i),
                    fg_color=DANGER_COLOR
                )
                remove_btn.pack(side="right", padx=3)

    def _remove_path(self, index: int):
        """Remove a path from scan list"""
        if 0 <= index < len(self.scan_paths):
            del self.scan_paths[index]
            self._update_paths_display()

    def _start_scan(self):
        """Start scanning for duplicates"""
        if not self.scan_paths:
            messagebox.showwarning(t("warning"), t("duplicate_no_paths_selected"))
            return

        # Get options
        comparison = self.comparison_method.get()

        try:
            min_size = int(self.min_size_entry.get() or "0")
        except ValueError:
            messagebox.showerror(t("error"), t("duplicate_invalid_size"))
            return

        extensions_text = self.extensions_entry.get().strip()
        extensions = None
        if extensions_text:
            extensions = [ext.strip() for ext in extensions_text.split(",")]

        recursive = self.recursive_var.get()

        # Run scan in background thread
        thread = threading.Thread(
            target=self._perform_scan,
            args=(comparison, min_size, extensions, recursive),
            daemon=True
        )
        thread.start()

    def _perform_scan(self, comparison: str, min_size: int, extensions: Optional[List[str]], recursive: bool):
        """Perform the actual scan"""
        try:
            # Clear previous results
            self._clear_results()

            # Update UI
            self.progress_card.update_progress(0, t("status_scanning"), "")
            self.files_scanned_card.update_value("...")
            self.groups_card.update_value("...")
            self.wasted_space_card.update_value("...")

            # Perform scan
            result = self.duplicate_service.scan_for_duplicates(
                scan_paths=self.scan_paths,
                comparison_method=comparison,
                min_file_size=min_size,
                file_extensions=extensions,
                recursive=recursive,
                progress_callback=self._scan_progress
            )

            if not result["success"]:
                messagebox.showerror(t("error"), result.get("error", "Unknown error"))
                self.progress_card.update_progress(0, t("status_error"), "")
                return

            # Update statistics
            self.files_scanned_card.update_value(str(result["total_files_scanned"]))
            self.groups_card.update_value(str(len(result["duplicate_groups"])))
            self.wasted_space_card.update_value(f"{result['space_wasted_mb']} MB")

            # Store results
            self.duplicate_groups = result["duplicate_groups"]

            # Display results
            self._display_results()

            self.progress_card.update_progress(1.0, t("status_completed"), "")

            # Show summary
            messagebox.showinfo(
                t("success"),
                t("duplicate_scan_complete",
                  groups=len(result["duplicate_groups"]),
                  duplicates=result["total_duplicates"],
                  space=result["space_wasted_mb"])
            )

        except Exception as e:
            messagebox.showerror(t("error"), str(e))
            self.progress_card.update_progress(0, t("status_error"), str(e))

    def _scan_progress(self, current: int, total: int, filename: str):
        """Progress callback for scan"""
        progress = current / total if total > 0 else 0
        self.progress_card.update_progress(
            progress,
            t("progress_scanning", current=current, total=total),
            filename[:50]
        )

    def _clear_results(self):
        """Clear results display"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

    def _display_results(self):
        """Display duplicate groups"""
        self._clear_results()

        if not self.duplicate_groups:
            self.no_results_label = ctk.CTkLabel(
                self.results_frame,
                text=t("duplicate_no_duplicates_found"),
                font=NORMAL_FONT,
                text_color=SUCCESS_COLOR
            )
            self.no_results_label.pack(pady=50)
            return

        # Display each duplicate group
        for idx, group in enumerate(self.duplicate_groups, 1):
            group_card = DuplicateGroupCard(
                self.results_frame,
                group_number=idx,
                group_data=group,
                duplicate_service=self.duplicate_service,
                on_action_complete=self._on_group_action_complete
            )
            group_card.pack(fill="x", pady=5, padx=5)

    def _on_group_action_complete(self, group_data: Dict):
        """Callback when action is performed on a group"""
        # Refresh the display
        self._display_results()

        # Recalculate statistics
        total_wasted = sum(g["wasted_space"] for g in self.duplicate_groups)
        self.groups_card.update_value(str(len(self.duplicate_groups)))
        self.wasted_space_card.update_value(f"{round(total_wasted / (1024 * 1024), 2)} MB")


class DuplicateGroupCard(ctk.CTkFrame):
    """Card displaying a duplicate group with actions"""

    def __init__(self, parent, group_number: int, group_data: Dict, duplicate_service, on_action_complete, **kwargs):
        super().__init__(parent, fg_color=CARD_BACKGROUND, corner_radius=10, **kwargs)

        self.group_data = group_data
        self.duplicate_service = duplicate_service
        self.on_action_complete = on_action_complete
        self.expanded = False

        self._create_widgets(group_number)

    def _create_widgets(self, group_number: int):
        """Create widgets for the group"""

        # Header with summary
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=10)

        # Group number and info
        info_text = (
            f"#{group_number}  |  "
            f"{self.group_data['count']} {t('duplicate_copies')}  |  "
            f"{self.group_data['file_size_mb']} MB {t('duplicate_each')}  |  "
            f"⚠️ {self.group_data['wasted_space_mb']} MB {t('duplicate_wasted')}"
        )

        info_label = ctk.CTkLabel(
            header,
            text=info_text,
            font=NORMAL_FONT,
            anchor="w"
        )
        info_label.pack(side="left", fill="x", expand=True)

        # Expand button
        self.expand_btn = ctk.CTkButton(
            header,
            text="▼",
            width=30,
            height=30,
            command=self._toggle_expand,
            font=("Arial", 14)
        )
        self.expand_btn.pack(side="right")

        # Expandable details frame
        self.details_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)

        # This will be populated when expanded

    def _toggle_expand(self):
        """Toggle expand/collapse"""
        if self.expanded:
            self.details_frame.pack_forget()
            self.expand_btn.configure(text="▼")
            self.expanded = False
        else:
            self._populate_details()
            self.details_frame.pack(fill="x", padx=10, pady=(0, 10))
            self.expand_btn.configure(text="▲")
            self.expanded = True

    def _populate_details(self):
        """Populate the details frame"""
        # Clear existing
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        # Files list
        files_label = ctk.CTkLabel(
            self.details_frame,
            text=t("duplicate_files_in_group"),
            font=HEADING_FONT
        )
        files_label.pack(anchor="w", padx=10, pady=(10, 5))

        for idx, file_info in enumerate(self.group_data["files"]):
            file_frame = ctk.CTkFrame(self.details_frame, fg_color=CARD_BACKGROUND)
            file_frame.pack(fill="x", padx=10, pady=2)

            # File path
            path_label = ctk.CTkLabel(
                file_frame,
                text=f"[{idx + 1}] {file_info['path']}",
                font=SMALL_FONT,
                anchor="w"
            )
            path_label.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        # Actions
        actions_frame = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=10, pady=10)

        StyledButton(
            actions_frame,
            text=t("btn_delete_duplicates"),
            command=self._delete_duplicates,
            variant="danger"
        ).pack(side="left", padx=5)

        StyledButton(
            actions_frame,
            text=t("btn_move_duplicates"),
            command=self._move_duplicates,
            variant="warning"
        ).pack(side="left", padx=5)

    def _delete_duplicates(self):
        """Delete duplicate files"""
        confirm = messagebox.askyesno(
            t("confirm"),
            t("duplicate_confirm_delete",
              count=self.group_data['count'] - 1,
              kept=self.group_data['files'][0]['path'])
        )

        if not confirm:
            return

        try:
            result = self.duplicate_service.delete_duplicates(self.group_data)

            if result["success"]:
                messagebox.showinfo(
                    t("success"),
                    t("duplicate_delete_success",
                      deleted=result["deleted"],
                      failed=result["failed"])
                )

                # Remove this group from results
                self.destroy()
                self.on_action_complete(self.group_data)
            else:
                messagebox.showerror(t("error"), result.get("error", "Unknown error"))

        except Exception as e:
            messagebox.showerror(t("error"), str(e))

    def _move_duplicates(self):
        """Move duplicate files to a folder"""
        dest_folder = filedialog.askdirectory(title=t("duplicate_select_move_folder"))

        if not dest_folder:
            return

        try:
            result = self.duplicate_service.move_duplicates(
                self.group_data,
                dest_folder
            )

            if result["success"]:
                messagebox.showinfo(
                    t("success"),
                    t("duplicate_move_success",
                      moved=result["moved"],
                      failed=result["failed"],
                      destination=result["destination"])
                )

                # Remove this group from results
                self.destroy()
                self.on_action_complete(self.group_data)
            else:
                messagebox.showerror(t("error"), result.get("error", "Unknown error"))

        except Exception as e:
            messagebox.showerror(t("error"), str(e))
