# Machine Learning Methodology & Resource Engine

This document provides a comprehensive technical overview of the machine learning methodology, synthetic data generation logic, model training procedures, empirical evaluation results, explainability engine, and resource allocation mechanics.

---

## 1. Synthetic Dataset Generation

### 1.1 Rationale
Real-world multi-hazard secondary disaster datasets with high-granularity environmental, geographical, and demographic features are extremely sparse, fragmented, or restricted across public repositories. To construct a working end-to-end prototype, a synthetic dataset generator (`backend/generate_data.py`) was implemented using domain-inspired physical principles.

### 1.2 Dataset Overview
- **Total Records**: 3,500 rows
- **Input Features**: 11 features (10 numerical continuous/discrete, 1 categorical)
- **Target Variables**: 
  - `secondary_disaster` (5 categorical classes: `Flood`, `Landslide`, `Infrastructure Failure`, `Fire`, `Disease Outbreak`)
  - `severity` (4 categorical classes: `Low`, `Medium`, `High`, `Critical`)

### 1.3 Feature Specifications

| Feature Name | Type | Range / Scale | Description |
| :--- | :--- | :--- | :--- |
| `rainfall_mm` | Float | 0.0 – 380.0 mm | Cumulative 24-hour precipitation depth |
| `river_level_m` | Float | 0.5 – 11.5 m | River gauge stage height above baseline |
| `soil_moisture` | Float | 0.05 – 0.98 | Volumetric soil water saturation fraction |
| `wind_speed_kmph` | Float | 5.0 – 155.0 km/h | Peak sustained wind speed |
| `temperature_c` | Float | 14.0 – 48.0 °C | Ambient surface air temperature |
| `population_density` | Float | 100 – 18,000 /km² | Human population concentration per square km |
| `elevation_m` | Float | 5.0 – 2,400.0 m | Terrain elevation above sea level |
| `infrastructure_vulnerability` | Float | 0.05 – 0.95 | Composite structural vulnerability index |
| `road_accessibility` | Float | 0.05 – 0.95 | Evacuation & emergency road access quality index |
| `distance_to_water_body` | Float | 0.1 – 25.0 km | Distance to nearest river or coastline |
| `primary_disaster` | String | Categorical | Primary trigger event (`Heavy Rain`, `Cyclone`, `Earthquake`, `Extreme Heat`, `Landslide Trigger`) |

### 1.4 Ground Truth Target Mapping Formulas
Unnormalized latent score functions with random Gaussian noise $\mathcal{N}(0, 0.03^2)$ dictate class selection:

$$S_{\text{flood}} = 0.35 \cdot \frac{\text{rainfall\_mm}}{400} + 0.30 \cdot \frac{\text{river\_level\_m}}{12} + 0.20 \cdot \text{soil\_moisture} + 0.15 \cdot \left(1 - \frac{\text{distance\_to\_water\_body}}{25}\right) + 0.20 \cdot \mathbb{I}_{\text{Heavy Rain}} + \epsilon$$

$$S_{\text{landslide}} = 0.35 \cdot \text{soil\_moisture} + 0.30 \cdot \frac{\text{elevation\_m}}{2400} + 0.20 \cdot \frac{\text{rainfall\_mm}}{400} + 0.15 \cdot (1 - \text{road\_accessibility}) + 0.20 \cdot \mathbb{I}_{\text{Landslide Trigger}} + \epsilon$$

$$S_{\text{infra}} = 0.40 \cdot \text{infrastructure\_vulnerability} + 0.35 \cdot \frac{\text{wind\_speed\_kmph}}{160} + 0.15 \cdot \frac{\text{population\_density}}{18000} + 0.10 \cdot (1 - \text{road\_accessibility}) + 0.20 \cdot \mathbb{I}_{\text{Cyclone}} + \epsilon$$

$$S_{\text{fire}} = 0.40 \cdot \frac{\text{temperature\_c}}{48} + 0.30 \cdot (1 - \text{soil\_moisture}) + 0.15 \cdot \frac{\text{population\_density}}{18000} + 0.15 \cdot \text{infrastructure\_vulnerability} + 0.20 \cdot \mathbb{I}_{\text{Extreme Heat}} + \epsilon$$

$$S_{\text{disease}} = 0.35 \cdot \frac{\text{population\_density}}{18000} + 0.25 \cdot \text{soil\_moisture} + 0.20 \cdot \frac{\text{temperature\_c}}{48} + 0.20 \cdot (1 - \text{road\_accessibility}) + 0.15 \cdot \mathbb{I}_{\text{Heavy Rain}} + \epsilon$$

The predicted target is assigned as $\text{secondary\_disaster} = \arg\max_k (S_k)$.

---

## 2. Preprocessing & Model Architecture

### 2.1 Preprocessing Pipeline
- **Numerical Feature Scaling**: `StandardScaler()` standardizes numeric inputs to zero mean and unit variance ($\mu=0, \sigma=1$).
- **Categorical Encoding**: `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` expands `primary_disaster` into binary dummy columns.
- **Train/Test Split**: Stratified 80% training set (2,800 rows) and 20% test set (700 rows) using `random_state=42`.

### 2.2 Model Architecture
1. **Secondary Disaster Model**: `RandomForestClassifier(n_estimators=120, max_depth=12, random_state=42)`.
2. **Cascade Severity Model**: `RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)`.

*Why Random Forest?*
- Non-parametric handling of non-linear feature interactions (e.g. high rainfall combined with low distance to water body).
- Robustness against multicollinearity and feature scale variances.
- Native calculation of Gini impurity-based feature importances.
- Low-latency batch and single-sample inference suitable for interactive APIs.

---

## 3. Empirical Model Evaluation

Evaluated on the 700 held-out test samples:

### 3.1 Overall Performance Summary

| Model Target | Accuracy | Weighted Precision | Weighted Recall | Weighted F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| **Secondary Disaster Classifier** | **92.4%** | **92.9%** | **92.4%** | **91.4%** |
| **Cascade Severity Classifier** | **82.4%** | **84.1%** | **82.4%** | **80.9%** |

### 3.2 Secondary Disaster Classification Report

| Target Class | Support | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| **Disease Outbreak** | 21 | 1.00 | 0.10 | 0.17 |
| **Fire** | 183 | 0.92 | 0.98 | 0.95 |
| **Flood** | 220 | 0.94 | 0.91 | 0.92 |
| **Infrastructure Failure** | 149 | 0.86 | 0.97 | 0.91 |
| **Landslide** | 127 | 0.99 | 0.95 | 0.97 |
| **Weighted Average** | **700** | **0.93** | **0.92** | **0.91** |

---

## 4. Explainability & Resource Allocation Engine

### 4.1 Explainability Engine (`backend/explainability.py`)
Rather than black-box approximations, the system implements a transparent factor-impact engine combining input parameter thresholds and model feature importances. Key trigger rules evaluate rainfall depth ($>100$ mm, $>200$ mm), soil moisture ($>60\%$, $>80\%$), wind speed ($>50$ km/h, $>90$ km/h), infrastructure vulnerability ($>65\%$), and road accessibility ($<35\%$).

### 4.2 Resource Allocation Mechanics (`backend/resource_engine.py`)
Calculates required emergency resources using:

$$\text{Demand}_r = \text{Round}\left( \text{BaseDemand}_{r, d} \times \text{SevMult}_s \times \sqrt{\frac{\text{PopDensity}}{3500}} \times \sqrt{\frac{\text{RiskScore}}{65}} \right)$$

Where:
- $\text{SevMult} \in \{ \text{Low}: 0.5, \text{Medium}: 1.0, \text{High}: 1.7, \text{Critical}: 2.5 \}$
- $\text{Allocated}_r = \min(\text{Required}_r, \text{Available}_r)$
- $\text{Shortage}_r = \max(0, \text{Required}_r - \text{Available}_r)$
