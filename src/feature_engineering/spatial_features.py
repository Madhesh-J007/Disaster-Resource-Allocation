"""
Terrain Feature Engineering Module (Stage 2B)
Derives topographic features:
- elevation_category
- slope_category (derived from elevation gradients across district boundaries)
- terrain_risk
- low_lying_area_flag
"""

import numpy as np
import pandas as pd

def compute_spatial_features(df_dem: pd.DataFrame) -> pd.DataFrame:
    """
    Computes derived terrain features from DEM elevation records.
    """
    df = df_dem.copy()
    
    # 1. Elevation Category
    def categorize_elevation(elev):
        if elev <= 15:
            return "Low Coastal (<15m)"
        elif elev <= 100:
            return "Inland Plains (15-100m)"
        elif elev <= 300:
            return "Plateau Zone (100-300m)"
        else:
            return "Hilly/Mountain Zone (>300m)"
            
    df["elevation_category"] = df["elevation_m"].apply(categorize_elevation)
    
    # 2. Derive Slope Category (estimated slope angle in degrees based on spatial elevation variance)
    # Estimate slope theta = arctan(delta_z / distance)
    # Average distance between neighboring Tamil Nadu district centroids ~40 km (40,000 meters)
    elevations = df["elevation_m"].values
    mean_elev = np.mean(elevations)
    elev_diffs = np.abs(elevations - mean_elev)
    estimated_slope_deg = np.degrees(np.arctan(elev_diffs / 40000.0))
    
    df["derived_slope_deg"] = np.round(estimated_slope_deg, 2)
    
    def categorize_slope(deg):
        if deg <= 0.2:
            return "Flat (<0.2°)"
        elif deg <= 0.8:
            return "Gentle Slope (0.2-0.8°)"
        elif deg <= 2.0:
            return "Moderate Slope (0.8-2.0°)"
        else:
            return "Steep Slope (>2.0°)"
            
    df["slope_category"] = df["derived_slope_deg"].apply(categorize_slope)
    
    # 3. Terrain Risk Score (0.0 to 1.0)
    # High risk if low-lying coastal flood plain OR steep landslide hill zone
    def compute_terrain_risk(row):
        elev = row["elevation_m"]
        slope = row["derived_slope_deg"]
        if elev <= 15:
            return round(0.90 + (15 - elev) * 0.005, 3) # Coastal inundation risk
        elif elev > 300:
            return round(0.70 + min(0.25, slope * 0.1), 3) # Landslide risk
        else:
            return round(0.20 + (slope * 0.15), 3)
            
    df["terrain_risk"] = df.apply(compute_terrain_risk, axis=1)
    
    # 4. Low Lying Area Flag (1 if elevation <= 15m else 0)
    df["low_lying_area_flag"] = (df["elevation_m"] <= 15).astype(int)
    
    return df
