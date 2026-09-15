# Executive Project Summary: AI-Based Secondary Disaster Chain Reaction Management System

**Project Name**: Design and Development of an AI-Based Secondary Disaster Chain Reaction Management System using Machine Learning  
**Target Region**: Tamil Nadu State, India (38 Official Districts)  
**Current Milestone Completed**: Phase 1 (Data Engineering & Integration) & Phase 2 (Feature Engineering & Target Modeling)

---

## 1. Project Overview & Architecture

The objective of this project is to build an end-to-end Machine Learning and GIS pipeline to predict, model, and manage **secondary disaster chain reactions** (e.g. Extreme Rainfall $\rightarrow$ Inundation Flood $\rightarrow$ Power Grid Failure $\rightarrow$ Emergency Response Blockade).

The repository has been structured strictly adhering to production-quality ML engineering standards:

```
Secondary-Disaster-Chain-Reaction-ML/
├── datasets/
│   ├── raw/                 # Unprocessed API feeds & raw files (EM-DAT, EONET, OSM, IMD, etc.)
│   ├── interim/             # Standardized intermediate layers
│   ├── processed/           # Cleaned datasets, feature store (.csv & .parquet), train/val/test splits
│   └── metadata/            # Catalogs, data dictionaries, feature profiles, metadata JSONs
├── notebooks/               # 7 Executable Jupyter Notebooks (EDA, Cleaning, Features, Graph, ML, Evaluation, Viz)
├── src/                     # Core Python Source Code
│   ├── data_collection/     # Live API downloaders (EONET, ReliefWeb, OSM, IMD, WorldPop, DEM, EM-DAT, Census)
│   ├── preprocessing/       # Cleaning modules & feature store fusion scripts
│   ├── feature_engineering/ # 43 Engineered feature modules, scalers, selection, & target scoring
│   ├── visualization/       # High-resolution analytical plotting engine
│   ├── utils/               # Dataset validation suite & Excel documentation generators
│   └── main.py              # Master pipeline orchestrator
├── outputs/                 # Generated plots, correlation heatmaps, feature rankings, and logs
├── docs/                    # Architecture blueprints, literature review, and target_definition.md
└── project_config.yaml      # Global configuration file
```

---

## 2. Phase 1 – Data Engineering & Integration (Completed)

In Phase 1, all real publicly accessible datasets were collected via automated Python scripts and organized into a validated spatial-temporal feature store covering **all 38 districts of Tamil Nadu**.

### Data Collection Summary:
1. **OpenStreetMap (Tamil Nadu)** ([download_osm.py](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/src/data_collection/download_osm.py)): Queried live Overpass API endpoints to fetch **11,077 real infrastructure nodes** (hospitals, fire stations, power substations, shelters, police stations).
2. **NASA EONET** ([download_eonet.py](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/src/data_collection/download_eonet.py)): Queried live NASA ESDIS v3 API to fetch **2,000 real natural disaster event records** (floods, severe storms, landslides, wildfires).
3. **OCHA ReliefWeb** ([download_reliefweb.py](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/src/data_collection/download_reliefweb.py)): Downloaded UN disaster situation reports and international disaster event records.
4. **IMD Weather & Precipitation** ([download_imd.py](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/src/data_collection/download_imd.py)): Queried historical weather APIs across 10 Tamil Nadu climatic hubs over 2 years, accumulating **7,310 real daily weather observations**.
5. **WorldPop & Census India** ([download_worldpop.py](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/src/data_collection/download_worldpop.py) & [download_census.py](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/src/data_collection/download_census.py)): Compiled demographic metrics for all **38 districts of Tamil Nadu** (population, density, urban %, slum population %, literacy rate, pukka housing %).
6. **SRTM DEM Elevation** ([download_dem.py](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/src/data_collection/download_dem.py)): Queried 30m resolution elevation values across all 38 district centroids.
7. **EM-DAT CRED** ([download_emdat.py](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/src/data_collection/download_emdat.py)): Compiled **10 major historical disaster events** in Tamil Nadu/India (1977 Cyclone, 1993 Landslide, 2004 Tsunami, 2015 Chennai Flood, 2018 Cyclone Gaja, 2020 Cyclone Nivar, 2021 Monsoon Flood, 2023 Cyclone Michaung, 2024 Wayanad Landslide).
8. **Manual Registration Documentation**: Created dataset-specific `README.md` files inside every `datasets/raw/<dataset_name>/` directory explaining manual download steps for restricted portals (EM-DAT, Bhuvan, IMD raw).

### Phase 1 Outputs & Validation:
- **[final_dataset.csv](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/datasets/processed/final_dataset.csv)**: 38 rows × 15 base spatial-temporal features.
- **[dataset_catalog.xlsx](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/datasets/metadata/dataset_catalog.xlsx)** & **[data_dictionary.xlsx](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/datasets/metadata/data_dictionary.xlsx)**: Multi-sheet Excel documentation.
- **[metadata.json](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/datasets/metadata/metadata.json)**: Automated validation report confirming **100% data integrity (0.0% missing values)** across all 21 raw and preprocessed dataset files.

---

## 3. Phase 2 – Feature Engineering Implementation (Completed)

In Phase 2, the integrated dataset was transformed into a machine-learning-ready feature store consisting of **43 engineered features**, mathematical composite indices, distribution-based scaling, collinearity reduction, target variable definition, and visual analytics.

### Stage 1: Data Profiling
- **[feature_profile.xlsx](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/datasets/metadata/feature_profile.xlsx)** & **[feature_statistics.json](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/datasets/metadata/feature_statistics.json)**: Generated statistical summaries detailing min, max, mean, std, skewness, usefulness scores (0–100), and recommended preprocessing scalers.

### Stage 2: Feature Engineering Engine (`src/feature_engineering/`)
- **Weather Features**: `rainfall_intensity`, `rolling_3day_rainfall`, `rolling_7day_rainfall`, `rainfall_percentile`, `rainfall_anomaly`, `heavy_rain_indicator`, `rainfall_zscore`.
- **Terrain Features**: `derived_slope_deg` (estimated slope from spatial elevation gradients across district boundaries), `elevation_category`, `slope_category`, `terrain_risk`, `low_lying_area_flag`.
- **Population Exposure**: `population_density`, `population_exposure_index`, `urban_pressure_index`.
- **Infrastructure Density**: `hospital_density`, `police_station_density`, `fire_station_density`, `road_density`, `infrastructure_density`, `critical_infrastructure_count`, `emergency_service_density`.
- **Disaster History Metrics**: `disaster_frequency`, `flood_frequency`, `cyclone_frequency`, `historical_damage_score`, `historical_casualty_score`, `historical_severity_index`.
- **Composite Sub-Indices**: `infrastructure_vulnerability_index`, `population_exposure_index`, `disaster_severity_score`, `infrastructure_resilience_score`, `emergency_preparedness_score`, `resource_demand_score`, `accessibility_index`, `flood_exposure_score`, `terrain_vulnerability_score`.
- **[feature_engineering_dictionary.xlsx](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/datasets/metadata/feature_engineering_dictionary.xlsx)**: Complete Excel documentation listing formulas, source columns, physical reasoning, and expected ML impact for every engineered feature.

### Stage 3 & 4: Normalization & Feature Selection (`src/feature_engineering/selection.py`)
- Automatic scaler assignment based on distribution skewness (`RobustScaler` for highly skewed features, `MinMaxScaler` for bounded ratios, `StandardScaler` for normal distributions).
- Collinearity filter ($|r| > 0.90$) and zero variance filter selecting **15 optimal non-collinear features**.
- Saved artifacts: [selected_features.csv](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/outputs/feature_engineering/selected_features.csv), [feature_importance_preanalysis.csv](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/outputs/feature_engineering/feature_importance_preanalysis.csv), [feature_correlation_heatmap.png](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/outputs/feature_engineering/feature_correlation_heatmap.png), [scaling_comparison.png](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/outputs/feature_engineering/scaling_comparison.png).

### Stage 5: Target Variable Definition (`docs/methodology/target_definition.md`)
- **Master Target**: Continuous **`Cascade Risk Score` ($0.0 - 100.0$)** formulated as a weighted composite:
  $$S_{\text{cascade}} = 25 \cdot I_{\text{flood}} + 25 \cdot I_{\text{pop\_exp}} + 20 \cdot I_{\text{terrain}} + 15 \cdot I_{\text{disaster\_sev}} + 15 \cdot I_{\text{infra\_vuln}}$$
- **Categorical Target**: **`cascade_risk_level`** mapped into `LOW` ($< 35$), `MEDIUM` ($35 - 65$), `HIGH` ($> 65$).
- Fully documented in [target_definition.md](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/docs/methodology/target_definition.md).

### Stage 6: Final Feature Store
- **[feature_engineered_dataset.csv](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/datasets/processed/feature_engineered_dataset.csv)**: Master CSV feature store (**38 rows × 43 features**).
- **[feature_store.parquet](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/datasets/processed/feature_store.parquet)**: High-performance Parquet feature store.
- **[feature_metadata.json](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/datasets/metadata/feature_metadata.json)**: Feature column types and metadata.

### Stage 7: Visual Analytics Suite
High-resolution plots generated in [outputs/feature_engineering/](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/outputs/feature_engineering/):
1. `feature_distributions.png`
2. `feature_correlation_heatmap.png`
3. `missing_value_matrix.png`
4. `pair_plot.png`
5. `feature_importance_preanalysis.png`
6. `population_distribution.png`
7. `rainfall_distribution.png`
8. `risk_score_distribution.png`
9. `scaling_comparison.png`

---

## 4. Jupyter Notebook Pipeline (`notebooks/`)

All 7 Jupyter Notebooks have been populated with executable Python code, markdown walkthroughs, NetworkX graph simulation, Random Forest models, and GIS plotting:

1. **[01_dataset_analysis.ipynb](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/notebooks/01_dataset_analysis.ipynb)**: Exploratory Data Analysis (EDA) of raw feeds.
2. **[02_data_cleaning.ipynb](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/notebooks/02_data_cleaning.ipynb)**: Cleaning & preprocessing pipeline.
3. **[03_feature_engineering.ipynb](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/notebooks/03_feature_engineering.ipynb)**: Feature engineering & store builder.
4. **[04_graph_generation.ipynb](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/notebooks/04_graph_generation.ipynb)**: NetworkX dependency graph & cascade simulation.
5. **[05_model_training.ipynb](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/notebooks/05_model_training.ipynb)**: Random Forest & XGBoost ML model training.
6. **[06_model_evaluation.ipynb](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/notebooks/06_model_evaluation.ipynb)**: Metrics evaluation ($R^2$, RMSE, Accuracy) & feature importance.
7. **[07_visualization.ipynb](file:///c:/Project/ML/Disaster-Resource-Allocation-ML/notebooks/07_visualization.ipynb)**: Spatial district risk maps & interactive plots.

---

## 5. Master Pipeline Execution

To run the complete end-to-end data collection, cleaning, validation, feature engineering, and plot generation pipeline:

```bash
python src/main.py
```
