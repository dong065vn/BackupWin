"""
BackupWin - GUI Application with Multi-language Support
A comprehensive Windows file backup and search desktop application
"""
import customtkinter as ctk
from tkinter import messagebox
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.styles import *
from gui.search_tab_i18n import SearchTab
from gui.backup_tab_i18n import BackupTab
from gui.restore_tab_i18n import RestoreTab
from gui.consolidate_tab_i18n import ConsolidateTab
from gui.duplicate_finder_tab_i18n import DuplicateFinderTab
from gui.organizer_tab_i18n import OrganizerTab
from gui.i18n import get_i18n, t
from gui.tab_header import TabHeader, TabContent


class BackupWinApp(ctk.CTk):
    """Main application window with multi-language support"""

    def __init__(self):
        super().__init__()

        # Initialize i18n
        self.i18n = get_i18n()

        # Configure window
        self.title(t("app_title"))
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        # Set theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create widgets
        self._create_modern_interface()
        self._create_footer()

        # Center window
        self._center_window()

        # Ensure backup directory exists
        self._ensure_backup_directory()

    def _create_modern_interface(self):
        """Create modern interface with professional header and tabs"""
        # Define tabs with icons
        tabs = [
            {"name": t("tab_search"), "icon": "🔍"},
            {"name": t("tab_backup"), "icon": "💾"},
            {"name": t("tab_consolidate"), "icon": "📁"},
            {"name": t("tab_duplicate_finder"), "icon": "🔄"},
            {"name": t("tab_organizer"), "icon": "🗂️"},
            {"name": t("tab_restore"), "icon": "⚙️"}
        ]

        # Create modern tab header
        self.tab_header = TabHeader(
            self,
            tabs=tabs,
            on_tab_change=self._on_tab_change
        )
        self.tab_header.grid(row=0, column=0, sticky="ew")

        # Configure language selector and about button
        lang_selector = self.tab_header.get_language_selector()
        lang_selector.configure(command=self._change_language)

        # Set current language
        current_lang = self.i18n.get_language()
        if current_lang == 'vi':
            lang_selector.set(t("lang_vietnamese"))
        else:
            lang_selector.set(t("lang_english"))

        # Configure about button
        about_btn = self.tab_header.get_about_button()
        about_btn.configure(command=self._show_about)

        # Create content container
        self.tab_content = TabContent(self)
        self.tab_content.grid(row=1, column=0, sticky="nsew")

        # Create all tab content frames
        self._create_tab_contents()

    def _create_tab_contents(self):
        """Create all tab content widgets"""
        # Create content frames
        search_container = ctk.CTkFrame(self.tab_content, fg_color="transparent")
        backup_container = ctk.CTkFrame(self.tab_content, fg_color="transparent")
        consolidate_container = ctk.CTkFrame(self.tab_content, fg_color="transparent")
        duplicate_container = ctk.CTkFrame(self.tab_content, fg_color="transparent")
        organizer_container = ctk.CTkFrame(self.tab_content, fg_color="transparent")
        restore_container = ctk.CTkFrame(self.tab_content, fg_color="transparent")

        # Create tab widgets
        self.search_tab = SearchTab(search_container)
        self.search_tab.pack(fill="both", expand=True, padx=SPACE_XL, pady=SPACE_LG)

        self.backup_tab = BackupTab(backup_container)
        self.backup_tab.pack(fill="both", expand=True, padx=SPACE_XL, pady=SPACE_LG)

        self.consolidate_tab = ConsolidateTab(consolidate_container)
        self.consolidate_tab.pack(fill="both", expand=True, padx=SPACE_XL, pady=SPACE_LG)

        self.duplicate_finder_tab = DuplicateFinderTab(duplicate_container)
        self.duplicate_finder_tab.pack(fill="both", expand=True, padx=SPACE_XL, pady=SPACE_LG)

        self.organizer_tab = OrganizerTab(organizer_container)
        self.organizer_tab.pack(fill="both", expand=True, padx=SPACE_XL, pady=SPACE_LG)

        self.restore_tab = RestoreTab(restore_container)
        self.restore_tab.pack(fill="both", expand=True, padx=SPACE_XL, pady=SPACE_LG)

        # Add all containers to tab content
        self.tab_content.add_content(search_container)
        self.tab_content.add_content(backup_container)
        self.tab_content.add_content(consolidate_container)
        self.tab_content.add_content(duplicate_container)
        self.tab_content.add_content(organizer_container)
        self.tab_content.add_content(restore_container)

        # Connect tabs - setup callbacks for search tab to send data to other tabs
        self._setup_tab_connections()

    def _setup_tab_connections(self):
        """Setup connections between tabs for data transfer"""
        # Setup callbacks for search tab to send files to other tabs
        self.search_tab.on_send_to_backup = self._handle_send_to_backup
        self.search_tab.on_send_to_consolidate = self._handle_send_to_consolidate
        self.search_tab.on_send_to_organizer = self._handle_send_to_organizer

    def _handle_send_to_backup(self, file_paths: list):
        """Handle sending files from search to backup tab"""
        # Switch to backup tab (index 1)
        self.tab_header.set_tab(1)
        # Send files to backup tab
        self.backup_tab.receive_files(file_paths)

    def _handle_send_to_consolidate(self, file_paths: list):
        """Handle sending files from search to consolidate tab"""
        # Switch to consolidate tab (index 2)
        self.tab_header.set_tab(2)
        # Send files to consolidate tab
        self.consolidate_tab.receive_files(file_paths)

    def _handle_send_to_organizer(self, file_paths: list):
        """Handle sending files from search to organizer tab"""
        # Switch to organizer tab (index 4)
        self.tab_header.set_tab(4)
        # Send files to organizer tab
        self.organizer_tab.receive_files(file_paths)

    def _on_tab_change(self, old_index: int, new_index: int):
        """Handle tab change event"""
        self.tab_content.show_content(new_index)

    def _create_footer(self):
        """Create modern footer with status and version"""
        footer = ctk.CTkFrame(self, fg_color=CARD_BACKGROUND, height=44)
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_propagate(False)

        # Divider line
        divider = ctk.CTkFrame(footer, height=1, fg_color=BORDER_COLOR)
        divider.pack(fill="x", side="top")

        # Footer content container
        content = ctk.CTkFrame(footer, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SPACE_XL, pady=SPACE_SM)

        # Version info
        version_label = ctk.CTkLabel(
            content,
            text=t("footer_version"),
            font=(FONT_FAMILY, 11),
            text_color=TEXT_SECONDARY
        )
        version_label.pack(side="left", padx=(0, SPACE_LG))

        # Status
        status_label = ctk.CTkLabel(
            content,
            text=t("footer_status"),
            font=(FONT_FAMILY, 11),
            text_color=SUCCESS_COLOR
        )
        status_label.pack(side="left")

        # Copyright
        copyright_label = ctk.CTkLabel(
            content,
            text=t("footer_copyright"),
            font=(FONT_FAMILY, 11),
            text_color=TEXT_SECONDARY
        )
        copyright_label.pack(side="right")

    def _center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _ensure_backup_directory(self):
        """Ensure backup directory exists"""
        try:
            from app.core.config import settings
            backup_path = settings.backup_path
            backup_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showwarning(
                t("error"),
                f"Could not create backup directory: {str(e)}\n\n"
                "You can still use the application, but you'll need to specify "
                "a backup destination manually."
            )

    def _change_language(self, choice):
        """Change application language"""
        # Determine language code from choice
        if choice == t("lang_vietnamese") or "Tiếng Việt" in choice:
            new_lang = 'vi'
        else:
            new_lang = 'en'

        # Only refresh if language actually changed
        if new_lang != self.i18n.get_language():
            self.i18n.set_language(new_lang)

            # Show restart message
            messagebox.showinfo(
                t("info"),
                t("msg_restart_language") if new_lang == 'vi'
                else "Please restart the application for language changes to take effect."
            )

    def _show_about(self):
        """Show about dialog"""
        messagebox.showinfo(t("about_title"), t("about_text"))


def main():
    """Main entry point"""
    try:
        # Check if .env file exists
        if not os.path.exists(".env"):
            print("Warning: .env file not found. Creating from template...")
            if os.path.exists(".env.example"):
                import shutil
                shutil.copy(".env.example", ".env")
                print("Created .env file. Please configure it if needed.")

        # Create and run app
        app = BackupWinApp()
        app.mainloop()

    except Exception as e:
        messagebox.showerror(
            "Fatal Error",
            f"Application failed to start:\n\n{str(e)}\n\n"
            "Please check that all dependencies are installed:\n"
            "pip install -r requirements.txt"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
