# Target Variable Specification: Secondary Disaster Cascade Risk Index

**Project**: Design and Development of an AI-Based Secondary Disaster Chain Reaction Management System using Machine Learning

---

## 1. Executive Overview

The target variable for Version 1 of the Secondary Disaster Chain Reaction ML System is the **Cascade Risk Score** ($S_{\text{cascade}}$), a continuous index bounded between $0.0$ and $100.0$. In addition, a 3-class categorical label (**`cascade_risk_level`**) is derived for multi-class machine learning classification models (e.g. Random Forest and XGBoost classifiers).

> [!IMPORTANT]
> **Data Integrity Directive**: As per project guidelines, no actual disaster outcome labels have been artificially fabricated. The target variable is an engineered, multi-factorial risk index based strictly on physical hazard exposure, terrain topography, socio-economic vulnerability, historical disaster severity, and critical infrastructure resilience.

---

## 2. Mathematical Formulation & Weighting Schema

The master continuous target variable $S_{\text{cascade}} \in [0.0, 100.0]$ is formulated as a weighted linear combination of 5 normalized domain sub-indices:

$$\text{Cascade Risk Score} = \sum_{i=1}^{5} w_i \cdot I_i \cdot 100$$

Where the sub-indices $I_i \in [0.0, 1.0]$ and corresponding weights $w_i$ are specified as follows:

| Index Symbol ($I_i$) | Sub-Index Name | Domain Scope | Weight ($w_i$) | Physical & Mathematical Rationale |
| :--- | :--- | :--- | :--- | :--- |
| $I_{\text{flood}}$ | **Flood & Hydro Exposure** | Meteorological | **0.25** (25%) | Combines 7-day cumulative rainfall accumulation ($0.6$) and low-lying elevation flag ($0.4$). Triggers secondary inundation. |
| $I_{\text{pop\_exp}}$ | **Population Exposure** | Demographics | **0.25** (25%) | Combines population density ($0.6$) and slum habitation ratio ($0.4$). High density amplifies human casualty risk. |
| $I_{\text{terrain}}$ | **Terrain Vulnerability** | Topography | **0.20** (20%) | Evaluates low-lying coastal flood inundation plains ($<15$m elevation) and steep mountain landslide slope zones ($>2^\circ$). |
| $I_{\text{disaster\_sev}}$ | **Disaster Severity History** | EM-DAT CRED | **0.15** (15%) | Aggregates multi-decadal historical disaster death tolls, affected population counts, and financial damage logs. |
| $I_{\text{infra\_vuln}}$ | **Infrastructure Fragility** | OpenStreetMap | **0.15** (15%) | Inverse of infrastructure resilience; measures low lifeline asset density relative to high structural slum exposure. |

$$\text{Cascade Risk Score} = 25 \cdot I_{\text{flood}} + 25 \cdot I_{\text{pop\_exp}} + 20 \cdot I_{\text{terrain}} + 15 \cdot I_{\text{disaster\_sev}} + 15 \cdot I_{\text{infra\_vuln}}$$

---

## 3. Categorical Risk Classification Thresholds

For classification models, $S_{\text{cascade}}$ is mapped into 3 discrete risk levels:

$$\text{cascade\_risk\_level} = \begin{cases} \text{LOW} & \text{if } S_{\text{cascade}} < 35.0 \\ \text{MEDIUM} & \text{if } 35.0 \le S_{\text{cascade}} \le 65.0 \\ \text{HIGH} & \text{if } S_{\text{cascade}} > 65.0 \end{cases}$$

### Class Definitions:
1. **`LOW` (Score < 35.0)**: Low physical hazard exposure, high terrain elevation, low population density, and high infrastructure resilience. Low secondary disaster propagation likelihood.
2. **`MEDIUM` (Score 35.0 – 65.0)**: Moderate precipitation anomaly or moderate urban density. Requires routine emergency monitoring.
3. **`HIGH` (Score > 65.0)**: High coastal/riverine flood exposure, high slum population density, low terrain elevation, and high historical disaster impact. High probability of secondary disaster chain reaction (e.g. Flood $\rightarrow$ Power Substation Failure $\rightarrow$ Emergency Hospital Access Blockade).

---

## 4. Key Assumptions & Limitations

### Assumptions:
1. **Equal Weighting across Core Hazards**: Weights $w_i$ reflect equal priority between immediate meteorological triggers (25%) and human exposure (25%), supported by topography (20%), asset vulnerability (15%), and historical prior probability (15%).
2. **Continuous Normalization**: All sub-indices are scaled min-max to $[0, 1]$ before weighted aggregation to prevent unit dominance.

### Limitations:
1. **Static Spatial Boundaries**: Aggregation is currently executed at the district spatial resolution ($N=38$ districts across Tamil Nadu). Higher spatial resolution (sub-district / 100m grid) will be implemented in future iterations.
2. **Surrogate Target Nature**: In Version 1, $S_{\text{cascade}}$ acts as an engineered proxy risk index. In subsequent phases (Phases 3 & 4), NetworkX graph centrality metrics and dynamic cascade propagation simulations will refine the target dynamically.
