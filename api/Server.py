from flask import Flask, render_template, jsonify, request
from data.Storage import price_data, signals

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/data")
def get_data():
    # возвращаем все пары и сигналы
    return jsonify({
        "price_data": price_data,
        "signals": signals
    })

@app.route("/add_pair", methods=["POST"])
def add_pair():
    sym = request.json.get("symbol")
    # добавить подписку в Websocket клиент
    # например: ws_client.symbols.append(sym)
    return jsonify({"status": "ok", "symbol": sym})
