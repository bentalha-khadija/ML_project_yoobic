"""
Theme Toggle Callbacks
"""

from dash import Input, Output, State, callback
from dash_iconify import DashIconify


def register_theme_callbacks(app):
    """Register theme-related callbacks"""
    
    @app.callback(
        [Output('mantine-provider', 'theme'),
         Output('theme-toggle', 'children'),
         Output('theme-store', 'data')],
        Input('theme-toggle', 'n_clicks'),
        State('theme-store', 'data'),
        prevent_initial_call=True,
    )
    def toggle_theme(n_clicks, current_theme):
        """Toggle between light and dark themes"""
        if current_theme == 'light':
            return (
                {"colorScheme": "dark", "primaryColor": "blue"},
                DashIconify(icon="ph:sun-fill", width=20),
                'dark'
            )
        else:
            return (
                {"colorScheme": "light", "primaryColor": "blue"},
                DashIconify(icon="ph:moon-fill", width=20),
                'light'
            )
