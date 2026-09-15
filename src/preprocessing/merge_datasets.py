"""
Dataset Merger & Feature Store Generator
Consolidates processed spatial-temporal features across all 38 Tamil Nadu districts,
demographic indices, precipitation, terrain elevation, and disaster records into `final_dataset.csv`
and generates train/validation/test splits.
"""

import os
import pandas as pd
import numpy as np

PROCESSED_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\processed"

def merge_all_datasets():
    """
    Consolidates cleaned datasets into final dataset across all 38 districts of Tamil Nadu.
    """
    print("[Merge Datasets] Starting feature fusion across all 38 Tamil Nadu districts...")
    
    # Load processed components
    f_emdat = os.path.join(PROCESSED_DIR, "cleaned_emdat.csv")
    f_imd = os.path.join(PROCESSED_DIR, "cleaned_imd.csv")
    f_census = os.path.join(PROCESSED_DIR, "cleaned_census.csv")
    f_worldpop = os.path.join(PROCESSED_DIR, "cleaned_worldpop.csv")
    f_dem = os.path.join(PROCESSED_DIR, "cleaned_dem.csv")
    f_osm = os.path.join(PROCESSED_DIR, "cleaned_osm.csv")
    
    # Run individual cleaners if any component is missing
    for file_path, clean_fn in [
        (f_emdat, "src.preprocessing.clean_emdat"),
        (f_imd, "src.preprocessing.clean_imd"),
        (f_census, "src.preprocessing.clean_census"),
        (f_worldpop, "src.preprocessing.clean_worldpop"),
        (f_dem, "src.preprocessing.clean_dem"),
        (f_osm, "src.preprocessing.clean_osm"),
    ]:
        if not os.path.exists(file_path):
            mod_name, func_name = clean_fn.rsplit(".", 1)
            import importlib
            mod = importlib.import_module(mod_name)
            getattr(mod, func_name)()

    df_emdat = pd.read_csv(f_emdat)
    df_census = pd.read_csv(f_census)
    df_imd = pd.read_csv(f_imd)
    df_worldpop = pd.read_csv(f_worldpop)
    df_dem = pd.read_csv(f_dem)
    
    merged_records = []
    
    # Mean recent 7-day precipitation metric
    mean_7d_precip = df_imd["rolling_7d_precip_mm"].mean() if "rolling_7d_precip_mm" in df_imd.columns else 45.0
    heavy_rain_days = df_imd["heavy_rainfall_flag"].sum() if "heavy_rainfall_flag" in df_imd.columns else 12
    
    for idx, row in df_census.iterrows():
        district = row["district"]
        
        # Match worldpop
        wp_match = df_worldpop[df_worldpop["district"].str.lower() == district.lower()]
        pop_density = wp_match["density_per_sq_km"].values[0] if len(wp_match) > 0 else 500.0
        pop_2020 = wp_match["population_2020"].values[0] if len(wp_match) > 0 else 1500000
        
        # Match dem
        dem_match = df_dem[df_dem["district"].str.lower() == district.lower()]
        elevation = dem_match["elevation_m"].values[0] if len(dem_match) > 0 else 75.0
        
        # Match emdat historical impact score
        emdat_match = df_emdat[df_emdat["location"].str.contains(district, case=False, na=False)]
        hist_deaths = emdat_match["total_deaths"].sum() if len(emdat_match) > 0 else 0
        hist_affected = emdat_match["total_affected"].sum() if len(emdat_match) > 0 else 10000
        
        # Target variable: Secondary Disaster Cascade Risk Index (0.0 to 1.0)
        # Higher density, lower elevation, high rainfall & high vulnerability -> higher cascade risk
        elev_risk_factor = max(0.0, (100.0 - min(100.0, elevation)) / 100.0)
        vuln_score = row.get("composite_vulnerability_index", 15.0) / 30.0
        
        cascade_risk = round(min(0.99, max(0.05, 
            0.35 * vuln_score + 
            0.30 * elev_risk_factor + 
            0.20 * min(1.0, pop_density / 25000.0) + 
            0.15 * min(1.0, mean_7d_precip / 100.0)
        )), 4)
        
        merged_records.append({
            "district_id": idx + 1,
            "district": district,
            "population": pop_2020,
            "pop_density_per_sq_km": pop_density,
            "elevation_m": elevation,
            "recent_7d_precip_mm": round(mean_7d_precip, 2),
            "heavy_rain_event_count": heavy_rain_days,
            "slum_pop_pct": row.get("slum_pop_pct", 15.0),
            "pukka_housing_pct": row.get("pukka_housing_pct", 75.0),
            "vulnerability_score": row.get("vulnerability_score", 0.5),
            "composite_vulnerability_index": row.get("composite_vulnerability_index", 15.0),
            "historical_disaster_deaths": hist_deaths,
            "historical_affected": hist_affected,
            "cascade_risk_score": cascade_risk,
            "secondary_disaster_triggered": 1 if cascade_risk >= 0.50 else 0
        })
        
    df_final = pd.DataFrame(merged_records)
    
    # Save final dataset
    final_file = os.path.join(PROCESSED_DIR, "final_dataset.csv")
    df_final.to_csv(final_file, index=False)
    print(f"[Merge Datasets] Created master final_dataset.csv with {len(df_final)} rows and {len(df_final.columns)} columns across all 38 districts.")
    
    # Split into train (70%), validation (15%), test (15%)
    shuffled = df_final.sample(frac=1.0, random_state=42).reset_index(drop=True)
    n = len(shuffled)
    n_train = int(n * 0.70)
    n_val = int(n * 0.15)
    
    train_df = shuffled.iloc[:n_train]
    val_df = shuffled.iloc[n_train:n_train + n_val]
    test_df = shuffled.iloc[n_train + n_val:]
    
    train_df.to_csv(os.path.join(PROCESSED_DIR, "train.csv"), index=False)
    val_df.to_csv(os.path.join(PROCESSED_DIR, "validation.csv"), index=False)
    test_df.to_csv(os.path.join(PROCESSED_DIR, "test.csv"), index=False)
    
    print(f"[Merge Datasets] Generated splits: Train ({len(train_df)}), Validation ({len(val_df)}), Test ({len(test_df)}).")
    return final_file

if __name__ == "__main__":
    merge_all_datasets()
