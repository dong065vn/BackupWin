"""GUI styles and constants - Modern Figma-inspired design"""

# ================================
# Color Palette - Modern & Professional
# ================================

# Primary Brand Colors
PRIMARY_COLOR = "#2563eb"  # Modern blue
PRIMARY_HOVER = "#1d4ed8"  # Darker blue for hover
PRIMARY_LIGHT = "#dbeafe"  # Light blue for accents
PRIMARY_GRADIENT_START = "#3b82f6"
PRIMARY_GRADIENT_END = "#2563eb"

# Secondary Colors
SECONDARY_COLOR = "#0f172a"  # Dark slate
SECONDARY_HOVER = "#1e293b"
ACCENT_COLOR = "#8b5cf6"  # Purple accent
ACCENT_HOVER = "#7c3aed"

# Status Colors
SUCCESS_COLOR = "#10b981"  # Modern green
SUCCESS_LIGHT = "#d1fae5"
ERROR_COLOR = "#ef4444"  # Modern red (alias for DANGER_COLOR)
DANGER_COLOR = "#ef4444"  # Modern red
DANGER_LIGHT = "#fee2e2"
WARNING_COLOR = "#f59e0b"  # Modern orange
WARNING_LIGHT = "#fef3c7"
INFO_COLOR = "#06b6d4"  # Cyan
INFO_LIGHT = "#cffafe"

# Background & Surface Colors
BACKGROUND_COLOR = "#f8fafc"  # Light gray-blue
BG_SECONDARY = "#f1f5f9"  # Secondary background
CARD_BACKGROUND = "#ffffff"
SURFACE_ELEVATED = "#ffffff"
OVERLAY_BG = "rgba(0, 0, 0, 0.5)"

# Text Colors
TEXT_COLOR = "#0f172a"  # Dark slate
TEXT_SECONDARY = "#64748b"  # Gray
TEXT_LIGHT = "#94a3b8"  # Light gray
TEXT_LIGHT_COLOR = "#94a3b8"  # Alias for backward compatibility
TEXT_ON_PRIMARY = "#ffffff"
TEXT_MUTED = "#cbd5e1"

# Border & Divider Colors
BORDER_COLOR = "#e2e8f0"
BORDER_LIGHT = "#f1f5f9"
DIVIDER_COLOR = "#e2e8f0"

# Input & Interactive Colors
INPUT_BACKGROUND = "#ffffff"
INPUT_BORDER = "#e2e8f0"
INPUT_BORDER_FOCUS = "#2563eb"
INPUT_HOVER = "#f8fafc"

# Shadow Colors (for depth)
SHADOW_SM = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
SHADOW_MD = "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
SHADOW_LG = "0 10px 15px -3px rgba(0, 0, 0, 0.1)"
SHADOW_XL = "0 20px 25px -5px rgba(0, 0, 0, 0.1)"

# ================================
# Typography - Modern Font System
# ================================

FONT_FAMILY = "Segoe UI"
FONT_FAMILY_MONO = "Consolas"

# Font Sizes & Weights
DISPLAY_FONT = (FONT_FAMILY, 32, "bold")  # Large titles
TITLE_FONT = (FONT_FAMILY, 24, "bold")  # Section titles
HEADING_FONT = (FONT_FAMILY, 18, "bold")  # Headings
SUBHEADING_FONT = (FONT_FAMILY, 16, "bold")  # Subheadings
NORMAL_FONT = (FONT_FAMILY, 13)  # Body text
SMALL_FONT = (FONT_FAMILY, 11)  # Small text
TINY_FONT = (FONT_FAMILY, 10)  # Tiny labels
MONO_FONT = (FONT_FAMILY_MONO, 11)  # Code/monospace

# ================================
# Layout & Spacing - 8px grid system
# ================================

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

# Spacing (8px base)
SPACE_XXS = 4
SPACE_XS = 8
SPACE_SM = 12
SPACE_MD = 16
SPACE_LG = 24
SPACE_XL = 32
SPACE_XXL = 48

# Legacy spacing (for backwards compatibility)
PADDING = 20
BUTTON_HEIGHT = 40

# Border Radius
RADIUS_SM = 6
RADIUS_MD = 8
RADIUS_LG = 12
RADIUS_XL = 16
RADIUS_FULL = 9999

# Component Sizes
HEADER_HEIGHT = 100
FOOTER_HEIGHT = 50
TAB_HEIGHT = 48
BUTTON_HEIGHT_SM = 32
BUTTON_HEIGHT_MD = 40
BUTTON_HEIGHT_LG = 48

# Icon Sizes
ICON_SM = 16
ICON_MD = 20
ICON_LG = 24
ICON_XL = 32

# ================================
# Modern Tab Design Tokens
# ================================

# Tab States
TAB_ACTIVE_COLOR = PRIMARY_COLOR
TAB_INACTIVE_COLOR = TEXT_SECONDARY
TAB_HOVER_COLOR = PRIMARY_HOVER
TAB_INDICATOR_HEIGHT = 3
TAB_INDICATOR_COLOR = PRIMARY_COLOR
TAB_INDICATOR_HOVER = PRIMARY_LIGHT

# Tab Spacing
TAB_PADDING_X = SPACE_SM
TAB_PADDING_Y = SPACE_SM
TAB_ICON_SPACING = SPACE_XS

# Tab Typography
TAB_FONT_ACTIVE = (FONT_FAMILY, 14, "bold")
TAB_FONT_INACTIVE = (FONT_FAMILY, 14, "normal")

# Tab Transitions (for future animation support)
TAB_TRANSITION_DURATION = 200  # milliseconds
TAB_TRANSITION_EASING = "ease-in-out"

# ================================
# Design System Notes
# ================================
"""
This design follows Figma best practices:

1. 8px Grid System: All spacing uses multiples of 8 (4px for half-spacing)
2. Consistent Color Palette: Primary, Secondary, and Status colors
3. Typography Scale: From Display (32px) to Tiny (10px)
4. Border Radius: sm (6px) to xl (16px) for different components
5. Professional Shadows: From sm to xl for depth hierarchy

Tab Design Pattern:
- Clean horizontal navigation
- Active state with colored underline indicator
- Smooth hover effects with color transitions
- Icon + Text for better UX
- Consistent spacing and alignment
"""
