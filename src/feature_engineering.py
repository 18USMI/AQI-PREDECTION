import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle
import os

def add_lag_features(df, col="AQI", lags=3):
    for lag in range(1, lags+1):
        df[f"{col}_lag{lag}"] = df[col].shift(lag)
    return df

def add_rolling_features(df, col="AQI"):
    df[f"{col}_roll7"]  = df[col].rolling(7,  min_periods=1).mean()
    df[f"{col}_roll14"] = df[col].rolling(14, min_periods=1).mean()
    return df

def create_sequences(data, ts=7):
    X, y = [], []
    for i in range(len(data)-ts):
        X.append(data[i:i+ts, :])
        y.append(data[i+ts, 0])
    return np.array(X), np.array(y)

def scale_and_prepare(df, time_steps=7, scaler_path="models/scaler.pkl", fit_scaler=True):
    cols = ["AQI","PM2.5","PM10","NO2","SO2","CO","O3",
            "Temperature","Humidity","WindSpeed",
            "Month","Season","DayOfWeek",
            "AQI_lag1","AQI_lag2","AQI_lag3",
            "AQI_roll7","AQI_roll14"]
    avail = [c for c in cols if c in df.columns]
    df2 = df[avail].dropna()
    data = df2.values
    if fit_scaler:
        sc = MinMaxScaler()
        ds = sc.fit_transform(data)
        os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
        pickle.dump(sc, open(scaler_path, "wb"))
    else:
        sc = pickle.load(open(scaler_path, "rb"))
        ds = sc.transform(data)
    X, y = create_sequences(ds, time_steps)
    sp = int(len(X)*0.8)
    print(f"X_train:{X[:sp].shape} X_test:{X[sp:].shape}")
    return X[:sp], X[sp:], y[:sp], y[sp:], sc, df2

def inverse_scale_aqi(sc, preds, n):
    dummy = np.zeros((len(preds), n))
    dummy[:,0] = preds
    return sc.inverse_transform(dummy)[:,0]