# India Meteorological Department (IMD) & Rainfall Dataset

## Dataset Overview
- **Source**: India Meteorological Department (IMD) / Open-Meteo Weather Archive.
- **URL**: [https://www.imdpune.gov.in/](https://www.imdpune.gov.in/) & [https://open-meteo.com/](https://open-meteo.com/)
- **Spatial Coverage**: India / Tamil Nadu state grid (8.0°N to 13.6°N, 76.0°E to 80.5°E).
- **Temporal Coverage**: Daily rainfall (mm), extreme precipitation indicators, and wind metrics.
- **License**: Government Open Data (IMD) / CC-BY 4.0 (Open-Meteo).

## Automated API & Manual IMD Binary Instructions
1. **Automated API**: `src/data_collection/download_imd.py` automatically downloads daily rainfall for Tamil Nadu to `datasets/raw/imd/india_rainfall.csv`.
2. **Manual IMD Gridded Binaries (Optional)**:
   - For official IMD 0.25° x 0.25° gridded binary files (`.grd`), visit [https://www.imdpune.gov.in/GRD_HP.html](https://www.imdpune.gov.in/GRD_HP.html).
   - Download the yearly binary files (e.g. `ind2023_rf.grd`).
   - Place them in `datasets/raw/imd/gridded_binaries/`.
