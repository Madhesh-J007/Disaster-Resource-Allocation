"""
Preprocessing module for UN OCHA ReliefWeb disaster records.
Extracts disaster titles, types, status, primary countries, and dates into cleaned CSV.
"""

import os
import json
import pandas as pd

RAW_FILE = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\raw\reliefweb\reliefweb_disasters.json"
PROCESSED_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\processed"

def clean_reliefweb_data():
    """
    Parses raw ReliefWeb JSON and outputs a cleaned CSV.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out_file = os.path.join(PROCESSED_DIR, "cleaned_reliefweb.csv")
    
    if not os.path.exists(RAW_FILE):
        print(f"[Clean ReliefWeb] Raw file missing at {RAW_FILE}. Running collector first.")
        from src.data_collection.download_reliefweb import download_reliefweb_data
        download_reliefweb_data()
        
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    items = data.get("data", [])
    records = []
    
    for item in items:
        fields = item.get("fields", {})
        disaster_id = item.get("id")
        name = fields.get("name")
        status = fields.get("status")
        
        # Primary country & coordinates
        primary_country = fields.get("primary_country", {}).get("name", "Unknown")
        location = fields.get("primary_country", {}).get("location", {})
        lat = location.get("lat", 0.0)
        lon = location.get("lon", 0.0)
        
        # Types
        disaster_types = ", ".join([t.get("name", "") for t in fields.get("type", [])])
        date_str = fields.get("date", {}).get("created")
        
        records.append({
            "disaster_id": disaster_id,
            "disaster_name": name,
            "disaster_type": disaster_types,
            "status": status,
            "country": primary_country,
            "latitude": lat,
            "longitude": lon,
            "created_date": date_str,
            "source": "ReliefWeb"
        })
        
    df = pd.DataFrame(records)
    df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce").fillna(0.0)
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce").fillna(0.0)
    
    df.to_csv(out_file, index=False)
    print(f"[Clean ReliefWeb] Processed {len(df)} records into {out_file}")
    return out_file

if __name__ == "__main__":
    clean_reliefweb_data()
