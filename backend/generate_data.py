import os
import numpy as np
import pandas as pd

def generate_synthetic_data(num_samples=3500, random_seed=42):
    np.random.seed(random_seed)
    
    primary_disasters = ['Heavy Rain', 'Cyclone', 'Earthquake', 'Extreme Heat', 'Landslide Trigger']
    primary_probs = [0.30, 0.25, 0.15, 0.15, 0.15]
    
    primary_disaster_col = np.random.choice(primary_disasters, size=num_samples, p=primary_probs)
    
    rainfall_mm = []
    river_level_m = []
    soil_moisture = []
    wind_speed_kmph = []
    temperature_c = []
    population_density = []
    elevation_m = []
    infrastructure_vulnerability = []
    road_accessibility = []
    distance_to_water_body = []
    
    for pd_type in primary_disaster_col:
        if pd_type == 'Heavy Rain':
            rf = np.random.uniform(50, 380)
            rl = np.random.uniform(2.5, 11.5)
            sm = np.random.uniform(0.40, 0.98)
            ws = np.random.uniform(10, 55)
            temp = np.random.uniform(18, 30)
            elev = np.random.uniform(10, 800)
            dist_w = np.random.uniform(0.1, 8.0)
        elif pd_type == 'Cyclone':
            rf = np.random.uniform(30, 300)
            rl = np.random.uniform(1.5, 9.5)
            sm = np.random.uniform(0.30, 0.90)
            ws = np.random.uniform(60, 155)
            temp = np.random.uniform(22, 33)
            elev = np.random.uniform(5, 400)
            dist_w = np.random.uniform(0.1, 12.0)
        elif pd_type == 'Earthquake':
            rf = np.random.uniform(0, 80)
            rl = np.random.uniform(0.5, 4.0)
            sm = np.random.uniform(0.15, 0.65)
            ws = np.random.uniform(5, 35)
            temp = np.random.uniform(15, 35)
            elev = np.random.uniform(50, 2200)
            dist_w = np.random.uniform(1.0, 20.0)
        elif pd_type == 'Extreme Heat':
            rf = np.random.uniform(0, 15)
            rl = np.random.uniform(0.5, 2.5)
            sm = np.random.uniform(0.05, 0.35)
            ws = np.random.uniform(5, 40)
            temp = np.random.uniform(34, 48)
            elev = np.random.uniform(20, 900)
            dist_w = np.random.uniform(2.0, 25.0)
        else: # Landslide Trigger
            rf = np.random.uniform(40, 280)
            rl = np.random.uniform(1.0, 7.0)
            sm = np.random.uniform(0.50, 0.96)
            ws = np.random.uniform(15, 60)
            temp = np.random.uniform(14, 28)
            elev = np.random.uniform(400, 2400)
            dist_w = np.random.uniform(1.0, 15.0)
            
        pop_dens = np.random.exponential(scale=3200) + 100
        pop_dens = np.clip(pop_dens, 100, 18000)
        
        infra_vuln = np.random.uniform(0.05, 0.95)
        road_acc = np.random.uniform(0.05, 0.95)
        
        rainfall_mm.append(round(rf, 1))
        river_level_m.append(round(rl, 2))
        soil_moisture.append(round(sm, 2))
        wind_speed_kmph.append(round(ws, 1))
        temperature_c.append(round(temp, 1))
        population_density.append(round(pop_dens, 0))
        elevation_m.append(round(elev, 1))
        infrastructure_vulnerability.append(round(infra_vuln, 2))
        road_accessibility.append(round(road_acc, 2))
        distance_to_water_body.append(round(dist_w, 2))
        
    df = pd.DataFrame({
        'rainfall_mm': rainfall_mm,
        'river_level_m': river_level_m,
        'soil_moisture': soil_moisture,
        'wind_speed_kmph': wind_speed_kmph,
        'temperature_c': temperature_c,
        'population_density': population_density,
        'elevation_m': elevation_m,
        'infrastructure_vulnerability': infrastructure_vulnerability,
        'road_accessibility': road_accessibility,
        'distance_to_water_body': distance_to_water_body,
        'primary_disaster': primary_disaster_col
    })
    
    # Calculate physics-inspired risk scores for each secondary disaster class
    s_flood = (
        0.35 * (df['rainfall_mm'] / 400.0) +
        0.30 * (df['river_level_m'] / 12.0) +
        0.20 * df['soil_moisture'] +
        0.15 * (1.0 - df['distance_to_water_body'] / 25.0) +
        (df['primary_disaster'] == 'Heavy Rain') * 0.20 +
        np.random.normal(0, 0.03, num_samples)
    )
    
    s_landslide = (
        0.35 * df['soil_moisture'] +
        0.30 * (df['elevation_m'] / 2400.0) +
        0.20 * (df['rainfall_mm'] / 400.0) +
        0.15 * (1.0 - df['road_accessibility']) +
        (df['primary_disaster'] == 'Landslide Trigger') * 0.20 +
        np.random.normal(0, 0.03, num_samples)
    )
    
    s_infra = (
        0.40 * df['infrastructure_vulnerability'] +
        0.35 * (df['wind_speed_kmph'] / 160.0) +
        0.15 * (df['population_density'] / 18000.0) +
        0.10 * (1.0 - df['road_accessibility']) +
        (df['primary_disaster'] == 'Cyclone') * 0.20 +
        np.random.normal(0, 0.03, num_samples)
    )
    
    s_fire = (
        0.40 * (df['temperature_c'] / 48.0) +
        0.30 * (1.0 - df['soil_moisture']) +
        0.15 * (df['population_density'] / 18000.0) +
        0.15 * df['infrastructure_vulnerability'] +
        (df['primary_disaster'] == 'Extreme Heat') * 0.20 +
        np.random.normal(0, 0.03, num_samples)
    )
    
    s_disease = (
        0.35 * (df['population_density'] / 18000.0) +
        0.25 * df['soil_moisture'] +
        0.20 * (df['temperature_c'] / 48.0) +
        0.20 * (1.0 - df['road_accessibility']) +
        (df['primary_disaster'] == 'Heavy Rain') * 0.15 +
        np.random.normal(0, 0.03, num_samples)
    )
    
    scores = np.column_stack([s_flood, s_landslide, s_infra, s_fire, s_disease])
    disaster_classes = ['Flood', 'Landslide', 'Infrastructure Failure', 'Fire', 'Disease Outbreak']
    
    max_indices = np.argmax(scores, axis=1)
    df['secondary_disaster'] = [disaster_classes[idx] for idx in max_indices]
    
    # Severity calculation based on composite risk
    max_score = np.max(scores, axis=1)
    composite_risk = (
        max_score * 60.0 +
        df['infrastructure_vulnerability'] * 15.0 +
        (df['population_density'] / 18000.0) * 15.0 +
        (1.0 - df['road_accessibility']) * 10.0 +
        np.random.normal(0, 1.5, num_samples)
    )
    
    composite_risk = np.clip(composite_risk, 8, 98)
    
    severity_labels = []
    for risk in composite_risk:
        if risk < 35:
            severity_labels.append('Low')
        elif risk < 55:
            severity_labels.append('Medium')
        elif risk < 75:
            severity_labels.append('High')
        else:
            severity_labels.append('Critical')
            
    df['severity'] = severity_labels
    
    output_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, 'synthetic_disaster_data.csv')
    df.to_csv(file_path, index=False)
    print(f"Successfully generated {len(df)} synthetic disaster records at: {file_path}")
    print("\nSecondary Disaster Distribution:")
    print(df['secondary_disaster'].value_counts())
    print("\nSeverity Distribution:")
    print(df['severity'].value_counts())
    return df

if __name__ == '__main__':
    generate_synthetic_data()
