"""File Organizer tab UI with i18n support"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from typing import Optional
from gui.components import *
from gui.styles import *
from gui.i18n import t
from app.services.file_organizer import FileOrganizer


class OrganizerTab(ctk.CTkFrame):
    """File organizer tab with multi-language support"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BACKGROUND_COLOR, **kwargs)

        try:
            self.organizer = FileOrganizer()
        except Exception as e:
            messagebox.showerror(t("error"), f"Failed to initialize File Organizer: {str(e)}")
            self.organizer = None

        self._create_widgets()

    def _create_widgets(self):
        """Create all widgets for organizer tab"""

        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

        # Left panel - Configuration
        left_panel = Card(container, title=t("organizer_title"))
        left_panel.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left_panel.configure(width=400)

        # Source directory
        self.source_input = FilePathInput(
            left_panel,
            label=t("organizer_source"),
            browse_callback=self._browse_source,
            mode="folder"
        )
        self.source_input.pack(fill="x", padx=PADDING, pady=10)

        # Destination directory
        self.dest_input = FilePathInput(
            left_panel,
            label=t("organizer_destination"),
            browse_callback=self._browse_dest,
            mode="folder"
        )
        self.dest_input.pack(fill="x", padx=PADDING, pady=10)

        # Options frame
        options_label = ctk.CTkLabel(left_panel, text=t("organizer_options"), font=HEADING_FONT)
        options_label.pack(anchor="w", padx=PADDING, pady=(10, 5))

        options_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        options_frame.pack(fill="x", padx=PADDING, pady=5)

        # Operation mode
        mode_label = ctk.CTkLabel(options_frame, text=t("organizer_mode"), font=NORMAL_FONT)
        mode_label.pack(anchor="w", pady=(5, 2))

        self.mode_var = ctk.StringVar(value="copy")

        ctk.CTkRadioButton(
            options_frame,
            text=t("organizer_mode_copy"),
            variable=self.mode_var,
            value="copy",
            font=NORMAL_FONT
        ).pack(anchor="w", pady=2)

        ctk.CTkRadioButton(
            options_frame,
            text=t("organizer_mode_move"),
            variable=self.mode_var,
            value="move",
            font=NORMAL_FONT
        ).pack(anchor="w", pady=2)

        ctk.CTkRadioButton(
            options_frame,
            text=t("organizer_mode_delete"),
            variable=self.mode_var,
            value="delete",
            font=NORMAL_FONT
        ).pack(anchor="w", pady=2)

        # Recursive option
        self.recursive_var = ctk.BooleanVar(value=False)
        recursive_cb = ctk.CTkCheckBox(
            options_frame,
            text=t("organizer_recursive"),
            variable=self.recursive_var,
            font=NORMAL_FONT
        )
        recursive_cb.pack(anchor="w", pady=10)

        # Organize button
        StyledButton(
            left_panel,
            text=t("btn_organize"),
            command=self._start_organize,
            variant="success"
        ).pack(fill="x", padx=PADDING, pady=20)

        # Right panel - Results and stats
        right_panel = ctk.CTkFrame(container, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True)

        # Info cards
        info_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        info_frame.pack(fill="x", pady=(0, 10))

        self.organized_card = InfoCard(
            info_frame,
            title=t("organizer_organized"),
            value="0",
            color=SUCCESS_COLOR
        )
        self.organized_card.pack(side="left", expand=True, fill="x", padx=5)

        self.failed_card = InfoCard(
            info_frame,
            title=t("organizer_failed"),
            value="0",
            color=DANGER_COLOR
        )
        self.failed_card.pack(side="left", expand=True, fill="x", padx=5)

        self.categories_card = InfoCard(
            info_frame,
            title=t("organizer_categories"),
            value="0",
            color=PRIMARY_COLOR
        )
        self.categories_card.pack(side="left", expand=True, fill="x", padx=5)

        # Progress
        self.progress_card = ProgressCard(right_panel)
        self.progress_card.pack(fill="x", pady=10)

        # Log/Results area
        log_card = Card(right_panel, title=t("organizer_log"))
        log_card.pack(fill="both", expand=True)

        self.log_text = ctk.CTkTextbox(
            log_card,
            font=SMALL_FONT,
            wrap="word",
            height=400
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

    def _browse_source(self, mode: str) -> Optional[str]:
        """Browse for source directory"""
        return filedialog.askdirectory(title=t("organizer_source"))

    def _browse_dest(self, mode: str) -> Optional[str]:
        """Browse for destination directory"""
        return filedialog.askdirectory(title=t("organizer_destination"))

    def _start_organize(self):
        """Start organization process"""
        if not self.organizer:
            messagebox.showerror(t("error"), "File Organizer not initialized")
            return

        source = self.source_input.get()
        destination = self.dest_input.get()

        if not source:
            messagebox.showerror(t("error"), t("msg_select_source"))
            return

        if not destination:
            messagebox.showerror(t("error"), t("msg_select_destination"))
            return

        # Confirm operation
        mode = self.mode_var.get()
        mode_text = {
            'copy': t("organizer_mode_copy"),
            'move': t("organizer_mode_move"),
            'delete': t("organizer_mode_delete")
        }.get(mode, "Copy")

        confirm_msg = t("msg_confirm_organize", mode=mode_text, source=source, dest=destination)
        if not messagebox.askyesno(t("confirm"), confirm_msg):
            return

        # Run in background thread
        thread = threading.Thread(target=self._perform_organize, daemon=True)
        thread.start()

    def _perform_organize(self):
        """Perform the actual organization"""
        try:
            source = self.source_input.get()
            destination = self.dest_input.get()
            mode = self.mode_var.get()
            recursive = self.recursive_var.get()

            # Clear log
            self.log_text.delete("1.0", "end")
            self._log(t("status_organizing") + "\n")
            self._log(f"{t('organizer_source')}: {source}\n")
            self._log(f"{t('organizer_destination')}: {destination}\n")
            self._log(f"{t('organizer_mode')}: {mode}\n\n")

            # Update progress
            self.progress_card.update_progress(0, t("status_organizing"), "")

            # Organize files
            organized, failed, errors = self.organizer.organize_files(
                source_dir=source,
                destination_dir=destination,
                mode=mode,
                recursive=recursive,
                progress_callback=self._organize_progress
            )

            # Get statistics
            stats = self.organizer.get_stats()

            # Update cards
            self.organized_card.update_value(str(organized))
            self.failed_card.update_value(str(failed))
            self.categories_card.update_value(str(len(stats.get('categories_used', {}))))

            # Log results
            self._log(f"\n{t('status_completed')}:\n")
            self._log(f"{t('organizer_organized')}: {organized}\n")
            self._log(f"{t('organizer_failed')}: {failed}\n")
            self._log(f"\n{t('organizer_categories_breakdown')}:\n")

            for category, count in sorted(stats.get('categories_used', {}).items()):
                self._log(f"  • {category}: {count} {t('files')}\n")

            if errors:
                self._log(f"\n{t('error')}:\n")
                for error in errors[:10]:  # Show first 10 errors
                    self._log(f"  ✗ {error}\n")
                if len(errors) > 10:
                    self._log(f"  ... and {len(errors) - 10} more errors\n")

            # Generate report
            self._log(f"\n{self.organizer.generate_report()}\n")

            self.progress_card.update_progress(1.0, t("status_completed"), "")
            messagebox.showinfo(t("info"), t("msg_organize_success"))

        except Exception as e:
            self._log(f"\n✗ {t('error')}: {str(e)}\n")
            messagebox.showerror(t("error"), t("error_organize_failed", error=str(e)))
            self.progress_card.update_progress(0, t("status_error"), str(e))

    def _organize_progress(self, progress: float, file_path: str):
        """Progress callback for organization"""
        self.progress_card.update_progress(
            progress / 100,
            t("status_organizing"),
            t("progress_current_file", file=file_path[-50:])
        )
        self._log(f"[{int(progress)}%] {file_path}\n")

    def _log(self, message: str):
        """Add message to log"""
        self.log_text.insert("end", message)
        self.log_text.see("end")
