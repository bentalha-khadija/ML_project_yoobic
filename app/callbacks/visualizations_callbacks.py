"""
Callbacks for the Visualizations page
"""

from dash import Input, Output
import pandas as pd


def register_visualizations_callbacks(app):
    """Register callbacks for the Visualizations page"""
    
    @app.callback(
        [Output('viz-store-selector', 'data'),
         Output('viz-store-selector', 'value'),
         Output('viz-store-selector', 'disabled')],
        Input('predictions-store', 'data'),
        prevent_initial_call=False,
    )
    def update_visualizations_selector(predictions_data):
        """Update store selector for visualizations"""
        
        if predictions_data is None or len(predictions_data) == 0:
            return [], None, True
        
        # Data available
        df_predictions = pd.DataFrame(predictions_data)
        
        # Store selector options
        stores = sorted(df_predictions['store'].unique())
        store_options = [
            {'label': f'Store {s}', 'value': str(s)} 
            for s in stores
        ]
        
        # Automatically select the first store
        default_store = str(stores[0]) if stores else None
        
        return store_options, default_store, False
