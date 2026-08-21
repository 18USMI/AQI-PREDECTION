"""
Full Training Pipeline
Run: python train.py --city Kolkata
"""

import sys, os, argparse
import numpy as np
import pickle

sys.path.insert(0, "src")

from generate_data import generate_aqi_dataset
from preprocess import preprocess_pipeline
from feature_engineering import add_lag_features, add_rolling_features, scale_and_prepare, inverse_scale_aqi
from lstm_model import train_model, predict, TF_AVAILABLE
from evaluate import compute_metrics, plot_actual_vs_predicted


def run_training(city: str = "Kolkata"):
    print(f"\n{'='*60}")
    print(f"  AQI LSTM Prediction — Training Pipeline")
    print(f"  City: {city}")
    print(f"{'='*60}\n")

    # 1. Generate / load data
    raw_path = "data/raw/aqi_data.csv"
    if not os.path.exists(raw_path):
        print("[Pipeline] Generating synthetic dataset...")
        df_raw = generate_aqi_dataset()
        os.makedirs("data/raw", exist_ok=True)
        df_raw.to_csv(raw_path, index=False)

    # 2. Preprocess
    df = preprocess_pipeline(raw_path, city=city)

    # 3. Feature engineering
    df = add_lag_features(df)
    df = add_rolling_features(df)

    # 4. Scale & create sequences
    scaler_path = f"models/scaler_{city.lower()}.pkl"
    X_train, X_test, y_train, y_test, scaler, df_feat = scale_and_prepare(
        df, scaler_path=scaler_path
    )

    # 5. Train model
    result, model_type = train_model(X_train, y_train, X_test, y_test)
    model = result[0] if isinstance(result, tuple) else result

    # 6. Predict
    y_pred = predict(model, X_test, model_type)

    # 7. Inverse scale
    n_features = X_train.shape[2]
    y_test_inv = inverse_scale_aqi(scaler, y_test, n_features)
    y_pred_inv = inverse_scale_aqi(scaler, y_pred, n_features)

    # 8. Evaluate
    metrics = compute_metrics(y_test_inv, y_pred_inv)
    plot_actual_vs_predicted(
        y_test_inv, y_pred_inv,
        title=f"AQI Prediction — {city}",
        save_path=f"notebooks/actual_vs_predicted_{city.lower()}.png"
    )

    # Save metadata
    meta = {
        "city": city,
        "model_type": model_type,
        "metrics": metrics,
        "n_features": n_features,
        "feature_cols": df_feat.columns.tolist(),
        "time_steps": 7,
    }
    os.makedirs("models", exist_ok=True)
    with open(f"models/meta_{city.lower()}.pkl", "wb") as f:
        pickle.dump(meta, f)

    print(f"\n✅ Training complete for {city}!")
    print(f"   RMSE: {metrics['RMSE']}  MAE: {metrics['MAE']}  R²: {metrics['R2']}")
    return model, scaler, metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", default="Kolkata", help="City to train on")
    parser.add_argument("--all",  action="store_true", help="Train all cities")
    args = parser.parse_args()

    cities = ["Bihar", "Delhi", "Mumbai", "Chennai", "Bangalore","kolkata"]

    if args.all:
        for c in cities:
            run_training(c)
    else:
        run_training(args.city)
