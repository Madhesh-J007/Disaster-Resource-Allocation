"""
Excel Documentation Generator
Creates formatted Excel workbooks for `dataset_catalog.xlsx` and `data_dictionary.xlsx` using openpyxl.
"""

import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

METADATA_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\metadata"

def style_header_and_cells(ws):
    """Applies professional styling to openpyxl worksheet."""
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    cell_font = Font(name="Calibri", size=10)
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font = cell_font
            cell.border = thin_border
            cell.alignment = Alignment(vertical="center")
            
    # Auto-fit columns
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 50)

def generate_dataset_catalog():
    """Generates datasets/metadata/dataset_catalog.xlsx."""
    catalog_data = [
        {
            "Dataset ID": "DS-01",
            "Dataset Name": "EM-DAT International Disaster Database",
            "Category": "Disaster History & Impacts",
            "Source": "CRED / Univ of Louvain",
            "Access Type": "Manual / Registration Required",
            "Registration Needed": "Yes (Free Academic)",
            "Format": "CSV / XLSX",
            "Spatial Resolution": "Point / District Level",
            "Temporal Coverage": "1900 - Present",
            "License": "Non-Commercial Academic",
            "Status": "Configured & Baseline Loaded",
            "URL / API": "https://public.emdat.be/",
            "Description": "Historical natural disaster events, total deaths, affected population, and economic damage."
        },
        {
            "Dataset ID": "DS-02",
            "Dataset Name": "NASA EONET Natural Events",
            "Category": "Real-time Natural Hazards",
            "Source": "NASA ESDIS",
            "Access Type": "Automated REST API",
            "Registration Needed": "No",
            "Format": "JSON",
            "Spatial Resolution": "Point / Polygon (Global)",
            "Temporal Coverage": "Real-time & 10-Yr Archive",
            "License": "NASA Open Data Policy",
            "Status": "Downloaded & Cleaned",
            "URL / API": "https://eonet.gsfc.nasa.gov/api/v3/events",
            "Description": "Global natural hazard event tracks (wildfires, floods, severe storms, landslides)."
        },
        {
            "Dataset ID": "DS-03",
            "Dataset Name": "OCHA ReliefWeb Reports & Events",
            "Category": "Humanitarian Disaster Reports",
            "Source": "United Nations OCHA",
            "Access Type": "Automated REST API",
            "Registration Needed": "No",
            "Format": "JSON",
            "Spatial Resolution": "Country / Regional",
            "Temporal Coverage": "1996 - Present",
            "License": "CC BY 4.0",
            "Status": "Downloaded & Cleaned",
            "URL / API": "https://api.reliefweb.int/v1/disasters",
            "Description": "UN disaster situation reports, disaster categories, primary country locations, and updates."
        },
        {
            "Dataset ID": "DS-04",
            "Dataset Name": "OpenStreetMap Tamil Nadu Infrastructure",
            "Category": "Critical Infrastructure & GIS",
            "Source": "OpenStreetMap Contributors",
            "Access Type": "Automated Overpass API",
            "Registration Needed": "No",
            "Format": "JSON / GeoJSON",
            "Spatial Resolution": "Node Point Level (< 10m)",
            "Temporal Coverage": "Real-time Vector Layer",
            "License": "ODbL",
            "Status": "Downloaded & Cleaned",
            "URL / API": "https://overpass-api.de/api/interpreter",
            "Description": "Hospitals, fire stations, multi-purpose cyclone shelters, power substations, and transport links."
        },
        {
            "Dataset ID": "DS-05",
            "Dataset Name": "IMD India Daily Rainfall & Weather",
            "Category": "Meteorological & Precipitation",
            "Source": "IMD / Open-Meteo Archive",
            "Access Type": "Automated API & Manual Binary",
            "Registration Needed": "No (API) / Yes (IMD raw .grd)",
            "Format": "CSV / Binary (.grd)",
            "Spatial Resolution": "0.25° x 0.25° Grid (~25km)",
            "Temporal Coverage": "Daily (1951 - Present)",
            "License": "OGD India / CC-BY 4.0",
            "Status": "Downloaded & Cleaned",
            "URL / API": "https://archive-api.open-meteo.com/v1/archive",
            "Description": "Daily precipitation accumulation, rain hours, rolling 3d/7d totals, and heavy rainfall flags."
        },
        {
            "Dataset ID": "DS-06",
            "Dataset Name": "WorldPop Population Density - Tamil Nadu",
            "Category": "Demographics & Spatial Pop",
            "Source": "WorldPop / Univ of Southampton",
            "Access Type": "Automated REST API / CSV",
            "Registration Needed": "No",
            "Format": "CSV / GeoTIFF",
            "Spatial Resolution": "100m x 100m Grid",
            "Temporal Coverage": "2000 - 2020",
            "License": "CC BY 4.0",
            "Status": "Downloaded & Cleaned",
            "URL / API": "https://www.worldpop.org/rest/data/",
            "Description": "District population counts, spatial density per sq km, and normalized exposure density index."
        },
        {
            "Dataset ID": "DS-07",
            "Dataset Name": "SRTM Digital Elevation Model (DEM)",
            "Category": "Topography & Elevation",
            "Source": "NASA / USGS SRTM 30m",
            "Access Type": "Automated Grid API",
            "Registration Needed": "No",
            "Format": "CSV / GeoTIFF",
            "Spatial Resolution": "30m (1-arc second)",
            "Temporal Coverage": "Static Topography",
            "License": "Public Domain",
            "Status": "Downloaded & Cleaned",
            "URL / API": "https://api.open-meteo.com/v1/elevation",
            "Description": "Point elevation (meters), terrain risk classification (inundation plains vs landslide mountain zones)."
        },
        {
            "Dataset ID": "DS-08",
            "Dataset Name": "Census Vulnerability Indicators",
            "Category": "Socio-Economic Demographics",
            "Source": "Census Commissioner of India",
            "Access Type": "Open Data / Scripted Table",
            "Registration Needed": "No",
            "Format": "CSV",
            "Spatial Resolution": "District Level",
            "Temporal Coverage": "2011 - Present",
            "License": "OGD India",
            "Status": "Downloaded & Cleaned",
            "URL / API": "https://censusindia.gov.in/",
            "Description": "Households, slum population %, literacy rate, pukka housing %, and composite vulnerability index."
        },
        {
            "Dataset ID": "DS-09",
            "Dataset Name": "ISRO Bhuvan Disaster Hazard Maps",
            "Category": "Satellite Flood & Landslide Maps",
            "Source": "ISRO NRSC",
            "Access Type": "Manual Guide / Baseline GeoJSON",
            "Registration Needed": "Yes (Bhuvan Portal)",
            "Format": "GeoJSON / KML / Shapefile",
            "Spatial Resolution": "Vector Polygon",
            "Temporal Coverage": "Event Specific Maps",
            "License": "Government Open Data",
            "Status": "Configured & Baseline Loaded",
            "URL / API": "https://bhuvan.nrsc.gov.in/",
            "Description": "Flood inundation zones, landslide hazard zonation, and coastal vulnerability boundaries."
        }
    ]
    
    df_catalog = pd.DataFrame(catalog_data)
    catalog_path = os.path.join(METADATA_DIR, "dataset_catalog.xlsx")
    
    with pd.ExcelWriter(catalog_path, engine="openpyxl") as writer:
        df_catalog.to_excel(writer, sheet_name="Dataset Catalog", index=False)
        
    wb = openpyxl.load_workbook(catalog_path)
    ws = wb["Dataset Catalog"]
    style_header_and_cells(ws)
    wb.save(catalog_path)
    print(f"[Excel Docs] Generated dataset catalog workbook at {catalog_path}")
    return catalog_path

def generate_data_dictionary():
    """Generates datasets/metadata/data_dictionary.xlsx."""
    dict_file = os.path.join(METADATA_DIR, "data_dictionary.xlsx")
    
    sheets_data = {
        "final_dataset": [
            {"Column": "district_id", "Data Type": "Integer", "Description": "Unique identifier for Tamil Nadu district", "Nullable": "No", "Valid Range": "1 to 32", "Unit": "ID"},
            {"Column": "district", "Data Type": "String", "Description": "Name of district in Tamil Nadu", "Nullable": "No", "Valid Range": "Category", "Unit": "Text"},
            {"Column": "population", "Data Type": "Integer", "Description": "Total projected district population", "Nullable": "No", "Valid Range": "100k to 12M", "Unit": "Persons"},
            {"Column": "pop_density_per_sq_km", "Data Type": "Float", "Description": "Population density per square kilometer", "Nullable": "No", "Valid Range": "100 to 30000", "Unit": "Persons/km²"},
            {"Column": "elevation_m", "Data Type": "Float", "Description": "Mean terrain elevation above sea level", "Nullable": "No", "Valid Range": "0 to 2695", "Unit": "Meters"},
            {"Column": "recent_7d_precip_mm", "Data Type": "Float", "Description": "7-day rolling precipitation accumulation", "Nullable": "No", "Valid Range": "0.0 to 500.0", "Unit": "Millimeters"},
            {"Column": "heavy_rain_event_count", "Data Type": "Integer", "Description": "Number of days exceeding heavy rainfall threshold (>64.5mm)", "Nullable": "No", "Valid Range": "0 to 30", "Unit": "Days"},
            {"Column": "slum_pop_pct", "Data Type": "Float", "Description": "Percentage of district population living in slum habitations", "Nullable": "No", "Valid Range": "0.0 to 50.0", "Unit": "Percent"},
            {"Column": "pukka_housing_pct", "Data Type": "Float", "Description": "Percentage of permanent concrete/brick (pukka) structures", "Nullable": "No", "Valid Range": "50.0 to 100.0", "Unit": "Percent"},
            {"Column": "vulnerability_score", "Data Type": "Float", "Description": "Normalized social vulnerability index", "Nullable": "No", "Valid Range": "0.0 to 1.0", "Unit": "Index"},
            {"Column": "composite_vulnerability_index", "Data Type": "Float", "Description": "Multi-factorial vulnerability index combining slum %, housing, literacy", "Nullable": "No", "Valid Range": "5.0 to 50.0", "Unit": "Score"},
            {"Column": "historical_disaster_deaths", "Data Type": "Integer", "Description": "Sum of historical disaster deaths in district from EM-DAT", "Nullable": "No", "Valid Range": "0 to 10000", "Unit": "Deaths"},
            {"Column": "historical_affected", "Data Type": "Integer", "Description": "Sum of historical affected population in district", "Nullable": "No", "Valid Range": "0 to 10M", "Unit": "Persons"},
            {"Column": "cascade_risk_score", "Data Type": "Float", "Description": "Predicted probability of secondary disaster chain reaction", "Nullable": "No", "Valid Range": "0.00 to 1.00", "Unit": "Probability"},
            {"Column": "secondary_disaster_triggered", "Data Type": "Integer", "Description": "Binary classification target flag (1 = High Trigger Risk, 0 = Low)", "Nullable": "No", "Valid Range": "0 or 1", "Unit": "Binary Flag"}
        ],
        "cleaned_emdat": [
            {"Column": "disaster_number", "Data Type": "String", "Description": "EM-DAT unique disaster identifier (e.g. 2015-0520-IND)", "Nullable": "No", "Valid Range": "Text", "Unit": "ID"},
            {"Column": "year", "Data Type": "Integer", "Description": "Year of disaster occurrence", "Nullable": "No", "Valid Range": "1900 to 2026", "Unit": "Year"},
            {"Column": "disaster_type", "Data Type": "String", "Description": "Main disaster classification (Flood, Storm, Landslide)", "Nullable": "No", "Valid Range": "Category", "Unit": "Text"},
            {"Column": "total_deaths", "Data Type": "Integer", "Description": "Confirmed total fatalities", "Nullable": "No", "Valid Range": "0 to 50000", "Unit": "Deaths"},
            {"Column": "total_affected", "Data Type": "Integer", "Description": "Total population requiring immediate emergency assistance", "Nullable": "No", "Valid Range": "0 to 20M", "Unit": "Persons"}
        ],
        "cleaned_imd": [
            {"Column": "date", "Data Type": "Date", "Description": "Observation date", "Nullable": "No", "Valid Range": "YYYY-MM-DD", "Unit": "Date"},
            {"Column": "precipitation_mm", "Data Type": "Float", "Description": "Daily 24-hour precipitation accumulation", "Nullable": "No", "Valid Range": "0.0 to 500.0", "Unit": "mm"},
            {"Column": "rolling_7d_precip_mm", "Data Type": "Float", "Description": "Calculated 7-day cumulative rainfall total", "Nullable": "No", "Valid Range": "0.0 to 1000.0", "Unit": "mm"},
            {"Column": "heavy_rainfall_flag", "Data Type": "Integer", "Description": "Flag indicating heavy rainfall >= 64.5mm", "Nullable": "No", "Valid Range": "0 or 1", "Unit": "Binary"}
        ]
    }
    
    with pd.ExcelWriter(dict_file, engine="openpyxl") as writer:
        for sheet_name, cols in sheets_data.items():
            df_sheet = pd.DataFrame(cols)
            df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
            
    wb = openpyxl.load_workbook(dict_file)
    for s_name in sheets_data.keys():
        style_header_and_cells(wb[s_name])
    wb.save(dict_file)
    print(f"[Excel Docs] Generated data dictionary workbook at {dict_file}")
    return dict_file

def generate_all_excel_docs():
    """Generates both catalog and dictionary files."""
    os.makedirs(METADATA_DIR, exist_ok=True)
    generate_dataset_catalog()
    generate_data_dictionary()

if __name__ == "__main__":
    generate_all_excel_docs()
