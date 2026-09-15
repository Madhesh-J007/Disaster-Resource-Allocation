"""
Feature Store Builder & Pipeline Orchestrator (Stage 6)
Assembles all engineered feature modules into datasets/processed/feature_engineered_dataset.csv,
feature_store.parquet, and datasets/metadata/feature_metadata.json.
"""

import os
import json
import numpy as np
import pandas as pd
from datetime import datetime

# Import feature modules
from src.preprocessing.merge_datasets import merge_all_datasets
from src.feature_engineering.weather_features import compute_weather_features
from src.feature_engineering.spatial_features import compute_spatial_features
from src.feature_engineering.vulnerability_index import compute_population_features
from src.feature_engineering.infrastructure_features import compute_infrastructure_features
from src.feature_engineering.graph_features import compute_disaster_history_features
from src.feature_engineering.cascade_risk_score import compute_composite_features_and_target, generate_feature_dictionary_excel
from src.feature_engineering.profiling import profile_dataset
from src.feature_engineering.selection import process_normalization_and_selection

BASE_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML"
PROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "processed")
METADATA_DIR = os.path.join(BASE_DIR, "datasets", "metadata")
RAW_DIR = os.path.join(BASE_DIR, "datasets", "raw")

def build_feature_store():
    """
    Assembles raw and processed datasets into 25-35 engineered features and saves feature store formats.
    """
    print("\n=======================================================================")
    print("      STAGE 2: FEATURE ENGINEERING ENGINE & STORE BUILDER              ")
    print("=======================================================================\n")
    
    # 1. Base spatial-temporal dataset
    f_final = os.path.join(PROCESSED_DIR, "final_dataset.csv")
    if not os.path.exists(f_final):
        f_final = merge_all_datasets()
        
    df_base = pd.read_csv(f_final)
    district_list = df_base["district"].tolist()
    
    # Load individual components
    df_imd = pd.read_csv(os.path.join(RAW_DIR, "imd", "india_rainfall.csv"))
    df_dem = pd.read_csv(os.path.join(RAW_DIR, "dem", "tamil_nadu_dem.csv"))
    df_pop = pd.read_csv(os.path.join(RAW_DIR, "worldpop", "worldpop_tamil_nadu.csv"))
    df_census = pd.read_csv(os.path.join(RAW_DIR, "census", "census_tamil_nadu.csv"))
    
    f_osm_raw = os.path.join(PROCESSED_DIR, "cleaned_osm.csv")
    df_osm = pd.read_csv(f_osm_raw) if os.path.exists(f_osm_raw) else pd.DataFrame()
    
    f_emdat_raw = os.path.join(PROCESSED_DIR, "cleaned_emdat.csv")
    df_emdat = pd.read_csv(f_emdat_raw) if os.path.exists(f_emdat_raw) else pd.DataFrame()

    # 2. Compute individual feature modules
    print("--- Deriving Weather Features ---")
    df_weather_ext = compute_weather_features(df_imd)
    
    print("--- Deriving Spatial & Terrain Features ---")
    df_terrain_ext = compute_spatial_features(df_dem)
    
    print("--- Deriving Population Exposure Features ---")
    df_pop_ext = compute_population_features(df_pop, df_census)
    
    print("--- Deriving Infrastructure Density Features ---")
    df_infra_ext = compute_infrastructure_features(df_osm, df_pop)
    
    print("--- Deriving Disaster History Metrics ---")
    df_history_ext = compute_disaster_history_features(df_emdat, district_list)

    # 3. Fuse engineered features into master district matrix
    df_master = df_base[["district_id", "district", "population", "pop_density_per_sq_km", "elevation_m", "recent_7d_precip_mm", "slum_pop_pct", "pukka_housing_pct"]].copy()
    
    # Merge terrain
    df_master = pd.merge(df_master, df_terrain_ext[["district", "derived_slope_deg", "terrain_risk", "low_lying_area_flag", "elevation_category", "slope_category"]], on="district", how="left")
    
    # Merge population
    df_master = pd.merge(df_master, df_pop_ext[["district", "population_density", "population_exposure_index", "urban_pressure_index"]], on="district", how="left")
    
    # Merge infrastructure
    df_master = pd.merge(df_master, df_infra_ext[["district", "hospital_density", "police_station_density", "fire_station_density", "road_density", "infrastructure_density", "critical_infrastructure_count", "emergency_service_density"]], on="district", how="left")
    
    # Merge disaster history
    df_master = pd.merge(df_master, df_history_ext[["district", "disaster_frequency", "flood_frequency", "cyclone_frequency", "historical_damage_score", "historical_casualty_score", "historical_severity_index"]], on="district", how="left")
    
    # Add weather summaries
    df_master["rainfall_intensity"] = np.round(df_master["recent_7d_precip_mm"] / 7.0, 2)
    df_master["rolling_3day_rainfall"] = np.round(df_master["recent_7d_precip_mm"] * 0.5, 2)
    df_master["rolling_7day_rainfall"] = df_master["recent_7d_precip_mm"]
    df_master["rainfall_anomaly"] = np.round(df_master["recent_7d_precip_mm"] - df_master["recent_7d_precip_mm"].mean(), 2)

    # 4. Compute Composite Indices & Version 1 Target Variable (Cascade Risk Score & Risk Level)
    print("--- Computing Composite Indices & Target Variable (Cascade Risk Score) ---")
    df_engineered = compute_composite_features_and_target(df_master)
    
    # 5. Save Feature Store Formats (.csv & .parquet)
    csv_store_path = os.path.join(PROCESSED_DIR, "feature_engineered_dataset.csv")
    df_engineered.to_csv(csv_store_path, index=False)
    print(f"[OK] Saved CSV feature store ({len(df_engineered)} rows x {len(df_engineered.columns)} features) to {csv_store_path}")

    parquet_store_path = os.path.join(PROCESSED_DIR, "feature_store.parquet")
    df_engineered.to_parquet(parquet_store_path, index=False)
    print(f"[OK] Saved Parquet feature store to {parquet_store_path}")

    # 6. Generate Feature Metadata JSON & Feature Engineering Dictionary Excel
    generate_feature_dictionary_excel()
    profile_dataset()
    
    # Run Selection & Normalization Analysis
    process_normalization_and_selection(df_engineered)
    
    num_cols = [c for c in df_engineered.columns if pd.api.types.is_numeric_dtype(df_engineered[c])]
    cat_cols = [c for c in df_engineered.columns if not pd.api.types.is_numeric_dtype(df_engineered[c])]
    
    feature_meta = {
        "feature_store_name": "Secondary Disaster Chain Reaction Feature Store",
        "created_at": datetime.now().isoformat(),
        "total_districts": len(df_engineered),
        "total_features": len(df_engineered.columns),
        "target_variables": ["cascade_risk_score", "cascade_risk_level"],
        "columns": list(df_engineered.columns),
        "numeric_features": num_cols,
        "categorical_features": cat_cols
    }
    
    meta_json_path = os.path.join(METADATA_DIR, "feature_metadata.json")
    with open(meta_json_path, "w", encoding="utf-8") as f:
        json.dump(feature_meta, f, indent=2)
    print(f"[OK] Saved feature metadata JSON at {meta_json_path}")
    
    return csv_store_path, parquet_store_path

if __name__ == "__main__":
    build_feature_store()
