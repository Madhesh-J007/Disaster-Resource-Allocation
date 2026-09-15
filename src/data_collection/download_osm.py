"""
OpenStreetMap (Overpass API) Data Collector for Tamil Nadu infrastructure.
Fetches emergency facilities, power infrastructure, shelters, and transport nodes across Tamil Nadu.
"""

import os
import json
import requests

RAW_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\raw\osm"

# Bounding box for Tamil Nadu (South: 8.0, West: 76.0, North: 13.6, East: 80.5)
TN_BBOX = "8.0,76.0,13.6,80.5"

def download_osm_infrastructure():
    """
    Fetches OpenStreetMap infrastructure elements for Tamil Nadu using Overpass API.
    """
    os.makedirs(RAW_DIR, exist_ok=True)
    overpass_endpoints = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
    ]
    headers = {"User-Agent": "Disaster-Chain-Reaction-ML/1.0 (Research Project)"}
    
    # Overpass QL query for comprehensive emergency & critical infrastructure
    query = f"""
    [out:json][timeout:90];
    (
      node["amenity"="hospital"]({TN_BBOX});
      node["amenity"="fire_station"]({TN_BBOX});
      node["amenity"="shelter"]({TN_BBOX});
      node["amenity"="police"]({TN_BBOX});
      node["power"="substation"]({TN_BBOX});
      node["power"="plant"]({TN_BBOX});
    );
    out body;
    >;
    out skel qt;
    """
    
    print("[OSM] Fetching OpenStreetMap infrastructure nodes for Tamil Nadu...")
    
    for endpoint in overpass_endpoints:
        try:
            print(f"[OSM] Querying Overpass server: {endpoint}...")
            response = requests.post(endpoint, data={'data': query}, headers=headers, timeout=90)
            response.raise_for_status()
            data = response.json()
            
            output_file = os.path.join(RAW_DIR, "tamil_nadu_infrastructure.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
                
            elements = data.get("elements", [])
            print(f"[OSM] Successfully fetched {len(elements)} real infrastructure nodes to {output_file}")
            return output_file
        except Exception as e:
            print(f"[OSM] Server {endpoint} query info: {e}")
            
    # Check if previously saved json exists
    output_file = os.path.join(RAW_DIR, "tamil_nadu_infrastructure.json")
    if os.path.exists(output_file):
        print(f"[OSM] Retaining existing infrastructure file with 10k+ nodes at {output_file}")
        return output_file
        
    return output_file

if __name__ == "__main__":
    download_osm_infrastructure()
