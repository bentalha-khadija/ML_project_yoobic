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
         Output('predictions-table', 'data'),
         Output('predictions-table', 'columns'),
         Output('table-section', 'style'),
         Output('viz-section', 'style'),
         Output('stats-section', 'style'),
         Output('viz-store-selector', 'data'),
         Output('viz-store-selector', 'disabled'),
         Output('download-button', 'disabled'),
         Output('summary-stats', 'children')],
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        prevent_initial_call=True,
    )
    def process_upload(contents, filename):
        """Process uploaded file and generate predictions"""
        
        if contents is None:
            return [
                None, None, [], [], 
                {'display': 'none'}, {'display': 'none'}, {'display': 'none'},
                [], True, True, None
            ]
        
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
                    None, [], [],
                    {'display': 'none'}, {'display': 'none'}, {'display': 'none'},
                    [], True, True, None
                ]
            
            # Check temporal continuity (warnings only, doesn't block)
            temporal_warnings = check_temporal_continuity(df, max_gap_days=14)
            if temporal_warnings:
                print(f"⚠️ Avertissements temporels: {len(temporal_warnings)}")
                for warning in temporal_warnings[:5]:  # Limiter l'affichage
                    print(f"  - {warning}")
            
            # Generate predictions
            df_predictions = predict_sales(df)
            
            # Format for display
            df_display = df_predictions.copy()
            df_display['date'] = pd.to_datetime(df_display['date']).dt.strftime('%Y-%m-%d')
            df_display['predicted_sales'] = df_display['predicted_sales'].round(2)
            
            # Table columns
            columns = [
                {'name': 'Store', 'id': 'store'},
                {'name': 'Date', 'id': 'date'},
                {'name': 'Predicted Sales', 'id': 'predicted_sales'},
                {'name': 'Cluster', 'id': 'cluster'}
            ]
            
            # Store selector options
            store_options = [
                {'label': f'Store {s}', 'value': str(s)} 
                for s in sorted(df_predictions['store'].unique())
            ]
            
            # Calculate statistics
            stats = get_summary_stats(df_predictions)
            stats_content = dmc.SimpleGrid(
                cols={"base": 1, "sm": 2, "md": 4},
                spacing="lg",
                children=[
                    create_stat_card(
                        "Total Predictions",
                        f"{stats['total_predictions']:,}",
                        "ph:chart-line-up"
                    ),
                    create_stat_card(
                        "Mean Sales",
                        f"${stats['mean_sales']:,.2f}",
                        "ph:currency-dollar"
                    ),
                    create_stat_card(
                        "Total Sales",
                        f"${stats['total_sales']:,.2f}",
                        "ph:coins"
                    ),
                    create_stat_card(
                        "Unique Stores",
                        f"{stats['unique_stores']}",
                        "ph:storefront"
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
                df_predictions.to_dict('records'),
                df_display.to_dict('records'),
                columns,
                {'display': 'block'},
                {'display': 'block'},
                {'display': 'block'},
                store_options,
                False,
                False,
                stats_content,
            ]
            
        except Exception as e:
            return [
                dmc.Alert(
                    title="Processing Error",
                    c="red",
                    icon=DashIconify(icon="ph:x-circle"),
                    children=f"Error processing file: {str(e)}",
                ),
                None, [], [],
                {'display': 'none'}, {'display': 'none'}, {'display': 'none'},
                [], True, True, None
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
