"""
Module pour charger le modèle optimal et les modèles par cluster
"""

import joblib
import os


def load_optimal_model(model_path='models/best_sales_model.pkl'):
    """
    Charge le modèle optimal sauvegardé
    
    Returns:
        dict: Contient le modèle et ses métadonnées
              {
                  'approche': 'Clustering',
                  'modele': 'LightGBM', 
                  'rmse': 63519.94,
                  'mae': 42650.00,
                  'mape': 4.24,
                  'predictions': DataFrame,
                  'comparison_table': DataFrame
              }
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Modèle introuvable à {model_path}. "
            "Exécutez d'abord le notebook 06_Comparison_Final.ipynb pour générer le modèle."
        )
    
    model_info = joblib.load(model_path)
    print(f"✓ Modèle optimal chargé: {model_info['approche']} + {model_info['modele']}")
    print(f"  RMSE: {model_info['rmse']:.2f}")
    
    return model_info


def load_cluster_models(models_dir='models'):
    """
    Charge tous les modèles LightGBM par cluster
    
    Returns:
        dict: {cluster_id: model}
    """
    cluster_models = {}
    
    # Chercher les fichiers lgb_cluster_*.pkl
    for filename in os.listdir(models_dir):
        if filename.startswith('lgb_cluster_') and filename.endswith('.pkl'):
            cluster_id = int(filename.replace('lgb_cluster_', '').replace('.pkl', ''))
            model_path = os.path.join(models_dir, filename)
            cluster_models[cluster_id] = joblib.load(model_path)
    
    if not cluster_models:
        raise FileNotFoundError(
            f"Aucun modèle de cluster trouvé dans {models_dir}. "
            "Exécutez d'abord le notebook 03_Modeling_Clustering.ipynb."
        )
    
    print(f"✓ {len(cluster_models)} modèles de cluster chargés")
    return cluster_models


def get_model_metadata():
    """
    Retourne les métadonnées du modèle optimal pour affichage
    """
    return {
        'approach': 'Clustering',
        'model_type': 'LightGBM',
        'rmse': 63519.94,
        'mae': 42650.00,
        'mape': 4.24,
        'description': 'Un modèle LightGBM par cluster de magasins (k=4)',
        'features': [
            'Lags: 1, 2, 4, 52 semaines',
            'Rolling features: moyennes et std',
            'Encodage cyclique: semaine, mois',
            'Variables exogènes: température, carburant, CPI, chômage'
        ]
    }
