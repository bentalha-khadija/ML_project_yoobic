"""
Header Component with Theme Toggle
"""

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def create_header(model_meta):
    """Create the application header with theme toggle"""
    
    return dmc.Stack(
        gap="md",
        children=[
            # Title Row
            dmc.Group(
                justify="space-between",
                children=[
                    # Title Section
                    html.Div([
                        dmc.Title(
                            "📊 Store Sales Prediction",
                            order=2,
                            style={'marginBottom': '8px'}
                        ),
                        dmc.Text(
                            f"Powered by {model_meta['model_type']} {model_meta['approach']} • RMSE: {model_meta['rmse']:,.0f}",
                            size="sm",
                            c="dimmed",
                        ),
                    ]),
                    
                    # Theme Toggle Button
                    dmc.ActionIcon(
                        DashIconify(icon="ph:moon-fill", width=20),
                        id="theme-toggle",
                        variant="subtle",
                        size="lg",
                        radius="md",
                    ),
                ],
            ),
            
            dmc.Divider(variant="solid"),
        ],
    )
