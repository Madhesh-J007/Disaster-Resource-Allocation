"""
Main Pipeline Orchestrator (Phase 1 & Phase 2 Complete)
Secondary Disaster Chain Reaction Management System

Orchestrates:
Phase 1: Data Collection, Preprocessing, Fusion, and Validation
Phase 2: Feature Engineering, Data Profiling, Normalization, Feature Store Generation, Target Definition, and Visual Analysis
"""

import sys
import os

# Ensure project root is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Phase 1 Data Collection
from src.data_collection.download_eonet import download_eonet_events
from src.data_collection.download_reliefweb import download_reliefweb_data
from src.data_collection.download_osm import download_osm_infrastructure
from src.data_collection.download_worldpop import download_worldpop_data
from src.data_collection.download_dem import download_dem_data
from src.data_collection.download_imd import download_imd_rainfall_data
from src.data_collection.download_emdat import download_emdat_data
from src.data_collection.download_census import download_census_data
from src.data_collection.download_bhuvan import download_bhuvan_data

# Phase 1 Preprocessing & Validation
from src.preprocessing.clean_eonet import clean_eonet_data
from src.preprocessing.clean_reliefweb import clean_reliefweb_data
from src.preprocessing.clean_osm import clean_osm_data
from src.preprocessing.clean_worldpop import clean_worldpop_data
from src.preprocessing.clean_dem import clean_dem_data
from src.preprocessing.clean_imd import clean_imd_data
from src.preprocessing.clean_emdat import clean_emdat_data
from src.preprocessing.clean_census import clean_census_data
from src.preprocessing.merge_datasets import merge_all_datasets
from src.utils.generate_excel_docs import generate_all_excel_docs
from src.utils.validate_all import validate_all_and_generate_metadata

# Phase 2 Feature Engineering
from src.feature_engineering.store_builder import build_feature_store
from src.visualization.plots import generate_all_feature_engineering_plots

def run_full_pipeline():
    """Executes end-to-end Phase 1 + Phase 2 pipeline."""
    print("=======================================================================")
    print("   SECONDARY DISASTER CHAIN REACTION ML - PHASE 1 & 2 PIPELINE START   ")
    print("=======================================================================\n")
    
    # ---------------------------------------------------------
    # PHASE 1: DATA PIPELINE & PREPROCESSING
    # ---------------------------------------------------------
    print("--- [PHASE 1 - STEP 1/3] Data Collection ---")
    download_eonet_events()
    download_reliefweb_data()
    download_osm_infrastructure()
    download_worldpop_data()
    download_dem_data()
    download_imd_rainfall_data()
    download_emdat_data()
    download_census_data()
    download_bhuvan_data()
    print("[OK] Data collection completed.\n")
    
    print("--- [PHASE 1 - STEP 2/3] Data Preprocessing & Fusion ---")
    clean_eonet_data()
    clean_reliefweb_data()
    clean_osm_data()
    clean_worldpop_data()
    clean_dem_data()
    clean_imd_data()
    clean_emdat_data()
    clean_census_data()
    merge_all_datasets()
    print("[OK] Preprocessing and base dataset fusion completed.\n")
    
    print("--- [PHASE 1 - STEP 3/3] Validation & Documentation ---")
    generate_all_excel_docs()
    validate_all_and_generate_metadata()
    print("[OK] Phase 1 verification completed.\n")

    # ---------------------------------------------------------
    # PHASE 2: FEATURE ENGINEERING & STORE BUILDER
    # ---------------------------------------------------------
    print("--- [PHASE 2 - STEP 1/2] Feature Engineering & Feature Store Generation ---")
    build_feature_store()
    print("[OK] Feature Store built (.csv, .parquet, feature_profile.xlsx, feature_engineering_dictionary.xlsx).\n")
    
    print("--- [PHASE 2 - STEP 2/2] Visual Analysis & Plot Generation ---")
    generate_all_feature_engineering_plots()
    print("[OK] Visual analysis plots generated in outputs/feature_engineering/.\n")

    print("=======================================================================")
    print("[OK] PHASE 2 FEATURE ENGINEERING COMPLETED SUCCESSFULLY!")
    print("     REPOSITORY IS FULLY PREPARED FOR PHASE 3 (NETWORKX GRAPH) & PHASE 4 (ML)")
    print("=======================================================================")

if __name__ == "__main__":
    run_full_pipeline()
