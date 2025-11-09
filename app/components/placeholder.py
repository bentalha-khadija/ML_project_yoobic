"""
Placeholder Components
"""

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def create_chart_placeholder(title, icon, message):
    """
    Create a placeholder for charts when no data is selected
    
    Args:
        title: Chart title
        icon: Icon name for DashIconify
        message: Message to display
    
    Returns:
        DMC component with placeholder styling
    """
    return dmc.Paper(
        p="xl",
        radius="md",
        withBorder=True,
        style={
            'backgroundColor': '#F8F9FA',
            'minHeight': '300px',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
        },
        children=[
            dmc.Stack(
                gap="md",
                align="center",
                children=[
                    DashIconify(
                        icon=icon,
                        width=64,
                        color="#ADB5BD",
                    ),
                    dmc.Stack(
                        gap="xs",
                        align="center",
                        children=[
                            dmc.Text(
                                title,
                                size="lg",
                                fw=600,
                                c="dimmed",
                            ),
                            dmc.Text(
                                message,
                                size="sm",
                                c="dimmed",
                                ta="center",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def create_empty_message(icon, title, message):
    """
    Create an empty state message component
    
    Args:
        icon: Icon name for DashIconify
        title: Title text
        message: Message text
    
    Returns:
        DMC component with empty state styling
    """
    return dmc.Center(
        style={'minHeight': '200px'},
        children=[
            dmc.Stack(
                gap="md",
                align="center",
                children=[
                    DashIconify(
                        icon=icon,
                        width=48,
                        color="#CED4DA",
                    ),
                    dmc.Stack(
                        gap="xs",
                        align="center",
                        children=[
                            dmc.Text(
                                title,
                                size="md",
                                fw=600,
                                c="dimmed",
                            ),
                            dmc.Text(
                                message,
                                size="sm",
                                c="dimmed",
                                ta="center",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def create_loading_placeholder(message="Loading..."):
    """
    Create a loading placeholder
    
    Args:
        message: Loading message
    
    Returns:
        DMC component with loading state
    """
    return dmc.Center(
        style={'minHeight': '300px'},
        children=[
            dmc.Stack(
                gap="md",
                align="center",
                children=[
                    dmc.Loader(size="lg", variant="dots"),
                    dmc.Text(
                        message,
                        size="sm",
                        c="dimmed",
                    ),
                ],
            ),
        ],
    )
