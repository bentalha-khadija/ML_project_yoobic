"""
Main Application Entry Point
Modern Store Sales Prediction App with Dash Mantine Components
"""

import dash
from flask import Flask

from app import config
from app.layouts import create_layout
from app.callbacks import (
    register_upload_callbacks,
    register_theme_callbacks,
    register_viz_callbacks,
)
from utils.model_loader import get_model_metadata


# Initialize Flask server
server = Flask(__name__)
server.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# Initialize Dash app
app = dash.Dash(
    __name__,
    server=server,
    title=config.APP_TITLE,
    suppress_callback_exceptions=True,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1, maximum-scale=1",
        }
    ],
)

# Load model metadata
model_meta = get_model_metadata()

# Set layout
app.layout = create_layout(model_meta)

# Register callbacks
register_upload_callbacks(app)
register_theme_callbacks(app)
register_viz_callbacks(app)


def main():
    """Run the application"""
    print("\n" + "="*80)
    print(f"🚀 Starting {config.APP_TITLE}")
    print("="*80)
    print(f"\n📍 Open your browser at: http://{config.HOST}:{config.PORT}")
    print("\n⚙️  Configuration:")
    print(f"  - Max file size: {config.MAX_CONTENT_LENGTH / (1024*1024):.0f}MB")
    print(f"  - Table page size: {config.TABLE_PAGE_SIZE}")
    print(f"  - Debug mode: {config.DEBUG}")
    print("\n📊 Model Information:")
    print(f"  - Approach: {model_meta['approach']}")
    print(f"  - Model: {model_meta['model_type']}")
    print(f"  - RMSE: {model_meta['rmse']:,.2f}")
    print("\n" + "="*80 + "\n")
    
    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT,
    )


if __name__ == '__main__':
    main()
