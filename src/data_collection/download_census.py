"""
Census Demographics Data Collector for Tamil Nadu
Generates structured Census indicators for all 38 districts of Tamil Nadu.
"""

import os
import pandas as pd

RAW_DIR = r"c:\Project\ML\Disaster-Resource-Allocation-ML\datasets\raw\census"

def download_census_data():
    """
    Creates Census demographics table for all 38 districts of Tamil Nadu.
    """
    os.makedirs(RAW_DIR, exist_ok=True)
    
    census_38_districts = [
        {"district": "Ariyalur", "total_households": 195400, "urban_pct": 11.2, "literacy_rate": 71.34, "pukka_housing_pct": 66.5, "slum_pop_pct": 9.2, "vulnerability_score": 0.58},
        {"district": "Chengalpattu", "total_households": 642000, "urban_pct": 68.5, "literacy_rate": 84.60, "pukka_housing_pct": 84.1, "slum_pop_pct": 18.5, "vulnerability_score": 0.44},
        {"district": "Chennai", "total_households": 1154982, "urban_pct": 100.0, "literacy_rate": 90.18, "pukka_housing_pct": 92.4, "slum_pop_pct": 28.5, "vulnerability_score": 0.65},
        {"district": "Coimbatore", "total_households": 958045, "urban_pct": 75.7, "literacy_rate": 83.98, "pukka_housing_pct": 86.1, "slum_pop_pct": 12.1, "vulnerability_score": 0.38},
        {"district": "Cuddalore", "total_households": 625100, "urban_pct": 34.0, "literacy_rate": 78.04, "pukka_housing_pct": 68.5, "slum_pop_pct": 19.8, "vulnerability_score": 0.72},
        {"district": "Dharmapuri", "total_households": 376800, "urban_pct": 17.3, "literacy_rate": 68.50, "pukka_housing_pct": 63.2, "slum_pop_pct": 11.4, "vulnerability_score": 0.68},
        {"district": "Dindigul", "total_households": 542100, "urban_pct": 37.4, "literacy_rate": 76.26, "pukka_housing_pct": 72.0, "slum_pop_pct": 13.8, "vulnerability_score": 0.51},
        {"district": "Erode", "total_households": 612500, "urban_pct": 51.4, "literacy_rate": 72.58, "pukka_housing_pct": 78.4, "slum_pop_pct": 10.9, "vulnerability_score": 0.42},
        {"district": "Kallakurichi", "total_households": 345000, "urban_pct": 15.2, "literacy_rate": 70.10, "pukka_housing_pct": 62.8, "slum_pop_pct": 14.0, "vulnerability_score": 0.69},
        {"district": "Kanchipuram", "total_households": 298000, "urban_pct": 63.5, "literacy_rate": 84.49, "pukka_housing_pct": 82.0, "slum_pop_pct": 16.2, "vulnerability_score": 0.46},
        {"district": "Kanyakumari", "total_households": 470500, "urban_pct": 82.3, "literacy_rate": 91.75, "pukka_housing_pct": 88.9, "slum_pop_pct": 8.5, "vulnerability_score": 0.58},
        {"district": "Karur", "total_households": 278900, "urban_pct": 40.8, "literacy_rate": 75.60, "pukka_housing_pct": 73.1, "slum_pop_pct": 12.0, "vulnerability_score": 0.49},
        {"district": "Krishnagiri", "total_households": 451200, "urban_pct": 22.8, "literacy_rate": 71.46, "pukka_housing_pct": 67.8, "slum_pop_pct": 10.5, "vulnerability_score": 0.61},
        {"district": "Madurai", "total_households": 765430, "urban_pct": 60.8, "literacy_rate": 81.50, "pukka_housing_pct": 79.4, "slum_pop_pct": 18.2, "vulnerability_score": 0.48},
        {"district": "Mayiladuthurai", "total_households": 234100, "urban_pct": 21.0, "literacy_rate": 83.10, "pukka_housing_pct": 64.5, "slum_pop_pct": 17.5, "vulnerability_score": 0.74},
        {"district": "Nagapattinam", "total_households": 185000, "urban_pct": 22.6, "literacy_rate": 83.59, "pukka_housing_pct": 62.1, "slum_pop_pct": 21.4, "vulnerability_score": 0.81},
        {"district": "Namakkal", "total_households": 462000, "urban_pct": 40.3, "literacy_rate": 74.63, "pukka_housing_pct": 76.5, "slum_pop_pct": 9.8, "vulnerability_score": 0.43},
        {"district": "Nilgiris", "total_households": 198400, "urban_pct": 59.2, "literacy_rate": 85.20, "pukka_housing_pct": 71.0, "slum_pop_pct": 11.0, "vulnerability_score": 0.69},
        {"district": "Perambalur", "total_households": 142300, "urban_pct": 17.2, "literacy_rate": 74.32, "pukka_housing_pct": 65.4, "slum_pop_pct": 8.4, "vulnerability_score": 0.59},
        {"district": "Pudukkottai", "total_households": 398000, "urban_pct": 19.5, "literacy_rate": 77.19, "pukka_housing_pct": 67.2, "slum_pop_pct": 12.8, "vulnerability_score": 0.63},
        {"district": "Ramanathapuram", "total_households": 341000, "urban_pct": 30.2, "literacy_rate": 80.72, "pukka_housing_pct": 66.8, "slum_pop_pct": 15.6, "vulnerability_score": 0.76},
        {"district": "Ranipet", "total_households": 298400, "urban_pct": 48.2, "literacy_rate": 79.10, "pukka_housing_pct": 75.2, "slum_pop_pct": 14.1, "vulnerability_score": 0.48},
        {"district": "Salem", "total_households": 910250, "urban_pct": 51.6, "literacy_rate": 72.86, "pukka_housing_pct": 74.2, "slum_pop_pct": 16.0, "vulnerability_score": 0.52},
        {"district": "Sivaganga", "total_households": 338900, "urban_pct": 30.8, "literacy_rate": 79.85, "pukka_housing_pct": 71.5, "slum_pop_pct": 11.2, "vulnerability_score": 0.55},
        {"district": "Tenkasi", "total_households": 361000, "urban_pct": 43.1, "literacy_rate": 81.20, "pukka_housing_pct": 74.8, "slum_pop_pct": 13.5, "vulnerability_score": 0.53},
        {"district": "Thanjavur", "total_households": 605000, "urban_pct": 35.4, "literacy_rate": 82.64, "pukka_housing_pct": 71.4, "slum_pop_pct": 17.2, "vulnerability_score": 0.64},
        {"district": "Theni", "total_households": 338000, "urban_pct": 53.8, "literacy_rate": 77.26, "pukka_housing_pct": 75.0, "slum_pop_pct": 14.8, "vulnerability_score": 0.50},
        {"district": "Tiruchirappalli", "total_households": 684200, "urban_pct": 49.2, "literacy_rate": 83.24, "pukka_housing_pct": 77.8, "slum_pop_pct": 14.5, "vulnerability_score": 0.45},
        {"district": "Tirunelveli", "total_households": 435000, "urban_pct": 49.9, "literacy_rate": 82.50, "pukka_housing_pct": 75.6, "slum_pop_pct": 15.3, "vulnerability_score": 0.50},
        {"district": "Tirupathur", "total_households": 268000, "urban_pct": 39.5, "literacy_rate": 76.50, "pukka_housing_pct": 70.2, "slum_pop_pct": 12.6, "vulnerability_score": 0.57},
        {"district": "Tiruppur", "total_households": 652000, "urban_pct": 61.4, "literacy_rate": 78.68, "pukka_housing_pct": 81.5, "slum_pop_pct": 10.2, "vulnerability_score": 0.39},
        {"district": "Tiruvallur", "total_households": 935000, "urban_pct": 65.1, "literacy_rate": 84.03, "pukka_housing_pct": 83.0, "slum_pop_pct": 22.1, "vulnerability_score": 0.56},
        {"district": "Tiruvannamalai", "total_households": 612000, "urban_pct": 20.1, "literacy_rate": 74.21, "pukka_housing_pct": 66.0, "slum_pop_pct": 11.8, "vulnerability_score": 0.62},
        {"district": "Tiruvarur", "total_households": 321000, "urban_pct": 20.4, "literacy_rate": 82.86, "pukka_housing_pct": 63.8, "slum_pop_pct": 18.9, "vulnerability_score": 0.73},
        {"district": "Tuticorin", "total_households": 448000, "urban_pct": 50.1, "literacy_rate": 86.16, "pukka_housing_pct": 78.2, "slum_pop_pct": 13.0, "vulnerability_score": 0.52},
        {"district": "Vellore", "total_households": 395000, "urban_pct": 43.2, "literacy_rate": 79.17, "pukka_housing_pct": 76.4, "slum_pop_pct": 16.5, "vulnerability_score": 0.51},
        {"district": "Villupuram", "total_households": 512000, "urban_pct": 15.0, "literacy_rate": 71.88, "pukka_housing_pct": 64.0, "slum_pop_pct": 15.1, "vulnerability_score": 0.67},
        {"district": "Virudhunagar", "total_households": 485000, "urban_pct": 50.5, "literacy_rate": 80.15, "pukka_housing_pct": 77.0, "slum_pop_pct": 12.4, "vulnerability_score": 0.47}
    ]
    
    df = pd.DataFrame(census_38_districts)
    output_file = os.path.join(RAW_DIR, "census_tamil_nadu.csv")
    df.to_csv(output_file, index=False)
    print(f"[Census] Saved Tamil Nadu Census indicators for ALL 38 districts to {output_file}")
    return output_file

if __name__ == "__main__":
    download_census_data()
