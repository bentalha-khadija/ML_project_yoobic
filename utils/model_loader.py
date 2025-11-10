"""
Module to load optimal model and cluster models
"""

import joblib
import os
import json


def load_optimal_model(model_path='models/best_sales_model.pkl'):
    """
    Load saved optimal model
    
    Returns:
        dict: Contains model and its metadata
              {
                  'approach': 'Clustering',
                  'model': 'LightGBM', 
                  'rmse': 63519.94,
                  'mae': 42650.00,
                  'mape': 4.24,
                  'predictions': DataFrame,
                  'comparison_table': DataFrame
              }
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found at {model_path}. "
            "Run notebook 06_Comparison_Final.ipynb first to generate the model."
        )
    
    model_info = joblib.load(model_path)
    print(f"Optimal model loaded: {model_info['approach']} + {model_info['model']}")
    print(f"  RMSE: {model_info['rmse']:.2f}")
    
    return model_info


def load_cluster_models(models_dir='models'):
    """
    Load all LightGBM models by cluster
    
    Returns:
        dict: {cluster_id: model}
    """
    cluster_models = {}
    
    # Look for lgb_cluster_*.pkl files
    for filename in os.listdir(models_dir):
        if filename.startswith('lgb_cluster_') and filename.endswith('.pkl'):
            cluster_id = int(filename.replace('lgb_cluster_', '').replace('.pkl', ''))
            model_path = os.path.join(models_dir, filename)
            cluster_models[cluster_id] = joblib.load(model_path)
    
    if not cluster_models:
        raise FileNotFoundError(
            f"No cluster models found in {models_dir}. "
            "Run notebook 03_Modeling_Clustering.ipynb first."
        )
    
    print(f"{len(cluster_models)} cluster models loaded")
    return cluster_models


def get_model_metadata(metadata_path='models/model_metadata.json'):
    """
    Load and return model metadata from JSON file
    
    Args:
        metadata_path: Path to metadata JSON file
        
    Returns:
        dict: Model metadata
    """
    try:
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            print(f"Metadata loaded from {metadata_path}")
            return metadata
        else:
            print(f"File {metadata_path} not found. Using default metadata.")
            # Default metadata if JSON file doesn't exist
            return {
                'approach': 'Clustering',
                'model_type': 'LightGBM',
                'rmse': 63519.94,
                'mae': 42650.00,
                'mape': 4.24,
                'description': 'One LightGBM model per store cluster (k=4)',
                'features': [
                    'Lags: 1, 2, 4, 52 weeks',
                    'Rolling features: means and std',
                    'Cyclic encoding: week, month',
                    'Exogenous variables: temperature, fuel, CPI, unemployment'
                ]
            }
    except Exception as e:
        print(f"Error loading metadata: {e}")
        print("   Using default metadata.")
        # Return default metadata in case of error
        return {
            'approach': 'Clustering',
            'model_type': 'LightGBM',
            'rmse': 63519.94,
            'mae': 42650.00,
            'mape': 4.24,
            'description': 'One LightGBM model per store cluster (k=4)',
            'features': [
                'Lags: 1, 2, 4, 52 weeks',
                'Rolling features: means and std',
                'Cyclic encoding: week, month',
                'Exogenous variables: temperature, fuel, CPI, unemployment'
            ]
        }
