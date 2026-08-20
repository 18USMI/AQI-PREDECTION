# 🌫️ AQI Intelligence System — LSTM-Based Air Quality Prediction

> Real-time Air Quality Index prediction using stacked Bidirectional LSTM deep learning, with a full-featured Streamlit dashboard.

---

## 🏗️ System Architecture

```
Data Sources → Ingestion → Preprocessing → Feature Engineering
    → MinMax Scaling → LSTM Model → Evaluation → Streamlit App
```

**Model:** Bidirectional LSTM (128) → Dropout → LSTM (64) → Dense(32) → Dense(1)  
**Input:** 7-day rolling window × 18 features  
**Output:** Next-day AQI prediction  

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit app
```bash
streamlit run app.py
```

### 3. Train model manually (optional)
```bash
python train.py --city Kolkata
python train.py --all          # Train all 5 cities
```

---

## 📂 Project Structure

```
AQI-LSTM-Prediction/
├── app.py                        # 🎯 Streamlit Dashboard
├── train.py                      # Training pipeline
├── requirements.txt
├── README.md
│
├── src/
│   ├── generate_data.py          # Synthetic data generator
│   ├── preprocess.py             # Data cleaning & preprocessing
│   ├── feature_engineering.py   # Lag/rolling features + 3D sequences
│   ├── lstm_model.py             # LSTM + sklearn fallback model
│   └── evaluate.py              # Metrics + visualization
│
├── data/
│   ├── raw/                      # Raw CSV files
│   └── processed/               # Cleaned datasets
│
├── models/
│   ├── lstm_model_*.h5          # Trained Keras models
│   ├── sklearn_model_*.pkl      # Fallback GB models
│   ├── scaler_*.pkl             # Feature scalers
│   └── meta_*.pkl               # Training metadata
│
└── notebooks/
    ├── eda.ipynb                 # Exploratory Data Analysis
    ├── training.ipynb           # Model training notebook
    └── *.png                    # Evaluation plots
```

---

## 📊 Features

| Feature | Description |
|---|---|
| **Real-time Prediction** | Input 7 AQI values → get tomorrow's forecast |
| **7-Day Forecast** | Iterative multi-step prediction |
| **City Comparison** | Compare Kolkata, Delhi, Mumbai, Chennai, Bangalore |
| **Pollutant Tracking** | PM2.5, PM10, NO2, SO2, CO, O3 |
| **Health Recommendations** | Color-coded AQI categories + personalized advice |
| **Feature Importance** | Which pollutants drive AQI the most |
| **Correlation Analysis** | Cross-feature correlation matrix |

---

## 🏷️ AQI Categories

| AQI Range | Category | Action |
|---|---|---|
| 0–50 | ✅ Good | Safe for all |
| 51–100 | 🟡 Moderate | Sensitive groups take caution |
| 101–150 | 🟠 Unhealthy-SG | Reduce outdoor exertion |
| 151–200 | 🔴 Unhealthy | Wear N95 mask |
| 201–300 | 🟣 Very Unhealthy | Stay indoors |
| 301+ | ☣️ Hazardous | Emergency conditions |

---

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| Deep Learning | TensorFlow / Keras |
| ML Fallback | Scikit-learn GradientBoosting |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Web App | Streamlit |
| Deployment | Streamlit Cloud / Render |

---

## 📡 Using Real Data

Replace `data/raw/aqi_data.csv` with data from:
- [CPCB](https://cpcb.nic.in/) — Central Pollution Control Board India
- [Kaggle AQI Dataset](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india)
- [OpenWeatherMap API](https://openweathermap.org/api/air-pollution)

Ensure the CSV has these columns:
```
Date, City, AQI, PM2.5, PM10, NO2, SO2, CO, O3, Temperature, Humidity, WindSpeed
```

---

## 👨‍💻 Author

Built as a Deep Learning project using LSTM for time-series AQI forecasting.
