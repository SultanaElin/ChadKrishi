from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import csv, os

from recommender import recommend
from care_plan import generate_care_plan

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(APP_ROOT, 'data')
DATA_PATH = os.path.join(DATA_DIR, 'plants_300.csv')

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

def load_plants():
    rows = []
    with open(DATA_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

# cache in memory
PLANTS = load_plants()

@app.get('/')
def home():
    return render_template('index.html')

@app.get('/api-ui')
def api_ui():
    return render_template('api_ui.html')

# NEW: CSV -> JSON for frontend (stop using inline <script> dataset)
@app.get('/api/plants_300')
def api_plants():
    return jsonify(PLANTS)

# NEW: serve raw CSV directly if needed
@app.get('/api/plants.csv')
def api_plants_csv():
    return send_from_directory(DATA_DIR, 'plants_300.csv', mimetype='text/csv')

# OPTIONAL: reload CSV at runtime after you replace/update the file
@app.post('/api/plants/reload')
def api_plants_reload():
    global PLANTS
    PLANTS = load_plants()
    return jsonify({"ok": True, "count": len(PLANTS)})

@app.post('/api/recommend')
def api_recommend():
    data = request.get_json(force=True, silent=True) or {}
    required = ['location','sunlight','temperature','humidity','area','soil','season']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': f'Missing keys: {missing}'}), 400

    top_k = int(data.get('top_k', 9))
    recs = recommend(PLANTS, data, top_k=9, threshold=50)
    care = generate_care_plan(recs)
    return jsonify({
        'recommendations': recs,
        'care_plan': care,
        'meta': {'total_plants': int(len(PLANTS)), 'threshold': 50}
    })

@app.get('/health')
def health():
    return {'ok': True}

if __name__ == '__main__':
    app.run(debug=True)
