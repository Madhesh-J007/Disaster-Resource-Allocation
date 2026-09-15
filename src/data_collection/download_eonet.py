"""
NASA EONET (Earth Observatory Natural Event Tracker) Data Collector
API Documentation: https://eonet.gsfc.nasa.gov/docs/v3
Fetches maximum available historical natural hazard event records (limit=2000, 10-year span).
"""

import os
import json
import requests

RAW_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\raw\eonet"

def download_eonet_events(limit: int = 2000, days: int = 3650):
    """
    Fetches natural disaster events from NASA EONET v3 REST API.
    """
    os.makedirs(RAW_DIR, exist_ok=True)
    url = f"https://eonet.gsfc.nasa.gov/api/v3/events?limit={limit}&days={days}&status=all"
    headers = {"User-Agent": "Disaster-Chain-Reaction-ML/1.0 (Research)"}
    
    print(f"[EONET] Fetching maximum natural disaster events (limit={limit}) from NASA EONET API...")
    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        output_file = os.path.join(RAW_DIR, "eonet_events.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            
        event_count = len(data.get("events", []))
        print(f"[EONET] Successfully downloaded {event_count} real events to {output_file}")
        return output_file
    except Exception as e:
        print(f"[EONET] Error fetching EONET data: {e}")
        return None

if __name__ == "__main__":
    download_eonet_events()
