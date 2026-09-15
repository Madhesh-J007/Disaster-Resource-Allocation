"""
Preprocessing module for NASA EONET events.
Extracts event categories, title, geometries (lat/lon), and timestamps into cleaned CSV.
"""

import os
import json
import pandas as pd

RAW_FILE = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\raw\eonet\eonet_events.json"
PROCESSED_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\processed"

def clean_eonet_data():
    """
    Parses raw EONET JSON and creates a standardized tabular CSV dataset.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out_file = os.path.join(PROCESSED_DIR, "cleaned_eonet.csv")
    
    if not os.path.exists(RAW_FILE):
        print(f"[Clean EONET] Raw file missing at {RAW_FILE}. Running collector first.")
        from src.data_collection.download_eonet import download_eonet_events
        download_eonet_events()
        
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    events = data.get("events", [])
    records = []
    
    for ev in events:
        event_id = ev.get("id")
        title = ev.get("title")
        categories = ", ".join([c.get("title", "") for c in ev.get("categories", [])])
        
        # Geometries
        geometries = ev.get("geometry", [])
        if geometries:
            first_geom = geometries[0]
            date_str = first_geom.get("date")
            coords = first_geom.get("coordinates", [0.0, 0.0])
            
            # Point geometry: [lon, lat]
            lon = coords[0] if len(coords) > 0 and isinstance(coords[0], (int, float)) else 0.0
            lat = coords[1] if len(coords) > 1 and isinstance(coords[1], (int, float)) else 0.0
        else:
            date_str = None
            lat, lon = 0.0, 0.0
            
        records.append({
            "event_id": event_id,
            "title": title,
            "category": categories,
            "date": date_str,
            "latitude": lat,
            "longitude": lon,
            "source": "NASA_EONET"
        })
        
    df = pd.DataFrame(records)
    
    # Cleaning & Normalization
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce").fillna(0.0)
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce").fillna(0.0)
    
    df.to_csv(out_file, index=False)
    print(f"[Clean EONET] Processed {len(df)} records into {out_file}")
    return out_file

if __name__ == "__main__":
    clean_eonet_data()
