"""
Model Information Component
"""

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def create_model_info(model_meta):
    """Create the model information section"""
    
    return dmc.Paper(
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
                            DashIconify(icon="ph:brain", width=24),
                            dmc.Title("Model Information", order=4),
                        ],
                    ),
                    
                    # Model Metrics
                    dmc.Grid(
                        children=[
                            dmc.GridCol(
                                _create_metric_item("Approach", model_meta['approach']),
                                span=6,
                            ),
                            dmc.GridCol(
                                _create_metric_item("Model", model_meta['model_type']),
                                span=6,
                            ),
                            dmc.GridCol(
                                _create_metric_item("RMSE", f"{model_meta['rmse']:,.2f}"),
                                span=4,
                            ),
                            dmc.GridCol(
                                _create_metric_item("MAE", f"{model_meta['mae']:,.2f}"),
                                span=4,
                            ),
                            dmc.GridCol(
                                _create_metric_item("MAPE", f"{model_meta['mape']:.2f}%"),
                                span=4,
                            ),
                        ],
                    ),
                    
                    dmc.Divider(),
                    
                    # Description
                    dmc.Text(
                        model_meta['description'],
                        size="sm",
                        c="dimmed",
                    ),
                    
                    # Features
                    dmc.Stack(
                        gap="xs",
                        children=[
                            dmc.Text("Key Features:", size="sm", fw=600),
                            dmc.List(
                                spacing="xs",
                                size="sm",
                                icon=DashIconify(icon="ph:check-circle", width=16, color="#52C41A"),
                                children=[
                                    dmc.ListItem(feat) for feat in model_meta['features']
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _create_metric_item(label, value):
    """Helper function to create a metric display item"""
    return dmc.Stack(
        gap="xs",
        children=[
            dmc.Text(label, size="xs", c="dimmed", fw=500),
            dmc.Text(value, size="md", fw=600),
        ],
    )
