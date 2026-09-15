# WorldPop Spatial Population Data

## Dataset Overview
- **Source**: WorldPop Research Group, University of Southampton.
- **URL**: [https://www.worldpop.org/](https://www.worldpop.org/)
- **Spatial Coverage**: India / Tamil Nadu state.
- **Resolution**: 100m x 100m raster grid & district population counts.
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0).

## Acquisition Method
Automated query to WorldPop REST API via `src/data_collection/download_worldpop.py` saving metadata to `datasets/raw/worldpop/worldpop_metadata.json` and district population table to `datasets/raw/worldpop/worldpop_tamil_nadu.csv`.
