import os, requests
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, static_folder=".")
BASE = "https://otcharts.com"
KEY = os.getenv("OTCHARTS_API_KEY", "").strip()
ALLOWED_VENUES = {"otc", "forex"}

def api_get(path, params=None):
    if not KEY:
        return None, (jsonify({"error":"Clé OTCharts absente. Configure OTCHARTS_API_KEY dans .env."}), 503)
    try:
        r = requests.get(BASE + path, params=params, headers={
            "Authorization": f"Bearer {KEY}",
            "User-Agent": "PocketSignalPro/2.0 (market-data client)"
        }, timeout=20)
        try:
            data = r.json()
        except Exception:
            data = {"error": f"Réponse fournisseur non JSON (HTTP {r.status_code})."}
        if not r.ok:
            return None, (jsonify({"error":data.get("error", f"Fournisseur HTTP {r.status_code}")}), r.status_code)
        return data, None
    except requests.RequestException as e:
        return None, (jsonify({"error":f"Connexion fournisseur impossible : {e}"}), 502)

@app.get("/")
def index():
    return send_from_directory(".", "index.html")

@app.get("/api/symbols")
def symbols():
    venue = request.args.get("venue", "otc")
    if venue not in ALLOWED_VENUES:
        return jsonify({"error":"Marché non pris en charge."}), 400
    data, err = api_get("/v1/symbols", {"venue":venue})
    if err: return err
    return jsonify(data)

@app.get("/api/candles")
def candles():
    venue = request.args.get("venue", "otc")
    symbol = request.args.get("symbol", "")
    try:
        tf = int(request.args.get("tf", "60"))
        limit = min(300, max(30, int(request.args.get("limit", "180"))))
    except ValueError:
        return jsonify({"error":"tf et limit doivent être des nombres."}), 400
    if venue not in ALLOWED_VENUES or not symbol:
        return jsonify({"error":"Marché ou symbole invalide."}), 400
    allowed = {5,15,30,60,120,180,300,600,900,1800,3600,14400} if venue=="otc" else {60,120,180,300,600,900,1800,3600,14400}
    if tf not in allowed:
        return jsonify({"error":f"Intervalle {tf}s non fourni pour {venue}. Intervalles autorisés : {sorted(allowed)}"}), 400
    data, err = api_get("/v1/candles", {"venue":venue,"symbol":symbol,"tf":tf,"limit":limit})
    if err: return err
    if data.get("gaps",{}).get("runs",0):
        data["warning"] = "Des lacunes existent dans l'historique ; prudence avec les signaux."
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT","8000")), debug=False)
