"""
Statistics Display Component
"""

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def create_stats_section():
    """Create the statistics display section"""
    
    return html.Div(
        id='stats-section',
        style={'display': 'none'},
        children=[
            dmc.Paper(
                p="xl",
                radius="md",
                withBorder=True,
                children=[
                    dmc.Stack(
                        gap="lg",
                        children=[
                            dmc.Group(
                                gap="sm",
                                children=[
                                    DashIconify(icon="ph:chart-line", width=24),
                                    dmc.Title("Summary Statistics", order=4),
                                ],
                            ),
                            html.Div(id='summary-stats'),
                        ],
                    ),
                ],
            ),
        ],
    )


def create_stat_card(title, value, icon):
    """Create a single stat card"""
    
    return dmc.Paper(
        p="lg",
        radius="md",
        withBorder=True,
        style={'backgroundColor': '#F5F7FA'},
        children=[
            dmc.Stack(
                gap="xs",
                children=[
                    dmc.Group(
                        gap="xs",
                        children=[
                            DashIconify(icon=icon, width=20, color="#4A90E2"),
                            dmc.Text(title, size="sm", c="dimmed", fw=500),
                        ],
                    ),
                    dmc.Title(value, order=3),
                ],
            ),
        ],
    )
