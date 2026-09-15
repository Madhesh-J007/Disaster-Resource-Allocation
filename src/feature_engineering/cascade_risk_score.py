"""
Composite Feature & Target Generator (Stage 2F)
Derives composite vulnerability indices, Version 1 Target Variable (Cascade Risk Score),
and exports datasets/metadata/feature_engineering_dictionary.xlsx.
"""

import os
import numpy as np
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML"
METADATA_DIR = os.path.join(BASE_DIR, "datasets", "metadata")

def compute_composite_features_and_target(df_fused: pd.DataFrame) -> pd.DataFrame:
    """
    Computes 9 scientific composite indices, Target Variable (Cascade Risk Score 0-100), and cascade_risk_level.
    """
    df = df_fused.copy()
    
    # Normalize helper (0 to 1 scaling)
    def min_max(series):
        s_min, s_max = series.min(), series.max()
        return (series - s_min) / (s_max - s_min + 1e-6)

    # 1. Infrastructure Vulnerability Index (0-1)
    # High if low infrastructure density relative to high population
    df["infrastructure_vulnerability_index"] = (
        0.5 * (1.0 - min_max(df["infrastructure_density"])) +
        0.5 * min_max(df["slum_pop_pct"])
    ).round(4)

    # 2. Population Exposure Index (0-1)
    df["population_exposure_index"] = (
        0.6 * min_max(df["population_density"]) +
        0.4 * min_max(df["slum_pop_pct"])
    ).round(4)

    # 3. Disaster Severity Score (0-1)
    df["disaster_severity_score"] = (
        0.5 * min_max(df["historical_casualty_score"]) +
        0.5 * min_max(df["historical_damage_score"])
    ).round(4)

    # 4. Infrastructure Resilience Score (0-1)
    df["infrastructure_resilience_score"] = (
        0.6 * min_max(df["pukka_housing_pct"]) +
        0.4 * min_max(df["emergency_service_density"])
    ).round(4)

    # 5. Emergency Preparedness Score (0-1)
    df["emergency_preparedness_score"] = (
        0.5 * min_max(df["hospital_density"]) +
        0.5 * min_max(df["fire_station_density"])
    ).round(4)

    # 6. Resource Demand Score (0-1)
    df["resource_demand_score"] = (
        0.5 * min_max(df["population"]) +
        0.5 * df["population_exposure_index"]
    ).round(4)

    # 7. Accessibility Index (0-1)
    df["accessibility_index"] = (
        0.7 * min_max(df["road_density"]) +
        0.3 * (1.0 - min_max(df["terrain_risk"]))
    ).round(4)

    # 8. Flood Exposure Score (0-1)
    df["flood_exposure_score"] = (
        0.6 * min_max(df["recent_7d_precip_mm"]) +
        0.4 * df["low_lying_area_flag"]
    ).round(4)

    # 9. Terrain Vulnerability Score (0-1)
    df["terrain_vulnerability_score"] = df["terrain_risk"].round(4)

    # =========================================================================
    # TARGET VARIABLE DEFINITION (Cascade Risk Score 0–100 & Risk Level)
    # =========================================================================
    # Weighted composite index:
    # W1 (0.25): Rainfall & Flood Exposure
    # W2 (0.25): Population Exposure
    # W3 (0.20): Terrain Vulnerability
    # W4 (0.15): Disaster Severity History
    # W5 (0.15): Infrastructure Vulnerability (1 - Resilience)
    
    raw_cascade_score = (
        25.0 * df["flood_exposure_score"] +
        25.0 * df["population_exposure_index"] +
        20.0 * df["terrain_vulnerability_score"] +
        15.0 * df["disaster_severity_score"] +
        15.0 * df["infrastructure_vulnerability_index"]
    )
    
    # Scale continuous target between 0.0 and 100.0
    df["cascade_risk_score"] = np.round(np.clip(raw_cascade_score, 0.0, 100.0), 2)
    
    # Categorical Risk Level Classes: LOW (<35), MEDIUM (35-65), HIGH (>65)
    def classify_risk(score):
        if score < 35.0:
            return "LOW"
        elif score <= 65.0:
            return "MEDIUM"
        else:
            return "HIGH"
            
    df["cascade_risk_level"] = df["cascade_risk_score"].apply(classify_risk)
    
    return df

def generate_feature_dictionary_excel():
    """
    Generates datasets/metadata/feature_engineering_dictionary.xlsx documenting all engineered features.
    """
    os.makedirs(METADATA_DIR, exist_ok=True)
    dict_path = os.path.join(METADATA_DIR, "feature_engineering_dictionary.xlsx")
    
    feature_doc_entries = [
        {
            "Feature Group": "Weather Features",
            "Feature Name": "rainfall_intensity",
            "Formula / Derivation": "precipitation_mm / max(1, precipitation_hours)",
            "Source Columns": "precipitation_mm, precipitation_hours",
            "Scientific Reasoning": "Measures hourly cloudburst rate. High intensity (>15mm/hr) triggers rapid surface runoff before soil infiltration.",
            "Expected Impact on ML": "Strong positive predictor for flash flood & urban drainage collapse."
        },
        {
            "Feature Group": "Weather Features",
            "Feature Name": "rolling_3day_rainfall",
            "Formula / Derivation": "Sum(precipitation_mm, 3-day rolling window)",
            "Source Columns": "precipitation_mm, date",
            "Scientific Reasoning": "Captures short-term cumulative ground saturation preceding sudden secondary landslides.",
            "Expected Impact on ML": "Predicts short-term slope instability and river overflow risk."
        },
        {
            "Feature Group": "Weather Features",
            "Feature Name": "rolling_7day_rainfall",
            "Formula / Derivation": "Sum(precipitation_mm, 7-day rolling window)",
            "Source Columns": "precipitation_mm, date",
            "Scientific Reasoning": "Measures long-term basin saturation causing regional river inundation and dam capacity stress.",
            "Expected Impact on ML": "Primary input for secondary regional inundation cascades."
        },
        {
            "Feature Group": "Weather Features",
            "Feature Name": "rainfall_anomaly",
            "Formula / Derivation": "precipitation_mm - Mean(precipitation_mm)",
            "Source Columns": "precipitation_mm",
            "Scientific Reasoning": "Quantifies extreme deviation from localized historical climatic norms.",
            "Expected Impact on ML": "Identifies unseasonable extreme rainfall events triggering un-prepared infrastructure failure."
        },
        {
            "Feature Group": "Terrain Features",
            "Feature Name": "derived_slope_deg",
            "Formula / Derivation": "degrees(arctan(|elev - mean_elev| / 40,000m))",
            "Source Columns": "elevation_m",
            "Scientific Reasoning": "Quantifies topographic gradient variance. High slope increases landslide risk; low slope traps flood waters.",
            "Expected Impact on ML": "Differentiates inundation plains from landslide hazard zones."
        },
        {
            "Feature Group": "Terrain Features",
            "Feature Name": "terrain_risk",
            "Formula / Derivation": "Composite risk function based on low elevation (<15m) or high slope (>2°)",
            "Source Columns": "elevation_m, derived_slope_deg",
            "Scientific Reasoning": "Integrates low-lying coastal surge risk and mountain slope instability into a unified spatial vulnerability index.",
            "Expected Impact on ML": "High feature importance for secondary disaster propagation mapping."
        },
        {
            "Feature Group": "Terrain Features",
            "Feature Name": "low_lying_area_flag",
            "Formula / Derivation": "1 if elevation_m <= 15 else 0",
            "Source Columns": "elevation_m",
            "Scientific Reasoning": "Binary spatial mask for low coastal/river basin zones prone to backwater inundation.",
            "Expected Impact on ML": "Key categorical feature for flood cascade classification."
        },
        {
            "Feature Group": "Population Features",
            "Feature Name": "population_exposure_index",
            "Formula / Derivation": "0.6 * Norm(pop_density) + 0.4 * Norm(slum_pop_pct)",
            "Source Columns": "population_density, slum_pop_pct",
            "Scientific Reasoning": "Combines human settlement density with informal housing vulnerability to quantify casualty exposure.",
            "Expected Impact on ML": "High weight in predicting emergency relief demand and human impact."
        },
        {
            "Feature Group": "Population Features",
            "Feature Name": "urban_pressure_index",
            "Formula / Derivation": "(urban_pct / 100) * log1p(population_density)",
            "Source Columns": "urban_pct, population_density",
            "Scientific Reasoning": "Captures urban infrastructure stress where impermeable surfaces accelerate runoff.",
            "Expected Impact on ML": "Predicts urban flash flood and secondary power grid disruption."
        },
        {
            "Feature Group": "Infrastructure Features",
            "Feature Name": "infrastructure_density",
            "Formula / Derivation": "(critical_infrastructure_count * 20) / area_sq_km",
            "Source Columns": "critical_infrastructure_count, area_sq_km",
            "Scientific Reasoning": "Measures spatial concentration of life-line assets (hospitals, power, stations).",
            "Expected Impact on ML": "Predicts asset exposure and potential inter-dependent network failure nodes."
        },
        {
            "Feature Group": "Infrastructure Features",
            "Feature Name": "emergency_service_density",
            "Formula / Derivation": "((hospital_count + fire_count) * 10) / area_sq_km",
            "Source Columns": "hospital_density, fire_station_density",
            "Scientific Reasoning": "Quantifies localized rapid-response capacity during disaster events.",
            "Expected Impact on ML": "Inverse predictor for casualty escalation and unmitigated secondary risk."
        },
        {
            "Feature Group": "Disaster History",
            "Feature Name": "historical_severity_index",
            "Formula / Derivation": "0.4 * Norm(freq) + 0.3 * Norm(casualty_score) + 0.3 * Norm(damage_score)",
            "Source Columns": "disaster_frequency, historical_casualty_score, historical_damage_score",
            "Scientific Reasoning": "Aggregates multi-decadal disaster impact history from EM-DAT CRED data.",
            "Expected Impact on ML": "Prior probability baseline for secondary disaster vulnerability."
        },
        {
            "Feature Group": "Composite Indices",
            "Feature Name": "infrastructure_vulnerability_index",
            "Formula / Derivation": "0.5 * (1 - Norm(infra_density)) + 0.5 * Norm(slum_pop_pct)",
            "Source Columns": "infrastructure_density, slum_pop_pct",
            "Scientific Reasoning": "Quantifies structural fragility resulting from low asset coverage and poor housing quality.",
            "Expected Impact on ML": "Direct input for secondary cascade likelihood."
        },
        {
            "Feature Group": "Composite Indices",
            "Feature Name": "accessibility_index",
            "Formula / Derivation": "0.7 * Norm(road_density) + 0.3 * (1 - Norm(terrain_risk))",
            "Source Columns": "road_density, terrain_risk",
            "Scientific Reasoning": "Measures transportation network connectivity for emergency evacuation.",
            "Expected Impact on ML": "Predicts evacuation bottlenecks and resource allocation delay."
        },
        {
            "Feature Group": "Target Variable",
            "Feature Name": "cascade_risk_score",
            "Formula / Derivation": "25*Flood_Exp + 25*Pop_Exp + 20*Terrain_Vuln + 15*Disaster_Sev + 15*Infra_Vuln",
            "Source Columns": "flood_exposure_score, population_exposure_index, terrain_vulnerability_score, disaster_severity_score, infrastructure_vulnerability_index",
            "Scientific Reasoning": "Continuous 0-100 master risk score combining physical hazards, terrain geometry, human exposure, and asset fragility.",
            "Expected Impact on ML": "Continuous target variable for regression models in Phase 4."
        },
        {
            "Feature Group": "Target Variable",
            "Feature Name": "cascade_risk_level",
            "Formula / Derivation": "LOW (<35), MEDIUM (35-65), HIGH (>65)",
            "Source Columns": "cascade_risk_score",
            "Scientific Reasoning": "Categorical risk classification for multi-class ML models.",
            "Expected Impact on ML": "Categorical target variable for Random Forest / XGBoost classifiers."
        }
    ]
    
    df_dict = pd.DataFrame(feature_doc_entries)
    
    with pd.ExcelWriter(dict_path, engine="openpyxl") as writer:
        df_dict.to_excel(writer, sheet_name="Feature Dictionary", index=False)
        
    wb = openpyxl.load_workbook(dict_path)
    ws = wb["Feature Dictionary"]
    
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    cell_font = Font(name="Calibri", size=10)
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'), right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'), bottom=Side(style='thin', color='D9D9D9')
    )
    
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font = cell_font
            cell.border = thin_border
            cell.alignment = Alignment(vertical="center")
            
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 55)
        
    wb.save(dict_path)
    print(f"[Feature Dictionary] Saved feature engineering dictionary Excel workbook at {dict_path}")
    return dict_path

if __name__ == "__main__":
    generate_feature_dictionary_excel()
