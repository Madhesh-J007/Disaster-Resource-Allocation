# UN OCHA ReliefWeb Disaster Database

## Dataset Overview
- **Source**: United Nations Office for the Coordination of Humanitarian Affairs (OCHA).
- **URL**: [https://apidoc.rwlabs.org/](https://apidoc.rwlabs.org/)
- **Spatial Coverage**: Global humanitarian disaster reports, situation updates, and event records.
- **Temporal Coverage**: 1996 – Present.
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0).

## Acquisition Method
Automated via `src/data_collection/download_reliefweb.py`. No API key required.

## Saved Files
- `datasets/raw/reliefweb/reliefweb_disasters.json`
- `datasets/raw/reliefweb/reliefweb_reports.json`
