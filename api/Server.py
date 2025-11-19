from flask import Flask, render_template, jsonify
from data.Storage import price_data, signals
import threading, asyncio
from lib.Fetch import start_ws

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/data")
def data():
    return jsonify({"price_data": price_data, "signals": signals})

def run_ws():
    asyncio.run(start_ws())

threading.Thread(target=run_ws, daemon=True).start()
