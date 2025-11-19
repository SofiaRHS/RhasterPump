import asyncio, json, websockets
from data.Storage import pairs
from lib.Analysis import analyze
from Config import BINANCE_WS, INTERVALS

async def start_ws():
    streams = [f"{p.lower()}@kline_{i}" for p in pairs for i in INTERVALS]
    url = f"{BINANCE_WS}/stream?streams={'/'.join(streams)}"
    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if "data" in data and "k" in data["data"]:
                k = data["data"]["k"]
                symbol_interval = f"{k['s']}@{k['i']}"
                analyze(symbol_interval, float(k["c"]))
