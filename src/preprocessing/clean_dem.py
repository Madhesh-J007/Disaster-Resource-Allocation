"""
Preprocessing module for SRTM Digital Elevation Model (DEM) data in Tamil Nadu.
Computes terrain slope estimates, flood susceptibility categories, and spatial elevation zones.
"""

import os
import pandas as pd
import numpy as np

RAW_FILE = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\raw\dem\tamil_nadu_dem.csv"
PROCESSED_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\processed"

def clean_dem_data():
    """
    Cleans DEM point elevation records and categorizes inundation risk.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out_file = os.path.join(PROCESSED_DIR, "cleaned_dem.csv")
    
    if not os.path.exists(RAW_FILE):
        print(f"[Clean DEM] Raw file missing. Running collector first.")
        from src.data_collection.download_dem import download_dem_data
        download_dem_data()
        
    df = pd.read_csv(RAW_FILE)
    
    # Categorize elevation flood risk zone
    # Low elevation (< 15m) -> High Flood Vulnerability
    # Mountainous (> 500m) -> Landslide Risk Zone
    def classify_topography(elev):
        if elev <= 15:
            return "High Flood Inundation Vulnerability"
        elif elev <= 100:
            return "Moderate Plain Vulnerability"
        elif elev <= 500:
            return "Low Inundation Risk"
        else:
            return "High Landslide Vulnerability"

    df["risk_category"] = df["elevation_m"].apply(classify_topography)
    df["source"] = "SRTM_30m"
    
    df.to_csv(out_file, index=False)
    print(f"[Clean DEM] Processed {len(df)} terrain elevation points into {out_file}")
    return out_file

if __name__ == "__main__":
    clean_dem_data()
