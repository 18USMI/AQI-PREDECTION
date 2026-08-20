import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

def generate_aqi_dataset(n_days=1000, seed=42):
    np.random.seed(seed)
    cities = ["Kolkata", "Delhi", "Mumbai", "Chennai", "Bangalore"]
    records = []
    for city in cities:
        base = {"Kolkata":120,"Delhi":200,"Mumbai":100,"Chennai":80,"Bangalore":90}[city]
        t = np.arange(n_days)
        aqi = np.clip(base + 50*np.sin(2*np.pi*t/365+np.pi) + 0.02*t + np.random.normal(0,15,n_days), 10, 500)
        for i in range(n_days):
            d = datetime(2020,1,1) + timedelta(days=i)
            records.append({
                "Date": d.strftime("%Y-%m-%d"), "City": city,
                "AQI": round(float(aqi[i]),2),
                "PM2.5": round(float(max(0, aqi[i]*0.4+np.random.normal(0,5))),2),
                "PM10":  round(float(max(0, aqi[i]*0.6+np.random.normal(0,8))),2),
                "NO2":   round(float(max(0, aqi[i]*0.15+np.random.normal(0,3))),2),
                "SO2":   round(float(max(0, aqi[i]*0.08+np.random.normal(0,2))),2),
                "CO":    round(float(max(0, aqi[i]*0.05+np.random.normal(0,1))),2),
                "O3":    round(float(max(0, aqi[i]*0.12+np.random.normal(0,4))),2),
                "Temperature": round(float(25+10*np.sin(2*np.pi*i/365)+np.random.normal(0,3)),2),
                "Humidity":    round(float(min(100,max(0,60+20*np.sin(2*np.pi*i/365)+np.random.normal(0,5)))),2),
                "WindSpeed":   round(float(abs(np.random.normal(8,3))),2)
            })
    return pd.DataFrame(records)

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    df = generate_aqi_dataset()
    df.to_csv("data/raw/aqi_data.csv", index=False)
    print(f"Generated {len(df)} records")