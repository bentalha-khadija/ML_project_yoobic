"""
Module pour effectuer les prédictions
"""

import pandas as pd
import numpy as np
import lightgbm as lgb
from utils.preprocessing import create_features, get_feature_columns, load_historical_stats
from utils.model_loader import load_cluster_models


# Charger le mapping store -> cluster (depuis le fichier de clustering)
def load_store_clusters(cluster_features_path='data/cluster_features.pkl'):
    """
    Charge le mapping store -> cluster depuis le fichier de clustering
    
    Returns:
        dict: {store_id: cluster_id}
    """
    try:
        cluster_features = pd.read_pickle(cluster_features_path)
        store_cluster_map = cluster_features.set_index('store')['cluster'].to_dict()
        print(f"✓ Mapping store->cluster chargé pour {len(store_cluster_map)} stores")
        return store_cluster_map
    except Exception as e:
        print(f"⚠️  Erreur lors du chargement du mapping: {e}")
        # Mapping par défaut si fichier introuvable
        return {i: i % 4 for i in range(1, 46)}  # 45 stores répartis sur 4 clusters


def predict_sales(df_input):
    """
    Effectue les prédictions sur le DataFrame d'entrée
    
    Args:
        df_input: DataFrame avec colonnes [store, date, temperature, fuel_Price, 
                  cpi, unemployment, holiday_flag]
    
    Returns:
        DataFrame avec colonnes [store, date, predicted_sales, cluster]
    """
    
    # 1. Charger les statistiques historiques pour imputation
    historical_stats = load_historical_stats()
    
    # 2. Supprimer weekly_sales si elle existe (forcer l'imputation pour prédiction)
    df_for_prediction = df_input.copy()
    if 'weekly_sales' in df_for_prediction.columns:
        print("ℹ️  Colonne 'weekly_sales' détectée - Elle sera ignorée pour la prédiction")
        print("    Les lags seront imputés avec les statistiques historiques")
        df_for_prediction = df_for_prediction.drop(columns=['weekly_sales'])
    
    # 3. Appliquer le feature engineering
    print("\n📊 Feature engineering...")
    df_features = create_features(df_for_prediction, historical_stats)
    
    if df_features.empty:
        raise ValueError("Aucune donnée disponible après le feature engineering")
    
    # 3. Charger le mapping store -> cluster
    store_cluster_map = load_store_clusters()
    df_features['cluster'] = df_features['store'].map(store_cluster_map)
    
    # Vérifier que tous les stores ont un cluster
    missing_clusters = df_features['cluster'].isna().sum()
    if missing_clusters > 0:
        print(f"⚠️  {missing_clusters} stores sans cluster assigné - utilisation du cluster 0")
        df_features['cluster'] = df_features['cluster'].fillna(0).astype(int)
    
    # 4. Essayer de charger les modèles par cluster, sinon utiliser un modèle global
    print("\n🤖 Chargement du modèle...")
    feature_cols = get_feature_columns()
    
    try:
        # Tenter de charger les modèles de cluster individuels
        cluster_models = load_cluster_models()
        use_cluster_models = True
        print(f"✓ {len(cluster_models)} modèles de cluster chargés")
    except FileNotFoundError:
        # Utiliser un modèle global unique
        print("⚠️  Modèles de cluster non trouvés, entraînement d'un modèle global...")
        use_cluster_models = False
        
        # Charger les données d'entraînement
        try:
            train_data = pd.read_pickle('data/train.pkl')
            print(f"✓ Données d'entraînement chargées: {len(train_data)} lignes")
            
            # Entraîner un modèle LightGBM global
            model = lgb.LGBMRegressor(n_estimators=100, random_state=42, verbose=-1)
            model.fit(train_data[feature_cols], train_data['weekly_sales'])
            print("✓ Modèle global entraîné")
        except Exception as e:
            raise ValueError(f"Impossible de charger les données d'entraînement: {e}")
    
    # 5. Prédire
    print("\n🎯 Prédiction...")
    
    if use_cluster_models:
        # Prédire avec les modèles par cluster
        predictions = []
        
        for cluster_id in sorted(df_features['cluster'].unique()):
            df_cluster = df_features[df_features['cluster'] == cluster_id].copy()
            
            if cluster_id not in cluster_models:
                print(f"⚠️  Modèle pour cluster {cluster_id} introuvable - skip")
                continue
            
            cluster_model = cluster_models[cluster_id]
            y_pred = cluster_model.predict(df_cluster[feature_cols])
            
            df_cluster['predicted_sales'] = y_pred
            predictions.append(df_cluster[['store', 'date', 'predicted_sales', 'cluster']])
            print(f"  Cluster {cluster_id}: {len(df_cluster)} prédictions")
        
        df_predictions = pd.concat(predictions).reset_index(drop=True)
    else:
        # Prédire avec le modèle global
        y_pred = model.predict(df_features[feature_cols])
        df_features['predicted_sales'] = y_pred
        df_predictions = df_features[['store', 'date', 'predicted_sales', 'cluster']].copy()
        print(f"  {len(df_predictions)} prédictions avec modèle global")
    
    print(f"\n✓ {len(df_predictions)} prédictions générées avec succès")
    
    return df_predictions


def get_summary_stats(df_predictions):
    """
    Calcule des statistiques descriptives sur les prédictions
    
    Returns:
        dict: Statistiques agrégées
    """
    return {
        'total_predictions': len(df_predictions),
        'mean_sales': df_predictions['predicted_sales'].mean(),
        'median_sales': df_predictions['predicted_sales'].median(),
        'min_sales': df_predictions['predicted_sales'].min(),
        'max_sales': df_predictions['predicted_sales'].max(),
        'total_sales': df_predictions['predicted_sales'].sum(),
        'unique_stores': df_predictions['store'].nunique(),
        'unique_dates': df_predictions['date'].nunique(),
    }
