import asyncio, websockets, json
from data.Storage import price_data

BINANCE_WS = "wss://stream.binance.com:9443/stream?streams="

class BinanceWS:
    def __init__(self):
        self.symbols = ["clankerusdt", "resolvusdt", "uselessusdt"]
        self.intervals = ["1m", "5m", "15m", "30m"]

    async def subscribe(self):
        streams = [f"{s}@kline_{i}" for s in self.symbols for i in self.intervals]
        url = BINANCE_WS + "/".join(streams)
        async with websockets.connect(url) as ws:
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                # сохраняем данные в price_data
                key = f"{data['stream']}"
                k = data["data"]["k"]
                price_data[key] = {
                    "time": k["t"],
                    "open": float(k["o"]),
                    "close": float(k["c"]),
                    "volume": float(k["v"])
                }
