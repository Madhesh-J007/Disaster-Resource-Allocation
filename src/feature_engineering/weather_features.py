"""
Weather Feature Engineering Module (Stage 2A)
Derives meteorological risk features:
- rainfall_intensity
- rolling_3day_rainfall
- rolling_7day_rainfall
- rainfall_percentile
- rainfall_anomaly
- heavy_rain_indicator
- rainfall_zscore
"""

import numpy as np
import pandas as pd

def compute_weather_features(df_imd: pd.DataFrame) -> pd.DataFrame:
    """
    Computes derived weather features from raw IMD daily weather observations.
    """
    df = df_imd.copy()
    
    # 1. Rainfall Intensity (mm per rain hour)
    if "precipitation_hours" in df.columns:
        df["rainfall_intensity"] = (df["precipitation_mm"] / df["precipitation_hours"].replace(0, 1)).round(3)
    else:
        df["rainfall_intensity"] = df["precipitation_mm"].round(3)

    # 2. Rolling 3-Day Rainfall
    df["rolling_3day_rainfall"] = df.groupby("location_name")["precipitation_mm"].transform(
        lambda x: x.rolling(3, min_periods=1).sum()
    ).round(2)

    # 3. Rolling 7-Day Rainfall
    df["rolling_7day_rainfall"] = df.groupby("location_name")["precipitation_mm"].transform(
        lambda x: x.rolling(7, min_periods=1).sum()
    ).round(2)

    # 4. Rainfall Percentile Rank
    df["rainfall_percentile"] = df.groupby("location_name")["precipitation_mm"].transform(
        lambda x: x.rank(pct=True)
    ).round(4)

    # 5. Rainfall Anomaly relative to location mean
    mean_by_loc = df.groupby("location_name")["precipitation_mm"].transform("mean")
    std_by_loc = df.groupby("location_name")["precipitation_mm"].transform("std").replace(0, 1.0)
    
    df["rainfall_anomaly"] = (df["precipitation_mm"] - mean_by_loc).round(3)

    # 6. Heavy Rain Indicator (>= 64.5 mm IMD threshold)
    df["heavy_rain_indicator"] = (df["precipitation_mm"] >= 64.5).astype(int)

    # 7. Rainfall Z-Score
    df["rainfall_zscore"] = ((df["precipitation_mm"] - mean_by_loc) / std_by_loc).round(4)
    
    return df
