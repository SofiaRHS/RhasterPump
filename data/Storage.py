from collections import deque, defaultdict

from Config import SYMBOLS, INTERVALS, HISTORY_CANDLES

price_history = {f"{s}_{i}": deque(maxlen=HISTORY_CANDLES) for s in SYMBOLS for i in INTERVALS}
volume_history = {f"{s}_{i}": deque(maxlen=HISTORY_CANDLES) for s in SYMBOLS for i in INTERVALS}
signals = defaultdict(list)

def add_candle(symbol, interval, timestamp, close, volume):
    key = f"{symbol}_{interval}"
    price_history[key].append((timestamp, close))
    volume_history[key].append((timestamp, volume))

def add_signal(symbol, interval, signal):
    key = f"{symbol}_{interval}"
    signals[key].append(signal)
