from flask import Flask, render_template, jsonify, request
from lib.Websocket import start_ws
from data.Storage import Storage
from lib.Analysis import analyze_signal
import threading

app = Flask(__name__)
storage = Storage("data/pairs.json")

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/signals")
def signals():
    timeframe = request.args.get("tf", "1m")
    data = []
    for pair in storage.get_pairs():
        signal = analyze_signal(pair, timeframe)
        data.append({
            "pair": pair,
            "percent": signal["percent"],
            "trend": signal["trend"]
        })
    return jsonify(data)

@app.route("/add_pair", methods=["POST"])
def add_pair():
    pair = request.json.get("pair")
    if pair:
        storage.add_pair(pair.upper())
        return jsonify({"status": "added", "pair": pair.upper()})
    return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    threading.Thread(target=start_ws, args=(storage,)).start()
    app.run(host="0.0.0.0", port=5000)
