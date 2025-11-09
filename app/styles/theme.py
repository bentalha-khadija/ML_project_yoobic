"""
Modern Minimalist Theme Configuration for Dash Mantine Components
"""

# Color Palette - Minimalist Blue Theme
COLORS = {
    'primary': '#4A90E2',      # Soft blue
    'secondary': '#7B8794',    # Neutral gray
    'success': '#52C41A',      # Green
    'warning': '#FAAD14',      # Orange
    'error': '#F5222D',        # Red
    'dark': '#0A1929',         # Deep blue-black
    'light': '#F5F7FA',        # Off-white
    'border': '#E8EAED',       # Light gray border
}

# Theme Configuration
LIGHT_THEME = {
    'colorScheme': 'light',
    'primaryColor': 'blue',
    'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    'fontFamilyMonospace': 'Monaco, Courier, monospace',
    'headings': {'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'},
}

DARK_THEME = {
    'colorScheme': 'dark',
    'primaryColor': 'blue',
    'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    'fontFamilyMonospace': 'Monaco, Courier, monospace',
    'headings': {'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'},
    'colors': {
        'dark': [
            '#C1C2C5',
            '#A6A7AB',
            '#909296',
            '#5C5F66',
            '#373A40',
            '#2C2E33',
            '#25262B',
            '#1A1B1E',
            '#141517',
            '#101113',
        ],
    },
}

# Component Styles
CARD_STYLE = {
    'light': {
        'borderRadius': '12px',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.08)',
        'border': f'1px solid {COLORS["border"]}',
        'padding': '24px',
    },
    'dark': {
        'borderRadius': '12px',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.3)',
        'border': '1px solid #2C2E33',
        'padding': '24px',
        'backgroundColor': '#1A1B1E',
    }
}

UPLOAD_ZONE_STYLE = {
    'borderRadius': '12px',
    'border': f'2px dashed {COLORS["border"]}',
    'padding': '40px',
    'textAlign': 'center',
    'backgroundColor': COLORS['light'],
    'cursor': 'pointer',
    'transition': 'all 0.2s ease',
}

TABLE_STYLE = {
    'borderRadius': '8px',
    'overflow': 'hidden',
}

# Icon Styles
ICON_SIZE = {
    'small': 16,
    'medium': 20,
    'large': 24,
    'xlarge': 32,
}

# Spacing
SPACING = {
    'xs': '4px',
    'sm': '8px',
    'md': '16px',
    'lg': '24px',
    'xl': '32px',
}

# Animation
TRANSITION = {
    'default': 'all 0.2s ease',
    'fast': 'all 0.1s ease',
    'slow': 'all 0.3s ease',
}
