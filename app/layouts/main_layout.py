"""
Main Application Layout
"""

import dash_mantine_components as dmc
from dash import html, dcc

from app.components import (
    create_header,
    create_upload_section,
    create_stats_section,
    create_table_section,
    create_charts_section,
    create_model_info,
)


def create_layout(model_meta):
    """
    Create the main application layout
    
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
            
            # Main Container
            dmc.Container(
                size="xl",
                px="md",
                py="xl",
                children=[
                    dmc.Stack(
                        gap="xl",
                        children=[
                            # Header
                            create_header(model_meta),
                            
                            # Upload Section
                            create_upload_section(),
                            
                            # Statistics Section
                            create_stats_section(),
                            
                            # Table Section
                            create_table_section(),
                            
                            # Charts Section
                            create_charts_section(),
                            
                            # Model Info Section
                            create_model_info(model_meta),
                        ],
                    ),
                ],
            ),
        ],
    )
