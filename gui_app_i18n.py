"""BackupWin - GUI Application with Multi-language Support"""
import customtkinter as ctk
from tkinter import messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.styles import *
from gui.search_tab_i18n import SearchTab
from gui.backup_tab_i18n import BackupTab
from gui.restore_tab_i18n import RestoreTab
from gui.consolidate_tab_i18n import ConsolidateTab
from gui.duplicate_finder_tab_i18n import DuplicateFinderTab
from gui.organizer_tab_i18n import OrganizerTab
from gui.resources_tab_i18n import ResourcesTab
from gui.i18n import get_i18n, t
from gui.tab_header import TabHeader, TabContent


class BackupWinApp(ctk.CTk):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.i18n = get_i18n()
        self.title(t("app_title"))
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._create_interface()
        self._create_footer()
        self._center_window()
        self._ensure_backup_directory()

    def _create_interface(self):
        tabs = [
            {"name": t("tab_search"), "icon": "🔍"},
            {"name": t("tab_backup"), "icon": "💾"},
            {"name": t("tab_consolidate"), "icon": "📁"},
            {"name": t("tab_duplicate_finder"), "icon": "🔄"},
            {"name": t("tab_organizer"), "icon": "🗂️"},
            {"name": t("tab_resources"), "icon": "📦"},
            {"name": t("tab_restore"), "icon": "⚙️"}
        ]

        self.tab_header = TabHeader(self, tabs=tabs, on_tab_change=self._on_tab_change)
        self.tab_header.grid(row=0, column=0, sticky="ew")

        lang_selector = self.tab_header.get_language_selector()
        lang_selector.configure(command=self._change_language)
        lang_selector.set(t("lang_vietnamese") if self.i18n.get_language() == 'vi' else t("lang_english"))
        self.tab_header.get_about_button().configure(command=self._show_about)

        self.tab_content = TabContent(self)
        self.tab_content.grid(row=1, column=0, sticky="nsew")
        self._create_tab_contents()

    def _create_tab_contents(self):
        containers = [ctk.CTkFrame(self.tab_content, fg_color="transparent") for _ in range(7)]
        
        self.search_tab = SearchTab(containers[0])
        self.backup_tab = BackupTab(containers[1])
        self.consolidate_tab = ConsolidateTab(containers[2])
        self.duplicate_finder_tab = DuplicateFinderTab(containers[3])
        self.organizer_tab = OrganizerTab(containers[4])
        self.resources_tab = ResourcesTab(containers[5])
        self.restore_tab = RestoreTab(containers[6])

        for tab, container in zip([self.search_tab, self.backup_tab, self.consolidate_tab, self.duplicate_finder_tab, self.organizer_tab, self.resources_tab, self.restore_tab], containers):
            tab.pack(fill="both", expand=True, padx=SPACE_XL, pady=SPACE_LG)
            self.tab_content.add_content(container)

        self.search_tab.on_send_to_backup = lambda paths: (self.tab_header.set_tab(1), self.backup_tab.receive_files(paths))
        self.search_tab.on_send_to_consolidate = lambda paths: (self.tab_header.set_tab(2), self.consolidate_tab.receive_files(paths))
        self.search_tab.on_send_to_organizer = lambda paths: (self.tab_header.set_tab(4), self.organizer_tab.receive_files(paths))

    def _on_tab_change(self, old_idx: int, new_idx: int):
        self.tab_content.show_content(new_idx)

    def _create_footer(self):
        footer = ctk.CTkFrame(self, fg_color=CARD_BACKGROUND, height=28)
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_propagate(False)
        ctk.CTkFrame(footer, height=1, fg_color=BORDER_COLOR).pack(fill="x", side="top")
        content = ctk.CTkFrame(footer, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SPACE_MD, pady=2)
        ctk.CTkLabel(content, text=t("footer_version"), font=(FONT_FAMILY, 10), text_color=TEXT_SECONDARY).pack(side="left", padx=(0, SPACE_SM))
        ctk.CTkLabel(content, text=t("footer_status"), font=(FONT_FAMILY, 10), text_color=SUCCESS_COLOR).pack(side="left")
        ctk.CTkLabel(content, text=t("footer_copyright"), font=(FONT_FAMILY, 10), text_color=TEXT_SECONDARY).pack(side="right")

    def _center_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"{w}x{h}+{(self.winfo_screenwidth() - w) // 2}+{(self.winfo_screenheight() - h) // 2}")

    def _ensure_backup_directory(self):
        try:
            from app.core.config import settings
            settings.backup_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showwarning(t("error"), f"Could not create backup directory: {e}")

    def _change_language(self, choice):
        new_lang = 'vi' if "Tiếng Việt" in choice or choice == t("lang_vietnamese") else 'en'
        if new_lang != self.i18n.get_language():
            self.i18n.set_language(new_lang)
            messagebox.showinfo(t("info"), t("msg_restart_language") if new_lang == 'vi' else "Please restart for language changes.")

    def _show_about(self):
        messagebox.showinfo(t("about_title"), t("about_text"))


def main():
    try:
        if not os.path.exists(".env") and os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
        BackupWinApp().mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application failed to start:\n\n{e}\n\nInstall dependencies: pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()
