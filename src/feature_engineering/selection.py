"""
Feature Normalization, Selection & Correlation Analysis Engine (Stages 3 & 4)
Executes distribution-based scaling, collinearity reduction (|r| > 0.90), feature importance preanalysis,
and saves scaling comparison plots & selection matrices into outputs/feature_engineering/.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.ensemble import RandomForestRegressor

BASE_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML"
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "feature_engineering")
PROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "processed")

def process_normalization_and_selection(df_engineered: pd.DataFrame) -> tuple:
    """
    Executes scaler selection, collinearity filter (|r| > 0.90), preanalysis importance ranking, and saves plots.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = df_engineered.copy()
    
    # Exclude non-feature columns
    non_feature_cols = ["district_id", "district", "cascade_risk_score", "cascade_risk_level", "secondary_disaster_triggered"]
    feature_cols = [c for c in df.columns if c not in non_feature_cols and pd.api.types.is_numeric_dtype(df[c])]
    
    # =========================================================================
    # STAGE 3: FEATURE NORMALIZATION (Distribution-based Scaler Selection)
    # =========================================================================
    scaled_df = df.copy()
    scaler_mapping = {}
    
    fig, axes = plt.subplots(len(feature_cols[:6]), 2, figsize=(12, 3 * len(feature_cols[:6])))
    fig.suptitle("Feature Normalization Comparison (Original vs Scaled)", fontsize=14, fontweight="bold")
    
    for idx, col in enumerate(feature_cols[:6]):
        skewness = df[col].skew()
        vals = df[[col]].values
        
        if abs(skewness) > 1.5:
            scaler = RobustScaler()
            scaler_mapping[col] = "RobustScaler (High Skew)"
        elif df[col].min() >= 0.0 and df[col].max() <= 1.0:
            scaler = MinMaxScaler()
            scaler_mapping[col] = "MinMaxScaler (Bounded 0-1)"
        else:
            scaler = StandardScaler()
            scaler_mapping[col] = "StandardScaler (Gaussian)"
            
        scaled_vals = scaler.fit_transform(vals).flatten()
        scaled_df[col] = scaled_vals
        
        # Plot original vs scaled
        sns.kdeplot(df[col], ax=axes[idx, 0], color="navy", fill=True)
        axes[idx, 0].set_title(f"Original: {col} (Skew: {skewness:.2f})", fontsize=10)
        
        sns.kdeplot(scaled_vals, ax=axes[idx, 1], color="darkgreen", fill=True)
        axes[idx, 1].set_title(f"Scaled: {col} ({scaler_mapping[col]})", fontsize=10)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    scale_plot_path = os.path.join(OUTPUT_DIR, "scaling_comparison.png")
    plt.savefig(scale_plot_path, dpi=300)
    plt.close()
    print(f"[Selection] Saved scaling comparison plot at {scale_plot_path}")

    # =========================================================================
    # STAGE 4: FEATURE SELECTION & COLLINEARITY FILTERING
    # =========================================================================
    corr_matrix = df[feature_cols].corr().abs()
    
    # Generate correlation heatmap
    plt.figure(figsize=(14, 12))
    sns.heatmap(corr_matrix, annot=False, cmap="coolwarm", vmin=0, vmax=1, linewidths=0.5)
    plt.title("Feature Correlation Heatmap Matrix (|r|)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    corr_plot_path = os.path.join(OUTPUT_DIR, "feature_correlation_heatmap.png")
    plt.savefig(corr_plot_path, dpi=300)
    plt.close()
    print(f"[Selection] Saved correlation heatmap plot at {corr_plot_path}")

    # Remove highly correlated features (> 0.90) and low variance (< 1e-4)
    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.90)]
    
    # Check low variance
    low_var_cols = [c for c in feature_cols if df[c].var() < 1e-4]
    to_drop = list(set(to_drop + low_var_cols))
    
    selected_features = [c for c in feature_cols if c not in to_drop]
    print(f"[Selection] Selected {len(selected_features)} features (dropped {len(to_drop)} correlated/low-variance features).")
    
    # Save selected_features.csv
    df_selected_info = pd.DataFrame({
        "feature_name": selected_features,
        "scaler_used": [scaler_mapping.get(f, "StandardScaler") for f in selected_features],
        "variance": [df[f].var() for f in selected_features],
        "skewness": [df[f].skew() for f in selected_features]
    })
    selected_csv_path = os.path.join(OUTPUT_DIR, "selected_features.csv")
    df_selected_info.to_csv(selected_csv_path, index=False)

    # Feature Importance Preanalysis (RandomForest Regressor)
    target = df["cascade_risk_score"]
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(df[selected_features], target)
    
    df_imp = pd.DataFrame({
        "feature_name": selected_features,
        "importance_score": rf.feature_importances_
    }).sort_values("importance_score", ascending=False)
    
    imp_csv_path = os.path.join(OUTPUT_DIR, "feature_importance_preanalysis.csv")
    df_imp.to_csv(imp_csv_path, index=False)
    print(f"[Selection] Saved preanalysis feature importance to {imp_csv_path}")

    return scaled_df, selected_features, df_imp

if __name__ == "__main__":
    from src.preprocessing.merge_datasets import merge_all_datasets
    from src.feature_engineering.cascade_risk_score import compute_composite_features_and_target
    df_base = pd.read_csv(merge_all_datasets())
    df_eng = compute_composite_features_and_target(df_base)
    process_normalization_and_selection(df_eng)
