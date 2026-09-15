import os
import json
import numpy as np
import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

from explainability import generate_explanations
from resource_engine import calculate_resource_allocation

app = FastAPI(
    title="AI-Based Secondary Disaster Chain Reaction Management System",
    description="Machine Learning API for Secondary Disaster Chain Reaction & Resource Allocation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE_DIR, "models")

disaster_model = None
severity_model = None
preprocessor = None
metrics_data = {}

def load_artifacts():
    global disaster_model, severity_model, preprocessor, metrics_data
    try:
        disaster_model_path = os.path.join(MODELS_DIR, "disaster_model.joblib")
        severity_model_path = os.path.join(MODELS_DIR, "severity_model.joblib")
        preprocessor_path = os.path.join(MODELS_DIR, "preprocessor.joblib")
        metrics_path = os.path.join(MODELS_DIR, "metrics.json")
        
        if os.path.exists(disaster_model_path):
            disaster_model = joblib.load(disaster_model_path)
            severity_model = joblib.load(severity_model_path)
            preprocessor = joblib.load(preprocessor_path)
            
        if os.path.exists(metrics_path):
            with open(metrics_path, "r") as f:
                metrics_data = json.load(f)
        print("ML Models & Artifacts loaded successfully.")
    except Exception as e:
        print(f"Warning loading artifacts: {e}")

@app.on_event("startup")
def startup_event():
    load_artifacts()

class DisasterConditions(BaseModel):
    rainfall_mm: float = Field(..., example=220.0, ge=0)
    river_level_m: float = Field(..., example=8.5, ge=0)
    soil_moisture: float = Field(..., example=0.85, ge=0, le=1.0)
    wind_speed_kmph: float = Field(..., example=25.0, ge=0)
    temperature_c: float = Field(..., example=28.0)
    population_density: float = Field(..., example=8500.0, ge=0)
    elevation_m: float = Field(..., example=120.0, ge=0)
    infrastructure_vulnerability: float = Field(..., example=0.65, ge=0, le=1.0)
    road_accessibility: float = Field(..., example=0.70, ge=0, le=1.0)
    distance_to_water_body: float = Field(..., example=0.8, ge=0)
    primary_disaster: str = Field(..., example="Heavy Rain")

class ResourceAllocationInput(BaseModel):
    predicted_disaster: str
    severity: str
    risk_score: int
    population_density: float

class SimulationInput(BaseModel):
    baseline: DisasterConditions
    modified: DisasterConditions

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Secondary Disaster Chain Management API",
        "models_loaded": disaster_model is not None,
        "dataset_records": metrics_data.get("dataset_size", 3500)
    }

@app.get("/statistics")
def get_statistics():
    if not metrics_data:
        raise HTTPException(status_code=404, detail="Metrics not found. Please train models first.")
    return metrics_data

@app.get("/demo-scenarios")
def get_demo_scenarios():
    return {
        "scenarios": [
            {
                "id": "scenario_1",
                "name": "Scenario 1: Severe Flood Risk",
                "description": "Torrential rain, river stage overflow, saturated soil, urban river basin",
                "expected": "Flood (High / Critical)",
                "data": {
                    "rainfall_mm": 280.0,
                    "river_level_m": 9.5,
                    "soil_moisture": 0.92,
                    "wind_speed_kmph": 20.0,
                    "temperature_c": 24.0,
                    "population_density": 9500.0,
                    "elevation_m": 15.0,
                    "infrastructure_vulnerability": 0.70,
                    "road_accessibility": 0.60,
                    "distance_to_water_body": 0.3,
                    "primary_disaster": "Heavy Rain"
                }
            },
            {
                "id": "scenario_2",
                "name": "Scenario 2: Landslide Risk",
                "description": "High slope elevation, waterlogged soil, poor access roads, heavy hill rainfall",
                "expected": "Landslide (High)",
                "data": {
                    "rainfall_mm": 180.0,
                    "river_level_m": 3.0,
                    "soil_moisture": 0.88,
                    "wind_speed_kmph": 35.0,
                    "temperature_c": 20.0,
                    "population_density": 1200.0,
                    "elevation_m": 850.0,
                    "infrastructure_vulnerability": 0.50,
                    "road_accessibility": 0.25,
                    "distance_to_water_body": 4.5,
                    "primary_disaster": "Landslide Trigger"
                }
            },
            {
                "id": "scenario_3",
                "name": "Scenario 3: Infrastructure Failure",
                "description": "Category 3 cyclone winds, high infrastructure vulnerability, dense population",
                "expected": "Infrastructure Failure (Critical)",
                "data": {
                    "rainfall_mm": 45.0,
                    "river_level_m": 2.1,
                    "soil_moisture": 0.35,
                    "wind_speed_kmph": 115.0,
                    "temperature_c": 29.0,
                    "population_density": 12000.0,
                    "elevation_m": 45.0,
                    "infrastructure_vulnerability": 0.85,
                    "road_accessibility": 0.50,
                    "distance_to_water_body": 3.0,
                    "primary_disaster": "Cyclone"
                }
            }
        ]
    }

def run_prediction_pipeline(data: DisasterConditions) -> Dict[str, Any]:
    if disaster_model is None or preprocessor is None:
        raise HTTPException(status_code=500, detail="Models not loaded. Train models first using train_models.py")
        
    input_dict = data.dict()
    df_input = pd.DataFrame([input_dict])
    
    # Feature transform
    X_trans = preprocessor.transform(df_input)
    
    # Predict secondary disaster probabilities
    disaster_probs = disaster_model.predict_proba(X_trans)[0]
    disaster_classes = list(disaster_model.classes_)
    
    class_prob_map = {cls: round(float(prob), 4) for cls, prob in zip(disaster_classes, disaster_probs)}
    
    top_idx = int(np.argmax(disaster_probs))
    pred_disaster = disaster_classes[top_idx]
    pred_disaster_prob = round(float(disaster_probs[top_idx]), 4)
    
    # Predict severity
    severity_probs = severity_model.predict_proba(X_trans)[0]
    severity_classes = list(severity_model.classes_)
    top_sev_idx = int(np.argmax(severity_probs))
    pred_severity = severity_classes[top_sev_idx]
    pred_severity_prob = round(float(severity_probs[top_sev_idx]), 4)
    
    # Risk score computation (0 - 100)
    sev_weights = {"Low": 0.3, "Medium": 0.55, "High": 0.8, "Critical": 0.95}
    sev_w = sev_weights.get(pred_severity, 0.6)
    
    raw_risk = (pred_disaster_prob * 55.0) + (sev_w * 30.0) + (data.infrastructure_vulnerability * 15.0)
    risk_score = int(np.clip(round(raw_risk), 10, 99))
    
    # Explainability engine
    exp_res = generate_explanations(input_dict, pred_disaster, risk_score)
    
    return {
        "primary_disaster": data.primary_disaster,
        "predicted_secondary_disaster": pred_disaster,
        "secondary_disaster_probability": pred_disaster_prob,
        "severity": pred_severity,
        "severity_probability": pred_severity_prob,
        "risk_score": risk_score,
        "class_probabilities": class_prob_map,
        "explanation": exp_res["explanations"],
        "top_contributing_factors": exp_res["top_contributing_factors"],
        "input_conditions": input_dict
    }

@app.post("/predict")
def predict_secondary_disaster(data: DisasterConditions):
    return run_prediction_pipeline(data)

@app.post("/resource-allocation")
def allocate_resources(input_data: ResourceAllocationInput):
    return calculate_resource_allocation(
        predicted_disaster=input_data.predicted_disaster,
        severity=input_data.severity,
        risk_score=input_data.risk_score,
        population_density=input_data.population_density
    )

@app.post("/simulate")
def run_simulation(sim_input: SimulationInput):
    res_base = run_prediction_pipeline(sim_input.baseline)
    res_mod = run_prediction_pipeline(sim_input.modified)
    
    delta_risk = res_mod["risk_score"] - res_base["risk_score"]
    
    return {
        "baseline": {
            "predicted_secondary_disaster": res_base["predicted_secondary_disaster"],
            "severity": res_base["severity"],
            "risk_score": res_base["risk_score"],
            "secondary_disaster_probability": res_base["secondary_disaster_probability"]
        },
        "modified": {
            "predicted_secondary_disaster": res_mod["predicted_secondary_disaster"],
            "severity": res_mod["severity"],
            "risk_score": res_mod["risk_score"],
            "secondary_disaster_probability": res_mod["secondary_disaster_probability"]
        },
        "delta_risk_score": delta_risk,
        "impact_summary": f"Risk score shifted by {delta_risk:+d} points ({res_base['risk_score']} → {res_mod['risk_score']}). Predicted disaster: {res_mod['predicted_secondary_disaster']}."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
