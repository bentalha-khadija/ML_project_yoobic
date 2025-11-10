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
        [Output('timeseries-plot', 'children'),
         Output('bar-plot', 'children'),
         Output('total-timeseries', 'children')],
        [Input('predictions-store', 'data'),
         Input('viz-store-selector', 'value')],
        prevent_initial_call=False,
    )
    def update_visualizations(data, selected_store):
        """Generate charts based on data and selected store or show placeholders"""
        
        # Show placeholders when no data
        if data is None or len(data) == 0:
            return (
                create_chart_placeholder(
                    title="Store Timeline",
                    icon="ph:chart-line-duotone",
                    message="Upload data first to view visualizations"
                ),
                create_chart_placeholder(
                    title="Top Stores",
                    icon="ph:chart-bar-duotone",
                    message="Upload data first to view visualizations"
                ),
                create_chart_placeholder(
                    title="Overall Timeline",
                    icon="ph:trend-up-duotone",
                    message="Upload data first to view visualizations"
                )
            )
        
        # If no store selected but data available: show placeholder for timeseries only
        if selected_store is None:
            try:
                df = pd.DataFrame(data)
                df['date'] = pd.to_datetime(df['date'])
                
                # Bar Chart and Average timeline can be displayed without store selection
                # Bar Chart - Average Sales by Store (Top 15)
                store_averages = df.groupby('store')['predicted_sales'].mean().sort_values(ascending=False).head(15)
                
                fig_bar = go.Figure()
                fig_bar.add_trace(go.Bar(
                    x=[f'Store {s}' for s in store_averages.index],
                    y=store_averages.values,
                    marker=dict(
                        color=store_averages.values,
                        colorscale='Blues',
                        showscale=False,
                    ),
                ))
                
                fig_bar.update_layout(
                    title='Average Predicted Sales by Store (Top 15)',
                    xaxis_title='Store',
                    yaxis_title='Average Sales ($)',
                    template='plotly_white',
                    height=400,
                    margin=dict(l=50, r=50, t=50, b=50),
                )
                
                # Average Sales Time Series (All Stores)
                daily_averages = df.groupby('date')['predicted_sales'].mean().reset_index()
                daily_averages = daily_averages.sort_values('date')
                
                fig_total = go.Figure()
                fig_total.add_trace(go.Scatter(
                    x=daily_averages['date'],
                    y=daily_averages['predicted_sales'],
                    mode='lines',
                    name='Average Sales',
                    line=dict(color='#52C41A', width=3, shape='spline'),
                    fill='tozeroy',
                    fillcolor='rgba(82, 196, 26, 0.1)',
                ))
                
                fig_total.update_layout(
                    title='Average Sales Prediction Across All Stores',
                    xaxis_title='Date',
                    yaxis_title='Average Predicted Sales ($)',
                    template='plotly_white',
                    hovermode='x unified',
                    height=400,
                    margin=dict(l=50, r=50, t=50, b=50),
                )
                
                return (
                    create_chart_placeholder(
                        title="Store Timeline",
                        icon="ph:chart-line-duotone",
                        message="Select a store from the dropdown above to view its sales timeline"
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
            except Exception as e:
                print(f"❌ Error creating default charts: {e}")
                return (
                    create_chart_placeholder(
                        title="Store Timeline",
                        icon="ph:chart-line-duotone",
                        message="Select a store from the dropdown above"
                    ),
                    create_chart_placeholder(
                        title="Top Stores",
                        icon="ph:chart-bar-duotone",
                        message="Error loading chart"
                    ),
                    create_chart_placeholder(
                        title="Overall Timeline",
                        icon="ph:trend-up-duotone",
                        message="Error loading chart"
                    )
                )
        
        try:
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            
            # Time Series for Selected Store
            # Ensure selected_store is converted to the same type as df['store']
            selected_store_int = int(selected_store)
            df_store = df[df['store'] == selected_store_int].sort_values('date')
            
            if df_store.empty:
                return (
                    create_chart_placeholder(
                        title="Store Timeline",
                        icon="ph:chart-line-duotone",
                        message=f"No data found for Store {selected_store_int}"
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
        except Exception as e:
            print(f"❌ Error in update_visualizations: {str(e)}")
            return (
                create_chart_placeholder(
                    title="Error",
                    icon="ph:warning-duotone",
                    message=f"An error occurred: {str(e)}"
                ),
                create_chart_placeholder(
                    title="Error",
                    icon="ph:warning-duotone",
                    message=f"An error occurred: {str(e)}"
                ),
                create_chart_placeholder(
                    title="Error",
                    icon="ph:warning-duotone",
                    message=f"An error occurred: {str(e)}"
                )
            )
        
        fig_timeseries = go.Figure()
        fig_timeseries.add_trace(go.Scatter(
            x=df_store['date'],
            y=df_store['predicted_sales'],
            mode='lines',
            name='Predicted Sales',
            line=dict(color='#4A90E2', width=3, shape='spline'),
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
        
        # Bar Chart - Average Sales by Store (Top 15)
        store_averages = df.groupby('store')['predicted_sales'].mean().sort_values(ascending=False).head(15)
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=[f'Store {s}' for s in store_averages.index],
            y=store_averages.values,
            marker=dict(
                color=store_averages.values,
                colorscale='Blues',
                showscale=False,
            ),
        ))
        
        fig_bar.update_layout(
            title='Average Predicted Sales by Store (Top 15)',
            xaxis_title='Store',
            yaxis_title='Average Sales ($)',
            template='plotly_white',
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
        )
        
        # Average Sales Time Series (All Stores)
        daily_averages = df.groupby('date')['predicted_sales'].mean().reset_index()
        daily_averages = daily_averages.sort_values('date')
        
        fig_total = go.Figure()
        fig_total.add_trace(go.Scatter(
            x=daily_averages['date'],
            y=daily_averages['predicted_sales'],
            mode='lines',
            name='Average Sales',
            line=dict(color='#52C41A', width=3, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(82, 196, 26, 0.1)',
        ))
        
        fig_total.update_layout(
            title='Average Sales Prediction Across All Stores',
            xaxis_title='Date',
            yaxis_title='Average Predicted Sales ($)',
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
