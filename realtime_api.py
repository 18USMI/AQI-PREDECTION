"""
Real-time Air Quality Data Fetcher
Uses Open-Meteo Air Quality API — completely FREE, no API key required.
Docs: https://open-meteo.com/en/docs/air-quality-api

Fetches: PM2.5, PM10, NO2, SO2, CO, O3, US AQI — current + 5-day forecast
"""

import urllib.request
import json
import math
from datetime import datetime, timezone
from typing import Optional


# ──────────────────────────────────────────────────────────────────────────────
# Open-Meteo Air Quality endpoint (free, no key)
# ──────────────────────────────────────────────────────────────────────────────
AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# Variables to fetch
HOURLY_VARS = "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi"
CURRENT_VARS = "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi"


def _http_get(url: str, timeout: int = 10) -> Optional[dict]:
    """Simple HTTP GET using stdlib (no requests dependency)."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[API] HTTP error: {e}")
        return None


def fetch_current_aqi(lat: float, lon: float) -> Optional[dict]:
    """
    Fetch current air quality for a lat/lon.
    Returns dict with keys: us_aqi, pm2_5, pm10, no2, so2, co, o3, timestamp
    """
    url = (
        f"{AIR_QUALITY_URL}?"
        f"latitude={lat:.4f}&longitude={lon:.4f}"
        f"&current={CURRENT_VARS}"
        f"&timezone=auto"
    )
    data = _http_get(url)
    if not data or "current" not in data:
        return None

    cur = data["current"]
    return {
        "us_aqi":  cur.get("us_aqi"),
        "pm2_5":   cur.get("pm2_5"),
        "pm10":    cur.get("pm10"),
        "no2":     cur.get("nitrogen_dioxide"),
        "so2":     cur.get("sulphur_dioxide"),
        "co":      cur.get("carbon_monoxide"),
        "o3":      cur.get("ozone"),
        "timestamp": cur.get("time", datetime.now(timezone.utc).isoformat()),
        "lat": lat,
        "lon": lon,
    }


def fetch_hourly_history(lat: float, lon: float, past_days: int = 7) -> Optional[dict]:
    """
    Fetch past N days of hourly air quality — used as LSTM input window.
    Returns dict with lists: times, us_aqi, pm2_5, pm10, no2, so2, co, o3
    """
    url = (
        f"{AIR_QUALITY_URL}?"
        f"latitude={lat:.4f}&longitude={lon:.4f}"
        f"&hourly={HOURLY_VARS}"
        f"&past_days={past_days}"
        f"&forecast_days=1"
        f"&timezone=auto"
    )
    data = _http_get(url)
    if not data or "hourly" not in data:
        return None

    h = data["hourly"]
    return {
        "times":  h.get("time", []),
        "us_aqi": h.get("us_aqi", []),
        "pm2_5":  h.get("pm2_5", []),
        "pm10":   h.get("pm10", []),
        "no2":    h.get("nitrogen_dioxide", []),
        "so2":    h.get("sulphur_dioxide", []),
        "co":     h.get("carbon_monoxide", []),
        "o3":     h.get("ozone", []),
    }


def fetch_forecast(lat: float, lon: float, days: int = 5) -> Optional[dict]:
    """
    Fetch up-to-5-day hourly AQI forecast.
    """
    url = (
        f"{AIR_QUALITY_URL}?"
        f"latitude={lat:.4f}&longitude={lon:.4f}"
        f"&hourly={HOURLY_VARS}"
        f"&forecast_days={days}"
        f"&timezone=auto"
    )
    data = _http_get(url)
    if not data or "hourly" not in data:
        return None

    h = data["hourly"]
    return {
        "times":  h.get("time", []),
        "us_aqi": h.get("us_aqi", []),
        "pm2_5":  h.get("pm2_5", []),
        "pm10":   h.get("pm10", []),
        "no2":    h.get("nitrogen_dioxide", []),
        "so2":    h.get("sulphur_dioxide", []),
        "co":     h.get("carbon_monoxide", []),
        "o3":     h.get("ozone", []),
    }


def safe_val(val, default=0.0):
    """Return float or default if None/NaN."""
    if val is None:
        return default
    try:
        f = float(val)
        return default if math.isnan(f) else f
    except (TypeError, ValueError):
        return default
