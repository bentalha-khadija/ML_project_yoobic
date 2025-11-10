"""
Main Application Layout with Sidebar Navigation
"""

import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify

from app.pages import (
    create_home_page,
    create_predictions_page,
    create_model_info_page,
)


def create_sidebar():
    """Crée la barre de navigation latérale"""
    return dmc.Stack(
        gap="md",
        children=[
            # Logo et titre
            dmc.Stack(
                gap="xs",
                mb="xl",
                children=[
                    dmc.Group(
                        gap="sm",
                        children=[
                            dmc.ThemeIcon(
                                DashIconify(icon="ph:storefront-duotone", width=32),
                                size="xl",
                                radius="md",
                                variant="light",
                                color="blue",
                            ),
                            dmc.Stack(
                                gap=0,
                                children=[
                                    dmc.Title("Store Sales", order=4),
                                    dmc.Text("Prediction", size="xs", c="dimmed"),
                                ],
                            ),
                        ],
                    ),
                    dmc.Divider(),
                ],
            ),
            
            # Navigation Links
            dmc.NavLink(
                id="nav-upload",
                label="Upload Data",
                leftSection=DashIconify(icon="ph:cloud-arrow-up", width=20),
                active=True,
                variant="light",
            ),
            
            dmc.NavLink(
                id="nav-predictions",
                label="Data Table",
                leftSection=DashIconify(icon="ph:table", width=20),
                variant="light",
            ),
            
            dmc.NavLink(
                id="nav-visualizations",
                label="Visualizations",
                leftSection=DashIconify(icon="ph:chart-line", width=20),
                variant="light",
            ),
            
            dmc.NavLink(
                id="nav-model",
                label="Model Info",
                leftSection=DashIconify(icon="ph:brain", width=20),
                variant="light",
            ),
            
        ],
    )


def create_layout(model_meta):
    """
    Create the main application layout with sidebar navigation
    
    Args:
        model_meta: Dictionary containing model metadata
        
    Returns:
        Dash layout component
    """
    
    return dmc.MantineProvider(
        id="mantine-provider",
        theme={
            "colorScheme": "light",
            "primaryColor": "blue",
        },
        withGlobalClasses=True,
        children=[
            # Theme store
            dcc.Store(id='theme-store', data='light'),
            
            # Predictions data store
            dcc.Store(id='predictions-store', data=None),
            
            # Download component
            dcc.Download(id="download-dataframe-csv"),
            
            # Store model metadata
            dcc.Store(id='model-metadata-store', data=model_meta),
            
            # Current page store
            dcc.Store(id='current-page-store', data='home'),
            
            # AppShell avec sidebar
            dmc.AppShell(
                [
                    dmc.AppShellNavbar(
                        p="md",
                        children=[create_sidebar()],
                    ),
                    dmc.AppShellMain(
                        children=[
                            dmc.Container(
                                size="xl",
                                px="md",
                                py="xl",
                                children=[
                                    html.Div(
                                        id='page-content',
                                        children=create_home_page()
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                navbar={
                    "width": 280,
                    "breakpoint": "sm",
                },
                padding="md",
            ),
        ],
    )
