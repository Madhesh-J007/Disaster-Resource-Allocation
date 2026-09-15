"""
Preprocessing module for Census demographic data in Tamil Nadu.
Computes social vulnerability metrics and normalizes district indicators.
"""

import os
import pandas as pd

RAW_FILE = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\raw\census\census_tamil_nadu.csv"
PROCESSED_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\processed"

def clean_census_data():
    """
    Cleans Census data and standardizes vulnerability scoring.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out_file = os.path.join(PROCESSED_DIR, "cleaned_census.csv")
    
    if not os.path.exists(RAW_FILE):
        print(f"[Clean Census] Raw file missing. Running collector first.")
        from src.data_collection.download_census import download_census_data
        download_census_data()
        
    df = pd.read_csv(RAW_FILE)
    
    # Calculate Composite Vulnerability Index
    # Formula: (Slum_Pct * 0.4) + ((100 - Pukka_Housing_Pct) * 0.4) + ((100 - Literacy_Rate) * 0.2)
    df["composite_vulnerability_index"] = (
        (df["slum_pop_pct"] * 0.4) +
        ((100.0 - df["pukka_housing_pct"]) * 0.4) +
        ((100.0 - df["literacy_rate"]) * 0.2)
    ).round(2)
    
    df["source"] = "Census_India"
    df.to_csv(out_file, index=False)
    print(f"[Clean Census] Processed {len(df)} district census records into {out_file}")
    return out_file

if __name__ == "__main__":
    clean_census_data()
