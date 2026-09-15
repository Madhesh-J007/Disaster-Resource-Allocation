"""
Disaster History Feature Engineering Module (Stage 2E)
Derives historical disaster impact features from EM-DAT CRED data:
- disaster_frequency
- flood_frequency
- cyclone_frequency
- historical_damage_score
- historical_casualty_score
- historical_severity_index
"""

import numpy as np
import pandas as pd

def compute_disaster_history_features(df_emdat: pd.DataFrame, district_list: list) -> pd.DataFrame:
    """
    Computes historical disaster metrics per district from EM-DAT database records.
    """
    history_records = []
    
    for district in district_list:
        # Match district location in EM-DAT records
        matches = df_emdat[df_emdat["location"].str.contains(district, case=False, na=False)] if "location" in df_emdat.columns else pd.DataFrame()
        
        disaster_freq = len(matches)
        
        floods = len(matches[matches["disaster_type"].str.contains("flood", case=False, na=False)]) if not matches.empty else 0
        cyclones = len(matches[matches["disaster_type"].str.contains("storm|cyclone", case=False, na=False)]) if not matches.empty else 0
        
        tot_deaths = matches["total_deaths"].sum() if not matches.empty and "total_deaths" in matches.columns else 0
        tot_affected = matches["total_affected"].sum() if not matches.empty and "total_affected" in matches.columns else 0
        tot_damages = matches["total_damages_usd_thousands"].sum() if not matches.empty and "total_damages_usd_thousands" in matches.columns else 0
        
        # Log scale scores
        damage_score = round(np.log1p(float(tot_damages)), 4)
        casualty_score = round(np.log1p(float(tot_deaths * 10 + tot_affected / 100)), 4)
        
        # Composite Historical Severity Index
        severity_index = round(min(1.0, 0.4 * (disaster_freq / 5.0) + 0.3 * (casualty_score / 12.0) + 0.3 * (damage_score / 15.0)), 4)
        
        history_records.append({
            "district": district,
            "disaster_frequency": disaster_freq,
            "flood_frequency": floods,
            "cyclone_frequency": cyclones,
            "historical_damage_score": damage_score,
            "historical_casualty_score": casualty_score,
            "historical_severity_index": severity_index
        })
        
    return pd.DataFrame(history_records)
