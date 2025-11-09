"""
Predictions Table Component
"""

import dash_mantine_components as dmc
from dash import html, dash_table, dcc
from dash_iconify import DashIconify
from app.config import TABLE_PAGE_SIZE


def create_table_section():
    """Create the predictions table section"""
    
    return html.Div(
        id='table-section',
        style={'display': 'none'},
        children=[
            dmc.Paper(
                p="xl",
                radius="md",
                withBorder=True,
                children=[
                    dmc.Stack(
                        gap="lg",
                        children=[
                            # Header with Download Button
                            dmc.Group(
                                justify="space-between",
                                children=[
                                    dmc.Group(
                                        gap="sm",
                                        children=[
                                            DashIconify(icon="ph:table", width=24),
                                            dmc.Title("Predictions Table", order=4),
                                        ],
                                    ),
                                    dmc.Button(
                                        "Download CSV",
                                        id='download-button',
                                        leftSection=DashIconify(icon="ph:download-simple"),
                                        variant="light",
                                        c="blue",
                                        disabled=True,
                                    ),
                                ],
                            ),
                            
                            # Data Table
                            dash_table.DataTable(
                                id='predictions-table',
                                columns=[],
                                data=[],
                                page_size=TABLE_PAGE_SIZE,
                                style_table={
                                    'overflowX': 'auto',
                                    'borderRadius': '8px',
                                },
                                style_cell={
                                    'textAlign': 'left',
                                    'padding': '12px 16px',
                                    'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                                    'fontSize': '14px',
                                    'border': '1px solid #E8EAED',
                                },
                                style_header={
                                    'backgroundColor': '#F5F7FA',
                                    'fontWeight': '600',
                                    'color': '#2C2E33',
                                    'border': '1px solid #E8EAED',
                                    'borderBottom': '2px solid #4A90E2',
                                },
                                style_data={
                                    'backgroundColor': 'white',
                                    'color': '#2C2E33',
                                },
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': '#FAFBFC',
                                    },
                                    {
                                        'if': {'state': 'selected'},
                                        'backgroundColor': '#EBF4FF',
                                        'border': '1px solid #4A90E2',
                                    },
                                ],
                                sort_action="native",
                                sort_mode="multi",
                                export_format="csv",
                                page_action="native",
                            ),
                            
                            dcc.Download(id="download-dataframe-csv"),
                        ],
                    ),
                ],
            ),
        ],
    )
