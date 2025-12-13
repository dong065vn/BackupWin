"""Duplicate Finder tab UI with i18n support"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from typing import List, Dict, Optional
from gui.components import *
from gui.styles import *
from gui.i18n import t
from app.services.duplicate_finder import DuplicateFinderService


class DuplicateFinderTab(ctk.CTkFrame):
    """Duplicate Finder tab"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BACKGROUND_COLOR, **kwargs)
        self.duplicate_service = DuplicateFinderService()
        self.scan_paths: List[str] = []
        self.duplicate_groups: List[Dict] = []
        self._create_widgets()

    def _create_widgets(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

        # Left panel
        left = Card(container, title=t("duplicate_scan_options"))
        left.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left.configure(width=400)

        ctk.CTkLabel(left, text=t("duplicate_scan_paths"), font=HEADING_FONT).pack(anchor="w", padx=PADDING, pady=(10, 5))
        self.paths_frame = ctk.CTkFrame(left, fg_color=BACKGROUND_COLOR, height=100)
        self.paths_frame.pack(fill="x", padx=PADDING, pady=5)
        self.paths_label = ctk.CTkLabel(self.paths_frame, text=t("duplicate_no_paths"), font=SMALL_FONT, text_color=TEXT_LIGHT_COLOR)
        self.paths_label.pack(pady=10)

        path_btns = ctk.CTkFrame(left, fg_color="transparent")
        path_btns.pack(fill="x", padx=PADDING, pady=5)
        StyledButton(path_btns, text=t("btn_add_folder"), command=self._add_scan_path, variant="primary").pack(side="left", padx=(0, 5))
        StyledButton(path_btns, text=t("btn_clear_paths"), command=self._clear_paths, variant="danger").pack(side="left")

        ctk.CTkLabel(left, text=t("duplicate_comparison_method"), font=HEADING_FONT).pack(anchor="w", padx=PADDING, pady=(15, 5))
        self.comparison_method = ctk.StringVar(value="quick")
        method_frame = ctk.CTkFrame(left, fg_color="transparent")
        method_frame.pack(fill="x", padx=PADDING, pady=5)
        for val, txt in [("quick", "duplicate_method_quick"), ("hash", "duplicate_method_hash"), ("size_name", "duplicate_method_size_name")]:
            ctk.CTkRadioButton(method_frame, text=t(txt), variable=self.comparison_method, value=val, font=NORMAL_FONT).pack(anchor="w", pady=2)

        ctk.CTkLabel(left, text=t("duplicate_options"), font=HEADING_FONT).pack(anchor="w", padx=PADDING, pady=(15, 5))
        size_frame = ctk.CTkFrame(left, fg_color="transparent")
        size_frame.pack(fill="x", padx=PADDING, pady=5)
        ctk.CTkLabel(size_frame, text=t("duplicate_min_size"), font=NORMAL_FONT).pack(anchor="w", pady=(0, 2))
        self.min_size_entry = ctk.CTkEntry(size_frame, font=NORMAL_FONT, height=35, placeholder_text="0")
        self.min_size_entry.pack(fill="x")
        self.min_size_entry.insert(0, "0")

        ext_frame = ctk.CTkFrame(left, fg_color="transparent")
        ext_frame.pack(fill="x", padx=PADDING, pady=5)
        ctk.CTkLabel(ext_frame, text=t("duplicate_file_types"), font=NORMAL_FONT).pack(anchor="w", pady=(0, 2))
        self.extensions_entry = ctk.CTkEntry(ext_frame, font=NORMAL_FONT, height=35, placeholder_text=t("duplicate_file_types_placeholder"))
        self.extensions_entry.pack(fill="x")

        self.recursive_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(left, text=t("duplicate_recursive"), variable=self.recursive_var, font=NORMAL_FONT).pack(anchor="w", padx=PADDING, pady=10)
        StyledButton(left, text=t("btn_start_scan"), command=self._start_scan, variant="success").pack(fill="x", padx=PADDING, pady=20)

        # Right panel
        right = ctk.CTkFrame(container, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)

        stats = ctk.CTkFrame(right, fg_color="transparent")
        stats.pack(fill="x", pady=(0, 10))
        self.files_scanned_card = InfoCard(stats, title=t("duplicate_files_scanned"), value="0", color=PRIMARY_COLOR)
        self.files_scanned_card.pack(side="left", expand=True, fill="both", padx=(0, 5))
        self.groups_card = InfoCard(stats, title=t("duplicate_groups_found"), value="0", color=WARNING_COLOR)
        self.groups_card.pack(side="left", expand=True, fill="both", padx=(0, 5))
        self.wasted_space_card = InfoCard(stats, title=t("duplicate_space_wasted"), value="0 MB", color=DANGER_COLOR)
        self.wasted_space_card.pack(side="left", expand=True, fill="both")

        self.progress_card = ProgressCard(right)
        self.progress_card.pack(fill="x", pady=10)

        results_card = Card(right, title=t("duplicate_results"))
        results_card.pack(fill="both", expand=True)
        self.results_frame = ctk.CTkScrollableFrame(results_card, fg_color=BACKGROUND_COLOR)
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.no_results_label = ctk.CTkLabel(self.results_frame, text=t("duplicate_no_results"), font=NORMAL_FONT, text_color=TEXT_LIGHT_COLOR)
        self.no_results_label.pack(pady=50)

    def _add_scan_path(self):
        if folder := filedialog.askdirectory(title=t("duplicate_select_folder")):
            if folder not in self.scan_paths:
                self.scan_paths.append(folder)
                self._update_paths_display()
            else:
                messagebox.showinfo(t("info"), t("duplicate_path_already_added"))

    def _clear_paths(self):
        if self.scan_paths:
            self.scan_paths.clear()
            self._update_paths_display()

    def _update_paths_display(self):
        for w in self.paths_frame.winfo_children():
            w.destroy()
        if not self.scan_paths:
            self.paths_label = ctk.CTkLabel(self.paths_frame, text=t("duplicate_no_paths"), font=SMALL_FONT, text_color=TEXT_LIGHT_COLOR)
            self.paths_label.pack(pady=10)
        else:
            for i, p in enumerate(self.scan_paths):
                item = ctk.CTkFrame(self.paths_frame, fg_color=CARD_BACKGROUND)
                item.pack(fill="x", pady=2, padx=5)
                ctk.CTkLabel(item, text=p, font=SMALL_FONT, anchor="w").pack(side="left", fill="x", expand=True, padx=5, pady=3)
                ctk.CTkButton(item, text="✕", width=25, height=25, command=lambda idx=i: self._remove_path(idx), fg_color=DANGER_COLOR).pack(side="right", padx=3)

    def _remove_path(self, idx: int):
        if 0 <= idx < len(self.scan_paths):
            del self.scan_paths[idx]
            self._update_paths_display()

    def _start_scan(self):
        if not self.scan_paths:
            messagebox.showwarning(t("warning"), t("duplicate_no_paths_selected"))
            return
        try:
            min_size = int(self.min_size_entry.get() or "0")
        except ValueError:
            messagebox.showerror(t("error"), t("duplicate_invalid_size"))
            return
        exts = [e.strip() for e in self.extensions_entry.get().split(",")] if self.extensions_entry.get().strip() else None
        threading.Thread(target=self._perform_scan, args=(self.comparison_method.get(), min_size, exts, self.recursive_var.get()), daemon=True).start()

    def _perform_scan(self, comparison: str, min_size: int, extensions: Optional[List[str]], recursive: bool):
        try:
            self._clear_results()
            self.progress_card.update_progress(0, t("status_scanning"), "")
            for card in [self.files_scanned_card, self.groups_card, self.wasted_space_card]:
                card.update_value("...")

            result = self.duplicate_service.scan_for_duplicates(self.scan_paths, comparison, min_size, extensions, recursive, self._scan_progress)

            if not result["success"]:
                messagebox.showerror(t("error"), result.get("error", "Unknown"))
                self.progress_card.update_progress(0, t("status_error"), "")
                return

            self.files_scanned_card.update_value(str(result["total_files_scanned"]))
            self.groups_card.update_value(str(len(result["duplicate_groups"])))
            self.wasted_space_card.update_value(f"{result['space_wasted_mb']} MB")
            self.duplicate_groups = result["duplicate_groups"]
            self._display_results()
            self.progress_card.update_progress(1.0, t("status_completed"), "")
            messagebox.showinfo(t("success"), t("duplicate_scan_complete", groups=len(result["duplicate_groups"]), duplicates=result["total_duplicates"], space=result["space_wasted_mb"]))
        except Exception as e:
            messagebox.showerror(t("error"), str(e))
            self.progress_card.update_progress(0, t("status_error"), str(e))

    def _scan_progress(self, current: int, total: int, filename: str):
        self.progress_card.update_progress(current / total if total else 0, t("progress_scanning", current=current, total=total), filename[:50])

    def _clear_results(self):
        for w in self.results_frame.winfo_children():
            w.destroy()

    def _display_results(self):
        self._clear_results()
        if not self.duplicate_groups:
            ctk.CTkLabel(self.results_frame, text=t("duplicate_no_duplicates_found"), font=NORMAL_FONT, text_color=SUCCESS_COLOR).pack(pady=50)
            return
        for i, group in enumerate(self.duplicate_groups, 1):
            DuplicateGroupCard(self.results_frame, i, group, self.duplicate_service, self._on_group_action).pack(fill="x", pady=5, padx=5)

    def _on_group_action(self, group: Dict):
        self._display_results()
        total = sum(g["wasted_space"] for g in self.duplicate_groups)
        self.groups_card.update_value(str(len(self.duplicate_groups)))
        self.wasted_space_card.update_value(f"{round(total / 1048576, 2)} MB")


class DuplicateGroupCard(ctk.CTkFrame):
    """Card displaying a duplicate group"""

    def __init__(self, parent, num: int, data: Dict, service, on_action, **kwargs):
        super().__init__(parent, fg_color=CARD_BACKGROUND, corner_radius=10, **kwargs)
        self.data, self.service, self.on_action, self.expanded = data, service, on_action, False

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=10)
        info = f"#{num}  |  {data['count']} {t('duplicate_copies')}  |  {data['file_size_mb']} MB {t('duplicate_each')}  |  ⚠️ {data['wasted_space_mb']} MB {t('duplicate_wasted')}"
        ctk.CTkLabel(header, text=info, font=NORMAL_FONT, anchor="w").pack(side="left", fill="x", expand=True)
        self.expand_btn = ctk.CTkButton(header, text="▼", width=30, height=30, command=self._toggle, font=("Arial", 14))
        self.expand_btn.pack(side="right")
        self.details_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)

    def _toggle(self):
        if self.expanded:
            self.details_frame.pack_forget()
            self.expand_btn.configure(text="▼")
        else:
            self._populate_details()
            self.details_frame.pack(fill="x", padx=10, pady=(0, 10))
            self.expand_btn.configure(text="▲")
        self.expanded = not self.expanded

    def _populate_details(self):
        for w in self.details_frame.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.details_frame, text=t("duplicate_files_in_group"), font=HEADING_FONT).pack(anchor="w", padx=10, pady=(10, 5))
        for i, f in enumerate(self.data["files"]):
            item = ctk.CTkFrame(self.details_frame, fg_color=CARD_BACKGROUND)
            item.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(item, text=f"[{i+1}] {f['path']}", font=SMALL_FONT, anchor="w").pack(side="left", fill="x", expand=True, padx=5, pady=5)

        actions = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        actions.pack(fill="x", padx=10, pady=10)
        StyledButton(actions, text=t("btn_delete_duplicates"), command=self._delete, variant="danger").pack(side="left", padx=5)
        StyledButton(actions, text=t("btn_move_duplicates"), command=self._move, variant="warning").pack(side="left", padx=5)

    def _delete(self):
        if not messagebox.askyesno(t("confirm"), t("duplicate_confirm_delete", count=self.data['count']-1, kept=self.data['files'][0]['path'])):
            return
        try:
            result = self.service.delete_duplicates(self.data)
            if result["success"]:
                messagebox.showinfo(t("success"), t("duplicate_delete_success", deleted=result["deleted"], failed=result["failed"]))
                self.destroy()
                self.on_action(self.data)
            else:
                messagebox.showerror(t("error"), result.get("error", "Unknown"))
        except Exception as e:
            messagebox.showerror(t("error"), str(e))

    def _move(self):
        if not (dest := filedialog.askdirectory(title=t("duplicate_select_move_folder"))):
            return
        try:
            result = self.service.move_duplicates(self.data, dest)
            if result["success"]:
                messagebox.showinfo(t("success"), t("duplicate_move_success", moved=result["moved"], failed=result["failed"], destination=result["destination"]))
                self.destroy()
                self.on_action(self.data)
            else:
                messagebox.showerror(t("error"), result.get("error", "Unknown"))
        except Exception as e:
            messagebox.showerror(t("error"), str(e))
