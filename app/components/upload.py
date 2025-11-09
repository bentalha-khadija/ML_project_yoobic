"""
File Upload Component
"""

import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify
from app.config import REQUIRED_COLUMNS


def create_upload_section():
    """Create the file upload section"""
    
    return dmc.Paper(
        p="xl",
        radius="md",
        withBorder=True,
        children=[
            dmc.Stack(
                gap="md",
                children=[
                    # Section Header
                    dmc.Group(
                        gap="sm",
                        children=[
                            DashIconify(icon="ph:cloud-arrow-up", width=24),
                            dmc.Title("Upload Your Data", order=4),
                        ],
                    ),
                    
                    # Upload Zone
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            html.Div("📄", style={
                                'fontSize': '48px',
                                'marginBottom': '16px',
                            }),
                            html.Div("Drag and Drop or Click to Select CSV File", style={
                                'fontSize': '16px',
                                'fontWeight': '600',
                                'color': '#212529',
                                'marginBottom': '8px',
                            }),
                            html.Div("Maximum file size: 16MB", style={
                                'fontSize': '13px',
                                'color': '#868e96',
                            }),
                        ]),
                        style={
                            'width': '100%',
                            'minHeight': '180px',
                            'border': '3px dashed #4A90E2',
                            'borderRadius': '12px',
                            'padding': '40px 20px',
                            'textAlign': 'center',
                            'backgroundColor': '#F8F9FA',
                            'cursor': 'pointer',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                        },
                        style_active={
                            'borderColor': '#0066CC',
                            'backgroundColor': '#E7F3FF',
                        },
                        multiple=False,
                    ),
                    
                    # Upload Status
                    html.Div(id='upload-status'),
                    
                    # Expected Columns Info
                    dmc.Alert(
                        title="Required Columns",
                        icon=DashIconify(icon="ph:info"),
                        c="blue",
                        variant="light",
                        children=dmc.Text(
                            ", ".join(REQUIRED_COLUMNS),
                            size="sm",
                        ),
                    ),
                ],
            ),
        ],
    )
