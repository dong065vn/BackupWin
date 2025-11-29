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
    """Resources management tab with multi-language support"""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        # Resource folders mapping
        self.resource_folders = {
            "software_installer": "Cai dat phan mem",
            "office_tools": "OFFICE, WINRAR, IDM",
            "backup_tools": "Sao luu du lieu"
        }

        self._create_widgets()

    def _create_widgets(self):
        """Create tab widgets"""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)

        # Title Section
        title_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, SPACE_LG))

        title_label = ctk.CTkLabel(
            title_frame,
            text=t("resources_title"),
            font=(FONT_FAMILY, 24, "bold"),
            text_color=TEXT_PRIMARY
        )
        title_label.pack(anchor="w")

        # Category Selection
        category_frame = ctk.CTkFrame(main_container, fg_color=CARD_BACKGROUND, corner_radius=RADIUS_MD)
        category_frame.pack(fill="x", pady=(0, SPACE_LG))

        # Inner padding
        category_inner = ctk.CTkFrame(category_frame, fg_color="transparent")
        category_inner.pack(fill="x", padx=SPACE_LG, pady=SPACE_LG)

        category_label = ctk.CTkLabel(
            category_inner,
            text=t("resources_category"),
            font=(FONT_FAMILY, 14, "bold"),
            text_color=TEXT_PRIMARY
        )
        category_label.pack(side="left", padx=(0, SPACE_MD))

        self.category_var = ctk.StringVar(value=t("resources_software_installer"))
        self.category_selector = ctk.CTkComboBox(
            category_inner,
            values=[
                t("resources_software_installer"),
                t("resources_office_tools"),
                t("resources_backup_tools")
            ],
            variable=self.category_var,
            command=self._on_category_change,
            width=300,
            height=40,
            font=(FONT_FAMILY, 13),
            dropdown_font=(FONT_FAMILY, 12)
        )
        self.category_selector.pack(side="left")

        # Resource Display Area
        self.resource_display = ctk.CTkFrame(
            main_container,
            fg_color=CARD_BACKGROUND,
            corner_radius=RADIUS_MD
        )
        self.resource_display.pack(fill="both", expand=True)

        # Load initial category
        self._load_category()

    def _on_category_change(self, choice):
        """Handle category change"""
        self._load_category()

    def _get_category_key(self):
        """Get current category key from display name"""
        category_map = {
            t("resources_software_installer"): "software_installer",
            t("resources_office_tools"): "office_tools",
            t("resources_backup_tools"): "backup_tools"
        }
        return category_map.get(self.category_var.get(), "software_installer")

    def _load_category(self):
        """Load and display resources for selected category"""
        # Clear existing content
        for widget in self.resource_display.winfo_children():
            widget.destroy()

        # Get category info
        category_key = self._get_category_key()
        folder_name = self.resource_folders[category_key]
        folder_path = Path(folder_name)

        # Inner container with padding
        content = ctk.CTkFrame(self.resource_display, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SPACE_LG, pady=SPACE_LG)

        # Description
        desc_key = f"resources_{category_key}_desc"
        desc_label = ctk.CTkLabel(
            content,
            text=t(desc_key),
            font=(FONT_FAMILY, 13),
            text_color=TEXT_SECONDARY
        )
        desc_label.pack(anchor="w", pady=(0, SPACE_LG))

        # Check if folder exists
        if not folder_path.exists():
            error_label = ctk.CTkLabel(
                content,
                text=f"⚠️ Folder not found: {folder_name}",
                font=(FONT_FAMILY, 13),
                text_color=ERROR_COLOR
            )
            error_label.pack(pady=SPACE_XL)
            return

        # Get files in folder
        try:
            files = []
            for item in folder_path.iterdir():
                if item.is_file():
                    files.append(item)

            if not files:
                empty_label = ctk.CTkLabel(
                    content,
                    text="📂 No files in this folder",
                    font=(FONT_FAMILY, 13),
                    text_color=TEXT_SECONDARY
                )
                empty_label.pack(pady=SPACE_XL)
                return

            # Display files
            for file_path in sorted(files):
                self._create_file_card(content, file_path, folder_path)

        except Exception as e:
            error_label = ctk.CTkLabel(
                content,
                text=f"Error reading folder: {str(e)}",
                font=(FONT_FAMILY, 13),
                text_color=ERROR_COLOR
            )
            error_label.pack(pady=SPACE_XL)

    def _create_file_card(self, parent, file_path: Path, folder_path: Path):
        """Create a card for each file"""
        card = ctk.CTkFrame(parent, fg_color=BG_SECONDARY, corner_radius=RADIUS_SM)
        card.pack(fill="x", pady=(0, SPACE_MD))

        # Card inner
        card_inner = ctk.CTkFrame(card, fg_color="transparent")
        card_inner.pack(fill="x", padx=SPACE_MD, pady=SPACE_MD)

        # File icon and info (left side)
        info_frame = ctk.CTkFrame(card_inner, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)

        # File name
        file_name_label = ctk.CTkLabel(
            info_frame,
            text=f"📄 {file_path.name}",
            font=(FONT_FAMILY, 14, "bold"),
            text_color=TEXT_PRIMARY,
            anchor="w"
        )
        file_name_label.pack(anchor="w")

        # File size
        file_size = file_path.stat().st_size
        size_mb = file_size / (1024 * 1024)
        size_label = ctk.CTkLabel(
            info_frame,
            text=f"💾 {size_mb:.2f} MB",
            font=(FONT_FAMILY, 12),
            text_color=TEXT_SECONDARY,
            anchor="w"
        )
        size_label.pack(anchor="w", pady=(2, 0))

        # Action buttons (right side)
        action_frame = ctk.CTkFrame(card_inner, fg_color="transparent")
        action_frame.pack(side="right")

        # Open folder button
        open_btn = ctk.CTkButton(
            action_frame,
            text=t("btn_open_folder_location"),
            command=lambda: self._open_folder(folder_path),
            width=140,
            height=36,
            font=(FONT_FAMILY, 12),
            fg_color=INFO_COLOR,
            hover_color=PRIMARY_HOVER
        )
        open_btn.pack(side="left", padx=(0, SPACE_SM))

        # Run file button (only for .exe and .bat files)
        if file_path.suffix.lower() in ['.exe', '.bat']:
            run_btn = ctk.CTkButton(
                action_frame,
                text=t("btn_run_executable"),
                command=lambda: self._run_file(file_path),
                width=120,
                height=36,
                font=(FONT_FAMILY, 12),
                fg_color=SUCCESS_COLOR,
                hover_color="#1e7e34"
            )
            run_btn.pack(side="left", padx=(0, SPACE_SM))

        # Copy to desktop button
        copy_btn = ctk.CTkButton(
            action_frame,
            text=t("btn_copy_to_desktop"),
            command=lambda: self._copy_to_desktop(file_path),
            width=140,
            height=36,
            font=(FONT_FAMILY, 12),
            fg_color=PRIMARY_COLOR,
            hover_color=PRIMARY_HOVER
        )
        copy_btn.pack(side="left")

    def _open_folder(self, folder_path: Path):
        """Open folder in file explorer"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(folder_path)
            else:
                subprocess.run(['xdg-open', folder_path])
        except Exception as e:
            messagebox.showerror(
                t("error"),
                t("error_run_failed").format(error=str(e))
            )

    def _run_file(self, file_path: Path):
        """Run executable file"""
        try:
            # Confirm before running
            if messagebox.askyesno(
                t("confirm"),
                t("msg_run_executable").format(file=file_path.name)
            ):
                if os.name == 'nt':  # Windows
                    os.startfile(file_path)
                else:
                    subprocess.Popen([str(file_path)])

                messagebox.showinfo(
                    t("success"),
                    t("msg_run_success").format(file=file_path.name)
                )
        except Exception as e:
            messagebox.showerror(
                t("error"),
                t("error_run_failed").format(error=str(e))
            )

    def _copy_to_desktop(self, file_path: Path):
        """Copy file to desktop"""
        try:
            # Get desktop path
            desktop = Path.home() / "Desktop"
            if not desktop.exists():
                desktop = Path.home() / "Bureau"  # French
            if not desktop.exists():
                desktop = Path.home()

            # Copy file
            dest_path = desktop / file_path.name

            # Handle duplicate names
            if dest_path.exists():
                base_name = file_path.stem
                extension = file_path.suffix
                counter = 1
                while dest_path.exists():
                    dest_path = desktop / f"{base_name}_{counter}{extension}"
                    counter += 1

            shutil.copy2(file_path, dest_path)

            messagebox.showinfo(
                t("success"),
                t("msg_copy_success")
            )
        except Exception as e:
            messagebox.showerror(
                t("error"),
                t("error_copy_failed").format(error=str(e))
            )
