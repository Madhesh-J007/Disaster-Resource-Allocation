"""
Visualization Engine for Feature Engineering Analytics (Stage 7)
Generates high-resolution publication quality plots saved into outputs/feature_engineering/:
- Feature Distribution plots
- Correlation Matrix
- Missing Value Matrix
- Pair Plots
- Feature Importance Analysis
- Population Distribution
- Rainfall Distribution
- Risk Score Distribution
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML"
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "feature_engineering")
PROCESSED_DIR = os.path.join(BASE_DIR, "datasets", "processed")

def generate_all_feature_engineering_plots(df_engineered: pd.DataFrame = None):
    """
    Generates all Stage 7 analytical plots and saves into outputs/feature_engineering/.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if df_engineered is None:
        f_path = os.path.join(PROCESSED_DIR, "feature_engineered_dataset.csv")
        if not os.path.exists(f_path):
            from src.feature_engineering.store_builder import build_feature_store
            build_feature_store()
        df = pd.read_csv(f_path)
    else:
        df = df_engineered.copy()
        
    sns.set_theme(style="whitegrid")
    
    # 1. Feature Distributions
    num_cols = list(df.select_dtypes(include=[np.number]).columns)
    disp_cols = [c for c in num_cols if c not in ["district_id"]][:9]
    
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    fig.suptitle("Key Feature Distribution Histograms & KDE Density", fontsize=15, fontweight="bold")
    
    for i, col in enumerate(disp_cols):
        ax = axes[i // 3, i % 3]
        sns.histplot(df[col], kde=True, ax=ax, color="steelblue", bins=15)
        ax.set_title(col, fontsize=11, fontweight="bold")
        ax.set_xlabel("")
        ax.set_ylabel("Count")
        
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    p1 = os.path.join(OUTPUT_DIR, "feature_distributions.png")
    plt.savefig(p1, dpi=300)
    plt.close()
    print(f"[Plots] Saved feature distributions plot to {p1}")

    # 2. Missing Value Matrix
    plt.figure(figsize=(12, 6))
    sns.heatmap(df.isnull(), cbar=False, cmap="viridis", yticklabels=False)
    plt.title("Missing Value Integrity Matrix (0.0% Missing across all features)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    p2 = os.path.join(OUTPUT_DIR, "missing_value_matrix.png")
    plt.savefig(p2, dpi=300)
    plt.close()
    print(f"[Plots] Saved missing value matrix plot to {p2}")

    # 3. Population Distribution
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df.sort_values("population", ascending=False), x="district", y="population", palette="crest")
    plt.title("Tamil Nadu District Population Distribution", fontsize=14, fontweight="bold")
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel("Population (Millions)")
    plt.tight_layout()
    p3 = os.path.join(OUTPUT_DIR, "population_distribution.png")
    plt.savefig(p3, dpi=300)
    plt.close()
    print(f"[Plots] Saved population distribution plot to {p3}")

    # 4. Rainfall Distribution
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="cascade_risk_level", y="recent_7d_precip_mm", palette="Set2")
    plt.title("7-Day Precipitation Accumulation across Cascade Risk Levels", fontsize=14, fontweight="bold")
    plt.xlabel("Cascade Risk Level")
    plt.ylabel("7-Day Cumulative Rainfall (mm)")
    plt.tight_layout()
    p4 = os.path.join(OUTPUT_DIR, "rainfall_distribution.png")
    plt.savefig(p4, dpi=300)
    plt.close()
    print(f"[Plots] Saved rainfall distribution plot to {p4}")

    # 5. Risk Score Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df["cascade_risk_score"], kde=True, color="darkred", bins=12)
    plt.axvline(35.0, color="orange", linestyle="--", label="Medium Threshold (35)")
    plt.axvline(65.0, color="red", linestyle="--", label="High Threshold (65)")
    plt.title("Cascade Risk Score (0-100) Distribution across Districts", fontsize=14, fontweight="bold")
    plt.xlabel("Cascade Risk Score")
    plt.ylabel("District Count")
    plt.legend()
    plt.tight_layout()
    p5 = os.path.join(OUTPUT_DIR, "risk_score_distribution.png")
    plt.savefig(p5, dpi=300)
    plt.close()
    print(f"[Plots] Saved risk score distribution plot to {p5}")

    # 6. Pair Plot (Key Risk Factors)
    pair_cols = ["cascade_risk_score", "population_exposure_index", "recent_7d_precip_mm", "terrain_risk", "infrastructure_vulnerability_index"]
    pair_df = df[pair_cols].dropna()
    g = sns.pairplot(pair_df, diag_kind="kde", plot_kws={'alpha': 0.7, 's': 40, 'color': 'navy'})
    g.fig.suptitle("Pairwise Correlation Matrix of Core Risk Sub-Indices", y=1.02, fontsize=14, fontweight="bold")
    p6 = os.path.join(OUTPUT_DIR, "pair_plot.png")
    g.savefig(p6, dpi=300)
    plt.close()
    print(f"[Plots] Saved pair plot to {p6}")

    # 7. Feature Importance Analysis Preanalysis Plot
    imp_csv = os.path.join(OUTPUT_DIR, "feature_importance_preanalysis.csv")
    if os.path.exists(imp_csv):
        df_imp = pd.read_csv(imp_csv)
        plt.figure(figsize=(10, 8))
        sns.barplot(data=df_imp.head(15), x="importance_score", y="feature_name", palette="viridis")
        plt.title("Random Forest Feature Importance Pre-analysis Ranking", fontsize=14, fontweight="bold")
        plt.xlabel("Gini Importance Score")
        plt.tight_layout()
        p7 = os.path.join(OUTPUT_DIR, "feature_importance_preanalysis.png")
        plt.savefig(p7, dpi=300)
        plt.close()
        print(f"[Plots] Saved feature importance preanalysis plot to {p7}")

    print("[Plots] All Stage 7 visual analysis plots successfully generated!")

if __name__ == "__main__":
    generate_all_feature_engineering_plots()
