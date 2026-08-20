import pandas as pd
import numpy as np

def load_data(fp):
    df = pd.read_csv(fp)
    print(f"Loaded {len(df)} rows")
    return df

def handle_missing_values(df):
    nc = df.select_dtypes(include=[np.number]).columns
    df[nc] = df[nc].ffill().bfill()
    df.dropna(inplace=True)
    return df

def convert_dates(df, date_col="Date"):
    df[date_col] = pd.to_datetime(df[date_col])
    df["Month"] = df[date_col].dt.month
    df["Day"] = df[date_col].dt.day
    df["DayOfWeek"] = df[date_col].dt.dayofweek
    df["Season"] = df["Month"].apply(lambda m: 0 if m in [12,1,2] else 1 if m in [3,4,5] else 2 if m in [6,7,8] else 3)
    return df

def remove_outliers(df, col="AQI", z=3.5):
    zs = np.abs((df[col]-df[col].mean())/df[col].std())
    return df[zs < z].copy()

def sort_by_time(df):
    return df.sort_values(["City","Date"]).reset_index(drop=True)

def preprocess_pipeline(fp, city=None):
    df = load_data(fp)
    df = handle_missing_values(df)
    df = convert_dates(df)
    df = remove_outliers(df)
    df = sort_by_time(df)
    if city:
        df = df[df["City"]==city].reset_index(drop=True)
        print(f"Filtered to {city}: {len(df)} rows")
    return df