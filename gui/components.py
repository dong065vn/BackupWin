"""Reusable GUI components"""
import customtkinter as ctk
from typing import Callable, Optional
from gui.styles import *
from gui.i18n import t


class Card(ctk.CTkFrame):
    """Card component for grouping content"""
    def __init__(self, parent, title: Optional[str] = None, **kwargs):
        super().__init__(parent, fg_color=CARD_BACKGROUND, corner_radius=10, **kwargs)

        if title:
            title_label = ctk.CTkLabel(
                self,
                text=title,
                font=HEADING_FONT,
                text_color=PRIMARY_COLOR
            )
            title_label.pack(pady=(10, 5), padx=10, anchor="w")


class StyledButton(ctk.CTkButton):
    """Styled button component"""
    def __init__(self, parent, text: str, command: Callable,
                 variant: str = "primary", **kwargs):

        colors = {
            "primary": PRIMARY_COLOR,
            "success": SUCCESS_COLOR,
            "danger": DANGER_COLOR,
            "warning": WARNING_COLOR
        }

        super().__init__(
            parent,
            text=text,
            command=command,
            font=NORMAL_FONT,
            fg_color=colors.get(variant, PRIMARY_COLOR),
            hover_color=SECONDARY_COLOR if variant == "primary" else colors.get(variant),
            height=BUTTON_HEIGHT,
            corner_radius=8,
            **kwargs
        )


class FilePathInput(ctk.CTkFrame):
    """File path input with browse button"""
    def __init__(self, parent, label: str, browse_callback: Callable,
                 mode: str = "file", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.mode = mode
        self.browse_callback = browse_callback

        # Label
        label_widget = ctk.CTkLabel(self, text=label, font=NORMAL_FONT)
        label_widget.pack(anchor="w", pady=(0, 5))

        # Input frame
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x")

        # Entry
        self.entry = ctk.CTkEntry(
            input_frame,
            font=NORMAL_FONT,
            height=35,
            placeholder_text=f"Select {mode}..."
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Browse button
        browse_btn = ctk.CTkButton(
            input_frame,
            text=t("btn_browse"),
            command=self._browse,
            font=NORMAL_FONT,
            width=100,
            height=35
        )
        browse_btn.pack(side="right")

    def _browse(self):
        """Handle browse button click"""
        result = self.browse_callback(self.mode)
        if result:
            self.entry.delete(0, "end")
            self.entry.insert(0, result)

    def get(self) -> str:
        """Get the current path"""
        return self.entry.get()

    def set(self, value: str):
        """Set the path value"""
        self.entry.delete(0, "end")
        self.entry.insert(0, value)


class ProgressCard(ctk.CTkFrame):
    """Card with progress bar"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=CARD_BACKGROUND, corner_radius=10, **kwargs)

        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            font=NORMAL_FONT,
            text_color=TEXT_COLOR
        )
        self.status_label.pack(pady=(10, 5))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self,
            width=300,
            height=20,
            corner_radius=10
        )
        self.progress_bar.pack(pady=10, padx=20)
        self.progress_bar.set(0)

        # Details label
        self.details_label = ctk.CTkLabel(
            self,
            text="",
            font=SMALL_FONT,
            text_color=TEXT_COLOR
        )
        self.details_label.pack(pady=(0, 10))

    def update_progress(self, value: float, status: str = "", details: str = ""):
        """Update progress bar and labels"""
        self.progress_bar.set(value)
        if status:
            self.status_label.configure(text=status)
        if details:
            self.details_label.configure(text=details)


class ResultsTable(ctk.CTkScrollableFrame):
    """Scrollable table for displaying results"""
    def __init__(self, parent, columns: list, **kwargs):
        super().__init__(parent, fg_color=CARD_BACKGROUND, **kwargs)

        self.columns = columns
        self.rows = []

        # Header
        header_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR)
        header_frame.pack(fill="x", pady=(0, 5))

        for col in columns:
            label = ctk.CTkLabel(
                header_frame,
                text=col,
                font=(FONT_FAMILY, 12, "bold"),
                text_color="white"
            )
            label.pack(side="left", expand=True, padx=5, pady=5)

    def add_row(self, data: list):
        """Add a row to the table"""
        row_frame = ctk.CTkFrame(self, fg_color="white")
        row_frame.pack(fill="x", pady=2)

        for item in data:
            label = ctk.CTkLabel(
                row_frame,
                text=str(item),
                font=SMALL_FONT,
                text_color=TEXT_COLOR
            )
            label.pack(side="left", expand=True, padx=5, pady=5)

        self.rows.append(row_frame)

    def clear(self):
        """Clear all rows"""
        for row in self.rows:
            row.destroy()
        self.rows = []


class InfoCard(ctk.CTkFrame):
    """Information display card"""
    def __init__(self, parent, title: str, value: str = "0",
                 color: str = PRIMARY_COLOR, **kwargs):
        super().__init__(parent, fg_color=color, corner_radius=10, **kwargs)

        # Title
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=NORMAL_FONT,
            text_color="white"
        )
        title_label.pack(pady=(10, 5))

        # Value
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=(FONT_FAMILY, 24, "bold"),
            text_color="white"
        )
        self.value_label.pack(pady=(0, 10))

    def update_value(self, value: str):
        """Update the displayed value"""
        self.value_label.configure(text=value)
