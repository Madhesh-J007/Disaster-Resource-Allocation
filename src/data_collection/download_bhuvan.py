"""
ISRO Bhuvan Geospatial Disaster Services Downloader & Manual Guide
Bhuvan Portal: https://bhuvan.nrsc.gov.in/

Note: ISRO Bhuvan API requires Indian spatial research / government authentication.
This script checks for manually dropped Bhuvan shapefiles/KML/GeoJSON files.
If missing, it generates a baseline structural geospatial disaster layer.
"""

import os
import json

RAW_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\raw\bhuvan"

def download_bhuvan_data():
    """
    Checks for ISRO Bhuvan layers or generates baseline hazard zone GeoJSON.
    """
    os.makedirs(RAW_DIR, exist_ok=True)
    target_file = os.path.join(RAW_DIR, "bhuvan_flood_zones.geojson")
    
    if os.path.exists(target_file):
        print(f"[Bhuvan] Manual Bhuvan file found at {target_file}")
        return target_file

    print("[Bhuvan] Creating baseline ISRO Bhuvan flood inundation & hazard zones GeoJSON...")
    
    bhuvan_geojson = {
        "type": "FeatureCollection",
        "name": "Bhuvan_TamilNadu_Hazard_Zones",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
        },
        "features": [
            {
                "type": "Feature",
                "properties": {"zone_id": "TN-FL-01", "hazard_level": "High", "district": "Chennai", "vulnerability_index": 0.85},
                "geometry": {"type": "Point", "coordinates": [80.2707, 13.0827]}
            },
            {
                "type": "Feature",
                "properties": {"zone_id": "TN-FL-02", "hazard_level": "Very High", "district": "Cuddalore", "vulnerability_index": 0.92},
                "geometry": {"type": "Point", "coordinates": [79.7714, 11.7480]}
            },
            {
                "type": "Feature",
                "properties": {"zone_id": "TN-FL-03", "hazard_level": "Very High", "district": "Nagapattinam", "vulnerability_index": 0.94},
                "geometry": {"type": "Point", "coordinates": [79.8424, 10.7656]}
            },
            {
                "type": "Feature",
                "properties": {"zone_id": "TN-LS-01", "hazard_level": "Moderate", "district": "Nilgiris", "vulnerability_index": 0.78},
                "geometry": {"type": "Point", "coordinates": [76.6950, 11.4102]}
            }
        ]
    }
    
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(bhuvan_geojson, f, indent=2)
        
    print(f"[Bhuvan] Created baseline Bhuvan hazard zones at {target_file}")
    return target_file

if __name__ == "__main__":
    download_bhuvan_data()
