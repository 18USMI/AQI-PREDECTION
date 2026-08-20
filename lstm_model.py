"""
LSTM Model Layer
- Stacked Bidirectional LSTM
- Dropout regularization
- Adam optimizer + MSE loss
- Early stopping & model checkpoint
"""

import numpy as np
import os

# ─── Try TensorFlow/Keras; fall back to sklearn if unavailable ────────────────
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import (LSTM, Bidirectional, Dense,
                                          Dropout, Input)
    from tensorflow.keras.callbacks import (EarlyStopping, ModelCheckpoint,
                                             ReduceLROnPlateau)
    from tensorflow.keras.optimizers import Adam
    TF_AVAILABLE = True
    print("[Model] TensorFlow available ✓")

except ImportError:
    TF_AVAILABLE = False
    print("[Model] TensorFlow NOT available – using sklearn GradientBoosting as fallback")
    from sklearn.ensemble import GradientBoostingRegressor
    import pickle


# ══════════════════════════════════════════════════════════════════════════════
# LSTM Model (TensorFlow/Keras)
# ══════════════════════════════════════════════════════════════════════════════

def build_lstm_model(input_shape: tuple, units1: int = 64, units2: int = 32,
                     dropout_rate: float = 0.2, bidirectional: bool = True) -> "tf.keras.Model":
    """
    Build stacked LSTM model.
    
    Architecture:
        Input → BiLSTM(128) → Dropout → LSTM(64) → Dense(32) → Dense(1)
    
    Args:
        input_shape: (time_steps, n_features)
    """
    model = Sequential([
        Input(shape=input_shape),
    ])
    
    if bidirectional:
        model.add(Bidirectional(LSTM(units=units1 * 2, return_sequences=True)))
    else:
        model.add(LSTM(units=units1, return_sequences=True))
    
    model.add(Dropout(dropout_rate))
    model.add(LSTM(units=units2, return_sequences=False))
    model.add(Dropout(dropout_rate / 2))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(1))
    
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="mse",
        metrics=["mae"]
    )
    
    print(model.summary())
    return model


def train_lstm(X_train, y_train, X_test, y_test,
               epochs: int = 100, batch_size: int = 32,
               model_path: str = "models/lstm_model.h5"):
    """Train LSTM model with early stopping."""
    
    input_shape = (X_train.shape[1], X_train.shape[2])
    model = build_lstm_model(input_shape)
    
    callbacks = [
        EarlyStopping(monitor="val_loss", patience=15, restore_best_weights=True),
        ModelCheckpoint(model_path, save_best_only=True, monitor="val_loss"),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=7, min_lr=1e-6)
    ]
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=1
    )
    
    print(f"[Model] Training complete. Model saved to {model_path}")
    return model, history


# ══════════════════════════════════════════════════════════════════════════════
# Sklearn Fallback Model (GradientBoosting)
# ══════════════════════════════════════════════════════════════════════════════

def build_sklearn_model():
    """Gradient Boosting fallback when TensorFlow unavailable."""
    return GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        random_state=42,
        verbose=1
    )


def train_sklearn(X_train, y_train, model_path: str = "models/sklearn_model.pkl"):
    """Train sklearn model — flattens 3D X to 2D."""
    X_2d = X_train.reshape(X_train.shape[0], -1)
    model = build_sklearn_model()
    model.fit(X_2d, y_train)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(sklearn_path, "wb") as f:
        pickle.dump(model, f)
    print(f"[Model] sklearn model saved to {model_path}")
    return model


def load_sklearn(model_path: str = "models/sklearn_model.pkl"):
    with open(model_path, "rb") as f:
        return pickle.load(f)


# ══════════════════════════════════════════════════════════════════════════════
# Unified Interface
# ══════════════════════════════════════════════════════════════════════════════

def train_model(X_train, y_train, X_test=None, y_test=None):
    """Train whichever model is available."""
    os.makedirs("models", exist_ok=True)
    if TF_AVAILABLE:
        return train_lstm(X_train, y_train, X_test, y_test), "lstm"
    else:
        return train_sklearn(X_train, y_train), "sklearn"


def predict(model, X, model_type: str = "sklearn") -> np.ndarray:
    """Run inference."""
    if model_type == "sklearn":
        X_2d = X.reshape(X.shape[0], -1)
        return model.predict(X_2d)
    else:
        return model.predict(X).flatten()


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "src")
    from preprocess import preprocess_pipeline
    from feature_engineering import add_lag_features, add_rolling_features, scale_and_prepare

    df = preprocess_pipeline("data/raw/aqi_data.csv", city="Kolkata")
    df = add_lag_features(df)
    df = add_rolling_features(df)
    X_train, X_test, y_train, y_test, scaler, df_feat = scale_and_prepare(df)
    
    result, mtype = train_model(X_train, y_train, X_test, y_test)
    print(f"Model type: {mtype}")
