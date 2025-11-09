"""
Module de preprocessing pour les prédictions
Applique le même feature engineering que dans les notebooks
"""

import pandas as pd
import numpy as np
import logging
import warnings
warnings.filterwarnings('ignore')

# Configuration du logger
logger = logging.getLogger(__name__)


def validate_csv_structure(df):
    """
    Validation complète et rigoureuse du CSV uploadé
    Vérifie: colonnes, types, plages de valeurs, dates, valeurs nulles
    
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    errors = []
    
    # 1. Vérification des colonnes requises
    required_cols = ['store', 'date', 'holiday_flag', 'temperature', 
                     'fuel_Price', 'cpi', 'unemployment']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        errors.append(f"Colonnes manquantes: {', '.join(missing_cols)}")
        return False, " | ".join(errors)  # Arrêt immédiat si colonnes manquantes
    
    # 2. Vérification des valeurs nulles
    null_cols = df[required_cols].columns[df[required_cols].isnull().any()].tolist()
    if null_cols:
        null_counts = {col: df[col].isnull().sum() for col in null_cols}
        errors.append(f"Valeurs nulles détectées: {null_counts}")
    
    # 3. Validation de 'store' (numérique et dans [1, 45])
    try:
        stores = pd.to_numeric(df['store'], errors='raise')
        invalid_stores = stores[(stores < 1) | (stores > 45) | (stores != stores.astype(int))]
        if len(invalid_stores) > 0:
            unique_invalid = invalid_stores.unique()[:5]  # Limiter affichage
            errors.append(f"'store' doit être un entier entre 1 et 45. Exemples invalides: {unique_invalid.tolist()}")
    except (ValueError, TypeError):
        errors.append("'store' doit contenir uniquement des nombres")
    
    # 4. Validation de 'holiday_flag' (0 ou 1)
    try:
        holiday = pd.to_numeric(df['holiday_flag'], errors='raise')
        if not holiday.isin([0, 1]).all():
            invalid_vals = holiday[~holiday.isin([0, 1])].unique()[:5]
            errors.append(f"'holiday_flag' doit être 0 ou 1. Valeurs invalides trouvées: {invalid_vals.tolist()}")
    except (ValueError, TypeError):
        errors.append("'holiday_flag' doit contenir uniquement 0 ou 1")
    
    # 5. Validation des dates
    try:
        dates = pd.to_datetime(df['date'], dayfirst=True, errors='raise')
        # Vérifier que les dates ne sont pas absurdes
        if (dates.dt.year < 2000).any() or (dates.dt.year > 2050).any():
            errors.append("Certaines dates sont hors de la plage réaliste (2000-2050)")
    except (ValueError, TypeError):
        errors.append("Format de date invalide. Utilisez YYYY-MM-DD ou DD/MM/YYYY")
    
    # 6. Validation des variables numériques (plages réalistes)
    if 'temperature' in df.columns:
        try:
            temp = pd.to_numeric(df['temperature'], errors='raise')
            if (temp < -50).any() or (temp > 150).any():
                errors.append("Température hors plage réaliste (-50°F à 150°F)")
        except (ValueError, TypeError):
            errors.append("'temperature' doit être numérique")
    
    if 'fuel_Price' in df.columns:
        try:
            fuel = pd.to_numeric(df['fuel_Price'], errors='raise')
            if (fuel < 0).any() or (fuel > 20).any():
                errors.append("'fuel_Price' doit être entre 0 et 20 $/gallon")
        except (ValueError, TypeError):
            errors.append("'fuel_Price' doit être numérique")
    
    if 'cpi' in df.columns:
        try:
            cpi = pd.to_numeric(df['cpi'], errors='raise')
            if (cpi < 100).any() or (cpi > 300).any():
                errors.append("'cpi' hors plage réaliste (100-300)")
        except (ValueError, TypeError):
            errors.append("'cpi' doit être numérique")
    
    if 'unemployment' in df.columns:
        try:
            unemp = pd.to_numeric(df['unemployment'], errors='raise')
            if (unemp < 0).any() or (unemp > 30).any():
                errors.append("'unemployment' doit être entre 0% et 30%")
        except (ValueError, TypeError):
            errors.append("'unemployment' doit être numérique")
    
    # 7. Retour du résultat
    if errors:
        return False, " | ".join(errors)
    
    return True, f"✅ Validation réussie ({len(df)} lignes, {df['store'].nunique()} stores)"


def check_temporal_continuity(df, max_gap_days=14):
    """
    Vérifie la continuité temporelle des séries par store
    Détecte les gaps (trous) dans les dates
    
    Args:
        df: DataFrame avec colonnes 'store' et 'date'
        max_gap_days: Nombre maximum de jours acceptable entre deux observations
    
    Returns:
        list: Liste des warnings (vide si tout est OK)
    """
    warnings_list = []
    df_temp = df.copy()
    df_temp['date'] = pd.to_datetime(df_temp['date'], dayfirst=True)
    
    for store in sorted(df_temp['store'].unique()):
        store_data = df_temp[df_temp['store'] == store].sort_values('date')
        
        if len(store_data) < 2:
            warnings_list.append(f"Store {store}: seulement {len(store_data)} observation(s)")
            continue
        
        # Calculer les différences entre dates consécutives
        date_diffs = store_data['date'].diff().dt.days
        
        # Identifier les gaps > max_gap_days
        gaps = date_diffs[date_diffs > max_gap_days]
        
        if len(gaps) > 0:
            max_gap = gaps.max()
            warnings_list.append(
                f"Store {store}: {len(gaps)} gap(s) détecté(s) (max: {int(max_gap)} jours)"
            )
    
    return warnings_list


def create_features(df, historical_stats=None):
    """
    Applique le feature engineering identique aux notebooks
    
    Args:
        df: DataFrame avec colonnes [store, date, temperature, fuel_Price, cpi, 
            unemployment, holiday_flag]
        historical_stats: Dict optionnel avec statistiques historiques pour imputer les lags
                         Format: {store_id: {'mean': ..., 'median': ..., 'std': ...}}
    
    Returns:
        DataFrame avec toutes les features nécessaires pour la prédiction
    """
    logger.info(f"Début feature engineering - {len(df)} lignes, {df['store'].nunique()} stores")
    
    df = df.copy()
    
    # Convertir date
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    df = df.sort_values(['store', 'date']).reset_index(drop=True)
    logger.info(f"Plage de dates: {df['date'].min()} à {df['date'].max()}")
    
    # Features temporelles de base
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    df['week'] = df['date'].dt.isocalendar().week
    
    # Encodage cyclique
    df['week_sin'] = np.sin(2 * np.pi * df['week'] / 52)
    df['week_cos'] = np.cos(2 * np.pi * df['week'] / 52)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    
    # =========================================================================
    # GESTION DES LAGS - CRITIQUE POUR LES NOUVELLES DONNÉES
    # =========================================================================
    
    # Option 1: Si weekly_sales existe dans le DataFrame (mode test avec données réelles)
    if 'weekly_sales' in df.columns:
        # Lags par store
        for lag in [1, 2, 4, 52]:
            df[f'lag_{lag}'] = df.groupby('store')['weekly_sales'].shift(lag)
        
        # Rolling features
        df['sales_lag1'] = df.groupby('store')['weekly_sales'].shift(1)
        for window in [4, 12, 26]:
            df[f'rolling_mean_{window}'] = df.groupby('store')['sales_lag1'].transform(
                lambda x: x.rolling(window, min_periods=1).mean()
            )
        df['rolling_std_4'] = df.groupby('store')['sales_lag1'].transform(
            lambda x: x.rolling(4, min_periods=1).std()
        )
    
    # Option 2: Pas de weekly_sales (vraies nouvelles données) - IMPUTER
    else:
        print("⚠️  Pas d'historique de ventes détecté. Imputation des lags...")
        
        if historical_stats is None:
            # Valeurs par défaut si pas de stats historiques
            print("⚠️  Utilisation de valeurs médianes globales pour les lags")
            # Ces valeurs doivent être calculées depuis le dataset d'entraînement
            default_mean = 15981.26  # Moyenne globale du train set
            default_std = 22711.18   # Écart-type global du train set
            
            # Imputer tous les lags avec la moyenne
            for lag in [1, 2, 4, 52]:
                df[f'lag_{lag}'] = default_mean
            
            df['sales_lag1'] = default_mean
            
            # Rolling features avec valeurs par défaut
            for window in [4, 12, 26]:
                df[f'rolling_mean_{window}'] = default_mean
            
            df['rolling_std_4'] = default_std
        
        else:
            # Imputer avec statistiques spécifiques par store
            print(f"✓ Imputation avec statistiques pour {len(historical_stats)} stores")
            
            for lag in [1, 2, 4, 52]:
                df[f'lag_{lag}'] = df['store'].map(
                    lambda s: historical_stats.get(s, {}).get('median', 15981.26)
                )
            
            df['sales_lag1'] = df['store'].map(
                lambda s: historical_stats.get(s, {}).get('median', 15981.26)
            )
            
            for window in [4, 12, 26]:
                df[f'rolling_mean_{window}'] = df['store'].map(
                    lambda s: historical_stats.get(s, {}).get('mean', 15981.26)
                )
            
            df['rolling_std_4'] = df['store'].map(
                lambda s: historical_stats.get(s, {}).get('std', 22711.18)
            )
    
    # Supprimer les NaN restants (si mode test avec weekly_sales)
    initial_len = len(df)
    df = df.dropna().reset_index(drop=True)
    dropped = initial_len - len(df)
    
    if dropped > 0:
        logger.warning(f"{dropped} lignes supprimées (NaN dans les lags)")
        print(f"ℹ️  {dropped} lignes supprimées (NaN dans les lags)")
    
    logger.info(f"Feature engineering terminé - Shape finale: {df.shape}")
    logger.info(f"Features créées: {len(get_feature_columns())} colonnes")
    
    return df


def get_feature_columns():
    """
    Retourne la liste exacte des colonnes de features dans l'ordre
    pour la prédiction avec LightGBM
    """
    return [
        'store', 'temperature', 'fuel_Price', 'cpi', 'unemployment', 'holiday_flag',
        'year', 'month', 'quarter', 'week',
        'lag_1', 'lag_2', 'lag_4', 'lag_52',
        'rolling_mean_4', 'rolling_mean_12', 'rolling_mean_26', 'rolling_std_4',
        'week_sin', 'week_cos', 'month_sin', 'month_cos'
    ]


def load_historical_stats(train_data_path='data/train.pkl'):
    """
    Charge les statistiques historiques depuis le dataset d'entraînement
    pour imputer les lags des nouvelles données
    
    Returns:
        dict: {store_id: {'mean': ..., 'median': ..., 'std': ...}}
    """
    try:
        import os
        if not os.path.exists(train_data_path):
            print(f"⚠️  Fichier {train_data_path} introuvable. Utilisation de valeurs par défaut.")
            return None
        
        train = pd.read_pickle(train_data_path)
        
        stats = {}
        for store in train['store'].unique():
            store_data = train[train['store'] == store]['weekly_sales']
            stats[store] = {
                'mean': store_data.mean(),
                'median': store_data.median(),
                'std': store_data.std()
            }
        
        print(f"✓ Statistiques historiques chargées pour {len(stats)} stores")
        return stats
    
    except Exception as e:
        print(f"⚠️  Erreur lors du chargement des stats historiques: {e}")
        return None
