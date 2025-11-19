import asyncio
import json
import websockets
from datetime import datetime
from Config import SYMBOLS, INTERVALS, BINANCE_WS
from data.Storage import add_candle
from lib.Analysis import check_pump

def make_payload():
    params = [f"{s.lower()}@kline_{i}" for s in SYMBOLS for i in INTERVALS]
    return json.dumps({
        "method": "SUBSCRIBE",
        "params": params,
        "id": 1
    })

async def start_ws():
    async with websockets.connect(BINANCE_WS) as ws:
        await ws.send(make_payload())
        async for msg in ws:
            data = json.loads(msg)
            if data.get("e") == "kline":
                k = data["k"]
                sym = k["s"]
                interval = k["i"]
                close = float(k["c"])
                volume = float(k["v"])
                ts = datetime.fromtimestamp(k["t"]/1000)
                add_candle(sym, interval, ts, close, volume)
                signal = check_pump(sym, interval)
                if signal:
                    print(f"[PUMP] {signal}")
