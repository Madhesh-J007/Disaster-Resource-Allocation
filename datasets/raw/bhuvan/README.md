# ISRO Bhuvan Geospatial Disaster Maps

## Dataset Overview
- **Source**: Indian Space Research Organisation (ISRO) National Remote Sensing Centre (NRSC).
- **URL**: [https://bhuvan.nrsc.gov.in/](https://bhuvan.nrsc.gov.in/)
- **Spatial Coverage**: India / Tamil Nadu disaster inundation and landslide hazard zones.
- **License**: Government Open Data / ISRO Bhuvan Terms of Service.

## Why Registration / Manual Steps are Required
ISRO Bhuvan Web Map Services (WMS/WFS) require registration and spatial data access authorization from NRSC for downloading vector shapefiles or GeoTIFF layers directly.

## Manual Download Steps
1. Register/Log in at [https://bhuvan.nrsc.gov.in/](https://bhuvan.nrsc.gov.in/).
2. Go to **Disaster Services -> Flood / Landslide Hazard Maps**.
3. Select Region: `Tamil Nadu`.
4. Export options: Download vector layers as **KML / GeoJSON / Shapefile**.
5. Save the downloaded shapefiles or GeoJSON into this directory as:
   `datasets/raw/bhuvan/bhuvan_flood_zones.geojson`

## Automated Fallback
`src/data_collection/download_bhuvan.py` automatically generates a baseline GeoJSON structure for Tamil Nadu hazard zones so the pipeline works seamlessly out-of-the-box.
