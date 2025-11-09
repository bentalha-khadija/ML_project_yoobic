"""
Script pour vérifier que tous les modèles nécessaires sont présents pour l'application web
"""

import os

print("="*80)
print("🔧 VÉRIFICATION DES MODÈLES POUR L'APPLICATION WEB")
print("="*80)

# Vérifier les fichiers nécessaires
required_files = {
    'data/train.pkl': 'Dataset d\'entraînement (pour stats historiques)',
    'data/cluster_features.pkl': 'Mapping store->cluster',
    'models/lgb_cluster_0.pkl': 'Modèle LightGBM cluster 0',
    'models/lgb_cluster_1.pkl': 'Modèle LightGBM cluster 1',
    'models/lgb_cluster_2.pkl': 'Modèle LightGBM cluster 2',
    'models/lgb_cluster_3.pkl': 'Modèle LightGBM cluster 3',
}

print("\n📋 Vérification des fichiers requis:")
missing = []
for file_path, description in required_files.items():
    if os.path.exists(file_path):
        print(f"  ✓ {file_path} - {description}")
    else:
        print(f"  ❌ {file_path} - {description}")
        missing.append(file_path)

if missing:
    print(f"\n⚠️  ATTENTION: {len(missing)} fichier(s) manquant(s)")
    print("   L'application ne pourra pas fonctionner correctement.")
    print("   Exécutez le notebook notebooks/data_modeling.ipynb pour générer ces fichiers.")
    exit(1)
else:
    print("\n✅ Tous les fichiers nécessaires sont présents!")

print("\n" + "="*80)
print("✅ VÉRIFICATION TERMINÉE")
print("="*80)
print("\n🚀 Vous pouvez maintenant lancer l'application:")
print("   python app/main.py")
print("\n📍 L'application sera accessible à: http://127.0.0.1:8050")
print("="*80)
