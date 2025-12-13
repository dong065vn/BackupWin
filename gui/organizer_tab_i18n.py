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
    """File organizer tab"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BACKGROUND_COLOR, **kwargs)
        try:
            self.organizer = FileOrganizer()
        except Exception as e:
            messagebox.showerror(t("error"), f"Failed to initialize: {e}")
            self.organizer = None
        self._create_widgets()

    def _create_widgets(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

        # Left panel
        left = Card(container, title=t("organizer_title"))
        left.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left.configure(width=400)

        self.source_input = FilePathInput(left, label=t("organizer_source"), browse_callback=lambda m: filedialog.askdirectory(title=t("organizer_source")), mode="folder")
        self.source_input.pack(fill="x", padx=PADDING, pady=10)

        self.dest_input = FilePathInput(left, label=t("organizer_destination"), browse_callback=lambda m: filedialog.askdirectory(title=t("organizer_destination")), mode="folder")
        self.dest_input.pack(fill="x", padx=PADDING, pady=10)

        ctk.CTkLabel(left, text=t("organizer_options"), font=HEADING_FONT).pack(anchor="w", padx=PADDING, pady=(10, 5))
        opts = ctk.CTkFrame(left, fg_color="transparent")
        opts.pack(fill="x", padx=PADDING, pady=5)

        ctk.CTkLabel(opts, text=t("organizer_mode"), font=NORMAL_FONT).pack(anchor="w", pady=(5, 2))
        self.mode_var = ctk.StringVar(value="copy")
        for val, txt in [("copy", "organizer_mode_copy"), ("move", "organizer_mode_move"), ("delete", "organizer_mode_delete")]:
            ctk.CTkRadioButton(opts, text=t(txt), variable=self.mode_var, value=val, font=NORMAL_FONT).pack(anchor="w", pady=2)

        self.recursive_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(opts, text=t("organizer_recursive"), variable=self.recursive_var, font=NORMAL_FONT).pack(anchor="w", pady=10)

        StyledButton(left, text=t("btn_organize"), command=self._start_organize, variant="success").pack(fill="x", padx=PADDING, pady=20)

        # Right panel
        right = ctk.CTkFrame(container, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)

        info = ctk.CTkFrame(right, fg_color="transparent")
        info.pack(fill="x", pady=(0, 10))
        self.organized_card = InfoCard(info, title=t("organizer_organized"), value="0", color=SUCCESS_COLOR)
        self.organized_card.pack(side="left", expand=True, fill="both", padx=(0, 5))
        self.failed_card = InfoCard(info, title=t("organizer_failed"), value="0", color=DANGER_COLOR)
        self.failed_card.pack(side="left", expand=True, fill="both", padx=(0, 5))
        self.categories_card = InfoCard(info, title=t("organizer_categories"), value="0", color=PRIMARY_COLOR)
        self.categories_card.pack(side="left", expand=True, fill="both")

        self.progress_card = ProgressCard(right)
        self.progress_card.pack(fill="x", pady=10)

        log_card = Card(right, title=t("organizer_log"))
        log_card.pack(fill="both", expand=True)
        self.log_text = ctk.CTkTextbox(log_card, font=SMALL_FONT, wrap="word", height=400)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

    def _start_organize(self):
        if not self.organizer:
            messagebox.showerror(t("error"), "Organizer not initialized")
            return
        source, dest = self.source_input.get(), self.dest_input.get()
        if not source:
            messagebox.showerror(t("error"), t("msg_select_source"))
            return
        if not dest:
            messagebox.showerror(t("error"), t("msg_select_destination"))
            return

        mode = self.mode_var.get()
        mode_text = {"copy": t("organizer_mode_copy"), "move": t("organizer_mode_move"), "delete": t("organizer_mode_delete")}.get(mode, "Copy")
        if not messagebox.askyesno(t("confirm"), t("msg_confirm_organize", mode=mode_text, source=source, dest=dest)):
            return
        threading.Thread(target=self._perform_organize, daemon=True).start()

    def _perform_organize(self):
        try:
            source, dest = self.source_input.get(), self.dest_input.get()
            mode, recursive = self.mode_var.get(), self.recursive_var.get()

            self.log_text.delete("1.0", "end")
            self._log(f"{t('status_organizing')}\nSource: {source}\nDest: {dest}\nMode: {mode}\n\n")
            self.progress_card.update_progress(0, t("status_organizing"), "")

            organized, failed, errors = self.organizer.organize_files(source, dest, mode, recursive, self._progress)
            stats = self.organizer.get_stats()

            self.organized_card.update_value(str(organized))
            self.failed_card.update_value(str(failed))
            self.categories_card.update_value(str(len(stats.get('categories_used', {}))))

            self._log(f"\n{t('status_completed')}:\n{t('organizer_organized')}: {organized}\n{t('organizer_failed')}: {failed}\n\n{t('organizer_categories_breakdown')}:\n")
            for cat, cnt in sorted(stats.get('categories_used', {}).items()):
                self._log(f"  • {cat}: {cnt} {t('files')}\n")

            if errors:
                self._log(f"\n{t('error')}:\n")
                for e in errors[:10]:
                    self._log(f"  ✗ {e}\n")
                if len(errors) > 10:
                    self._log(f"  ... and {len(errors) - 10} more\n")

            self._log(f"\n{self.organizer.generate_report()}\n")
            self.progress_card.update_progress(1.0, t("status_completed"), "")
            messagebox.showinfo(t("info"), t("msg_organize_success"))
        except Exception as e:
            self._log(f"\n✗ {t('error')}: {str(e)}\n")
            messagebox.showerror(t("error"), t("error_organize_failed", error=str(e)))
            self.progress_card.update_progress(0, t("status_error"), str(e))

    def _progress(self, progress: float, file_path: str):
        self.progress_card.update_progress(progress / 100, t("status_organizing"), file_path[-50:])
        self._log(f"[{int(progress)}%] {file_path}\n")

    def _log(self, msg: str):
        self.log_text.insert("end", msg)
        self.log_text.see("end")

    def receive_files(self, file_paths: list):
        if not file_paths:
            return
        from pathlib import Path
        folders = set(str(Path(f).parent) for f in file_paths)
        if len(folders) == 1:
            self.source_input.set(folders.pop())
            self._log(f"\nSet source to folder with {len(file_paths)} file(s)\n")
        else:
            messagebox.showinfo(t("info"), f"Files from {len(folders)} folders. Please select source manually.")
            self._log(f"\nReceived {len(file_paths)} files from {len(folders)} folders\n")
