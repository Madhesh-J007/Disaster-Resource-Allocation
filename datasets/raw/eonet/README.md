# NASA EONET (Earth Observatory Natural Event Tracker)

## Dataset Overview
- **Source**: NASA Earth Science Data and Information System (ESDIS).
- **URL**: [https://eonet.gsfc.nasa.gov/docs/v3](https://eonet.gsfc.nasa.gov/docs/v3)
- **Spatial Coverage**: Global natural disaster events (Wildfires, Floods, Severe Storms, Volcanoes, Landslides).
- **Temporal Coverage**: Real-time & 10+ year historical archive.
- **License**: Public Domain (NASA Open Data Policy).

## Acquisition Method
Automated via `src/data_collection/download_eonet.py`. No registration or API key required.

## File Format
Raw JSON object saved to `datasets/raw/eonet/eonet_events.json`.
