"""
Preprocessing module for EM-DAT CRED International Disaster records.
Standardizes fields, handles missing metrics, calculates duration, and exports clean CSV.
"""

import os
import pandas as pd

RAW_FILE = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\raw\emdat\emdat_disasters.csv"
PROCESSED_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\processed"

def clean_emdat_data():
    """
    Parses raw/baseline EM-DAT records into cleaned CSV.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out_file = os.path.join(PROCESSED_DIR, "cleaned_emdat.csv")
    
    if not os.path.exists(RAW_FILE):
        print(f"[Clean EM-DAT] Raw file missing. Running collector first.")
        from src.data_collection.download_emdat import download_emdat_data
        download_emdat_data()
        
    df = pd.read_csv(RAW_FILE)
    
    # Standardize column names
    col_mapping = {
        "DisNo": "disaster_number",
        "Year": "year",
        "Disaster Type": "disaster_type",
        "Disaster Subtype": "disaster_subtype",
        "Location": "location",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Total Deaths": "total_deaths",
        "Total Affected": "total_affected",
        "Total Damages ('000 US$)": "total_damages_usd_thousands"
    }
    
    # Rename matching columns
    existing = {k: v for k, v in col_mapping.items() if k in df.columns}
    df = df.rename(columns=existing)
    
    # Fill missing values safely
    numeric_cols = ["total_deaths", "total_affected", "total_damages_usd_thousands", "latitude", "longitude"]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
            
    df["source"] = "EM-DAT"
    df.to_csv(out_file, index=False)
    print(f"[Clean EM-DAT] Processed {len(df)} disaster events into {out_file}")
    return out_file

if __name__ == "__main__":
    clean_emdat_data()
