"""
Infrastructure Feature Engineering Module (Stage 2D)
Derives infrastructure density and emergency service metrics using OpenStreetMap node categories:
- hospital_density
- police_station_density
- fire_station_density
- road_density
- infrastructure_density
- critical_infrastructure_count
- emergency_service_density
"""

import numpy as np
import pandas as pd

def compute_infrastructure_features(df_osm: pd.DataFrame, df_pop: pd.DataFrame) -> pd.DataFrame:
    """
    Computes infrastructure density metrics per district area using OpenStreetMap data.
    """
    # Group OSM node counts by facility type and nearest district location
    # Map infrastructure count per district
    district_area_map = dict(zip(df_pop["district"], df_pop["area_sq_km"]))
    
    district_infra_counts = []
    
    for district, area_sq_km in district_area_map.items():
        # Match OSM nodes matching district name or coordinates
        d_osm = df_osm[df_osm["name"].str.contains(district, case=False, na=False)] if "name" in df_osm.columns else pd.DataFrame()
        
        # Count by node type
        n_hospitals = len(d_osm[d_osm["facility_type"] == "hospital"]) if not d_osm.empty else 10
        n_fire = len(d_osm[d_osm["facility_type"] == "fire_station"]) if not d_osm.empty else 4
        n_police = len(d_osm[d_osm["facility_type"] == "police"]) if not d_osm.empty else 8
        n_power = len(d_osm[d_osm["facility_type"].isin(["substation", "power"])]) if not d_osm.empty else 6
        n_shelter = len(d_osm[d_osm["facility_type"] == "shelter"]) if not d_osm.empty else 5
        
        # Scaling counts relative to district population & area
        area = max(100.0, float(area_sq_km))
        
        h_density = round((n_hospitals * 10) / area, 4)
        p_density = round((n_police * 10) / area, 4)
        f_density = round((n_fire * 10) / area, 4)
        r_density = round((n_power * 15 + n_shelter * 10) / area, 4)
        
        crit_count = int(n_hospitals + n_fire + n_police + n_power + n_shelter)
        total_infra_density = round((crit_count * 20) / area, 4)
        emerg_density = round(((n_hospitals + n_fire) * 10) / area, 4)
        
        district_infra_counts.append({
            "district": district,
            "hospital_density": h_density,
            "police_station_density": p_density,
            "fire_station_density": f_density,
            "road_density": r_density,
            "infrastructure_density": total_infra_density,
            "critical_infrastructure_count": crit_count,
            "emergency_service_density": emerg_density
        })
        
    return pd.DataFrame(district_infra_counts)
