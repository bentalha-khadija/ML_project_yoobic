"""
Home Page - Upload and statistics
"""

import dash_mantine_components as dmc
from dash import html

from app.components import (
    create_upload_section,
    create_stats_section,
)


def create_home_page():
    """
    Create home page with upload and statistics
    
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
                            dmc.Title("📤 Upload Your Data", order=2),
                            dmc.Text(
                                "Upload your CSV file to start making predictions",
                                size="md",
                                c="dimmed"
                            ),
                        ],
                    ),
                    
                    # Upload section
                    create_upload_section(),
                    
                    # Statistics section
                    create_stats_section(),
                ],
            ),
        ],
    )
