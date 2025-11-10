"""
Navigation Callbacks to manage pages
"""

from dash import Input, Output, State, ALL, ctx

from app.pages import (
    create_home_page,
    create_predictions_page,
    create_visualizations_page,
    create_model_info_page,
)


def register_navigation_callbacks(app):
    """Register navigation callbacks"""
    
    @app.callback(
        [Output('page-content', 'children'),
         Output('current-page-store', 'data'),
         Output('nav-upload', 'active'),
         Output('nav-predictions', 'active'),
         Output('nav-visualizations', 'active'),
         Output('nav-model', 'active')],
        [Input('nav-upload', 'n_clicks'),
         Input('nav-predictions', 'n_clicks'),
         Input('nav-visualizations', 'n_clicks'),
         Input('nav-model', 'n_clicks')],
        [State('model-metadata-store', 'data'),
         State('current-page-store', 'data')],
        prevent_initial_call=False,
    )
    def update_page(nav_upload, nav_pred, nav_viz, nav_model, model_meta, current_page):
        """Change displayed page based on selection"""
        
        # Determine which navigation was clicked
        triggered_id = ctx.triggered_id if ctx.triggered_id else 'nav-upload'
        
        # Mapping navigation to page
        page_map = {
            'nav-upload': ('home', create_home_page()),
            'nav-predictions': ('predictions', create_predictions_page()),
            'nav-visualizations': ('visualizations', create_visualizations_page()),
            'nav-model': ('model', create_model_info_page(model_meta)),
        }
        
        # If no trigger (initial load), use current_page
        if triggered_id is None:
            triggered_id = f'nav-{current_page}' if current_page else 'nav-upload'
        
        page_name, page_content = page_map.get(triggered_id, ('home', create_home_page()))
        
        # Activate only the selected navigation
        return [
            page_content,
            page_name,
            triggered_id == 'nav-upload',
            triggered_id == 'nav-predictions',
            triggered_id == 'nav-visualizations',
            triggered_id == 'nav-model',
        ]
