"""
Callbacks for the Predictions page
"""

from dash import Input, Output, State, callback
import pandas as pd


def register_predictions_callbacks(app):
    """Register callbacks for the Predictions page"""
    
    @app.callback(
        [Output('predictions-table', 'data'),
         Output('predictions-table', 'columns'),
         Output('table-section', 'style'),
         Output('download-button', 'disabled')],
        Input('predictions-store', 'data'),
        prevent_initial_call=False,
    )
    def update_predictions_page(predictions_data):
        """Update Predictions page when data is available"""
        
        if predictions_data is None or len(predictions_data) == 0:
            # No data: hide table
            return [
                [],
                [],
                {'display': 'none'},
                True
            ]
        
        # Data available: show everything
        df_predictions = pd.DataFrame(predictions_data)
        
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
        
        return [
            df_display.to_dict('records'),
            columns,
            {'display': 'block'},
            False
        ]
