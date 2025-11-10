"""
Module for making predictions
"""

import pandas as pd
import numpy as np
import lightgbm as lgb
from utils.preprocessing import create_features, get_feature_columns, load_historical_stats
from utils.model_loader import load_cluster_models


# Load store to cluster mapping
def load_store_clusters(cluster_features_path='data/cluster_features.pkl'):
    """
    Load store to cluster mapping from clustering file
    
    Returns:
        dict: {store_id: cluster_id}
    """
    try:
        cluster_features = pd.read_pickle(cluster_features_path)
        store_cluster_map = cluster_features.set_index('store')['cluster'].to_dict()
        print(f"Store->cluster mapping loaded for {len(store_cluster_map)} stores")
        return store_cluster_map
    except Exception as e:
        print(f"Error loading mapping: {e}")
        # Default mapping if file not found
        return {i: i % 4 for i in range(1, 46)}  # 45 stores distributed over 4 clusters


def predict_sales(df_input):
    """
    Make predictions on input DataFrame
    
    Args:
        df_input: DataFrame with columns [store, date, temperature, fuel_Price, 
                  cpi, unemployment, holiday_flag]
    
    Returns:
        DataFrame with columns [store, date, predicted_sales, cluster]
    """
    
    # 1. Load historical statistics for imputation
    historical_stats = load_historical_stats()
    
    # 2. Remove weekly_sales if it exists (force imputation for prediction)
    df_for_prediction = df_input.copy()
    if 'weekly_sales' in df_for_prediction.columns:
        print("Column 'weekly_sales' detected - It will be ignored for prediction")
        print("Lags will be imputed with historical statistics")
        df_for_prediction = df_for_prediction.drop(columns=['weekly_sales'])
    
    # 3. Apply feature engineering
    print("\nFeature engineering...")
    df_features = create_features(df_for_prediction, historical_stats)
    
    if df_features.empty:
        raise ValueError("No data available after feature engineering")
    
    # 3. Load store to cluster mapping
    store_cluster_map = load_store_clusters()
    df_features['cluster'] = df_features['store'].map(store_cluster_map)
    
    # Check that all stores have a cluster
    missing_clusters = df_features['cluster'].isna().sum()
    if missing_clusters > 0:
        print(f"{missing_clusters} stores without assigned cluster - using cluster 0")
        df_features['cluster'] = df_features['cluster'].fillna(0).astype(int)
    
    # 4. Try to load cluster models, otherwise use global model
    print("\nLoading model...")
    feature_cols = get_feature_columns()
    
    try:
        # Try to load individual cluster models
        cluster_models = load_cluster_models()
        use_cluster_models = True
        print(f"{len(cluster_models)} cluster models loaded")
    except FileNotFoundError:
        # Use single global model
        print("Cluster models not found, training global model...")
        use_cluster_models = False
        
        # Load training data
        try:
            train_data = pd.read_pickle('data/train.pkl')
            print(f"Training data loaded: {len(train_data)} rows")
            
            # Train global LightGBM model
            model = lgb.LGBMRegressor(n_estimators=100, random_state=42, verbose=-1)
            model.fit(train_data[feature_cols], train_data['weekly_sales'])
            print("Global model trained")
        except Exception as e:
            raise ValueError(f"Cannot load training data: {e}")
    
    # 5. Predict
    print("\nPredicting...")
    
    if use_cluster_models:
        # Predict with cluster models
        predictions = []
        
        for cluster_id in sorted(df_features['cluster'].unique()):
            df_cluster = df_features[df_features['cluster'] == cluster_id].copy()
            
            if cluster_id not in cluster_models:
                print(f"Model for cluster {cluster_id} not found - skipping")
                continue
            
            cluster_model = cluster_models[cluster_id]
            y_pred = cluster_model.predict(df_cluster[feature_cols])
            
            df_cluster['predicted_sales'] = y_pred
            predictions.append(df_cluster[['store', 'date', 'predicted_sales', 'cluster']])
            print(f"  Cluster {cluster_id}: {len(df_cluster)} predictions")
        
        df_predictions = pd.concat(predictions).reset_index(drop=True)
    else:
        # Predict with global model
        y_pred = model.predict(df_features[feature_cols])
        df_features['predicted_sales'] = y_pred
        df_predictions = df_features[['store', 'date', 'predicted_sales', 'cluster']].copy()
        print(f"  {len(df_predictions)} predictions with global model")
    
    print(f"\n{len(df_predictions)} predictions generated successfully")
    
    return df_predictions


def get_summary_stats(df_predictions):
    """
    Calculate descriptive statistics on predictions
    
    Returns:
        dict: Aggregated statistics
    """
    return {
        'total_predictions': len(df_predictions),
        'mean_sales': df_predictions['predicted_sales'].mean(),
        'median_sales': df_predictions['predicted_sales'].median(),
        'min_sales': df_predictions['predicted_sales'].min(),
        'max_sales': df_predictions['predicted_sales'].max(),
        'std_sales': df_predictions['predicted_sales'].std(),
        'total_sales': df_predictions['predicted_sales'].sum(),
        'unique_stores': df_predictions['store'].nunique(),
        'unique_dates': df_predictions['date'].nunique(),
    }
