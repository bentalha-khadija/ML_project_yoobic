"""
Script to verify that all necessary models are present for the web application
"""

import os

print("="*80)
print("MODEL VERIFICATION FOR WEB APPLICATION")
print("="*80)

# Check required files
required_files = {
    'data/train.pkl': 'Training dataset (for historical stats)',
    'data/cluster_features.pkl': 'Mapping store->cluster',
    'models/lgb_cluster_0.pkl': 'LightGBM model cluster 0',
    'models/lgb_cluster_1.pkl': 'LightGBM model cluster 1',
    'models/lgb_cluster_2.pkl': 'LightGBM model cluster 2',
    'models/lgb_cluster_3.pkl': 'LightGBM model cluster 3',
}

print("\nVerifying required files:")
missing = []
for file_path, description in required_files.items():
    if os.path.exists(file_path):
        print(f"  [OK] {file_path} - {description}")
    else:
        print(f"  [MISSING] {file_path} - {description}")
        missing.append(file_path)

if missing:
    print(f"\n[WARNING] {len(missing)} file(s) missing")
    print("   The application will not work correctly.")
    print("   Run the notebook notebooks/data_modeling.ipynb to generate these files.")
    exit(1)
else:
    print("\n[SUCCESS] All required files are present!")

print("\n" + "="*80)
print("VERIFICATION COMPLETED")
print("="*80)
print("\nYou can now launch the application:")
print("   python app/main.py")
print("\nThe application will be accessible at: http://127.0.0.1:8050")
print("="*80)
