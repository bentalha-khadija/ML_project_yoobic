"""
Charts and Visualizations Component
"""

import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify
from .placeholder import create_chart_placeholder


def create_charts_section():
    """Create the visualizations section"""
    
    return html.Div(
        id='viz-section',
        style={'display': 'block'},
        children=[
            dmc.Paper(
                p="xl",
                radius="md",
                withBorder=True,
                children=[
                    dmc.Stack(
                        gap="lg",
                        children=[
                            # Header
                            dmc.Group(
                                gap="sm",
                                children=[
                                    DashIconify(icon="ph:chart-bar", width=24),
                                    dmc.Title("Visualizations", order=4),
                                ],
                            ),
                            
                            # Store Selector
                            dmc.Stack(
                                gap="xs",
                                children=[
                                    dmc.Text("Select Store for Time Series", size="sm", fw=500),
                                    dmc.Select(
                                        id='viz-store-selector',
                                        placeholder="Choose a store",
                                        disabled=True,
                                        searchable=True,
                                        nothingFoundMessage="No stores found",
                                        radius="md",
                                        style={'width': '300px'},
                                    ),
                                ],
                            ),
                            
                            # Charts - Will be replaced by callbacks
                            html.Div(id='timeseries-plot'),
                            html.Div(id='bar-plot'),
                            html.Div(id='total-timeseries'),
                        ],
                    ),
                ],
            ),
        ],
    )
