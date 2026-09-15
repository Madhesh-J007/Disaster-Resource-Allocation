"""
Preprocessing module for IMD / Open-Meteo precipitation and meteorological data.
Computes rolling precipitation accumulations and extreme rainfall trigger flags.
"""

import os
import pandas as pd
import numpy as np

RAW_FILE = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\raw\imd\india_rainfall.csv"
PROCESSED_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\processed"

def clean_imd_data():
    """
    Cleans precipitation dataset and derives extreme precipitation indices.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out_file = os.path.join(PROCESSED_DIR, "cleaned_imd.csv")
    
    if not os.path.exists(RAW_FILE):
        print(f"[Clean IMD] Raw file missing. Running collector first.")
        from src.data_collection.download_imd import download_imd_rainfall_data
        download_imd_rainfall_data()
        
    df = pd.read_csv(RAW_FILE)
    
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    
    # Feature engineering: 3-day and 7-day rolling rainfall accumulation (mm)
    df["rolling_3d_precip_mm"] = df["precipitation_mm"].rolling(window=3, min_periods=1).sum().round(2)
    df["rolling_7d_precip_mm"] = df["precipitation_mm"].rolling(window=7, min_periods=1).sum().round(2)
    
    # Extreme Rainfall Flag (> 64.5 mm is IMD Heavy Rainfall threshold)
    df["heavy_rainfall_flag"] = (df["precipitation_mm"] >= 64.5).astype(int)
    df["extreme_rainfall_flag"] = (df["precipitation_mm"] >= 115.6).astype(int)
    
    df.to_csv(out_file, index=False)
    print(f"[Clean IMD] Processed {len(df)} daily weather records into {out_file}")
    return out_file

if __name__ == "__main__":
    clean_imd_data()
