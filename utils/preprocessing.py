"""
Preprocessing module for predictions
Applies the same feature engineering as in notebooks
"""

import pandas as pd
import numpy as np
import logging
import warnings
warnings.filterwarnings('ignore')

# Logger configuration
logger = logging.getLogger(__name__)


def validate_csv_structure(df):
    """
    Complete and rigorous validation of uploaded CSV
    Checks: columns, types, value ranges, dates, null values
    
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    errors = []
    
    # 1. Check required columns
    required_cols = ['store', 'date', 'holiday_flag', 'temperature', 
                     'fuel_Price', 'cpi', 'unemployment']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing columns: {', '.join(missing_cols)}")
        return False, " | ".join(errors)  # Stop immediately if columns missing
    
    # 2. Check null values
    null_cols = df[required_cols].columns[df[required_cols].isnull().any()].tolist()
    if null_cols:
        null_counts = {col: df[col].isnull().sum() for col in null_cols}
        errors.append(f"Null values detected: {null_counts}")
    
    # 3. Validate 'store' (numeric and in [1, 45])
    try:
        stores = pd.to_numeric(df['store'], errors='raise')
        invalid_stores = stores[(stores < 1) | (stores > 45) | (stores != stores.astype(int))]
        if len(invalid_stores) > 0:
            unique_invalid = invalid_stores.unique()[:5]  # Limit display
            errors.append(f"'store' must be an integer between 1 and 45. Invalid examples: {unique_invalid.tolist()}")
    except (ValueError, TypeError):
        errors.append("'store' must contain only numbers")
    
    # 4. Validate 'holiday_flag' (0 or 1)
    try:
        holiday = pd.to_numeric(df['holiday_flag'], errors='raise')
        if not holiday.isin([0, 1]).all():
            invalid_vals = holiday[~holiday.isin([0, 1])].unique()[:5]
            errors.append(f"'holiday_flag' must be 0 or 1. Invalid values found: {invalid_vals.tolist()}")
    except (ValueError, TypeError):
        errors.append("'holiday_flag' must contain only 0 or 1")
    
    # 5. Validate dates
    try:
        dates = pd.to_datetime(df['date'], dayfirst=True, errors='raise')
        # Check that dates are not absurd
        if (dates.dt.year < 2000).any() or (dates.dt.year > 2050).any():
            errors.append("Some dates are out of realistic range (2000-2050)")
    except (ValueError, TypeError):
        errors.append("Invalid date format. Use YYYY-MM-DD or DD/MM/YYYY")
    
    # 6. Validate numeric variables (realistic ranges)
    if 'temperature' in df.columns:
        try:
            temp = pd.to_numeric(df['temperature'], errors='raise')
            if (temp < -50).any() or (temp > 150).any():
                errors.append("Temperature out of realistic range (-50°F to 150°F)")
        except (ValueError, TypeError):
            errors.append("'temperature' must be numeric")
    
    if 'fuel_Price' in df.columns:
        try:
            fuel = pd.to_numeric(df['fuel_Price'], errors='raise')
            if (fuel < 0).any() or (fuel > 20).any():
                errors.append("'fuel_Price' must be between 0 and 20 $/gallon")
        except (ValueError, TypeError):
            errors.append("'fuel_Price' must be numeric")
    
    if 'cpi' in df.columns:
        try:
            cpi = pd.to_numeric(df['cpi'], errors='raise')
            if (cpi < 100).any() or (cpi > 300).any():
                errors.append("'cpi' out of realistic range (100-300)")
        except (ValueError, TypeError):
            errors.append("'cpi' must be numeric")
    
    if 'unemployment' in df.columns:
        try:
            unemp = pd.to_numeric(df['unemployment'], errors='raise')
            if (unemp < 0).any() or (unemp > 30).any():
                errors.append("'unemployment' must be between 0% and 30%")
        except (ValueError, TypeError):
            errors.append("'unemployment' must be numeric")
    
    # 7. Return result
    if errors:
        return False, " | ".join(errors)
    
    return True, f"Validation successful ({len(df)} rows, {df['store'].nunique()} stores)"


def check_temporal_continuity(df, max_gap_days=14):
    """
    Check temporal continuity of series by store
    Detects gaps in dates
    
    Args:
        df: DataFrame with columns 'store' and 'date'
        max_gap_days: Maximum number of days acceptable between two observations
    
    Returns:
        list: List of warnings (empty if all OK)
    """
    warnings_list = []
    df_temp = df.copy()
    df_temp['date'] = pd.to_datetime(df_temp['date'], dayfirst=True)
    
    for store in sorted(df_temp['store'].unique()):
        store_data = df_temp[df_temp['store'] == store].sort_values('date')
        
        if len(store_data) < 2:
            warnings_list.append(f"Store {store}: only {len(store_data)} observation(s)")
            continue
        
        # Calculate differences between consecutive dates
        date_diffs = store_data['date'].diff().dt.days
        
        # Identify gaps > max_gap_days
        gaps = date_diffs[date_diffs > max_gap_days]
        
        if len(gaps) > 0:
            max_gap = gaps.max()
            warnings_list.append(
                f"Store {store}: {len(gaps)} gap(s) detected (max: {int(max_gap)} days)"
            )
    
    return warnings_list


def create_features(df, historical_stats=None):
    """
    Apply feature engineering identical to notebooks
    
    Args:
        df: DataFrame with columns [store, date, temperature, fuel_Price, cpi, 
            unemployment, holiday_flag]
        historical_stats: Optional dict with historical statistics to impute lags
                         Format: {store_id: {'mean': ..., 'median': ..., 'std': ...}}
    
    Returns:
        DataFrame with all features needed for prediction
    """
    logger.info(f"Starting feature engineering - {len(df)} rows, {df['store'].nunique()} stores")
    
    df = df.copy()
    
    # Convert date
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    df = df.sort_values(['store', 'date']).reset_index(drop=True)
    logger.info(f"Date range: {df['date'].min()} to {df['date'].max()}")
    
    # Basic temporal features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    df['week'] = df['date'].dt.isocalendar().week
    
    # Cyclic encoding
    df['week_sin'] = np.sin(2 * np.pi * df['week'] / 52)
    df['week_cos'] = np.cos(2 * np.pi * df['week'] / 52)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    
    # =========================================================================
    # LAGS HANDLING - CRITICAL FOR NEW DATA
    # =========================================================================
    
    # Option 1: If weekly_sales exists in DataFrame (test mode with real data)
    if 'weekly_sales' in df.columns:
        # Lags by store
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
    
    # Option 2: No weekly_sales (real new data) - IMPUTE
    else:
        print("No sales history detected. Imputing lags...")
        
        if historical_stats is None:
            # Default values if no historical stats
            print("Using global median values for lags")
            # These values should be calculated from training dataset
            default_mean = 15981.26  # Global mean from train set
            default_std = 22711.18   # Global std from train set
            
            # Impute all lags with mean
            for lag in [1, 2, 4, 52]:
                df[f'lag_{lag}'] = default_mean
            
            df['sales_lag1'] = default_mean
            
            # Rolling features with default values
            for window in [4, 12, 26]:
                df[f'rolling_mean_{window}'] = default_mean
            
            df['rolling_std_4'] = default_std
        
        else:
            # Impute with store-specific statistics
            print(f"Imputation with statistics for {len(historical_stats)} stores")
            
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
    
    # Remove remaining NaN (if test mode with weekly_sales)
    initial_len = len(df)
    df = df.dropna().reset_index(drop=True)
    dropped = initial_len - len(df)
    
    if dropped > 0:
        logger.warning(f"{dropped} rows removed (NaN in lags)")
        print(f"{dropped} rows removed (NaN in lags)")
    
    logger.info(f"Feature engineering completed - Final shape: {df.shape}")
    logger.info(f"Features created: {len(get_feature_columns())} columns")
    
    return df


def get_feature_columns():
    """
    Return exact list of feature columns in order
    for prediction with LightGBM
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
    Load historical statistics from training dataset
    to impute lags for new data
    
    Returns:
        dict: {store_id: {'mean': ..., 'median': ..., 'std': ...}}
    """
    try:
        import os
        if not os.path.exists(train_data_path):
            print(f"File {train_data_path} not found. Using default values.")
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
        
        print(f"Historical statistics loaded for {len(stats)} stores")
        return stats
    
    except Exception as e:
        print(f"Error loading historical stats: {e}")
        return None
