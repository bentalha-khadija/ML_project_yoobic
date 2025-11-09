"""
Application Configuration
"""

# Server Configuration
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
HOST = '127.0.0.1'
PORT = 8050
DEBUG = True

# Application Metadata
APP_TITLE = "Store Sales Prediction"
APP_ICON = "📊"

# File Upload
ACCEPTED_FILE_TYPES = ['.csv']
REQUIRED_COLUMNS = [
    'store', 'date', 'holiday_flag', 
    'temperature', 'fuel_Price', 'cpi', 'unemployment'
]

# Pagination
TABLE_PAGE_SIZE = 20

# Paths
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.insert(0, PROJECT_ROOT)
