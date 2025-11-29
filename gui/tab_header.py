"""
Modern Tab Header Component - Figma-inspired design
Professional tab navigation with smooth animations and hover effects
"""
import customtkinter as ctk
from typing import Callable, List, Optional
from gui.styles import *


class TabButton(ctk.CTkFrame):
    """Individual tab button with hover and active states"""

    def __init__(self, parent, text: str, icon: str, index: int,
                 on_click: Callable, is_active: bool = False, **kwargs):
        super().__init__(parent, fg_color="transparent", cursor="hand2", **kwargs)

        self.text = text
        self.icon = icon
        self.index = index
        self.on_click = on_click
        self.is_active = is_active
        self.hover_state = False

        # Configure layout
        self.grid_columnconfigure(0, weight=1)

        # Main button container
        self.button_container = ctk.CTkFrame(
            self,
            fg_color="transparent",
            cursor="hand2"
        )
        self.button_container.grid(row=0, column=0, sticky="ew", padx=2, pady=0)  # Minimal padding

        # Tab label with icon (compact)
        self.label = ctk.CTkLabel(
            self.button_container,
            text=f"{icon} {text}",  # Single space between icon and text
            font=(FONT_FAMILY, 12, "normal"),  # Smaller font
            text_color=TEXT_SECONDARY if not is_active else PRIMARY_COLOR,
            cursor="hand2"
        )
        self.label.pack(pady=(SPACE_XXS, SPACE_XXS))

        # Active indicator (animated underline)
        self.indicator = ctk.CTkFrame(
            self.button_container,
            height=2,  # Thinner indicator
            fg_color=PRIMARY_COLOR if is_active else "transparent",
            corner_radius=RADIUS_SM
        )
        self.indicator.pack(fill="x", padx=SPACE_XS)

        # Bind events
        self._bind_events(self)
        self._bind_events(self.button_container)
        self._bind_events(self.label)
        self._bind_events(self.indicator)

    def _bind_events(self, widget):
        """Bind mouse events to widget"""
        widget.bind("<Button-1>", self._handle_click)
        widget.bind("<Enter>", self._on_hover)
        widget.bind("<Leave>", self._on_leave)

    def _handle_click(self, event):
        """Handle tab click"""
        self.on_click(self.index)

    def _on_hover(self, event):
        """Handle mouse hover"""
        if not self.is_active:
            self.hover_state = True
            self.label.configure(text_color=PRIMARY_HOVER)
            self.indicator.configure(fg_color=PRIMARY_LIGHT)

    def _on_leave(self, event):
        """Handle mouse leave"""
        if not self.is_active:
            self.hover_state = False
            self.label.configure(text_color=TEXT_SECONDARY)
            self.indicator.configure(fg_color="transparent")

    def set_active(self, active: bool):
        """Set active state with smooth transition"""
        self.is_active = active

        if active:
            self.label.configure(
                text_color=PRIMARY_COLOR,
                font=(FONT_FAMILY, 12, "bold")  # Smaller font
            )
            self.indicator.configure(fg_color=PRIMARY_COLOR)
        else:
            self.label.configure(
                text_color=TEXT_SECONDARY,
                font=(FONT_FAMILY, 12, "normal")  # Smaller font
            )
            self.indicator.configure(fg_color="transparent")


class TabHeader(ctk.CTkFrame):
    """
    Modern Tab Header Component
    Features:
    - Clean Figma-inspired design
    - Smooth tab switching
    - Hover effects
    - Active state indicators
    - Professional spacing and typography
    """

    def __init__(self, parent, tabs: List[dict], on_tab_change: Optional[Callable] = None, **kwargs):
        """
        Initialize TabHeader

        Args:
            parent: Parent widget
            tabs: List of tab dictionaries with 'name', 'icon' keys
            on_tab_change: Callback when tab changes (receives index)
        """
        super().__init__(
            parent,
            fg_color=CARD_BACKGROUND,
            corner_radius=0,
            **kwargs
        )

        self.tabs = tabs
        self.on_tab_change = on_tab_change
        self.current_tab = 0
        self.tab_buttons = []

        # Configure layout
        self.grid_columnconfigure(0, weight=1)

        # Create header sections
        self._create_title_section()
        self._create_tabs_section()
        self._create_divider()

    def _create_title_section(self):
        """Create compact title and action section"""
        title_frame = ctk.CTkFrame(self, fg_color="transparent", height=56)
        title_frame.grid(row=0, column=0, sticky="ew", padx=SPACE_LG, pady=(SPACE_SM, 0))
        title_frame.grid_propagate(False)

        # App title (compact)
        title_label = ctk.CTkLabel(
            title_frame,
            text="BackupWin",
            font=(FONT_FAMILY, 18, "bold"),
            text_color=TEXT_COLOR
        )
        title_label.pack(side="left", padx=(0, SPACE_MD))

        # Right section - Language & About (compact)
        right_section = ctk.CTkFrame(title_frame, fg_color="transparent")
        right_section.pack(side="right")

        # Language selector (compact)
        from gui.i18n import t
        self.lang_selector = ctk.CTkComboBox(
            right_section,
            values=[t("lang_english"), t("lang_vietnamese")],
            font=(FONT_FAMILY, 12),
            width=120,
            height=32,
            corner_radius=RADIUS_SM,
            border_width=1,
            button_color=PRIMARY_COLOR,
            button_hover_color=PRIMARY_HOVER
        )
        self.lang_selector.pack(side="left", padx=(0, SPACE_SM))

        # About button (compact)
        self.about_btn = ctk.CTkButton(
            right_section,
            text="ℹ️",
            font=(FONT_FAMILY, 14),
            width=32,
            height=32,
            corner_radius=RADIUS_SM,
            fg_color="transparent",
            border_width=1,
            border_color=BORDER_COLOR,
            text_color=TEXT_COLOR,
            hover_color=BACKGROUND_COLOR
        )
        self.about_btn.pack(side="left")

    def _create_tabs_section(self):
        """Create compact tabs navigation"""
        tabs_frame = ctk.CTkFrame(self, fg_color="transparent", height=38)  # Reduced height
        tabs_frame.grid(row=1, column=0, sticky="ew", padx=SPACE_MD, pady=0)  # Reduced padding
        tabs_frame.grid_propagate(False)

        # Create tab buttons
        for i, tab_info in enumerate(self.tabs):
            tab_btn = TabButton(
                tabs_frame,
                text=tab_info['name'],
                icon=tab_info.get('icon', '📄'),
                index=i,
                on_click=self._handle_tab_click,
                is_active=(i == 0)
            )
            tab_btn.pack(side="left", padx=0, fill="y", expand=True)  # Equal width distribution
            self.tab_buttons.append(tab_btn)

    def _create_divider(self):
        """Create divider line"""
        divider = ctk.CTkFrame(
            self,
            height=1,
            fg_color=BORDER_COLOR
        )
        divider.grid(row=2, column=0, sticky="ew")

    def _handle_tab_click(self, index: int):
        """Handle tab button click"""
        if index == self.current_tab:
            return

        # Update button states
        for i, btn in enumerate(self.tab_buttons):
            btn.set_active(i == index)

        # Update current tab
        old_tab = self.current_tab
        self.current_tab = index

        # Call callback
        if self.on_tab_change:
            self.on_tab_change(old_tab, index)

    def get_current_tab(self) -> int:
        """Get current active tab index"""
        return self.current_tab

    def set_tab(self, index: int):
        """Programmatically set active tab"""
        if 0 <= index < len(self.tab_buttons):
            self._handle_tab_click(index)

    def get_language_selector(self):
        """Get language selector widget"""
        return self.lang_selector

    def get_about_button(self):
        """Get about button widget"""
        return self.about_btn


class TabContent(ctk.CTkFrame):
    """Container for tab content with smooth transitions"""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=BACKGROUND_COLOR,
            corner_radius=0,
            **kwargs
        )

        self.content_frames = []
        self.current_frame = None

    def add_content(self, content_widget):
        """Add content frame"""
        content_widget.pack(fill="both", expand=True)
        content_widget.pack_forget()  # Hide initially
        self.content_frames.append(content_widget)

        # Show first frame by default
        if len(self.content_frames) == 1:
            self.show_content(0)

    def show_content(self, index: int):
        """Show content at index with smooth transition"""
        if 0 <= index < len(self.content_frames):
            # Hide current
            if self.current_frame is not None:
                self.content_frames[self.current_frame].pack_forget()

            # Show new
            self.content_frames[index].pack(fill="both", expand=True)
            self.current_frame = index
