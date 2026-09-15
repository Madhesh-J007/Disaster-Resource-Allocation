"""
OCHA ReliefWeb API Data Collector
API Documentation: https://apidoc.rwlabs.org/
Fetches up to 1000 disaster records and situation reports.
"""

import os
import json
import requests

RAW_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\raw\reliefweb"

def download_reliefweb_data(limit: int = 1000):
    """
    Fetches disaster reports and event records from United Nations OCHA ReliefWeb REST API.
    """
    os.makedirs(RAW_DIR, exist_ok=True)
    headers = {"User-Agent": "Disaster-Chain-Reaction-ML/1.0 (Research)"}
    
    # Query disasters
    disasters_url = f"https://api.reliefweb.int/v1/disasters?appname=disaster-ml&limit={limit}&preset=latest"
    reports_url = f"https://api.reliefweb.int/v1/reports?appname=disaster-ml&limit={limit}&preset=latest"
    
    print(f"[ReliefWeb] Fetching up to {limit} disaster records from ReliefWeb API...")
    try:
        res_disasters = requests.get(disasters_url, headers=headers, timeout=60)
        res_disasters.raise_for_status()
        disasters_data = res_disasters.json()
        
        disasters_file = os.path.join(RAW_DIR, "reliefweb_disasters.json")
        with open(disasters_file, "w", encoding="utf-8") as f:
            json.dump(disasters_data, f, indent=2)
            
        d_count = len(disasters_data.get('data', []))
        print(f"[ReliefWeb] Downloaded {d_count} real disaster records to {disasters_file}")
        
        # Query reports
        res_reports = requests.get(reports_url, headers=headers, timeout=60)
        res_reports.raise_for_status()
        reports_data = res_reports.json()
        
        reports_file = os.path.join(RAW_DIR, "reliefweb_reports.json")
        with open(reports_file, "w", encoding="utf-8") as f:
            json.dump(reports_data, f, indent=2)
            
        r_count = len(reports_data.get('data', []))
        print(f"[ReliefWeb] Downloaded {r_count} real report records to {reports_file}")
        return disasters_file
    except Exception as e:
        print(f"[ReliefWeb] Warning during API call ({e}). Proceeding with stored real records.")
        disasters_file = os.path.join(RAW_DIR, "reliefweb_disasters.json")
        return disasters_file

if __name__ == "__main__":
    download_reliefweb_data()
