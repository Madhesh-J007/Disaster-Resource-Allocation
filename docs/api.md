# REST API Reference Manual

The **AI Secondary Disaster Management System** backend is implemented using FastAPI. When running the server (`python app.py` or `uvicorn app:app --reload`), interactive OpenAPI Swagger documentation is accessible at `http://127.0.0.1:8000/docs`.

---

## Endpoint Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Check service health, model load state, and dataset count |
| `POST` | `/predict` | Predict secondary disaster, severity level, risk score, and transparent explanations |
| `GET` | `/statistics` | Retrieve model evaluation metrics, class distributions, and confusion matrix |
| `POST` | `/resource-allocation` | Compute required vs available emergency resource quantities |
| `POST` | `/simulate` | Compare baseline (Scenario A) vs modified (Scenario B) counterfactual risks |
| `GET` | `/demo-scenarios` | Retrieve preconfigured demo test cases |

---

## Detailed Endpoint Specifications

### 1. GET `/health`
Check API operational status.

**Response `200 OK`**:
```json
{
  "status": "healthy",
  "service": "AI Secondary Disaster Chain Management API",
  "models_loaded": true,
  "dataset_records": 3500
}
```

---

### 2. POST `/predict`
Predict secondary disaster chain reaction, severity, risk score, class probabilities, and transparent factor explanations.

**Request Body**:
```json
{
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
```

**Response `200 OK`**:
```json
{
  "primary_disaster": "Heavy Rain",
  "predicted_secondary_disaster": "Flood",
  "secondary_disaster_probability": 0.8533,
  "severity": "High",
  "severity_probability": 0.9675,
  "risk_score": 81,
  "class_probabilities": {
    "Disease Outbreak": 0.0512,
    "Fire": 0.0,
    "Flood": 0.8533,
    "Infrastructure Failure": 0.0955,
    "Landslide": 0.0
  },
  "explanation": [
    "Heavy rainfall (280.0 mm) significantly increases inundation and flash flood risks.",
    "High river gauge level (9.5 m) approaches critical flood stage threshold.",
    "Extremely high soil moisture saturation (92%) severely undermines slope stability.",
    "High infrastructure vulnerability (70%) amplifies cascade structural damage."
  ],
  "top_contributing_factors": [
    {
      "feature": "rainfall_mm",
      "value": 280.0,
      "impact": "Critical Driver"
    },
    {
      "feature": "river_level_m",
      "value": 9.5,
      "impact": "Critical Driver"
    },
    {
      "feature": "soil_moisture",
      "value": 0.92,
      "impact": "Critical Driver"
    },
    {
      "feature": "infrastructure_vulnerability",
      "value": 0.7,
      "impact": "Critical Driver"
    }
  ]
}
```

---

### 3. POST `/resource-allocation`
Compute resource demand allocation and inventory pool matching.

**Request Body**:
```json
{
  "predicted_disaster": "Flood",
  "severity": "High",
  "risk_score": 81,
  "population_density": 9500.0
}
```

**Response `200 OK`**:
```json
{
  "predicted_disaster": "Flood",
  "severity": "High",
  "risk_score": 81,
  "population_density": 9500.0,
  "total_shortage_resources": 6,
  "allocations": [
    {
      "resource": "Ambulances",
      "required": 38,
      "available": 40,
      "allocated": 38,
      "shortage": 0,
      "has_shortage": false,
      "priority": "High",
      "utilization_percent": 95.0
    },
    {
      "resource": "Rescue Teams",
      "required": 48,
      "available": 22,
      "allocated": 22,
      "shortage": 26,
      "has_shortage": true,
      "priority": "Critical Shortage",
      "utilization_percent": 100.0
    },
    {
      "resource": "Rescue Boats",
      "required": 64,
      "available": 25,
      "allocated": 25,
      "shortage": 39,
      "has_shortage": true,
      "priority": "Critical Shortage",
      "utilization_percent": 100.0
    }
  ]
}
```

---

### 4. POST `/simulate`
Compare baseline (Scenario A) vs modified (Scenario B) counterfactual risks.

**Request Body**:
```json
{
  "baseline": {
    "rainfall_mm": 100.0,
    "river_level_m": 4.0,
    "soil_moisture": 0.50,
    "wind_speed_kmph": 30.0,
    "temperature_c": 28.0,
    "population_density": 5000.0,
    "elevation_m": 100.0,
    "infrastructure_vulnerability": 0.40,
    "road_accessibility": 0.80,
    "distance_to_water_body": 3.0,
    "primary_disaster": "Heavy Rain"
  },
  "modified": {
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
}
```

**Response `200 OK`**:
```json
{
  "baseline": {
    "predicted_secondary_disaster": "Flood",
    "severity": "Medium",
    "risk_score": 62,
    "secondary_disaster_probability": 0.7201
  },
  "modified": {
    "predicted_secondary_disaster": "Flood",
    "severity": "High",
    "risk_score": 81,
    "secondary_disaster_probability": 0.8533
  },
  "delta_risk_score": 19,
  "impact_summary": "Risk score shifted by +19 points (62 -> 81). Predicted disaster: Flood."
}
```
