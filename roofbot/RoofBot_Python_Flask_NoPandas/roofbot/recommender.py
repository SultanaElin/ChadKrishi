from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class UserInput:
    location: str
    sunlight: int
    temperature: int
    humidity: int
    area: int
    soil: str
    season: str

def _dist_to_range(value: float, low: float, high: float) -> float:
    if value < low:
        return low - value
    if value > high:
        return value - high
    return 0.0

def _parse_list(s: str) -> set:
    return set([x.strip() for x in str(s or '').split(';') if x.strip()])

def score_row(row: dict, ui: UserInput) -> Dict[str, Any]:
    # ints
    sunlight_min = int(row['sunlight_min']); sunlight_max = int(row['sunlight_max'])
    temp_min = int(row['temp_min']); temp_max = int(row['temp_max'])
    humidity_min = int(row['humidity_min']); humidity_max = int(row['humidity_max'])
    area_min = int(row['area_min'])
    diff = str(row['difficulty_level']).lower()

    score = 0.0
    total = 0.0

    # sunlight (max 20)
    total += 20
    sdist = _dist_to_range(ui.sunlight, sunlight_min, sunlight_max)
    score += max(0, 20 - sdist * 5)

    # temperature (max 20)
    total += 20
    tdist = _dist_to_range(ui.temperature, temp_min, temp_max)
    score += max(0, 20 - tdist * 3)

    # humidity (max 10)
    total += 10
    hdist = _dist_to_range(ui.humidity, humidity_min, humidity_max)
    score += max(0, 10 - hdist * 0.5)

    # soil (max 10)
    total += 10
    soils = _parse_list(row.get('soils'))
    if ui.soil in soils:
        score += 10

    # season (max 15)
    total += 15
    seasons = _parse_list(row.get('seasons'))
    score += 15 if ui.season in seasons else 5

    # location (max 10)
    total += 10
    locations = _parse_list(row.get('locations'))
    score += 10 if ui.location in locations else 6

    # area (max 10)
    total += 10
    if ui.area >= area_min:
        score += 10
    else:
        score += max(0, 10 - (area_min - ui.area))

    # difficulty (max 5)
    total += 5
    score += 5 if diff == 'easy' else (3 if diff == 'medium' else 1)

    confidence = int(round((score / total) * 100))
    return {
        'plant_name': row['plant_name'],
        'category': row['category'],
        'difficulty_level': row['difficulty_level'],
        'growth_days': int(row['growth_days']),
        'confidence': confidence,
        'care_instructions': row['care_instructions'],
        'sunlight_min': sunlight_min,
        'humidity_min': humidity_min,
    }

def recommend(plants: List[dict], ui_dict: Dict[str, Any], top_k: int = 6, threshold: int = 50) -> List[Dict[str, Any]]:
    ui = UserInput(**ui_dict)
    scores = [score_row(row, ui) for row in plants]
    hits = [s for s in scores if s['confidence'] >= threshold]
    hits.sort(key=lambda x: x['confidence'], reverse=True)
    return hits[:top_k]
