import os
import json
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support, confusion_matrix

def train():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, 'data', 'synthetic_disaster_data.csv')
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    if not os.path.exists(data_path):
        from generate_data import generate_synthetic_data
        df = generate_synthetic_data()
    else:
        df = pd.read_csv(data_path)
        
    print(f"Loaded synthetic dataset with shape: {df.shape}")
    
    num_cols = [
        'rainfall_mm', 'river_level_m', 'soil_moisture', 'wind_speed_kmph',
        'temperature_c', 'population_density', 'elevation_m',
        'infrastructure_vulnerability', 'road_accessibility', 'distance_to_water_body'
    ]
    cat_cols = ['primary_disaster']
    feature_cols = num_cols + cat_cols
    
    X = df[feature_cols]
    y_disaster = df['secondary_disaster']
    y_severity = df['severity']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols)
        ]
    )
    
    X_processed = preprocessor.fit_transform(X)
    
    cat_feature_names = list(preprocessor.named_transformers_['cat'].get_feature_names_out(cat_cols))
    all_feature_names = num_cols + cat_feature_names
    
    # Train test split
    X_train, X_test, yd_train, yd_test, ys_train, ys_test = train_test_split(
        X_processed, y_disaster, y_severity, test_size=0.2, random_state=42, stratify=y_disaster
    )
    
    print("\n--- Training Random Forest Classifier for Secondary Disaster ---")
    disaster_rf = RandomForestClassifier(n_estimators=120, max_depth=12, random_state=42)
    disaster_rf.fit(X_train, yd_train)
    yd_pred = disaster_rf.predict(X_test)
    
    d_acc = accuracy_score(yd_test, yd_pred)
    d_prec, d_rec, d_f1, _ = precision_recall_fscore_support(yd_test, yd_pred, average='weighted')
    d_classes = list(disaster_rf.classes_)
    d_cm = confusion_matrix(yd_test, yd_pred, labels=d_classes).tolist()
    
    print(f"Secondary Disaster Model Accuracy: {d_acc:.4f}")
    print(f"Precision: {d_prec:.4f} | Recall: {d_rec:.4f} | F1-Score: {d_f1:.4f}")
    print("\nClassification Report (Disaster):")
    print(classification_report(yd_test, yd_pred))
    print("Confusion Matrix (Disaster):")
    print(d_cm)
    
    print("\n--- Training Random Forest Classifier for Severity ---")
    severity_rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    severity_rf.fit(X_train, ys_train)
    ys_pred = severity_rf.predict(X_test)
    
    s_acc = accuracy_score(ys_test, ys_pred)
    s_prec, s_rec, s_f1, _ = precision_recall_fscore_support(ys_test, ys_pred, average='weighted')
    s_classes = list(severity_rf.classes_)
    s_cm = confusion_matrix(ys_test, ys_pred, labels=s_classes).tolist()
    
    print(f"Severity Model Accuracy: {s_acc:.4f}")
    print(f"Precision: {s_prec:.4f} | Recall: {s_rec:.4f} | F1-Score: {s_f1:.4f}")
    print("\nClassification Report (Severity):")
    print(classification_report(ys_test, ys_pred))
    print("Confusion Matrix (Severity):")
    print(s_cm)
    
    # Save trained artifacts
    joblib.dump(disaster_rf, os.path.join(models_dir, 'disaster_model.joblib'))
    joblib.dump(severity_rf, os.path.join(models_dir, 'severity_model.joblib'))
    joblib.dump(preprocessor, os.path.join(models_dir, 'preprocessor.joblib'))
    
    # Feature importances
    disaster_importances = [
        {"feature": name, "importance": float(imp)}
        for name, imp in sorted(zip(all_feature_names, disaster_rf.feature_importances_), key=lambda x: x[1], reverse=True)
    ]
    
    metrics = {
        "dataset_size": len(df),
        "features_count": len(feature_cols),
        "disaster_model": {
            "accuracy": float(d_acc),
            "precision": float(d_prec),
            "recall": float(d_rec),
            "f1_score": float(d_f1),
            "classes": d_classes,
            "confusion_matrix": d_cm,
            "feature_importances": disaster_importances
        },
        "severity_model": {
            "accuracy": float(s_acc),
            "precision": float(s_prec),
            "recall": float(s_rec),
            "f1_score": float(s_f1),
            "classes": s_classes,
            "confusion_matrix": s_cm
        },
        "class_distribution": df['secondary_disaster'].value_counts().to_dict(),
        "severity_distribution": df['severity'].value_counts().to_dict()
    }
    
    metrics_path = os.path.join(models_dir, 'metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
        
    print(f"\nSaved models and metrics to {models_dir}")
    return metrics

if __name__ == '__main__':
    train()
