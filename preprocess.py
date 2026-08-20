"""
Data Preprocessing Layer
- Load raw CSV
- Handle missing values
- Convert dates
- Remove outliers
- Sort chronologically
"""

import pandas as pd
import numpy as np
import os


def load_data(filepath: str) -> pd.DataFrame:
    """Load CSV dataset."""
    df = pd.read_csv(filepath)
    print(f"[Preprocess] Loaded {len(df)} rows, {df.shape[1]} columns")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill or drop missing values."""
    # Forward fill for time-series continuity
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].ffill().bfill()
    df.dropna(inplace=True)
    print(f"[Preprocess] After missing value handling: {len(df)} rows")
    return df


def convert_dates(df: pd.DataFrame, date_col: str = "Date") -> pd.DataFrame:
    """Convert date column to datetime and extract features."""
    df[date_col] = pd.to_datetime(df[date_col])
    df["Year"]  = df[date_col].dt.year
    df["Month"] = df[date_col].dt.month
    df["Day"]   = df[date_col].dt.day
    df["DayOfWeek"] = df[date_col].dt.dayofweek
    df["Season"] = df["Month"].apply(lambda m:
        0 if m in [12, 1, 2] else   # Winter
        1 if m in [3, 4, 5]  else   # Spring
        2 if m in [6, 7, 8]  else   # Monsoon
        3                            # Autumn
    )
    print("[Preprocess] Dates converted and features extracted")
    return df


def remove_outliers(df: pd.DataFrame, col: str = "AQI", z_thresh: float = 3.5) -> pd.DataFrame:
    """Remove statistical outliers using Z-score."""
    z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
    before = len(df)
    df = df[z_scores < z_thresh]
    print(f"[Preprocess] Removed {before - len(df)} outliers from '{col}'")
    return df


def sort_by_time(df: pd.DataFrame, date_col: str = "Date", city_col: str = "City") -> pd.DataFrame:
    """Sort data by city and date."""
    df = df.sort_values([city_col, date_col]).reset_index(drop=True)
    print("[Preprocess] Data sorted chronologically per city")
    return df


def preprocess_pipeline(filepath: str, city: str = None) -> pd.DataFrame:
    """Full preprocessing pipeline."""
    df = load_data(filepath)
    df = handle_missing_values(df)
    df = convert_dates(df)
    df = remove_outliers(df)
    df = sort_by_time(df)
    
    if city:
        df = df[df["City"] == city].reset_index(drop=True)
        print(f"[Preprocess] Filtered to city: {city} ({len(df)} rows)")
    
    return df


if __name__ == "__main__":
    df = preprocess_pipeline("data/raw/aqi_data.csv", city="Kolkata")
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/aqi_kolkata_clean.csv", index=False)
    print(df.head())
