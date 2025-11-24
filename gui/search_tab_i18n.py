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

        self._create_widgets()

    def _create_widgets(self):
        """Create all widgets for search tab"""

        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

        # Left panel - Search options
        left_panel = Card(container, title=t("search_title"))
        left_panel.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left_panel.configure(width=400)

        # Search path
        self.path_input = FilePathInput(
            left_panel,
            label=t("search_path"),
            browse_callback=self._browse_path,
            mode="folder"
        )
        self.path_input.pack(fill="x", padx=PADDING, pady=10)

        # File pattern
        pattern_label = ctk.CTkLabel(left_panel, text=t("search_pattern"), font=NORMAL_FONT)
        pattern_label.pack(anchor="w", padx=PADDING, pady=(10, 5))

        self.pattern_entry = ctk.CTkEntry(
            left_panel,
            font=NORMAL_FONT,
            height=35,
            placeholder_text=t("search_pattern_placeholder")
        )
        self.pattern_entry.pack(fill="x", padx=PADDING)
        self.pattern_entry.insert(0, "*")

        # File extension
        ext_label = ctk.CTkLabel(left_panel, text=t("search_extension"), font=NORMAL_FONT)
        ext_label.pack(anchor="w", padx=PADDING, pady=(10, 5))

        self.ext_entry = ctk.CTkEntry(
            left_panel,
            font=NORMAL_FONT,
            height=35,
            placeholder_text=t("search_extension_placeholder")
        )
        self.ext_entry.pack(fill="x", padx=PADDING)

        # Options frame
        options_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        options_frame.pack(fill="x", padx=PADDING, pady=10)

        # Recursive checkbox
        self.recursive_var = ctk.BooleanVar(value=True)
        recursive_cb = ctk.CTkCheckBox(
            options_frame,
            text=t("search_recursive"),
            variable=self.recursive_var,
            font=NORMAL_FONT
        )
        recursive_cb.pack(anchor="w", pady=5)

        # Case sensitive checkbox
        self.case_sensitive_var = ctk.BooleanVar(value=False)
        case_cb = ctk.CTkCheckBox(
            options_frame,
            text=t("search_case_sensitive"),
            variable=self.case_sensitive_var,
            font=NORMAL_FONT
        )
        case_cb.pack(anchor="w", pady=5)

        # Max results
        max_label = ctk.CTkLabel(left_panel, text=t("search_max_results"), font=NORMAL_FONT)
        max_label.pack(anchor="w", padx=PADDING, pady=(10, 5))

        self.max_results_entry = ctk.CTkEntry(
            left_panel,
            font=NORMAL_FONT,
            height=35,
            placeholder_text=t("search_max_results_placeholder")
        )
        self.max_results_entry.pack(fill="x", padx=PADDING)
        self.max_results_entry.insert(0, "100")

        # Search buttons
        btn_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=PADDING, pady=20)

        StyledButton(
            btn_frame,
            text=t("btn_search"),
            command=self._start_search,
            variant="primary"
        ).pack(fill="x", pady=5)

        StyledButton(
            btn_frame,
            text=t("btn_search_all_drives"),
            command=self._search_all_drives,
            variant="success"
        ).pack(fill="x", pady=5)

        StyledButton(
            btn_frame,
            text=t("btn_get_drives"),
            command=self._show_drives,
            variant="primary"
        ).pack(fill="x", pady=5)

        # Right panel - Results
        right_panel = ctk.CTkFrame(container, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True)

        # Info cards
        info_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        info_frame.pack(fill="x", pady=(0, 10))

        self.results_count_card = InfoCard(
            info_frame,
            title=t("files_found"),
            value="0",
            color=PRIMARY_COLOR
        )
        self.results_count_card.pack(side="left", expand=True, fill="x", padx=5)

        self.total_size_card = InfoCard(
            info_frame,
            title=t("total_size"),
            value="0 MB",
            color=SUCCESS_COLOR
        )
        self.total_size_card.pack(side="left", expand=True, fill="x", padx=5)

        # Progress
        self.progress_card = ProgressCard(right_panel)
        self.progress_card.pack(fill="x", pady=10)

        # Results table
        results_card = Card(right_panel, title=t("search_results"))
        results_card.pack(fill="both", expand=True)

        self.results_table = ResultsTable(
            results_card,
            columns=[t("col_file_name"), t("col_path"), t("col_size"), t("col_modified")],
            height=400
        )
        self.results_table.pack(fill="both", expand=True, padx=10, pady=10)

    def _browse_path(self, mode: str) -> Optional[str]:
        """Browse for folder"""
        folder = filedialog.askdirectory(title=t("search_path"))
        return folder if folder else None

    def _start_search(self):
        """Start file search"""
        search_path = self.path_input.get()

        if not search_path:
            messagebox.showerror(t("error"), t("msg_select_path"))
            return

        # Run search in background thread
        thread = threading.Thread(target=self._perform_search, daemon=True)
        thread.start()

    def _perform_search(self):
        """Perform the actual search"""
        try:
            # Get search parameters
            search_path = self.path_input.get()
            pattern = self.pattern_entry.get() or "*"
            extension = self.ext_entry.get() or None
            recursive = self.recursive_var.get()
            case_sensitive = self.case_sensitive_var.get()

            max_results = self.max_results_entry.get()
            max_results = int(max_results) if max_results else None

            # Clear previous results
            self.results_table.clear()
            self.search_results = []

            # Update UI
            self.progress_card.update_progress(0, t("status_searching"), "")

            # Perform search
            count = 0
            total_size = 0

            for file_info in self.search_service.search_files(
                search_path=search_path,
                file_pattern=pattern,
                file_extension=extension,
                recursive=recursive,
                max_results=max_results,
                case_sensitive=case_sensitive
            ):
                self.search_results.append(file_info)
                count += 1
                total_size += file_info['size']

                # Add to table
                self.results_table.add_row([
                    file_info['name'],
                    file_info['path'][:50] + "..." if len(file_info['path']) > 50 else file_info['path'],
                    file_info['size_mb'],
                    file_info['modified'][:19]
                ])

                # Update progress
                if max_results:
                    progress = count / max_results
                    self.progress_card.update_progress(
                        progress,
                        t("progress_found_files", count=count),
                        f"{total_size / (1024 * 1024):.2f} MB"
                    )

            # Update final stats
            self.results_count_card.update_value(str(count))
            self.total_size_card.update_value(f"{total_size / (1024 * 1024):.2f} MB")
            self.progress_card.update_progress(
                1.0,
                t("status_completed"),
                t("progress_found_files", count=count) + f" ({total_size / (1024 * 1024):.2f} MB)"
            )

        except Exception as e:
            messagebox.showerror(t("error"), t("error_search_failed", error=str(e)))
            self.progress_card.update_progress(0, t("status_error"), str(e))

    def _search_all_drives(self):
        """Search across all drives"""
        messagebox.showinfo(
            t("info"),
            t("msg_search_all_drives")
        )

        # Update path to show all drives
        self.path_input.set("All Drives")

        # Run search in background
        thread = threading.Thread(target=self._perform_all_drives_search, daemon=True)
        thread.start()

    def _perform_all_drives_search(self):
        """Search all drives"""
        try:
            pattern = self.pattern_entry.get() or "*"
            extension = self.ext_entry.get() or None
            max_per_drive = 50

            self.results_table.clear()
            self.search_results = []
            self.progress_card.update_progress(0, t("status_searching"), "")

            count = 0
            total_size = 0

            for file_info in self.search_service.search_in_multiple_drives(
                file_pattern=pattern,
                file_extension=extension,
                max_results_per_drive=max_per_drive
            ):
                self.search_results.append(file_info)
                count += 1
                total_size += file_info['size']

                self.results_table.add_row([
                    file_info['name'],
                    f"{file_info['drive']} - {file_info['path'][:40]}...",
                    file_info['size_mb'],
                    file_info['modified'][:19]
                ])

            self.results_count_card.update_value(str(count))
            self.total_size_card.update_value(f"{total_size / (1024 * 1024):.2f} MB")
            self.progress_card.update_progress(1.0, t("status_completed"), t("progress_found_files", count=count))

        except Exception as e:
            messagebox.showerror(t("error"), t("error_search_failed", error=str(e)))

    def _show_drives(self):
        """Show available drives"""
        try:
            drives = self.search_service.get_available_drives()
            drives_str = "\n".join(drives)
            messagebox.showinfo(
                t("info"),
                t("info_drives_found", count=len(drives), drives=drives_str)
            )
        except Exception as e:
            messagebox.showerror(t("error"), t("error_get_drives", error=str(e)))
