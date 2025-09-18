
from datetime import date

def care_plan(plant_name, division=None, sunlight="partial", water_need="medium", soil_type="loam"):
    # Very lightweight rules
    water_rule = {
        "low": "Water lightly when top 3–4 cm soil is dry (every 7–10 days in winter, 4–6 days in summer).",
        "medium": "Water when top 2–3 cm soil is dry (every 3–5 days in summer; 5–7 days in winter).",
        "high": "Keep soil evenly moist (every 1–3 days in hot months; 3–4 days in winter).",
    }.get(str(water_need).lower(), "Water when topsoil is dry to touch (3–6 days).")

    sun_rule = {
        "full": "Place in 6–8 hours of direct sunlight; rotate weekly for even growth.",
        "partial": "Place in 3–6 hours of sun or bright partial shade; avoid harsh noon sun.",
        "shade": "Keep in bright shade / indirect light; avoid direct sun.",
    }.get(str(sunlight).lower(), "Keep in bright light; avoid harsh noon sun.")

    soil_rule = {
        "loam": "Use well‑drained loam + 20% compost + 10% cocopeat.",
        "sandy": "Use sandy mix with 30% coarse sand + 50% garden soil + 20% compost.",
        "clay": "Amend with 30–40% compost + cocopeat; ensure drainage holes."
    }.get(str(soil_type).lower(), "Use well‑drained mix with compost + cocopeat.")

    monthly = [
        {"month": "Jan‑Feb", "task": "Prune dead/diseased growth; check pests (aphids, mites)."},
        {"month": "Mar‑Apr", "task": "Top‑dress with 1–2 tbsp compost per pot; stake tall plants."},
        {"month": "May‑Jun", "task": "Mulch 2–3 cm to reduce evaporation; increase watering frequency."},
        {"month": "Jul‑Aug", "task": "Watch for fungal issues in rain; improve airflow; use neem spray weekly."},
        {"month": "Sep‑Oct", "task": "Add slow‑release fertilizer (NPK ~10‑10‑10, 1–2 tsp per 12\" pot)."},
        {"month": "Nov‑Dec", "task": "Reduce watering; protect from cold wind; move tender plants under cover."},
    ]

    return {
        "plant": plant_name,
        "division": division,
        "daily": sun_rule,
        "watering": water_rule,
        "soil": soil_rule,
        "monthly_schedule": monthly,
        "generated_on": date.today().isoformat()
    }
