"""Modern Tab Header Component"""
import customtkinter as ctk
from typing import Callable, List, Optional
from gui.styles import *


class TabButton(ctk.CTkFrame):
    """Individual tab button with hover and active states"""
    def __init__(self, parent, text: str, icon: str, index: int, on_click: Callable, is_active: bool = False, **kwargs):
        super().__init__(parent, fg_color="transparent", cursor="hand2", **kwargs)
        self.index, self.on_click, self.is_active = index, on_click, is_active
        self.grid_columnconfigure(0, weight=1)
        
        self.button_container = ctk.CTkFrame(self, fg_color="transparent", cursor="hand2")
        self.button_container.grid(row=0, column=0, sticky="ew", padx=2)
        
        self.label = ctk.CTkLabel(self.button_container, text=f"{icon} {text}", font=(FONT_FAMILY, 12, "bold" if is_active else "normal"),
                                  text_color=PRIMARY_COLOR if is_active else TEXT_SECONDARY, cursor="hand2")
        self.label.pack(pady=SPACE_XXS)
        
        self.indicator = ctk.CTkFrame(self.button_container, height=2, fg_color=PRIMARY_COLOR if is_active else "transparent", corner_radius=RADIUS_SM)
        self.indicator.pack(fill="x", padx=SPACE_XS)
        
        for w in [self, self.button_container, self.label, self.indicator]:
            w.bind("<Button-1>", lambda e: self.on_click(self.index))
            w.bind("<Enter>", self._on_hover)
            w.bind("<Leave>", self._on_leave)

    def _on_hover(self, e):
        if not self.is_active:
            self.label.configure(text_color=PRIMARY_HOVER)
            self.indicator.configure(fg_color=PRIMARY_LIGHT)

    def _on_leave(self, e):
        if not self.is_active:
            self.label.configure(text_color=TEXT_SECONDARY)
            self.indicator.configure(fg_color="transparent")

    def set_active(self, active: bool):
        self.is_active = active
        self.label.configure(text_color=PRIMARY_COLOR if active else TEXT_SECONDARY, font=(FONT_FAMILY, 12, "bold" if active else "normal"))
        self.indicator.configure(fg_color=PRIMARY_COLOR if active else "transparent")


class TabHeader(ctk.CTkFrame):
    """Modern Tab Header Component"""
    def __init__(self, parent, tabs: List[dict], on_tab_change: Optional[Callable] = None, **kwargs):
        super().__init__(parent, fg_color=CARD_BACKGROUND, corner_radius=0, **kwargs)
        self.tabs, self.on_tab_change, self.current_tab, self.tab_buttons = tabs, on_tab_change, 0, []
        self.grid_columnconfigure(0, weight=1)
        self._create_title_section()
        self._create_tabs_section()
        ctk.CTkFrame(self, height=1, fg_color=BORDER_COLOR).grid(row=2, column=0, sticky="ew")

    def _create_title_section(self):
        title_frame = ctk.CTkFrame(self, fg_color="transparent", height=56)
        title_frame.grid(row=0, column=0, sticky="ew", padx=SPACE_LG, pady=(SPACE_SM, 0))
        title_frame.grid_propagate(False)
        
        ctk.CTkLabel(title_frame, text="BackupWin", font=(FONT_FAMILY, 18, "bold"), text_color=TEXT_COLOR).pack(side="left", padx=(0, SPACE_MD))
        
        right = ctk.CTkFrame(title_frame, fg_color="transparent")
        right.pack(side="right")
        
        from gui.i18n import t
        self.lang_selector = ctk.CTkComboBox(right, values=[t("lang_english"), t("lang_vietnamese")], font=(FONT_FAMILY, 12),
                                             width=120, height=32, corner_radius=RADIUS_SM, border_width=1, button_color=PRIMARY_COLOR, button_hover_color=PRIMARY_HOVER)
        self.lang_selector.pack(side="left", padx=(0, SPACE_SM))
        
        self.about_btn = ctk.CTkButton(right, text="ℹ️", font=(FONT_FAMILY, 14), width=32, height=32, corner_radius=RADIUS_SM,
                                       fg_color="transparent", border_width=1, border_color=BORDER_COLOR, text_color=TEXT_COLOR, hover_color=BACKGROUND_COLOR)
        self.about_btn.pack(side="left")

    def _create_tabs_section(self):
        tabs_frame = ctk.CTkFrame(self, fg_color="transparent", height=38)
        tabs_frame.grid(row=1, column=0, sticky="ew", padx=SPACE_MD)
        tabs_frame.grid_propagate(False)
        
        for i, tab in enumerate(self.tabs):
            btn = TabButton(tabs_frame, text=tab['name'], icon=tab.get('icon', '📄'), index=i, on_click=self._handle_tab_click, is_active=(i == 0))
            btn.pack(side="left", fill="y", expand=True)
            self.tab_buttons.append(btn)

    def _handle_tab_click(self, index: int):
        if index == self.current_tab:
            return
        for i, btn in enumerate(self.tab_buttons):
            btn.set_active(i == index)
        old, self.current_tab = self.current_tab, index
        if self.on_tab_change:
            self.on_tab_change(old, index)

    def get_current_tab(self) -> int:
        return self.current_tab

    def set_tab(self, index: int):
        if 0 <= index < len(self.tab_buttons):
            self._handle_tab_click(index)

    def get_language_selector(self):
        return self.lang_selector

    def get_about_button(self):
        return self.about_btn


class TabContent(ctk.CTkFrame):
    """Container for tab content"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BACKGROUND_COLOR, corner_radius=0, **kwargs)
        self.content_frames, self.current_frame = [], None

    def add_content(self, widget):
        widget.pack(fill="both", expand=True)
        widget.pack_forget()
        self.content_frames.append(widget)
        if len(self.content_frames) == 1:
            self.show_content(0)

    def show_content(self, index: int):
        if 0 <= index < len(self.content_frames):
            if self.current_frame is not None:
                self.content_frames[self.current_frame].pack_forget()
            self.content_frames[index].pack(fill="both", expand=True)
            self.current_frame = index
