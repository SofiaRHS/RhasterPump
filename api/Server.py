import os
from flask import Flask, jsonify
from data.Storage import signals

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "<h2>Pump Monitor API</h2><p>Доступные эндпоинты: /signals</p>"

@app.route("/signals", methods=["GET"])
def get_signals():
    return jsonify(signals)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
