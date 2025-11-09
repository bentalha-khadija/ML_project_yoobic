# 📊 ML Project Yoobic - Store Sales Prediction

Web application for store sales prediction using Machine Learning with a modern interactive interface.

## 🎯 Objective

Predict store sales using LightGBM models with clustering and an interactive Dash web interface.

## 🛠️ Technologies

- **Machine Learning**: LightGBM, Scikit-learn, Prophet
- **Web App**: Dash, Flask, Plotly
- **UI**: Dash Mantine Components
- **Data**: Pandas, NumPy

## 📁 Project Structure

```
ML_project_yoobic/
├── app/                    # Dash web application
│   ├── callbacks/          # Callback logic
│   ├── components/         # UI components
│   ├── layouts/            # Interface layouts
│   └── main.py            # Entry point
├── data/                   # CSV data
├── models/                 # Trained ML models
├── notebooks/              # Jupyter notebooks
├── utils/                  # Utilities (preprocessing, predictions)
└── requirements.txt        # Dependencies
```

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/bentalha-khadija/ML_project_yoobic.git
cd ML_project_yoobic

# Install dependencies
pip install -r requirements.txt
```

## 🏃 Usage

### 1. Prepare the models

Run the notebook to train the models:
```bash
jupyter notebook notebooks/data_modeling.ipynb
```

### 2. Check the models

```bash
python prepare_model.py
```

### 3. Launch the application

```bash
python app/main.py
```

The application will be accessible at: **http://127.0.0.1:8050**

## 📈 Features

- 📤 CSV data upload and visualization
- 📊 Exploratory sales analysis
- 🤖 ML predictions with LightGBM models
- 📉 Interactive visualizations with Plotly
- 🎨 Modern interface with light/dark theme

## 📊 Model

- **Approach**: Clustering + LightGBM per cluster
- **Features**: Date, Store, Time variables
- **Metrics**: RMSE, MAE

## 👤 Author

Khadija Bentalha

## 📝 License

This project is for educational and professional use.
