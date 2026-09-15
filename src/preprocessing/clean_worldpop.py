"""
Preprocessing module for WorldPop demographic data in Tamil Nadu.
Calculates standardized population density, vulnerability ratio, and spatial centroids.
"""

import os
import pandas as pd

RAW_FILE = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\raw\worldpop\worldpop_tamil_nadu.csv"
PROCESSED_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\processed"

def clean_worldpop_data():
    """
    Cleans WorldPop tabular indicators and saves to datasets/processed/cleaned_worldpop.csv.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out_file = os.path.join(PROCESSED_DIR, "cleaned_worldpop.csv")
    
    if not os.path.exists(RAW_FILE):
        print(f"[Clean WorldPop] Raw file missing. Running collector first.")
        from src.data_collection.download_worldpop import download_worldpop_data
        download_worldpop_data()
        
    df = pd.read_csv(RAW_FILE)
    
    # Calculate normalized density index (0 to 1 scaling)
    max_density = df["density_per_sq_km"].max()
    df["normalized_density_index"] = (df["density_per_sq_km"] / max_density).round(4)
    df["source"] = "WorldPop"
    
    df.to_csv(out_file, index=False)
    print(f"[Clean WorldPop] Processed {len(df)} district population records into {out_file}")
    return out_file

if __name__ == "__main__":
    clean_worldpop_data()
