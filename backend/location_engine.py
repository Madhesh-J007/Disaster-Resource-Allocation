import os
import pandas as pd
import numpy as np

# Path to Tamil Nadu feature store
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, 'datasets', 'processed', 'feature_engineered_dataset.csv')

district_store = {}

def load_district_feature_store():
    global district_store
    if os.path.exists(DATASET_PATH):
        try:
            df = pd.read_csv(DATASET_PATH)
            for _, row in df.iterrows():
                d_name = row['district']
                district_store[d_name] = row.to_dict()
            print(f"Successfully loaded {len(district_store)} Tamil Nadu districts from feature store.")
        except Exception as e:
            print(f"Error loading district feature store: {e}")
    else:
        print(f"Warning: Feature store file not found at {DATASET_PATH}")

load_district_feature_store()

def get_all_districts():
    if not district_store:
        load_district_feature_store()
    
    district_list = []
    for d_name, d_data in district_store.items():
        district_list.append({
            "district": d_name,
            "population": int(d_data.get("population", 0)),
            "population_density": float(d_data.get("pop_density_per_sq_km", d_data.get("population_density", 0))),
            "elevation_m": float(d_data.get("elevation_m", 0)),
            "elevation_category": str(d_data.get("elevation_category", "Coastal")),
            "infrastructure_vulnerability": float(d_data.get("infrastructure_vulnerability_index", 0.5)),
            "accessibility_index": float(d_data.get("accessibility_index", 0.5)),
            "historical_risk_level": str(d_data.get("cascade_risk_level", "MEDIUM")),
            "critical_infrastructure_count": int(d_data.get("critical_infrastructure_count", 0)),
            "hospital_density": float(d_data.get("hospital_density", 0)),
            "low_lying": int(d_data.get("low_lying_area_flag", 0)) == 1
        })
    # Sort with Chennai first as primary demo area
    district_list.sort(key=lambda x: (x["district"] != "Chennai", x["district"]))
    return district_list

def get_district_baseline(district_name: str):
    if not district_store:
        load_district_feature_store()
        
    data = district_store.get(district_name)
    if not data:
        # Fallback to Chennai or default
        data = district_store.get("Chennai", {})
        
    pop_dens = float(data.get("pop_density_per_sq_km", data.get("population_density", 5000)))
    elev = float(data.get("elevation_m", 20))
    infra_vuln = float(data.get("infrastructure_vulnerability_index", 0.55))
    access = float(data.get("accessibility_index", 0.50))
    if access < 0.05:
        # Road accessibility index scaling for 0-1 model input
        road_acc = round(min(0.95, max(0.15, access * 15.0)), 2)
    else:
        road_acc = round(min(0.95, max(0.15, access)), 2)
        
    soil_m = 0.85 if elev < 50 else 0.70
    river_l = 8.5 if elev < 30 else 3.5
    rain_m = float(data.get("recent_7d_precip_mm", 180.0))
    if rain_m < 50:
        rain_m = 220.0 # Standard scenario default for demonstration
        
    return {
        "district": district_name,
        "rainfall_mm": round(rain_m, 1),
        "river_level_m": round(river_l, 1),
        "soil_moisture": round(soil_m, 2),
        "wind_speed_kmph": 35.0,
        "temperature_c": 28.0,
        "population_density": round(pop_dens, 0),
        "elevation_m": round(elev, 1),
        "infrastructure_vulnerability": round(infra_vuln, 2),
        "road_accessibility": road_acc,
        "distance_to_water_body": 0.8 if elev < 30 else 5.0,
        "primary_disaster": "Heavy Rain"
    }

def assess_affected_systems(location: str, primary_disaster: str, secondary_disaster: str, risk_score: int, input_data: dict):
    data = district_store.get(location, {})
    
    pop_dens = float(input_data.get("population_density", data.get("pop_density_per_sq_km", 5000)))
    slum_pct = float(data.get("slum_pop_pct", 15.0))
    access_idx = float(data.get("accessibility_index", input_data.get("road_accessibility", 0.5)))
    crit_count = int(data.get("critical_infrastructure_count", 25))
    hosp_dens = float(data.get("hospital_density", 0.5))
    elev = float(input_data.get("elevation_m", data.get("elevation_m", 20)))
    is_low_lying = int(data.get("low_lying_area_flag", 0)) == 1 or elev < 20
    infra_vuln = float(input_data.get("infrastructure_vulnerability", 0.5))
    
    systems = []
    
    # 1. Population & Residential Exposure
    if pop_dens >= 8000 or slum_pct >= 20:
        pop_level = "HIGH"
        pop_detail = f"High population concentration ({pop_dens:,.0f}/km²) with {slum_pct}% informal housing vulnerability."
    elif pop_dens >= 3000:
        pop_level = "ELEVATED"
        pop_detail = f"Moderate population density ({pop_dens:,.0f}/km²) subject to localized exposure."
    else:
        pop_level = "MODERATE"
        pop_detail = f"Low to moderate population density ({pop_dens:,.0f}/km²)."
        
    systems.append({
        "category": "Population & Residential Exposure",
        "exposure_level": pop_level,
        "detail": pop_detail,
        "metric": f"{pop_dens:,.0f} people/km²"
    })
    
    # 2. Transport & Road Access Network
    if access_idx < 0.20 or input_data.get("road_accessibility", 0.5) < 0.40:
        road_level = "HIGH RISK"
        road_detail = "Restricted road network and low emergency accessibility index create significant transport disruption risks."
    elif access_idx < 0.50:
        road_level = "ELEVATED"
        road_detail = "Moderate accessibility constraints could delay heavy rescue vehicle transit."
    else:
        road_level = "MODERATE"
        road_detail = "Road access network remains stable under current conditions."
        
    systems.append({
        "category": "Roads & Transport Network",
        "exposure_level": road_level,
        "detail": road_detail,
        "metric": f"Access Index: {access_idx:.3f}"
    })
    
    # 3. Critical Infrastructure & Power Nodes
    if infra_vuln >= 0.60 or crit_count >= 30:
        infra_level = "HIGH"
        infra_detail = f"Elevated infrastructure vulnerability ({infra_vuln*100:.0f}%) exposing {crit_count} OSM power/shelter nodes."
    else:
        infra_level = "ELEVATED"
        infra_detail = f"{crit_count} critical infrastructure nodes monitored for secondary impact."
        
    systems.append({
        "category": "Critical Infrastructure & Substation Nodes",
        "exposure_level": infra_level,
        "detail": infra_detail,
        "metric": f"{crit_count} Critical Nodes"
    })
    
    # 4. Healthcare & Emergency Services
    if hosp_dens >= 0.8 or secondary_disaster in ["Flood", "Disease Outbreak"]:
        hosp_level = "ELEVATED"
        hosp_detail = f"Hospital density ({hosp_dens:.2f}/km²) exposed to secondary access friction and surge demand."
    else:
        hosp_level = "MODERATE"
        hosp_detail = f"Medical service density ({hosp_dens:.2f}/km²) operational with baseline capacity."
        
    systems.append({
        "category": "Healthcare & Emergency Response Services",
        "exposure_level": hosp_level,
        "detail": hosp_detail,
        "metric": f"Hospital Density: {hosp_dens:.2f}/km²"
    })
    
    # 5. Terrain & Inundation Risk
    if is_low_lying or secondary_disaster == "Flood":
        terrain_level = "HIGH"
        terrain_detail = f"Low elevation ({elev}m) coastal/basin topography with low-lying inundation vulnerability."
    elif elev >= 600 or secondary_disaster == "Landslide":
        terrain_level = "HIGH RISK"
        terrain_detail = f"Steep slope elevation ({elev}m) subject to saturated terrain shear stress."
    else:
        terrain_level = "MODERATE"
        terrain_detail = f"Terrain elevation ({elev}m) provides baseline drainage capacity."
        
    systems.append({
        "category": "Terrain & Inundation Risk",
        "exposure_level": terrain_level,
        "detail": terrain_detail,
        "metric": f"Elevation: {elev} m"
    })
    
    # Build Cascade Chain Reaction Steps
    cascade_chain = [
        f"PRIMARY EVENT: {primary_disaster.upper()} IN {location.upper()}",
        f"SECONDARY HAZARD TRIGGERED: {secondary_disaster.upper()}",
        f"SEVERITY ESCALATION: {input_data.get('severity', 'HIGH').upper()} (RISK SCORE: {risk_score}/100)",
        f"ROAD ACCESSIBILITY IMPACTED (INDEX: {access_idx:.2f})",
        f"POPULATION EXPOSURE ({pop_dens:,.0f} PEOPLE/KM²)",
        "EMERGENCY RESOURCE ALLOCATION & SHORTAGE ALERT"
    ]
    
    return {
        "potentially_affected_systems": systems,
        "cascade_chain": cascade_chain
    }

def generate_response_priorities(predicted_disaster: str, severity: str, risk_score: int, resource_allocations: list):
    priorities = []
    
    # Extract shortages first
    shortages = [r for r in resource_allocations if r.get("shortage", 0) > 0]
    shortages.sort(key=lambda x: x["shortage"], reverse=True)
    
    rank = 1
    for s in shortages:
        priorities.append({
            "rank": rank,
            "resource": s["resource"],
            "priority": "CRITICAL SHORTAGE",
            "required": s["required"],
            "allocated": s["allocated"],
            "shortage": s["shortage"],
            "reason": f"Required demand ({s['required']}) exceeds available inventory ({s['available']}). Immediate inter-district staging dispatch required."
        })
        rank += 1
        
    # High demand items
    high_demand = [r for r in resource_allocations if r.get("shortage", 0) == 0 and r.get("required", 0) >= 15]
    high_demand.sort(key=lambda x: x["required"], reverse=True)
    
    for h in high_demand:
        if rank <= 5:
            priorities.append({
                "rank": rank,
                "resource": h["resource"],
                "priority": "HIGH DEMAND",
                "required": h["required"],
                "allocated": h["allocated"],
                "shortage": 0,
                "reason": f"High demand ({h['required']} units) fully allocated from local inventory pool."
            })
            rank += 1
            
    return priorities
