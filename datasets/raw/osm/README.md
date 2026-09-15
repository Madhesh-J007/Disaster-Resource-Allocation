# OpenStreetMap (OSM) Infrastructure - Tamil Nadu

## Dataset Overview
- **Source**: OpenStreetMap Contributors / Overpass API.
- **URL**: [https://overpass-api.de/](https://overpass-api.de/)
- **Spatial Coverage**: Tamil Nadu bounding box (`8.0, 76.0, 13.6, 80.5`).
- **Features Extracted**: Hospitals, Fire Stations, Multi-purpose Shelters, Power Substations, and Power Plants.
- **License**: Open Database License (ODbL).

## Acquisition Method
Automated via `src/data_collection/download_osm.py`. Queries Overpass API and saves raw nodes to `datasets/raw/osm/tamil_nadu_infrastructure.json`.
