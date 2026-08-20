import sys, os, pickle
import numpy as np

# Fix path automatically — no need to set PYTHONPATH manually
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from preprocess import preprocess_pipeline
from feature_engineering import add_lag_features, add_rolling_features, scale_and_prepare, inverse_scale_aqi
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

cities = ["Kolkata", "Delhi", "Mumbai", "Chennai", "Bangalore"]

print("\n" + "="*55)
print("  AQI MODEL ACCURACY REPORT")
print("="*55)
print(f"{'City':<12} {'RMSE':>8} {'MAE':>8} {'R2':>8}")
print("-"*55)

for city in cities:
    try:
        df = preprocess_pipeline("data/raw/aqi_data.csv", city=city)
        df = add_lag_features(df)
        df = add_rolling_features(df)

        scaler_path = f"models/scaler_{city.lower()}.pkl"
        X_train, X_test, y_train, y_test, scaler, df_feat = scale_and_prepare(
            df, scaler_path=scaler_path, fit_scaler=False
        )

        model_path = f"models/sklearn_model_{city.lower()}.pkl"
        with open(model_path, "rb") as f:
            model = pickle.load(f)

        X_2d = X_test.reshape(X_test.shape[0], -1)
        y_pred = model.predict(X_2d)

        n_feat = X_test.shape[2]
        y_true_inv = inverse_scale_aqi(scaler, y_test, n_feat)
        y_pred_inv = inverse_scale_aqi(scaler, y_pred, n_feat)

        rmse = np.sqrt(mean_squared_error(y_true_inv, y_pred_inv))
        mae  = mean_absolute_error(y_true_inv, y_pred_inv)
        r2   = r2_score(y_true_inv, y_pred_inv)

        print(f"{city:<12} {rmse:>8.2f} {mae:>8.2f} {r2:>8.3f}")

    except FileNotFoundError:
        print(f"{city:<12}   Model not found — run: python train.py --city {city}")
    except Exception as e:
        print(f"{city:<12}   Error: {e}")

print("="*55)
print("RMSE & MAE = lower is better | R2 = closer to 1 is better")
print("="*55)