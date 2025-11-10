"""
Model Information Page
"""

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def create_model_info_page(model_meta=None):
    """
    Create model information page
    
    Args:
        model_meta: Dictionary containing model metadata
        
    Returns:
        DMC component
    """
    
    # Extract information
    training_info = model_meta.get('training_info', {})
    performance = model_meta.get('performance', {})
    
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
                            dmc.Title("🤖 Model Information", order=2),
                            dmc.Text(
                                f"Version {model_meta.get('version', 'N/A')} - Last updated: {model_meta.get('last_updated', 'N/A')}",
                                size="md",
                                c="dimmed"
                            ),
                        ],
                    ),
                    
                    # Section 1: Overview
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
                                            dmc.Title("Overview", order=4),
                                        ],
                                    ),
                                    
                                    dmc.SimpleGrid(
                                        cols={"base": 1, "sm": 2},
                                        spacing="lg",
                                        children=[
                                            # Approach
                                            dmc.Stack(
                                                gap="xs",
                                                children=[
                                                    dmc.Text("Approach", size="sm", fw=700, c="dimmed"),
                                                    dmc.Badge(
                                                        model_meta.get('approach', 'N/A'),
                                                        size="lg",
                                                        variant="light",
                                                        color="blue"
                                                    ),
                                                ],
                                            ),
                                            
                                            # Model type
                                            dmc.Stack(
                                                gap="xs",
                                                children=[
                                                    dmc.Text("Model Type", size="sm", fw=700, c="dimmed"),
                                                    dmc.Badge(
                                                        model_meta.get('model_type', 'N/A'),
                                                        size="lg",
                                                        variant="light",
                                                        color="green"
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    
                                    # Description
                                    dmc.Alert(
                                        icon=DashIconify(icon="ph:info"),
                                        title="Description",
                                        color="blue",
                                        variant="light",
                                        children=dmc.Text(
                                            model_meta.get('description', 'No description available'),
                                            size="sm"
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    
                    # Section 2: Performance
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
                                            DashIconify(icon="ph:target", width=24),
                                            dmc.Title("Performance Metrics", order=4),
                                        ],
                                    ),
                                    
                                    dmc.SimpleGrid(
                                        cols={"base": 1, "sm": 2, "md": 3},
                                        spacing="lg",
                                        children=[
                                            # RMSE
                                            dmc.Paper(
                                                p="md",
                                                radius="sm",
                                                withBorder=True,
                                                style={'backgroundColor': '#F8F9FA'},
                                                children=[
                                                    dmc.Stack(
                                                        gap="xs",
                                                        align="center",
                                                        children=[
                                                            DashIconify(
                                                                icon="ph:chart-line-up",
                                                                width=32,
                                                                color="#4A90E2"
                                                            ),
                                                            dmc.Text("RMSE", size="sm", fw=600, c="dimmed"),
                                                            dmc.Text(
                                                                f"${performance.get('rmse', 0):,.2f}",
                                                                size="xl",
                                                                fw=700,
                                                                c="blue"
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            
                                            # MAE
                                            dmc.Paper(
                                                p="md",
                                                radius="sm",
                                                withBorder=True,
                                                style={'backgroundColor': '#F8F9FA'},
                                                children=[
                                                    dmc.Stack(
                                                        gap="xs",
                                                        align="center",
                                                        children=[
                                                            DashIconify(
                                                                icon="ph:trend-up",
                                                                width=32,
                                                                color="#52C41A"
                                                            ),
                                                            dmc.Text("MAE", size="sm", fw=600, c="dimmed"),
                                                            dmc.Text(
                                                                f"${performance.get('mae', 0):,.2f}",
                                                                size="xl",
                                                                fw=700,
                                                                c="green"
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            
                                            # MAPE
                                            dmc.Paper(
                                                p="md",
                                                radius="sm",
                                                withBorder=True,
                                                style={'backgroundColor': '#F8F9FA'},
                                                children=[
                                                    dmc.Stack(
                                                        gap="xs",
                                                        align="center",
                                                        children=[
                                                            DashIconify(
                                                                icon="ph:percent",
                                                                width=32,
                                                                color="#FA8C16"
                                                            ),
                                                            dmc.Text("MAPE", size="sm", fw=600, c="dimmed"),
                                                            dmc.Text(
                                                                f"{performance.get('mape', 0):.2f}%",
                                                                size="xl",
                                                                fw=700,
                                                                c="orange"
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    
                    # Section 3: Training Information
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
                                            DashIconify(icon="ph:gear", width=24),
                                            dmc.Title("Training Configuration", order=4),
                                        ],
                                    ),
                                    
                                    dmc.SimpleGrid(
                                        cols={"base": 1, "sm": 2},
                                        spacing="md",
                                        children=[
                                            _create_info_item("Number of Clusters", training_info.get('n_clusters', 'N/A')),
                                            _create_info_item("Algorithm", training_info.get('algorithm', 'N/A')),
                                            _create_info_item("Clustering Method", training_info.get('clustering_method', 'N/A')),
                                            _create_info_item("Number of Features", training_info.get('n_features', 'N/A')),
                                            _create_info_item("Stores Range", training_info.get('stores_range', 'N/A')),
                                            _create_info_item("Created Date", model_meta.get('created_date', 'N/A')),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    
                    # Section 4: Features
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
                                            DashIconify(icon="ph:list-bullets", width=24),
                                            dmc.Title("Features", order=4),
                                        ],
                                    ),
                                    
                                    dmc.List(
                                        icon=DashIconify(icon="ph:check-circle", color="green"),
                                        spacing="sm",
                                        children=[
                                            dmc.ListItem(
                                                dmc.Text(feature, size="sm")
                                            )
                                            for feature in model_meta.get('features', [])
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _create_info_item(label, value):
    """Helper to create an information item"""
    return dmc.Stack(
        gap="xs",
        children=[
            dmc.Text(label, size="sm", fw=600, c="dimmed"),
            dmc.Text(str(value), size="md", fw=500),
        ],
    )
