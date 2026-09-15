"""
Data Profiling & Inspection Engine for Feature Engineering (Stage 1)
Generates feature_profile.xlsx and feature_statistics.json.
"""

import os
import json
import numpy as np
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML"
PROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "processed")
METADATA_DIR = os.path.join(BASE_DIR, "datasets", "metadata")

def profile_dataset():
    """
    Inspects all processed datasets and computes comprehensive statistical profiles.
    """
    os.makedirs(METADATA_DIR, exist_ok=True)
    
    # Target dataset for profiling
    final_file = os.path.join(PROCESSED_DIR, "final_dataset.csv")
    if not os.path.exists(final_file):
        from src.preprocessing.merge_datasets import merge_all_datasets
        merge_all_datasets()
        
    df = pd.read_csv(final_file)
    
    profiles = []
    stats_dict = {}
    
    for col in df.columns:
        series = df[col]
        dtype_str = str(series.dtype)
        null_count = int(series.isnull().sum())
        null_pct = round((null_count / len(series)) * 100, 2)
        unique_vals = int(series.nunique())
        
        is_num = pd.api.types.is_numeric_dtype(series)
        
        if is_num:
            col_min = float(series.min()) if not series.empty else 0.0
            col_max = float(series.max()) if not series.empty else 0.0
            col_mean = float(series.mean()) if not series.empty else 0.0
            col_std = float(series.std()) if not series.empty else 0.0
            col_skew = float(series.skew()) if not series.empty and len(series) > 2 else 0.0
            
            # Recommend scaler based on skewness
            if abs(col_skew) > 1.5:
                rec_prep = "RobustScaler / Log Transform"
            elif col_max <= 1.0 and col_min >= 0.0:
                rec_prep = "None (Already Bounded)"
            else:
                rec_prep = "StandardScaler"
                
            # Usefulness score algorithm (0 - 100)
            usefulness = min(100, max(20, int(100 - (null_pct * 2) - (10 if unique_vals < 3 else 0))))
        else:
            col_min = "N/A"
            col_max = "N/A"
            col_mean = "N/A"
            col_std = "N/A"
            col_skew = "N/A"
            rec_prep = "OneHotEncoder / TargetEncoder"
            usefulness = 70 if unique_vals > 1 else 10

        profiles.append({
            "Feature Name": col,
            "Data Type": dtype_str,
            "Null %": null_pct,
            "Unique Values": unique_vals,
            "Min": col_min,
            "Max": col_max,
            "Mean": round(col_mean, 4) if isinstance(col_mean, float) else col_mean,
            "Std Dev": round(col_std, 4) if isinstance(col_std, float) else col_std,
            "Skewness": round(col_skew, 4) if isinstance(col_skew, float) else col_skew,
            "Usefulness Score (0-100)": usefulness,
            "Recommended Preprocessing": rec_prep
        })
        
        stats_dict[col] = {
            "dtype": dtype_str,
            "null_pct": null_pct,
            "unique_count": unique_vals,
            "min": col_min,
            "max": col_max,
            "mean": col_mean,
            "std": col_std,
            "skewness": col_skew,
            "usefulness_score": usefulness,
            "recommended_preprocessing": rec_prep
        }
        
    df_prof = pd.DataFrame(profiles)
    
    # Save Excel Profile
    excel_path = os.path.join(METADATA_DIR, "feature_profile.xlsx")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_prof.to_excel(writer, sheet_name="Feature Profile", index=False)
        
    wb = openpyxl.load_workbook(excel_path)
    ws = wb["Feature Profile"]
    
    # Styling
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
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 45)
        
    wb.save(excel_path)
    print(f"[Profiling] Saved feature profile Excel workbook at {excel_path}")
    
    # Save JSON Statistics
    json_path = os.path.join(METADATA_DIR, "feature_statistics.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(stats_dict, f, indent=2)
    print(f"[Profiling] Saved feature statistics JSON at {json_path}")
    
    return excel_path, json_path

if __name__ == "__main__":
    profile_dataset()
