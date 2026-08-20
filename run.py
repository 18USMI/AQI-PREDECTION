import sys, os, pickle
import numpy as np
sys.path.insert(0, 'src')

from generate_data import generate_aqi_dataset
from preprocess import preprocess_pipeline
from feature_engineering import add_lag_features, add_rolling_features, scale_and_prepare, inverse_scale_aqi
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

os.makedirs('data/raw', exist_ok=True)
os.makedirs('models', exist_ok=True)

print("Generating data...")
df = generate_aqi_dataset()
df.to_csv('data/raw/aqi_data.csv', index=False)
print("Done!\n")

cities = ['Kolkata', 'Delhi', 'Mumbai', 'Chennai', 'Bangalore']
print("=" * 52)
print("   AQI MODEL ACCURACY REPORT")
print("=" * 52)
print(f"{'City':<12} {'RMSE':>8} {'MAE':>8} {'R2':>8}")
print("-" * 52)

for city in cities:
    df2 = preprocess_pipeline('data/raw/aqi_data.csv', city=city)
    df2 = add_lag_features(df2)
    df2 = add_rolling_features(df2)
    sp = f'models/scaler_{city.lower()}.pkl'
    X_train, X_test, y_train, y_test, scaler, df_feat = scale_and_prepare(df2, scaler_path=sp)
    model = GradientBoostingRegressor(n_estimators=200, learning_rate=0.07,
                                       max_depth=5, subsample=0.85,
                                       random_state=42, verbose=0)
    model.fit(X_train.reshape(X_train.shape[0], -1), y_train)
    pickle.dump(model, open(f'models/sklearn_model_{city.lower()}.pkl', 'wb'))
    meta = {'city':city, 'model_type':'GBM', 'n_features':X_test.shape[2],
            'time_steps':7, 'feature_cols':df_feat.columns.tolist(), 'metrics':{}}
    y_pred = model.predict(X_test.reshape(X_test.shape[0], -1))
    n = X_test.shape[2]
    yt = inverse_scale_aqi(scaler, y_test, n)
    yp = inverse_scale_aqi(scaler, y_pred, n)
    rmse = np.sqrt(mean_squared_error(yt, yp))
    mae  = mean_absolute_error(yt, yp)
    r2   = r2_score(yt, yp)
    meta['metrics'] = {'RMSE':round(rmse,4), 'MAE':round(mae,4), 'R2':round(r2,4)}
    pickle.dump(meta, open(f'models/meta_{city.lower()}.pkl', 'wb'))
    print(f"{city:<12} {rmse:>8.2f} {mae:>8.2f} {r2:>8.3f}")

print("=" * 52)
print("RMSE and MAE = lower is better")
print("R2 = closer to 1.0 is better")
print("=" * 52)
print("\nAll done! Models saved in models/ folder")