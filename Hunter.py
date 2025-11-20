# hunter.py
import requests
import json
import time
from datetime import datetime
from collections import defaultdict

class PumpHunter:
    def __init__(self):
        self.data = defaultdict(lambda: {"p": [], "v": [], "t": None})
        self.alerts = []
        self.new_listings = set()
        self.known_coins = set()

    def get_tracked_coins(self):
        try:
            with open("coins.json", "r") as f:
                return json.load(f)
        except:
            default = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
            with open("coins.json", "w") as f:
                json.dump(default, f)
            return default

    def run(self):
        while True:
            try:
                info = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo", timeout=10).json()
                all_futures = [s["symbol"] for s in info["symbols"] 
                               if s["contractType"] == "PERPETUAL" and s["quoteAsset"] == "USDT"]

                # Новые листинги
                for sym in all_futures:
                    if sym not in self.known_coins and sym not in self.new_listings:
                        self.new_listings.add(sym)
                        self.alerts.append({"type": "NEW LISTING", "coin": sym, "time": datetime.now().strftime("%H:%M:%S")})
                        # Автодобавление
                        coins = self.get_tracked_coins()
                        if sym not in coins:
                            coins.append(sym)
                            with open("coins.json", "w") as f:
                                json.dump(coins, f)
                self.known_coins = set(all_futures)

                tickers = requests.get("https://fapi.binance.com/fapi/v1/ticker/24hr", timeout=10).json()
                ticker_dict = {t["symbol"]: t for t in tickers}

                for sym in self.get_tracked_coins():
                    if sym not in ticker_dict: continue
                    t = ticker_dict[sym]
                    price = float(t["lastPrice"])
                    volume = float(t["quoteVolume"])
                    ts = time.time()

                    d = self.data[sym]
                    d["p"].append((ts, price))
                    d["v"].append((ts, volume))
                    d["t"] = ts

                    d["p"] = [x for x in d["p"] if ts - x[0] < 600]
                    d["v"] = [x for x in d["v"] if ts - x[0] < 600]

                    if len(d["p"]) < 5: continue

                    # 1m изменение
                    old_price = next((p for t,p in reversed(d["p"]) if ts-t >= 55), d["p"][0][1])
                    change = (price / old_price - 1) * 100

                    # Объём
                    recent_vol = [v for t,v in d["v"] if ts-t < 300]
                    avg_vol = sum(recent_vol)/len(recent_vol) if recent_vol else volume
                    vol_mult = volume / avg_vol

                    now = time.time()
                    if change >= 8 and vol_mult >= 3:
                        if not any(a.get("coin")==sym and a["type"]=="PUMP" and now-a.get("ts",0)<120 for a in self.alerts[-5:]):
                            self.alerts.append({"type": "PUMP", "coin": sym, "change": change, "time": datetime.now().strftime("%H:%M:%S"), "ts": now})
                    if change <= -8 and vol_mult >= 3:
                        if not any(a.get("coin")==sym and a["type"]=="DUMP" and now-a.get("ts",0)<120 for a in self.alerts[-5:]):
                            self.alerts.append({"type": "DUMP", "coin": sym, "change": change, "time": datetime.now().strftime("%H:%M:%S"), "ts": now})

            except:
                pass
            time.sleep(3)

    def get_realtime_data(self):
        rows = []
        for sym, d in self.data.items():
            if d["t"] and time.time() - d["t"] < 20 and len(d["p"]) >= 2:
                old = next((p for t,p in reversed(d["p"]) if time.time()-t >= 55), d["p"][0][1])
                ch = (d["p"][-1][1] / old - 1) * 100
                status = "PUMP" if ch >= 8 else "DUMP" if ch <= -8 else "—"
                rows.append({"Пара": sym, "Цена": f"${d['p'][-1][1]:,.2f}", "1m %": f"{ch:+.2f}", "Статус": status})
        return rows