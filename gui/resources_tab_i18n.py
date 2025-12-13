"""Resources Tab with Multi-language Support"""
import customtkinter as ctk
from tkinter import messagebox
import os
import subprocess
import shutil
from pathlib import Path
from .styles import *
from .i18n import t


class ResourcesTab(ctk.CTkFrame):
    """Resources management tab"""

    FOLDERS = {"software_installer": "Cai dat phan mem", "office_tools": "OFFICE, WINRAR, IDM", "backup_tools": "Sao luu du lieu"}

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._create_widgets()

    def _create_widgets(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True)

        title_frame = ctk.CTkFrame(main, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, SPACE_LG))
        ctk.CTkLabel(title_frame, text=t("resources_title"), font=(FONT_FAMILY, 24, "bold"), text_color=TEXT_COLOR).pack(anchor="w")

        cat_frame = ctk.CTkFrame(main, fg_color=CARD_BACKGROUND, corner_radius=RADIUS_MD)
        cat_frame.pack(fill="x", pady=(0, SPACE_LG))
        cat_inner = ctk.CTkFrame(cat_frame, fg_color="transparent")
        cat_inner.pack(fill="x", padx=SPACE_LG, pady=SPACE_LG)

        ctk.CTkLabel(cat_inner, text=t("resources_category"), font=(FONT_FAMILY, 14, "bold"), text_color=TEXT_COLOR).pack(side="left", padx=(0, SPACE_MD))
        self.category_var = ctk.StringVar(value=t("resources_software_installer"))
        self.category_selector = ctk.CTkComboBox(cat_inner, values=[t("resources_software_installer"), t("resources_office_tools"), t("resources_backup_tools")],
            variable=self.category_var, command=lambda _: self._load_category(), width=300, height=40, font=(FONT_FAMILY, 13), dropdown_font=(FONT_FAMILY, 12))
        self.category_selector.pack(side="left")

        self.resource_display = ctk.CTkFrame(main, fg_color=CARD_BACKGROUND, corner_radius=RADIUS_MD)
        self.resource_display.pack(fill="both", expand=True)
        self._load_category()

    def _get_category_key(self):
        return {"resources_software_installer": "software_installer", "resources_office_tools": "office_tools", "resources_backup_tools": "backup_tools"}.get(
            next((k for k, v in {t("resources_software_installer"): "software_installer", t("resources_office_tools"): "office_tools", t("resources_backup_tools"): "backup_tools"}.items() if k == self.category_var.get()), "software_installer"), "software_installer")

    def _load_category(self):
        for w in self.resource_display.winfo_children():
            w.destroy()

        key = self._get_category_key()
        folder = Path(self.FOLDERS[key])
        content = ctk.CTkFrame(self.resource_display, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SPACE_LG, pady=SPACE_LG)

        ctk.CTkLabel(content, text=t(f"resources_{key}_desc"), font=(FONT_FAMILY, 13), text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, SPACE_LG))

        if not folder.exists():
            ctk.CTkLabel(content, text=f"⚠️ Folder not found: {folder}", font=(FONT_FAMILY, 13), text_color=DANGER_COLOR).pack(pady=SPACE_XL)
            return

        try:
            files = [f for f in folder.iterdir() if f.is_file()]
            if not files:
                ctk.CTkLabel(content, text="📂 No files", font=(FONT_FAMILY, 13), text_color=TEXT_SECONDARY).pack(pady=SPACE_XL)
                return
            for f in sorted(files):
                self._create_file_card(content, f, folder)
        except Exception as e:
            ctk.CTkLabel(content, text=f"Error: {e}", font=(FONT_FAMILY, 13), text_color=DANGER_COLOR).pack(pady=SPACE_XL)

    def _create_file_card(self, parent, file_path: Path, folder: Path):
        card = ctk.CTkFrame(parent, fg_color=BG_SECONDARY, corner_radius=RADIUS_SM)
        card.pack(fill="x", pady=(0, SPACE_MD))
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=SPACE_MD, pady=SPACE_MD)

        info = ctk.CTkFrame(inner, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(info, text=f"📄 {file_path.name}", font=(FONT_FAMILY, 14, "bold"), text_color=TEXT_COLOR, anchor="w").pack(anchor="w")
        ctk.CTkLabel(info, text=f"💾 {file_path.stat().st_size / 1048576:.2f} MB", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY, anchor="w").pack(anchor="w", pady=(2, 0))

        actions = ctk.CTkFrame(inner, fg_color="transparent")
        actions.pack(side="right")
        ctk.CTkButton(actions, text=t("btn_open_folder_location"), command=lambda: self._open_folder(folder), width=140, height=36, font=(FONT_FAMILY, 12), fg_color=INFO_COLOR, hover_color=PRIMARY_HOVER).pack(side="left", padx=(0, SPACE_SM))
        if file_path.suffix.lower() in ['.exe', '.bat']:
            ctk.CTkButton(actions, text=t("btn_run_executable"), command=lambda: self._run_file(file_path), width=120, height=36, font=(FONT_FAMILY, 12), fg_color=SUCCESS_COLOR, hover_color="#1e7e34").pack(side="left", padx=(0, SPACE_SM))
        ctk.CTkButton(actions, text=t("btn_copy_to_desktop"), command=lambda: self._copy_to_desktop(file_path), width=140, height=36, font=(FONT_FAMILY, 12), fg_color=PRIMARY_COLOR, hover_color=PRIMARY_HOVER).pack(side="left")

    def _open_folder(self, folder: Path):
        try:
            os.startfile(folder) if os.name == 'nt' else subprocess.run(['xdg-open', folder])
        except Exception as e:
            messagebox.showerror(t("error"), t("error_run_failed").format(error=str(e)))

    def _run_file(self, file_path: Path):
        try:
            if messagebox.askyesno(t("confirm"), t("msg_run_executable").format(file=file_path.name)):
                os.startfile(file_path) if os.name == 'nt' else subprocess.Popen([str(file_path)])
                messagebox.showinfo(t("success"), t("msg_run_success").format(file=file_path.name))
        except Exception as e:
            messagebox.showerror(t("error"), t("error_run_failed").format(error=str(e)))

    def _copy_to_desktop(self, file_path: Path):
        try:
            desktop = Path.home() / "Desktop"
            if not desktop.exists():
                desktop = Path.home() / "Bureau"
            if not desktop.exists():
                desktop = Path.home()
            dest = desktop / file_path.name
            counter = 1
            while dest.exists():
                dest = desktop / f"{file_path.stem}_{counter}{file_path.suffix}"
                counter += 1
            shutil.copy2(file_path, dest)
            messagebox.showinfo(t("success"), t("msg_copy_success"))
        except Exception as e:
            messagebox.showerror(t("error"), t("error_copy_failed").format(error=str(e)))
