"""
Visualizations Page - Charts and visualizations
"""

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def create_visualizations_page():
    """
    Create visualizations page
    
    Returns:
        DMC component
    """
    return dmc.Container(
        size="xl",
        px="md",
        py="xl",
        children=[
            dmc.Stack(
                gap="xl",
                children=[
                    # Page title
                    dmc.Stack(
                        gap="sm",
                        children=[
                            dmc.Title("📈 Visualizations", order=2),
                            dmc.Text(
                                "Interactive charts and graphs for your predictions",
                                size="md",
                                c="dimmed"
                            ),
                        ],
                    ),
                    
                    # Visualizations section
                    dmc.Paper(
                        p="xl",
                        radius="md",
                        withBorder=True,
                        children=[
                            dmc.Stack(
                                gap="lg",
                                children=[
                                    # Store Selector
                                    dmc.Stack(
                                        gap="xs",
                                        children=[
                                            dmc.Text("Select Store for Timeline", size="sm", fw=500),
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
                                    
                                    # Charts
                                    html.Div(id='timeseries-plot'),
                                    html.Div(id='bar-plot'),
                                    html.Div(id='total-timeseries'),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
