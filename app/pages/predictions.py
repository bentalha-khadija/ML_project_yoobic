"""
Predictions Page - Display predictions table
"""

import dash_mantine_components as dmc
from dash import html

from app.components import create_table_section


def create_predictions_page():
    """
    Create predictions page with table
    
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
                            dmc.Title("📋 Data Table", order=2),
                            dmc.Text(
                                "View your predictions in tabular format",
                                size="md",
                                c="dimmed"
                            ),
                        ],
                    ),
                    
                    # Table section
                    create_table_section(),
                ],
            ),
        ],
    )
