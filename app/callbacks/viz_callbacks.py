"""
Visualization Callbacks
"""

from dash import Input, Output, State, callback, dcc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from app.components.placeholder import create_chart_placeholder


def register_viz_callbacks(app):
    """Register visualization-related callbacks"""
    
    @app.callback(
        [Output('timeseries-plot', 'children', allow_duplicate=True),
         Output('bar-plot', 'children', allow_duplicate=True),
         Output('total-timeseries', 'children', allow_duplicate=True)],
        Input('predictions-store', 'data'),
        prevent_initial_call=True,
    )
    def show_initial_placeholders(data):
        """Show placeholders when data is uploaded but no store selected"""
        if data is not None:
            return (
                create_chart_placeholder(
                    title="Store Timeline",
                    icon="ph:chart-line-duotone",
                    message="Select a store from the dropdown above to view its sales timeline"
                ),
                create_chart_placeholder(
                    title="Top Stores",
                    icon="ph:chart-bar-duotone",
                    message="Top 15 stores by total predicted sales will appear here"
                ),
                create_chart_placeholder(
                    title="Overall Timeline",
                    icon="ph:trend-up-duotone",
                    message="Total sales prediction across all stores will appear here"
                )
            )
        return (None, None, None)
    
    @app.callback(
        [Output('timeseries-plot', 'children'),
         Output('bar-plot', 'children'),
         Output('total-timeseries', 'children')],
        Input('viz-store-selector', 'value'),
        State('predictions-store', 'data'),
        prevent_initial_call=True,
    )
    def update_visualizations(selected_store, data):
        """Update all visualizations based on selected store"""
        
        # Show placeholders when no store is selected
        if data is None or selected_store is None:
            return (
                create_chart_placeholder(
                    title="Store Timeline",
                    icon="ph:chart-line-duotone",
                    message="Select a store from the dropdown above to view its sales timeline"
                ),
                create_chart_placeholder(
                    title="Top Stores",
                    icon="ph:chart-bar-duotone",
                    message="Top 15 stores by total predicted sales will appear here"
                ),
                create_chart_placeholder(
                    title="Overall Timeline",
                    icon="ph:trend-up-duotone",
                    message="Total sales prediction across all stores will appear here"
                )
            )
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        
        # Time Series for Selected Store
        df_store = df[df['store'] == int(selected_store)].sort_values('date')
        
        fig_timeseries = go.Figure()
        fig_timeseries.add_trace(go.Scatter(
            x=df_store['date'],
            y=df_store['predicted_sales'],
            mode='lines+markers',
            name='Predicted Sales',
            line=dict(color='#4A90E2', width=2),
            marker=dict(size=6),
        ))
        
        fig_timeseries.update_layout(
            title=f'Sales Prediction Timeline - Store {selected_store}',
            xaxis_title='Date',
            yaxis_title='Predicted Sales ($)',
            template='plotly_white',
            hovermode='x unified',
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
        )
        
        # Bar Chart - Sales by Store (Top 15)
        store_totals = df.groupby('store')['predicted_sales'].sum().sort_values(ascending=False).head(15)
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=[f'Store {s}' for s in store_totals.index],
            y=store_totals.values,
            marker=dict(
                color=store_totals.values,
                colorscale='Blues',
                showscale=False,
            ),
        ))
        
        fig_bar.update_layout(
            title='Total Predicted Sales by Store (Top 15)',
            xaxis_title='Store',
            yaxis_title='Total Sales ($)',
            template='plotly_white',
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
        )
        
        # Total Sales Time Series (All Stores)
        daily_totals = df.groupby('date')['predicted_sales'].sum().reset_index()
        daily_totals = daily_totals.sort_values('date')
        
        fig_total = go.Figure()
        fig_total.add_trace(go.Scatter(
            x=daily_totals['date'],
            y=daily_totals['predicted_sales'],
            mode='lines',
            name='Total Sales',
            line=dict(color='#52C41A', width=2),
            fill='tozeroy',
            fillcolor='rgba(82, 196, 26, 0.1)',
        ))
        
        fig_total.update_layout(
            title='Total Sales Prediction Across All Stores',
            xaxis_title='Date',
            yaxis_title='Total Predicted Sales ($)',
            template='plotly_white',
            hovermode='x unified',
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
        )
        
        # Return actual graphs wrapped in dcc.Graph components
        return (
            dcc.Graph(
                figure=fig_timeseries,
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                }
            ),
            dcc.Graph(
                figure=fig_bar,
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                }
            ),
            dcc.Graph(
                figure=fig_total,
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                }
            )
        )
