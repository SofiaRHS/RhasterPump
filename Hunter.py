# hunter_core.py
# Чистое ядро Pump Hunter Pro 2025 — работает без GUI, без лагов, 1500+ монет

import json
import time
import requests
from datetime import datetime
from collections import defaultdict
import threading
import os
import winsound

class PumpHunterCore:
    def __init__(self):
        self.data = defaultdict(lambda: {"p": [], "v": [], "t": None})
        self.alerts = []
        self.new_listings = set()
        self.known_coins = set()
        self.first_run = True
        self.lock = threading.Lock()

    def load_coins(self):
        try:
            with open("coins.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            default = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "1000SATSUSDT"]
            with open("coins.json", "w", encoding="utf-8") as f:
                json.dump(default, f, indent=2)
            return default

    def beep(self, freq=1800, dur=800):
        try: winsound.Beep(freq, dur)
        except: pass

    def popup(self, text):
        if os.name == "nt":
            try:
                os.system(f'powershell -Command "[Console]::Beep(2000,300); [System.Windows.Forms.MessageBox]::Show(\'{text}\', \'PUMP HUNTER PRO\', \'OK\', \'Warning\')"')
            except: pass

    def add_alert(self, alert_type, coin, change=None, vol=None):
        with self.lock:
            now = time.time()
            # Анти-дребезг: не больше 1 алерта на монету каждые 90 сек
            recent = [a for a in self.alerts[-15:] if a["coin"] == coin and a["type"] == alert_type]
            if any(now - a["ts"] < 90 for a in recent):
                return

            alert = {
                "type": alert_type,
                "coin": coin,
                "change": round(change, 2) if change is not None else None,
                "vol": round(vol, 1) if vol is not None else None,
                "time": datetime.now().strftime("%H:%M:%S"),
                "ts": now
            }
            self.alerts.append(alert)

            if alert_type == "PUMP":
                self.beep(2200, 900)
                self.popup(f"PUMP! {coin} +{change:.1f}% ×{vol:.1f}")
            elif alert_type == "DUMP":
                self.beep(600, 1200)

    def run(self):
        session = requests.Session()
        session.headers.update({"User-Agent": "PumpHunterPro/2025"})

        while True:
            try:
                # Все перпы USDT
                info = session.get("https://fapi.binance.com/fapi/v1/exchangeInfo", timeout=8).json()
                all_perps = {
                    s["symbol"] for s in info.get("symbols", [])
                    if s.get("contractType") == "PERPETUAL" and s.get("quoteAsset") == "USDT"
                }

                # Новые листинги
                if self.first_run:
                    self.known_coins = all_perps.copy()
                    self.first_run = False
                else:
                    new = all_perps - self.known_coins
                    for sym in new:
                        if sym not in self.new_listings:
                            self.new_listings.add(sym)
                            self.add_alert("NEW", sym)
                            # Автодобавление
                            coins = self.load_coins()
                            if sym not in coins:
                                coins.append(sym)
                                with open("coins.json", "w", encoding="utf-8") as f:
                                    json.dump(coins, f, indent=2)

                self.known_coins = all_perps

                # Тикеры
                tickers = session.get("https://fapi.binance.com/fapi/v1/ticker/24hr", timeout=8).json()
                tracked = self.load_coins()
                td = {t["symbol"]: t for t in tickers if t["symbol"] in tracked}

                now = time.time()
                for sym in tracked:
                    if sym not in td: continue
                    t = td[sym]
                    price = float(t["lastPrice"])
                    volume = float(t["quoteVolume"])
                    ts = time.time()

                    d = self.data[sym]
                    d["p"].append((ts, price))
                    d["v"].append((ts, volume))
                    d["t"] = ts

                    # Очистка старых точек (10 мин)
                    d["p"] = [x for x in d["p"] if ts - x[0] < 600]
                    d["v"] = [x for x in d["v"] if ts - x[0] < 600]

                    if len(d["p"]) < 5: continue

                    # Цена 55+ сек назад
                    old_price = next((p for t,p in reversed(d["p"]) if ts-t >= 55), d["p"][0][1])
                    change_pct = (price / old_price - 1) * 100

                    # Объём за последние 5 минут
                    recent_vols = [v for t,v in d["v"] if ts-t < 300]
                    avg_vol = sum(recent_vols) / len(recent_vols) if recent_vols else volume
                    vol_mult = volume / avg_vol if avg_vol > 0 else 1

                    if change_pct >= 8.0 and vol_mult >= 3.0:
                        self.add_alert("PUMP", sym, change_pct, vol_mult)
                    elif change_pct <= -8.0 and vol_mult >= 3.0:
                        self.add_alert("DUMP", sym, change_pct, vol_mult)

            except Exception as e:
                print(f"[ERROR] {e}")
            time.sleep(2.15)

    def get_table_data(self):
        rows = []
        now = time.time()
        for sym in self.load_coins():
            d = self.data.get(sym, {})
            if not d.get("t") or now - d["t"] > 30 or len(d.get("p", [])) < 2:
                continue
            old = next((p for t,p in reversed(d["p"]) if now-t >= 55), d["p"][0][1])
            change = (d["p"][-1][1] / old - 1) * 100
            price = d["p"][-1][1]
            status = "PUMP" if change >= 8 else "DUMP" if change <= -8 else ""
            rows.append((sym, price, change, status))
        rows.sort(key=lambda x: abs(x[2]), reverse=True)
        return rows