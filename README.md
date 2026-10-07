# Location-Aware Secondary Disaster Chain Reaction Management System

> An ML-powered disaster intelligence prototype that predicts potential secondary disaster chain reactions, estimates severity, evaluates potentially affected systems, and recommends emergency resource allocation across Tamil Nadu districts.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-RandomForest-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-6.0-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.style=flat-square)](LICENSE)

---

## ⚠️ Academic Honesty & Data Integrity Notice

> [!IMPORTANT]
> **Data Integrity Statement**:
> 1. **Real-Data Feature Store**: Incorporates a 38-district Tamil Nadu feature store (`datasets/processed/feature_engineered_dataset.csv`) constructed from Census 2011, SRTM DEM elevation grids, OpenStreetMap infrastructure nodes, and IMD rainfall records.
> 2. **ML Prediction Model**: The Random Forest classifiers are trained on a 3,500-record synthetic dataset designed for prototype evaluation.
> 3. **Proof-of-Concept Cascade Graph**: The "What Happens Next?" multi-hazard propagation steps represent conceptual decision-support logic.
> 4. **Do not claim real-world deployment accuracy** for live emergency command without real-time sensor streams and expert validation.

---

## 📍 System Workflow — "What Happens Next?"

```
LOCATION (Select Tamil Nadu District - e.g., Chennai)
   ↓
PRIMARY DISASTER + ENVIRONMENTAL CONDITIONS (Heavy Rainfall)
   ↓
SECONDARY DISASTER PREDICTION (Random Forest ML → Flood)
   ↓
SEVERITY PREDICTION (Critical / High)
   ↓
POTENTIALLY AFFECTED SYSTEMS (Population, Transport, Hospitals, Infra, Terrain)
   ↓
CASCADE CHAIN REACTION PROPAGATION ("What Happens Next?")
   ↓
RESOURCE RESPONSE PLAN (Required vs Available vs Allocated vs Shortage)
   ↓
LOCATION RESPONSE PRIORITIES (Ranked Decision Support)
   ↓
LOCATION WHAT-IF SIMULATOR (Counterfactual Sensitivity Analysis)
```

---

## 📌 Features

1. **Location Impact Assessment**: Select any of the **38 Tamil Nadu districts** (with **Chennai** as the core demonstration area).
2. **Real District Baseline Auto-Population**: Automatically populates real demographic, elevation, infrastructure vulnerability, and transport accessibility parameters.
3. **Secondary Disaster ML Classifier**: Classifies input conditions into 5 secondary disaster categories (`Flood`, `Landslide`, `Infrastructure Failure`, `Fire`, `Disease Outbreak`).
4. **Cascade Severity Estimator**: Evaluates impact across a 4-tier scale (`Low`, `Medium`, `High`, `Critical`).
5. **Potentially Affected Systems**: Assesses exposure levels across 5 critical domains:
   - 👥 *Population & Residential Exposure*
   - 🛣️ *Roads & Transport Network*
   - 🏥 *Healthcare & Emergency Response Services*
   - 🏗️ *Critical Infrastructure & Substation Nodes*
   - 🏔️ *Terrain & Inundation Risk*
6. **"What Happens Next?" Cascade Chain**: Visualizes step-by-step multi-hazard propagation.
7. **Resource Response Plan**: Matches required equipment (Ambulances, Rescue Boats, Medical Kits, Shelters, etc.) against static inventory pools.
8. **Ranked Location Response Priorities**: Decision-support layer prioritizing critical equipment shortages.
9. **Searchable Location Selector**: Searchable 38-district selection with instant filter capabilities.
10. **Location What-If Simulator**: Simulates counterfactual weather escalation (e.g. increasing rainfall in Chennai from 220mm to 350mm).

---

## 📂 Project Structure

```text
Disaster-Resource-Allocation-ML/
│
├── backend/                  # FastAPI web application & ML inference server
│   ├── app.py                # Main FastAPI API routes and middleware
│   ├── location_engine.py    # Tamil Nadu 38-district assessment engine
│   ├── explainability.py      # Transparent risk reasoning calculator
│   ├── resource_engine.py    # Resource allocation & shortage optimizer
│   ├── train_models.py       # Random Forest training script
│   ├── generate_data.py      # Synthetic dataset generator (3,500 records)
│   ├── data/                 # Synthetic disaster dataset CSV
│   └── models/               # Trained ML models (.joblib) & metrics.json
│
├── frontend/                 # React + Vite + Tailwind CSS Command Center UI
│   ├── src/                  # Components, pages, EOC dark theme styles, API services
│   ├── index.html            # Main HTML shell
│   ├── package.json          # Frontend npm package configuration
│   ├── tailwind.config.js    # Tailwind CSS styling configuration
│   └── vite.config.js        # Vite dev server & API proxy configuration
│
├── datasets/                 # Real & synthetic data repository
│   ├── raw/                  # Downloaded raw feeds (EM-DAT, EONET, OSM, IMD, Census, WorldPop, DEM)
│   ├── processed/            # Cleaned CSVs, feature store (.csv & .parquet), train/val/test splits
│   ├── interim/              # Intermediate processing layers
│   └── metadata/             # Data dictionaries, schema, metadata JSONs, dataset catalogs
│
├── src/                      # Core Python data pipeline source code
│   ├── data_collection/      # 9 Live API downloaders (Census, DEM, EM-DAT, EONET, IMD, OSM, etc.)
│   ├── preprocessing/        # Dataset cleaning modules & feature store fusion
│   ├── feature_engineering/  # 43 Feature modules, vulnerability indices, scalers, selection
│   ├── graph/                # Infrastructure dependency network & cascade simulation
│   ├── models/               # ML algorithms (Random Forest, XGBoost, LightGBM)
│   ├── evaluation/           # Metrics, confusion matrix, ROC-AUC, SHAP analysis
│   ├── visualization/        # GIS maps & analytical visualization engine
│   ├── utils/                # Data validation suite & Excel documentation generators
│   └── main.py               # Master real-data pipeline orchestrator
│
├── notebooks/                # Executable Jupyter Notebooks
│   ├── 01_dataset_analysis.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_graph_generation.ipynb
│   ├── 05_model_training.ipynb
│   ├── 06_model_evaluation.ipynb
│   └── 07_visualization.ipynb
│
├── outputs/                  # Generated correlation heatmaps, feature rankings, and distribution plots
├── docs/                     # Architecture documentation, literature review, target definitions
├── deployment/               # Dockerfile, docker-compose.yml, nginx.conf, deployment guides
├── tests/                    # Unit test suite for feature engineering, models, and graph modules
│
├── app.py                    # Root entry point to launch FastAPI backend
├── generate_data.py          # Root wrapper script for synthetic dataset generation
├── train_models.py           # Root wrapper script for model training
├── package.json              # Root npm package configuration with shortcut scripts
├── requirements.txt          # Python dependency specifications
├── environment.yml           # Conda environment configuration
├── project_config.yaml       # Master project parameters and file path configurations
├── PROJECT_SUMMARY.md        # Comprehensive technical & algorithmic project summary
└── README.md                 # Main project README
```

---

## 🚀 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Check service health and dataset counts |
| `GET` | `/districts` | Retrieve metadata for all 38 Tamil Nadu districts |
| `GET` | `/districts/{name}` | Retrieve baseline feature parameters for a specific district |
| `POST` | `/location-impact` | Perform complete location-aware impact assessment |
| `POST` | `/predict` | Single-scenario secondary disaster prediction |
| `POST` | `/resource-allocation` | Resource demand allocation matcher |
| `POST` | `/simulate` | Compare baseline vs modified counterfactual scenarios |
| `GET` | `/demo-scenarios` | Preconfigured regional test cases |

---

## 💻 Quick Start Guide

### 1. Clone & Setup
```bash
git clone https://github.com/Madhesh-J007/Disaster-Resource-Allocation-ML.git
cd Disaster-Resource-Allocation-ML
```

### 2. Python Environment & Installation
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
npm install
```

### 3. Launch Backend API Server
From the root directory:
```cmd
python app.py
# Backend running at: http://127.0.0.1:8000
```

### 4. Launch React Frontend Command Center
In a new terminal, from the root directory:
```cmd
npm run dev
# Frontend running at: http://localhost:5173
```

---

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
