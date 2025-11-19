import asyncio
import json
import websockets
from Config import SYMBOLS, INTERVALS
from lib.Analysis import analyze_candle
from data.Storage import add_candle

BINANCE_WS = "wss://fstream.binance.com/stream?streams="

def build_stream_url():
    streams = []
    for s in SYMBOLS:
        for i in INTERVALS:
            streams.append(f"{s.lower()}@kline_{i}")
    return BINANCE_WS + "/".join(streams)

async def start_ws():
    url = build_stream_url()
    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            k = data["data"]["k"]
            symbol = k["s"]
            interval = k["i"]
            close = float(k["c"])
            volume = float(k["v"])
            add_candle(symbol, interval, close, volume)
            analyze_candle(symbol, interval, close, volume)
