"""
Validation Orchestrator & Metadata JSON Generator
Scans raw, interim, and processed datasets, executes validation checks, and saves metadata.json.
"""

import os
import json
from datetime import datetime
from src.utils.validation import validate_dataset

BASE_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML"
METADATA_DIR = os.path.join(BASE_DIR, "datasets", "metadata")

RAW_DATASETS = [
    "datasets/raw/emdat/emdat_disasters.csv",
    "datasets/raw/eonet/eonet_events.json",
    "datasets/raw/reliefweb/reliefweb_disasters.json",
    "datasets/raw/imd/india_rainfall.csv",
    "datasets/raw/osm/tamil_nadu_infrastructure.json",
    "datasets/raw/census/census_tamil_nadu.csv",
    "datasets/raw/worldpop/worldpop_tamil_nadu.csv",
    "datasets/raw/bhuvan/bhuvan_flood_zones.geojson",
    "datasets/raw/dem/tamil_nadu_dem.csv",
]

PROCESSED_DATASETS = [
    "datasets/processed/cleaned_emdat.csv",
    "datasets/processed/cleaned_eonet.csv",
    "datasets/processed/cleaned_reliefweb.csv",
    "datasets/processed/cleaned_imd.csv",
    "datasets/processed/cleaned_osm.csv",
    "datasets/processed/cleaned_census.csv",
    "datasets/processed/cleaned_worldpop.csv",
    "datasets/processed/cleaned_dem.csv",
    "datasets/processed/final_dataset.csv",
    "datasets/processed/train.csv",
    "datasets/processed/validation.csv",
    "datasets/processed/test.csv",
]

def validate_all_and_generate_metadata():
    """
    Validates all raw and processed datasets and writes datasets/metadata/metadata.json.
    """
    os.makedirs(METADATA_DIR, exist_ok=True)
    
    full_metadata = {
        "project": "Secondary Disaster Chain Reaction ML",
        "last_validated": datetime.now().isoformat(),
        "total_datasets_checked": len(RAW_DATASETS) + len(PROCESSED_DATASETS),
        "raw_datasets": {},
        "processed_datasets": {}
    }
    
    print("\n================ DATASET VALIDATION REPORT ================\n")
    print(f"{'File Name':<35} | {'Status':<7} | {'Rows':<7} | {'Cols':<5} | {'Null %':<7} | {'CRS'}")
    print("-" * 85)
    
    for rel_path in RAW_DATASETS:
        full_path = os.path.join(BASE_DIR, rel_path)
        report = validate_dataset(full_path)
        key = os.path.basename(rel_path)
        full_metadata["raw_datasets"][key] = report
        print(f"{report['file_name']:<35} | {report['status']:<7} | {report.get('row_count', 0):<7} | {report.get('column_count', 0):<5} | {report.get('missing_values_pct', 0.0):<7}% | {report.get('coordinate_system', 'N/A')}")
        
    print("-" * 85)
    for rel_path in PROCESSED_DATASETS:
        full_path = os.path.join(BASE_DIR, rel_path)
        report = validate_dataset(full_path)
        key = os.path.basename(rel_path)
        full_metadata["processed_datasets"][key] = report
        print(f"{report['file_name']:<35} | {report['status']:<7} | {report.get('row_count', 0):<7} | {report.get('column_count', 0):<5} | {report.get('missing_values_pct', 0.0):<7}% | {report.get('coordinate_system', 'N/A')}")
        
    print("=" * 85)
    
    metadata_json_path = os.path.join(METADATA_DIR, "metadata.json")
    with open(metadata_json_path, "w", encoding="utf-8") as f:
        json.dump(full_metadata, f, indent=2)
        
    print(f"\n[Validation] Successfully updated metadata report at {metadata_json_path}\n")
    return metadata_json_path

if __name__ == "__main__":
    validate_all_and_generate_metadata()
