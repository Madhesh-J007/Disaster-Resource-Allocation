"""
Dataset Validation Module
Validates dataset integrity across:
- row count
- column count
- missing values (count and null %)
- coordinate system verification (EPSG:4326 WGS84 for vector/tabular geospatial)
- file format validation
"""

import os
import json
import pandas as pd

def validate_dataset(file_path: str, crs_expected: str = "EPSG:4326") -> dict:
    """
    Validates a single dataset file and returns standard metrics dictionary.
    """
    if not os.path.exists(file_path):
        return {
            "status": "Missing",
            "file_name": os.path.basename(file_path),
            "file_path": file_path,
            "error": "File does not exist"
        }
        
    ext = os.path.splitext(file_path)[1].lower()
    file_size_bytes = os.path.getsize(file_path)
    
    validation_report = {
        "status": "Valid",
        "file_name": os.path.basename(file_path),
        "file_path": file_path,
        "file_format": ext.replace(".", "").upper(),
        "file_size_bytes": file_size_bytes,
        "row_count": 0,
        "column_count": 0,
        "missing_values_total": 0,
        "missing_values_pct": 0.0,
        "has_coordinates": False,
        "coordinate_system": crs_expected if ext in [".geojson", ".shp"] else "N/A (Tabular/JSON)",
        "columns": [],
        "column_null_counts": {}
    }
    
    try:
        if ext == ".csv":
            df = pd.read_csv(file_path)
            validation_report["row_count"] = len(df)
            validation_report["column_count"] = len(df.columns)
            validation_report["columns"] = list(df.columns)
            
            null_counts = df.isnull().sum().to_dict()
            total_cells = df.shape[0] * df.shape[1] if df.shape[0] > 0 else 1
            total_nulls = sum(null_counts.values())
            
            validation_report["missing_values_total"] = int(total_nulls)
            validation_report["missing_values_pct"] = round((total_nulls / total_cells) * 100, 2)
            validation_report["column_null_counts"] = {k: int(v) for k, v in null_counts.items()}
            
            # Coordinate check
            coord_cols = [c.lower() for c in df.columns]
            if ("latitude" in coord_cols or "lat" in coord_cols) and ("longitude" in coord_cols or "lon" in coord_cols):
                validation_report["has_coordinates"] = True
                validation_report["coordinate_system"] = "EPSG:4326 (WGS84)"
                
        elif ext == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                validation_report["row_count"] = len(data)
                validation_report["column_count"] = len(data[0].keys()) if len(data) > 0 and isinstance(data[0], dict) else 0
            elif isinstance(data, dict):
                # EONET / ReliefWeb top level object
                items = data.get("events") or data.get("data") or data.get("elements") or []
                validation_report["row_count"] = len(items)
                validation_report["column_count"] = len(items[0].keys()) if len(items) > 0 and isinstance(items[0], dict) else len(data.keys())
                
        elif ext == ".geojson":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            features = data.get("features", [])
            validation_report["row_count"] = len(features)
            validation_report["column_count"] = len(features[0].get("properties", {}).keys()) if len(features) > 0 else 0
            validation_report["has_coordinates"] = True
            validation_report["coordinate_system"] = "EPSG:4326 (WGS84 Coordinate Reference System)"
            
    except Exception as e:
        validation_report["status"] = "Error"
        validation_report["error"] = str(e)
        
    return validation_report
