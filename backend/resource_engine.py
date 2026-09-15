AVAILABLE_RESOURCES = {
    "Ambulances": 40,
    "Rescue Teams": 22,
    "Medical Kits": 500,
    "Rescue Boats": 25,
    "Water Units": 120,
    "Food Packages": 1000,
    "Temporary Shelters": 30
}

DISASTER_BASE_DEMAND = {
    "Flood": {
        "Ambulances": 12, "Rescue Teams": 15, "Medical Kits": 180,
        "Rescue Boats": 20, "Water Units": 60, "Food Packages": 450, "Temporary Shelters": 18
    },
    "Landslide": {
        "Ambulances": 18, "Rescue Teams": 20, "Medical Kits": 220,
        "Rescue Boats": 3, "Water Units": 35, "Food Packages": 300, "Temporary Shelters": 15
    },
    "Infrastructure Failure": {
        "Ambulances": 22, "Rescue Teams": 24, "Medical Kits": 250,
        "Rescue Boats": 5, "Water Units": 45, "Food Packages": 400, "Temporary Shelters": 22
    },
    "Fire": {
        "Ambulances": 25, "Rescue Teams": 16, "Medical Kits": 300,
        "Rescue Boats": 2, "Water Units": 90, "Food Packages": 350, "Temporary Shelters": 20
    },
    "Disease Outbreak": {
        "Ambulances": 20, "Rescue Teams": 8, "Medical Kits": 450,
        "Rescue Boats": 1, "Water Units": 80, "Food Packages": 500, "Temporary Shelters": 14
    }
}

SEVERITY_MULTIPLIER = {
    "Low": 0.5,
    "Medium": 1.0,
    "High": 1.7,
    "Critical": 2.5
}

def calculate_resource_allocation(predicted_disaster, severity, risk_score, population_density):
    base_demands = DISASTER_BASE_DEMAND.get(predicted_disaster, DISASTER_BASE_DEMAND["Flood"])
    sev_mult = SEVERITY_MULTIPLIER.get(severity, 1.0)
    pop_scale = max(0.6, population_density / 3500.0)
    risk_mult = max(0.6, risk_score / 65.0)
    
    overall_mult = sev_mult * (pop_scale ** 0.5) * (risk_mult ** 0.5)
    
    resource_results = []
    total_shortage_items = 0
    
    for resource_name, base_val in base_demands.items():
        req = int(round(base_val * overall_mult))
        avail = AVAILABLE_RESOURCES.get(resource_name, 50)
        alloc = min(req, avail)
        shortage = max(0, req - avail)
        
        if shortage > 0:
            total_shortage_items += 1
            priority = "Critical Shortage"
        elif severity in ["Critical", "High"]:
            priority = severity
        else:
            priority = "Medium" if req > 15 else "Low"
            
        resource_results.append({
            "resource": resource_name,
            "required": req,
            "available": avail,
            "allocated": alloc,
            "shortage": shortage,
            "has_shortage": shortage > 0,
            "priority": priority,
            "utilization_percent": min(100.0, round((alloc / avail) * 100, 1)) if avail > 0 else 0.0
        })
        
    return {
        "predicted_disaster": predicted_disaster,
        "severity": severity,
        "risk_score": risk_score,
        "population_density": population_density,
        "total_shortage_resources": total_shortage_items,
        "allocations": resource_results
    }
