# EM-DAT: International Disaster Database

## Dataset Overview
- **Source**: Centre for Research on the Epidemiology of Disasters (CRED), Université catholique de Louvain, Brussels, Belgium.
- **URL**: [https://public.emdat.be/](https://public.emdat.be/)
- **Spatial Coverage**: Global (filtered for India & Tamil Nadu region).
- **Temporal Coverage**: 1900 – Present.
- **License**: Free for academic and non-commercial research (attribution required).

## Why Registration is Required
EM-DAT requires users to create a free account on `public.emdat.be` to agree to their non-commercial usage license before exporting the dataset.

## Manual Download Instructions
1. Visit [https://public.emdat.be/](https://public.emdat.be/) and create a free account or log in.
2. Navigate to **Data -> Query Tool**.
3. Select Country: `India`.
4. Select Disaster Types: `Flood`, `Storm`, `Landslide`, `Earthquake`, `Extreme Temperature`.
5. Export format: Select **CSV** or **Excel (.xlsx)**.
6. Save the downloaded file into this directory as:
   `c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\raw\emdat\emdat_disasters.csv`

## Automated Fallback
`download_emdat.py` automatically checks for `emdat_disasters.csv`. If absent, it creates a baseline EM-DAT schema dataset containing real historical disaster records for Tamil Nadu (e.g., 2015 Chennai Flood, 2018 Cyclone Gaja, 2020 Cyclone Nivar, 2023 Cyclone Michaung) so the pipeline runs out-of-the-box.
