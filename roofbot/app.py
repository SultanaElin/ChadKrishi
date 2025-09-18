
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os, json
from recommender import load_data, recommend, layout_plan
from care_plan import care_plan

HERE = os.path.dirname(__file__)
app = Flask(__name__, static_folder=HERE, static_url_path="")
CORS(app)

@app.route("/")
def index():
    return send_from_directory(HERE, "index.html")

@app.get("/api/health")
def health():
    return jsonify({"ok": True, "msg": "RoofBot API running"})

@app.get("/api/plants")
def list_plants():
    plants, _ = load_data()
    # return first 50 plants with key fields
    cols = [c for c in ["name","sunlight","water_need","soil_type","season","height_cm","spread_cm","notes"] if c in plants.columns]
    sample = plants[cols].head(50).to_dict(orient="records")
    return jsonify({"count": len(sample), "plants": sample})

@app.post("/api/garden-plan")
def garden_plan():
    body = request.get_json(force=True) or {}
    division = body.get("division")
    soil_type = body.get("soil_type", "loam")
    sun_hours = body.get("sun_hours", 5.0)
    season = body.get("season")
    count = int(body.get("count", 6))
    roof_area = body.get("roof_area_m2", 6)

    plants_df, divisions = load_data()
    top, climate, prefs = recommend(plants_df, divisions, division, soil_type, sun_hours, count=count, season=season)
    layout = layout_plan(top, roof_area)
    return jsonify({
        "ok": True,
        "division": division,
        "climate": climate,
        "preferences": prefs,
        "recommendations": top,
        "layout": layout
    })

@app.post("/api/care-plan")
def care():
    body = request.get_json(force=True) or {}
    plant = body.get("plant_name") or body.get("name")
    division = body.get("division")
    sunlight = body.get("sunlight", "partial")
    water_need = body.get("water_need", "medium")
    soil_type = body.get("soil_type", "loam")
    if not plant:
        return jsonify({"ok": False, "error": "plant_name is required"}), 400
    plan = care_plan(plant_name=plant, division=division, sunlight=sunlight, water_need=water_need, soil_type=soil_type)
    return jsonify({"ok": True, "plan": plan})

if __name__ == "__main__":
    # pick PORT from env for Render/Heroku etc.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
