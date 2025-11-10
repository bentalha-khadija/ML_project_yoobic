"""
File Upload and Processing Callbacks
"""

from dash import Input, Output, State, callback, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import base64
import io

from utils.preprocessing import validate_csv_structure, check_temporal_continuity
from utils.predictor import predict_sales, get_summary_stats
from app.components.stats import create_stat_card


def register_upload_callbacks(app):
    """Register upload and data processing callbacks"""
    
    @app.callback(
        [Output('upload-status', 'children'),
         Output('predictions-store', 'data'),
         Output('summary-stats', 'children'),
         Output('stats-section', 'style')],
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        prevent_initial_call=True,
    )
    def process_upload(contents, filename):
        """Process uploaded file and generate predictions"""
        
        if contents is None:
            return [None, None, None, {'display': 'none'}]
        
        try:
            # Decode the file
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            
            # Validate structure
            is_valid, message = validate_csv_structure(df)
            if not is_valid:
                return [
                    dmc.Alert(
                        title="Validation Error",
                        c="red",
                        icon=DashIconify(icon="ph:warning"),
                        children=message,
                    ),
                    None,
                    None,
                    {'display': 'none'}
                ]
            
            # Check temporal continuity (warnings only, doesn't block)
            temporal_warnings = check_temporal_continuity(df, max_gap_days=14)
            if temporal_warnings:
                print(f"⚠️ Avertissements temporels: {len(temporal_warnings)}")
                for warning in temporal_warnings[:5]:  # Limiter l'affichage
                    print(f"  - {warning}")
            
            # Generate predictions
            df_predictions = predict_sales(df)
            
            # Calculate statistics
            # Calculate additional statistics
            n_stores = df_predictions['store'].nunique()
            n_days = df_predictions['date'].nunique()
            date_range = f"{df_predictions['date'].min()} to {df_predictions['date'].max()}"
            total_sales = df_predictions['predicted_sales'].sum()
            summary_stats = get_summary_stats(df_predictions)
            
            # Create summary stats with more information
            stats_content = dmc.Stack(
                gap="lg",
                children=[
                    # Row 1: Overview metrics
                    dmc.SimpleGrid(
                        cols={"base": 1, "sm": 2, "md": 4},
                        spacing="lg",
                        children=[
                            create_stat_card(
                                "Total Stores",
                                f"{n_stores}",
                                "ph:storefront"
                            ),
                            create_stat_card(
                                "Time Period",
                                f"{n_days} days",
                                "ph:calendar"
                            ),
                            create_stat_card(
                                "Total Predictions",
                                f"{len(df_predictions):,}",
                                "ph:chart-line-up"
                            ),
                            create_stat_card(
                                "Total Sales",
                                f"${total_sales:,.0f}",
                                "ph:currency-dollar"
                            ),
                        ],
                    ),
                    
                    # Row 2: Sales statistics
                    dmc.SimpleGrid(
                        cols={"base": 1, "sm": 2, "md": 4},
                        spacing="lg",
                        children=[
                            create_stat_card(
                                "Average Sales",
                                f"${summary_stats['mean_sales']:,.2f}",
                                "ph:coin"
                            ),
                            create_stat_card(
                                "Max Sales",
                                f"${summary_stats['max_sales']:,.2f}",
                                "ph:trend-up"
                            ),
                            create_stat_card(
                                "Min Sales",
                                f"${summary_stats['min_sales']:,.2f}",
                                "ph:trend-down"
                            ),
                            create_stat_card(
                                "Std Deviation",
                                f"${summary_stats['std_sales']:,.2f}",
                                "ph:chart-scatter"
                            ),
                        ],
                    ),
                    
                    # Date range info
                    dmc.Alert(
                        icon=DashIconify(icon="ph:calendar-check"),
                        title="Prediction Period",
                        color="blue",
                        variant="light",
                        children=date_range,
                    ),
                ],
            )
            
            return [
                dmc.Alert(
                    title="Success!",
                    c="green",
                    icon=DashIconify(icon="ph:check-circle"),
                    children=f"File '{filename}' processed successfully! Generated {len(df_predictions):,} predictions.",
                ),
                df_predictions.to_dict('records'),  # Store the data
                stats_content,  # Display stats on Home page
                {'display': 'block'}  # Show stats section
            ]
            
        except Exception as e:
            return [
                dmc.Alert(
                    title="Processing Error",
                    c="red",
                    icon=DashIconify(icon="ph:x-circle"),
                    children=f"Error processing file: {str(e)}",
                ),
                None,
                None,
                {'display': 'none'}
            ]
    
    
    @app.callback(
        Output("download-dataframe-csv", "data"),
        Input("download-button", "n_clicks"),
        State('predictions-store', 'data'),
        prevent_initial_call=True,
    )
    def download_predictions(n_clicks, data):
        """Download predictions as CSV"""
        if data is None:
            return None
        
        df = pd.DataFrame(data)
        df = df[['store', 'date', 'predicted_sales']].copy()
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        return dcc.send_data_frame(df.to_csv, "predictions.csv", index=False)
