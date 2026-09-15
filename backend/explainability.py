def generate_explanations(input_data, predicted_disaster, risk_score):
    explanations = []
    contributing_factors = []
    
    rf = input_data.get('rainfall_mm', 0)
    rl = input_data.get('river_level_m', 0)
    sm = input_data.get('soil_moisture', 0)
    ws = input_data.get('wind_speed_kmph', 0)
    temp = input_data.get('temperature_c', 0)
    pop = input_data.get('population_density', 0)
    elev = input_data.get('elevation_m', 0)
    vuln = input_data.get('infrastructure_vulnerability', 0)
    road = input_data.get('road_accessibility', 1.0)
    dist_w = input_data.get('distance_to_water_body', 10.0)
    primary = input_data.get('primary_disaster', 'Heavy Rain')
    
    # Feature specific rules
    if rf >= 200:
        explanations.append(f"Heavy rainfall ({rf} mm) significantly increases inundation and flash flood risks.")
        contributing_factors.append({"feature": "rainfall_mm", "value": rf, "impact": "Critical Driver"})
    elif rf >= 100:
        explanations.append(f"Moderate to high rainfall ({rf} mm) elevates surface runoff and river levels.")
        contributing_factors.append({"feature": "rainfall_mm", "value": rf, "impact": "High Contributor"})
        
    if rl >= 7.0:
        explanations.append(f"High river gauge level ({rl} m) approaches critical flood stage threshold.")
        contributing_factors.append({"feature": "river_level_m", "value": rl, "impact": "Critical Driver"})
    elif rl >= 4.5:
        explanations.append(f"Elevated river level ({rl} m) indicates heightened water volume.")
        contributing_factors.append({"feature": "river_level_m", "value": rl, "impact": "Moderate Influence"})
        
    if sm >= 0.80:
        explanations.append(f"Extremely high soil moisture saturation ({sm*100:.0f}%) severely undermines slope stability.")
        contributing_factors.append({"feature": "soil_moisture", "value": sm, "impact": "Critical Driver"})
    elif sm >= 0.60:
        explanations.append(f"Saturated soil conditions ({sm*100:.0f}%) reduce ground absorption capacity.")
        contributing_factors.append({"feature": "soil_moisture", "value": sm, "impact": "High Contributor"})
        
    if ws >= 90:
        explanations.append(f"Severe wind speeds ({ws} km/h) expose power grids and buildings to collapse.")
        contributing_factors.append({"feature": "wind_speed_kmph", "value": ws, "impact": "Critical Driver"})
    elif ws >= 50:
        explanations.append(f"High gusty winds ({ws} km/h) threaten weak structures and trees.")
        contributing_factors.append({"feature": "wind_speed_kmph", "value": ws, "impact": "Moderate Influence"})
        
    if temp >= 38:
        explanations.append(f"Extreme ambient temperature ({temp}°C) accelerates dry fuel ignition and thermal stress.")
        contributing_factors.append({"feature": "temperature_c", "value": temp, "impact": "Critical Driver"})
        
    if vuln >= 0.65:
        explanations.append(f"High infrastructure vulnerability ({vuln*100:.0f}%) amplifies cascade structural damage.")
        contributing_factors.append({"feature": "infrastructure_vulnerability", "value": vuln, "impact": "Critical Driver"})
        
    if pop >= 7000:
        explanations.append(f"High population density ({pop:,.0f} people/km²) multiplies potential human impact.")
        contributing_factors.append({"feature": "population_density", "value": pop, "impact": "High Contributor"})
        
    if elev >= 600 and (sm >= 0.7 or rf >= 100):
        explanations.append(f"Steep elevation ({elev} m) combined with wet ground triggers debris flow potential.")
        contributing_factors.append({"feature": "elevation_m", "value": elev, "impact": "High Contributor"})
        
    if dist_w <= 1.5:
        explanations.append(f"Close proximity to water bodies ({dist_w} km) heightens immediate spillover threat.")
        contributing_factors.append({"feature": "distance_to_water_body", "value": dist_w, "impact": "High Contributor"})
        
    if road <= 0.35:
        explanations.append(f"Poor road accessibility ({road*100:.0f}%) restricts rapid evacuation and emergency dispatch.")
        contributing_factors.append({"feature": "road_accessibility", "value": road, "impact": "Vulnerability Multiplier"})
        
    # Disaster context explanation fallback
    if not explanations:
        explanations.append(f"Primary event '{primary}' creates moderate secondary chain reaction risks across localized sectors.")
        contributing_factors.append({"feature": "primary_disaster", "value": primary, "impact": "Primary Trigger"})
        
    # Sort factors by impact rank
    rank_map = {"Critical Driver": 1, "Vulnerability Multiplier": 2, "High Contributor": 3, "Moderate Influence": 4, "Primary Trigger": 5}
    contributing_factors.sort(key=lambda x: rank_map.get(x["impact"], 9))
    
    return {
        "explanations": explanations[:4],
        "top_contributing_factors": contributing_factors[:4]
    }
