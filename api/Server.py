from flask import Flask, jsonify, render_template
from data.Storage import signals, price_history
from lib.Fetch import get_symbols

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/signals")
def get_signals():
    return jsonify(signals)

@app.route("/symbols")
def symbols():
    return jsonify(get_symbols())

@app.route("/candles/<symbol>/<interval>")
def candles(symbol, interval):
    key = f"{symbol}_{interval}"
    data = [{"time": t.isoformat(), "close": c, "volume": v} for t,c,v in price_history.get(key,[])]
    return jsonify(data)
