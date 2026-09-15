"""
Preprocessing module for OpenStreetMap infrastructure elements in Tamil Nadu.
Cleans amenity nodes, normalizes coordinates, tags, and spatial metadata into CSV.
"""

import os
import json
import pandas as pd

RAW_FILE = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\raw\osm\tamil_nadu_infrastructure.json"
PROCESSED_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\processed"

def clean_osm_data():
    """
    Parses OpenStreetMap nodes JSON and saves cleaned infrastructure CSV.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out_file = os.path.join(PROCESSED_DIR, "cleaned_osm.csv")
    
    if not os.path.exists(RAW_FILE):
        print(f"[Clean OSM] Raw file missing at {RAW_FILE}. Running collector first.")
        from src.data_collection.download_osm import download_osm_infrastructure
        download_osm_infrastructure()
        
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    elements = data.get("elements", [])
    records = []
    
    for el in elements:
        if el.get("type") == "node":
            tags = el.get("tags", {})
            amenity = tags.get("amenity") or tags.get("power") or "infrastructure"
            name = tags.get("name") or f"Facility_{el.get('id')}"
            
            records.append({
                "osm_id": el.get("id"),
                "name": name,
                "facility_type": amenity,
                "latitude": el.get("lat", 0.0),
                "longitude": el.get("lon", 0.0),
                "state": "Tamil Nadu",
                "source": "OpenStreetMap"
            })
            
    df = pd.DataFrame(records)
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce").fillna(0.0)
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce").fillna(0.0)
    
    df.to_csv(out_file, index=False)
    print(f"[Clean OSM] Processed {len(df)} infrastructure nodes into {out_file}")
    return out_file

if __name__ == "__main__":
    clean_osm_data()
