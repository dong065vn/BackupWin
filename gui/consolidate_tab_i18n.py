"""Consolidate files tab UI with i18n support"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from typing import List
from pathlib import Path
from gui.components import *
from gui.styles import *
from gui.i18n import t
from app.services.file_consolidation import FileConsolidationService


class ConsolidateTab(ctk.CTkFrame):
    """Consolidate files tab"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BACKGROUND_COLOR, **kwargs)
        self.consolidation_service = FileConsolidationService()
        self.file_list: List[str] = []
        self._create_widgets()

    def _create_widgets(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

        # Left panel
        left = Card(container, title=t("consolidate_title"))
        left.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left.configure(width=400)

        ctk.CTkLabel(left, text=t("consolidate_operation"), font=HEADING_FONT).pack(anchor="w", padx=PADDING, pady=(10, 5))
        self.operation_mode = ctk.StringVar(value="copy")
        mode_frame = ctk.CTkFrame(left, fg_color="transparent")
        mode_frame.pack(fill="x", padx=PADDING, pady=5)
        ctk.CTkRadioButton(mode_frame, text=t("consolidate_copy"), variable=self.operation_mode, value="copy", font=NORMAL_FONT).pack(anchor="w", pady=2)
        ctk.CTkRadioButton(mode_frame, text=t("consolidate_move"), variable=self.operation_mode, value="move", font=NORMAL_FONT).pack(anchor="w", pady=2)

        self.dest_input = FilePathInput(left, label=t("consolidate_destination"), browse_callback=lambda m: filedialog.askdirectory(title=t("consolidate_destination")), mode="folder")
        self.dest_input.pack(fill="x", padx=PADDING, pady=10)

        ctk.CTkLabel(left, text=t("consolidate_duplicate_handling"), font=HEADING_FONT).pack(anchor="w", padx=PADDING, pady=(10, 5))
        self.duplicate_handling = ctk.StringVar(value="rename")
        dup_frame = ctk.CTkFrame(left, fg_color="transparent")
        dup_frame.pack(fill="x", padx=PADDING, pady=5)
        for val, txt in [("skip", "consolidate_skip"), ("rename", "consolidate_rename"), ("overwrite", "consolidate_overwrite")]:
            ctk.CTkRadioButton(dup_frame, text=t(txt), variable=self.duplicate_handling, value=val, font=NORMAL_FONT).pack(anchor="w", pady=2)

        self.preserve_structure_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(left, text=t("consolidate_preserve_structure"), variable=self.preserve_structure_var, font=NORMAL_FONT).pack(anchor="w", padx=PADDING, pady=10)

        StyledButton(left, text=t("btn_preview"), command=self._show_preview, variant="primary").pack(fill="x", padx=PADDING, pady=(10, 5))
        StyledButton(left, text=t("btn_start_consolidate"), command=self._start_consolidation, variant="success").pack(fill="x", padx=PADDING, pady=(5, 20))

        # Right panel
        right = ctk.CTkFrame(container, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)

        # Stats cards at top
        info_cards = ctk.CTkFrame(right, fg_color="transparent")
        info_cards.pack(fill="x", pady=(0, 10))
        self.successful_card = InfoCard(info_cards, title=t("consolidate_successful"), value="0", color=SUCCESS_COLOR)
        self.successful_card.pack(side="left", expand=True, fill="both", padx=(0, 5))
        self.skipped_card = InfoCard(info_cards, title=t("consolidate_skipped"), value="0", color=WARNING_COLOR)
        self.skipped_card.pack(side="left", expand=True, fill="both", padx=(0, 5))
        self.failed_card = InfoCard(info_cards, title=t("consolidate_failed"), value="0", color=DANGER_COLOR)
        self.failed_card.pack(side="left", expand=True, fill="both")

        self.progress_card = ProgressCard(right)
        self.progress_card.pack(fill="x", pady=(0, 10))

        # File list card
        file_card = Card(right, title=t("consolidate_file_list"))
        file_card.pack(fill="both", expand=True)

        btn_frame = ctk.CTkFrame(file_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=PADDING, pady=10)
        StyledButton(btn_frame, text=t("btn_add_file"), command=self._add_single_file, variant="primary").pack(side="left", padx=5)
        StyledButton(btn_frame, text=t("btn_add_files"), command=self._add_multiple_files, variant="primary").pack(side="left", padx=5)
        StyledButton(btn_frame, text=t("btn_add_from_folder"), command=self._add_from_folder, variant="primary").pack(side="left", padx=5)
        StyledButton(btn_frame, text=t("btn_clear_all"), command=self._clear_all, variant="danger").pack(side="right", padx=5)

        self.file_list_frame = ctk.CTkScrollableFrame(file_card, fg_color=BACKGROUND_COLOR)
        self.file_list_frame.pack(fill="both", expand=True, padx=PADDING, pady=(0, 10))

        info_frame = ctk.CTkFrame(file_card, fg_color="transparent")
        info_frame.pack(fill="x", padx=PADDING, pady=(0, 10))
        self.file_count_label = ctk.CTkLabel(info_frame, text=t("consolidate_total_files", count=0), font=NORMAL_FONT)
        self.file_count_label.pack(side="left", padx=5)
        self.file_size_label = ctk.CTkLabel(info_frame, text=t("consolidate_total_size", size="0 MB"), font=NORMAL_FONT)
        self.file_size_label.pack(side="left", padx=5)

    def _add_single_file(self):
        if f := filedialog.askopenfilename(title=t("btn_add_file")):
            self._add_file_to_list(f)

    def _add_multiple_files(self):
        for f in filedialog.askopenfilenames(title=t("btn_add_files")):
            self._add_file_to_list(f)

    def _add_from_folder(self):
        if folder := filedialog.askdirectory(title=t("btn_add_from_folder")):
            try:
                files = [str(f) for f in Path(folder).iterdir() if f.is_file()]
                if not files:
                    messagebox.showinfo(t("info"), t("msg_no_files_in_folder"))
                    return
                for f in files:
                    self._add_file_to_list(f)
                messagebox.showinfo(t("info"), t("msg_files_added", count=len(files)))
            except Exception as e:
                messagebox.showerror(t("error"), t("msg_error_reading_folder", error=str(e)))

    def _add_file_to_list(self, path: str):
        if path not in self.file_list:
            self.file_list.append(path)
            self._refresh_file_list_display()

    def _refresh_file_list_display(self):
        for w in self.file_list_frame.winfo_children():
            w.destroy()
        total_size = 0
        for i, f in enumerate(self.file_list):
            item = ctk.CTkFrame(self.file_list_frame, fg_color=CARD_BACKGROUND, corner_radius=5)
            item.pack(fill="x", pady=2)
            content = ctk.CTkFrame(item, fg_color="transparent")
            content.pack(side="left", fill="both", expand=True, padx=10, pady=5)
            p = Path(f)
            ctk.CTkLabel(content, text=p.name, font=NORMAL_FONT, anchor="w").pack(anchor="w")
            try:
                size = p.stat().st_size
                total_size += size
                size_txt = f"{size/1048576:.3f} MB" if size >= 1024 else f"{size} bytes"
            except:
                size_txt = "Unknown"
            ctk.CTkLabel(content, text=f"{p.parent} | {size_txt}", font=SMALL_FONT, text_color=TEXT_LIGHT_COLOR, anchor="w").pack(anchor="w")
            ctk.CTkButton(item, text="✕", command=lambda idx=i: self._remove_file(idx), width=30, height=30, fg_color=DANGER_COLOR, font=("Arial", 14, "bold")).pack(side="right", padx=5)
        
        self.file_count_label.configure(text=t("consolidate_total_files", count=len(self.file_list)))
        self.file_size_label.configure(text=t("consolidate_total_size", size=f"{total_size/1048576:.2f} MB"))

    def _remove_file(self, idx: int):
        if 0 <= idx < len(self.file_list):
            del self.file_list[idx]
            self._refresh_file_list_display()

    def _clear_all(self):
        if self.file_list and messagebox.askyesno(t("confirm"), t("msg_confirm_clear_all", count=len(self.file_list))):
            self.file_list.clear()
            self._refresh_file_list_display()
            for card in [self.successful_card, self.skipped_card, self.failed_card]:
                card.update_value("0")
            self.progress_card.update_progress(0, t("status_ready"), "")

    def _show_preview(self):
        if not self.file_list:
            messagebox.showwarning(t("warning"), t("msg_no_files_selected"))
            return
        if not (dest := self.dest_input.get()):
            messagebox.showwarning(t("warning"), t("msg_select_destination"))
            return
        try:
            preview = self.consolidation_service.get_consolidation_preview(self.file_list, dest, self.preserve_structure_var.get(), self.duplicate_handling.get())
            if "error" in preview:
                messagebox.showerror(t("error"), preview["error"])
                return
            messagebox.showinfo(t("preview_title"), t("msg_preview_info", count=preview["total_files"], size=preview["total_size_mb"], conflicts=preview["conflicts"]))
        except Exception as e:
            messagebox.showerror(t("error"), str(e))

    def _start_consolidation(self):
        if not self.file_list:
            messagebox.showwarning(t("warning"), t("msg_no_files_selected"))
            return
        if not (dest := self.dest_input.get()):
            messagebox.showwarning(t("warning"), t("msg_select_destination"))
            return
        op = self.operation_mode.get()
        if not messagebox.askyesno(t("confirm"), t("msg_confirm_consolidate", count=len(self.file_list), operation=t(f"consolidate_{op}"), destination=dest)):
            return
        threading.Thread(target=self._perform_consolidation, daemon=True).start()

    def _perform_consolidation(self):
        try:
            for card in [self.successful_card, self.skipped_card, self.failed_card]:
                card.update_value("0")
            self.progress_card.update_progress(0, t("status_consolidating"), "")

            result = self.consolidation_service.consolidate_files(
                self.file_list, self.dest_input.get(), self.operation_mode.get(),
                self.duplicate_handling.get(), self.preserve_structure_var.get(),
                lambda c, t, f: self.progress_card.update_progress(c/t if t else 0, t("progress_consolidating", current=c, total=t), f)
            )

            if not result["success"]:
                messagebox.showerror(t("error"), result.get("error", "Unknown"))
                self.progress_card.update_progress(0, t("status_error"), "")
                return

            self.successful_card.update_value(str(result["successful"]))
            self.skipped_card.update_value(str(result["skipped"]))
            self.failed_card.update_value(str(result["failed"]))
            self.progress_card.update_progress(1.0, t("status_completed"), "")
            messagebox.showinfo(t("success"), t("msg_consolidation_complete", successful=result["successful"], skipped=result["skipped"], failed=result["failed"], size=result["total_size_mb"]))
        except Exception as e:
            messagebox.showerror(t("error"), str(e))
            self.progress_card.update_progress(0, t("status_error"), str(e))

    def receive_files(self, file_paths: list):
        if file_paths:
            for f in file_paths:
                self._add_file_to_list(f)
            messagebox.showinfo(t("info"), t("msg_files_added", count=len(file_paths)))
