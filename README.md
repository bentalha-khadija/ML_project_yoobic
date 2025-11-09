# 📊 ML Project Yoobic - Store Sales Prediction

Application web de prédiction des ventes de magasins utilisant Machine Learning et une interface interactive moderne.

## 🎯 Objectif

Prédire les ventes de magasins en utilisant des modèles LightGBM avec clustering et une interface web interactive Dash.

## 🛠️ Technologies

- **Machine Learning**: LightGBM, Scikit-learn, Prophet
- **Web App**: Dash, Flask, Plotly
- **UI**: Dash Mantine Components
- **Data**: Pandas, NumPy

## 📁 Structure du Projet

```
ML_project_yoobic/
├── app/                    # Application web Dash
│   ├── callbacks/          # Logique des callbacks
│   ├── components/         # Composants UI
│   ├── layouts/            # Layouts de l'interface
│   └── main.py            # Point d'entrée
├── data/                   # Données CSV
├── models/                 # Modèles ML entraînés
├── notebooks/              # Notebooks Jupyter
├── utils/                  # Utilitaires (preprocessing, prédictions)
└── requirements.txt        # Dépendances
```

## 🚀 Installation

```bash
# Cloner le dépôt
git clone https://github.com/bentalha-khadija/ML_project_yoobic.git
cd ML_project_yoobic

# Installer les dépendances
pip install -r requirements.txt
```

## 🏃 Utilisation

### 1. Préparer les modèles

Exécutez le notebook pour entraîner les modèles :
```bash
jupyter notebook notebooks/data_modeling.ipynb
```

### 2. Vérifier les modèles

```bash
python prepare_model.py
```

### 3. Lancer l'application

```bash
python app/main.py
```

L'application sera accessible à : **http://127.0.0.1:8050**

## 📈 Fonctionnalités

- 📤 Upload et visualisation de données CSV
- 📊 Analyse exploratoire des ventes
- 🤖 Prédictions ML avec modèles LightGBM
- 📉 Visualisations interactives avec Plotly
- 🎨 Interface moderne avec thème clair/sombre

## 📊 Modèle

- **Approche**: Clustering + LightGBM par cluster
- **Features**: Date, Store, Variables temporelles
- **Métriques**: RMSE, MAE

## 👤 Auteur

Khadija Bentalha

## 📝 Licence

Ce projet est à usage éducatif et professionnel.
