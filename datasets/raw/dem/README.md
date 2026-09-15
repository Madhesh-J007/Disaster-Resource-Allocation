# SRTM Digital Elevation Model (DEM)

## Dataset Overview
- **Source**: NASA Shuttle Radar Topography Mission (SRTM) / USGS.
- **URL**: [https://earthexplorer.usgs.gov/](https://earthexplorer.usgs.gov/) & Open-Meteo SRTM Elevation API.
- **Spatial Coverage**: Tamil Nadu state (Western Ghats to coastal plains).
- **Resolution**: 30m 1-arc second spatial resolution.
- **License**: Public Domain (NASA Open Data).

## Acquisition Method
Automated via `src/data_collection/download_dem.py` querying SRTM 30m grid endpoints saving values to `datasets/raw/dem/tamil_nadu_dem.csv`.
