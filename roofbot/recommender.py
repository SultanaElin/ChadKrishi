
import os, json, math, pandas as pd

HERE = os.path.dirname(__file__)

PLANTS_CSV = os.path.join(HERE, "plants_300.csv")  # expected real dataset
DIVISIONS_CSV = os.path.join(HERE, "divisions.csv")

# if real plants CSV missing, create a tiny demo so the app runs
def _ensure_demo_plants():
    if os.path.exists(PLANTS_CSV):
        return
    demo = pd.DataFrame([
        {"name": "Tulsi", "sunlight": "full", "water_need": "medium", "soil_type": "loam", "height_cm": 60, "spread_cm": 40, "season": "all", "notes":"holy basil"},
        {"name": "Aloevera", "sunlight": "full", "water_need": "low", "soil_type": "sandy", "height_cm": 40, "spread_cm": 30, "season": "all", "notes":"succulent"},
        {"name": "Mint", "sunlight": "partial", "water_need": "high", "soil_type": "loam", "height_cm": 50, "spread_cm": 60, "season": "cool", "notes":"herb"},
        {"name": "Chili", "sunlight": "full", "water_need": "medium", "soil_type": "loam", "height_cm": 80, "spread_cm": 50, "season": "warm", "notes":"vegetable"},
        {"name": "Marigold", "sunlight": "full", "water_need": "medium", "soil_type": "loam", "height_cm": 30, "spread_cm": 30, "season": "winter", "notes":"flower"},
        {"name": "Snake Plant", "sunlight": "shade", "water_need": "low", "soil_type": "sandy", "height_cm": 70, "spread_cm": 30, "season": "all", "notes":"indoor"},
    ])
    demo.to_csv(PLANTS_CSV, index=False)

def load_data():
    _ensure_demo_plants()
    plants = pd.read_csv(PLANTS_CSV)
    divisions = pd.read_csv(DIVISIONS_CSV)
    # Normalize categories
    for col in ["sunlight", "water_need", "soil_type", "season"]:
        if col in plants.columns:
            plants[col] = plants[col].astype(str).str.strip().str.lower()
    # Simple derived features
    if "height_cm" not in plants.columns: plants["height_cm"] = 50
    if "spread_cm" not in plants.columns: plants["spread_cm"] = 40
    return plants, divisions

# Map numeric sunlight hours to category
def sunlight_category(hours: float):
    if hours is None: return "partial"
    try:
        h = float(hours)
    except:
        return "partial"
    if h >= 6.5: return "full"
    if h >= 3.5: return "partial"
    return "shade"

# 'Bayesian-like' scoring: naive multiplicative likelihoods with smoothing
def score_plant(plant, prefs, climate):
    score = 1.0
    # Sunlight
    pref_sun = prefs.get("sunlight_cat")
    if pref_sun:
        score *= 2.5 if str(plant.get("sunlight","")) == pref_sun else 0.9
    # Soil
    soil = prefs.get("soil_type")
    if soil:
        score *= 2.0 if soil in str(plant.get("soil_type","")) else 0.95
    # Water vs rainfall/humidity
    need = str(plant.get("water_need",""))
    rain = float(climate.get("annual_rain_mm", 2000))
    hum = float(climate.get("humidity_pct", 75))
    if need == "low":
        score *= 1.8 if (rain < 1800 and hum < 75) else 0.95
    elif need == "medium":
        score *= 1.5 if (1500 <= rain <= 2800) else 0.9
    elif need == "high":
        score *= 1.6 if (rain > 2200 or hum > 78) else 0.85
    # Season (soft boost)
    season = prefs.get("season")
    if season and str(plant.get("season","")) in [season, "all"]:
        score *= 1.2
    # Space/size soft penalty if too big for average 0.5 m2 slot
    height = float(plant.get("height_cm", 50))
    spread = float(plant.get("spread_cm", 40))
    area_m2 = (spread/100.0) * (spread/100.0) * 0.6  # crude crown factor
    if area_m2 > 0.5: score *= 0.85
    return score

def recommend(plants_df, divisions_df, division, soil_type, sun_hours, count=6, season=None):
    # Get climate row (fallback to average of all)
    div_row = divisions_df[divisions_df["division"].str.lower()==str(division).lower()]
    if div_row.empty:
        climate = divisions_df.mean(numeric_only=True).to_dict()
        climate.update({"division":"Avg"})
    else:
        climate = div_row.iloc[0].to_dict()

    prefs = {
        "soil_type": str(soil_type).strip().lower() if soil_type else None,
        "sunlight_cat": sunlight_category(sun_hours) if sun_hours is not None else None,
        "season": str(season).lower() if season else None
    }
    scored = []
    for _idx, plant in plants_df.iterrows():
        s = score_plant(plant, prefs, climate)
        scored.append((s, plant.to_dict()))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [p for s,p in scored[:max(3,int(count))]]
    return top, climate, prefs

# Simple grid packing for roof area
def _get_display_name(p: dict):
    
    for key in ["name", "plant_name", "Plant", "গাছ", "title"]:
        if key in p and p[key]:
            return str(p[key]).strip()
    # fallback: যেকোনো কলাম যার নামের মধ্যে 'name' আছে
    for k, v in p.items():
        if "name" in k.lower() and v:
            return str(v).strip()
    return None

def layout_plan(plants, roof_area_m2, cols=3):
    if roof_area_m2 is None or roof_area_m2 <= 0:
        roof_area_m2 = 6
    slots = max(len(plants), int(min(12, roof_area_m2*2.0)))
    rows = (slots + cols - 1) // cols
    grid = []
    i = 0
    for r in range(rows):
        for c in range(cols):
            grid.append({
                "row": r+1,
                "col": c+1,
                "plant": (_get_display_name(plants[i]) if i < len(plants) else None)
            })
            i += 1
    return {"rows": rows, "cols": cols, "cells": grid}
