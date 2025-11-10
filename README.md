# 🛒 Store Sales Prediction App

A web app that predicts weekly sales for retail stores using machine learning. Upload your data, get predictions, and visualize results.

Please see the Demo folder, it contains a video demonstrating the app.

---

## What Does It Do?

This app helps you predict how much each store will sell in the coming weeks. upload a CSV file with store data, and you'll get:
- Sales predictions for all your stores
- Interactive charts to explore trends
- A downloadable table with all the results

---

## The Magic Behind It

Instead of using one model for all stores, we did the following :

1. **Group similar stores together** (using K-Means clustering)
2. **Train a separate model for each group** (using LightGBM)


**Result:** RMSE of 63,519 

---

## Quick Start

### 1. Install

```bash
# Clone the repo
git clone https://github.com/yourusername/ML_project_yoobic.git
cd ML_project_yoobic

# Create a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install packages
pip install -r requirements.txt
```

### 2. Check Everything's Ready

```bash
python prepare_model.py
```

You should see `All required files are present!`

### 3. Run It

```bash
python -m app.main
```

Open your browser at **http://127.0.0.1:8050** 

---

## How to Use

1. **Upload Data** : Go to the home page and upload your CSV file
2. **View Predictions** : Check the "Data Table" page for results
3. **Explore Charts** : Head to "Visualizations" to see trends
4. **Download** : Export predictions as CSV when you're done

---

## Project Structure

```
ML_project_yoobic/
├── app/                    # The web application
│   ├── main.py            # Start here
│   ├── pages/             # Different pages (home, predictions, etc.)
│   ├── callbacks/         # What happens when you click stuff
│   └── components/        # UI pieces (tables, charts, upload)
│
├── data/                   # Training data and store info
├── models/                 # The 4 trained models (one per cluster)
├── utils/                  # Helper functions (predictions, preprocessing)
├── logs/                   # App logs (for debugging)
│
└── prepare_model.py       # Check if everything's installed correctly
```

---

## Tech Stack

- **Python 3.10** - The brains
- **Dash** - Makes the web interface
- **LightGBM** - The ML model (fast and accurate)
- **Plotly** - Interactive charts
- **Pandas** - Data handling


---

## Questions?

The code is commented, the logs are detailed, and the UI is intuitive. If you're stuck:
1. Check the logs in `logs/`
2. Look at the notebooks in `notebooks/` for modeling details
3. Read the code comments


```bash
python -m app.main
```
