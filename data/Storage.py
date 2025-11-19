from collections import defaultdict
from datetime import datetime

# Структуры хранения
signals = defaultdict(list)        # {"SYMBOL_INTERVAL": [signal,...]}
price_history = defaultdict(list)  # {"SYMBOL_INTERVAL": [(time, close, volume), ...]}

def add_candle(symbol, interval, close, volume):
    key = f"{symbol}_{interval}"
    price_history[key].append((datetime.utcnow(), close, volume))
    # Сохраняем только последние 500 свечей
    if len(price_history[key]) > 500:
        price_history[key] = price_history[key][-500:]

def add_signal(symbol, interval, change, volume, avg_volume):
    key = f"{symbol}_{interval}"
    signals[key].append({
        "time": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "interval": interval,
        "change": change,
        "volume": volume,
        "avg_volume": avg_volume
    })
    # Сохраняем максимум 50 сигналов
    if len(signals[key]) > 50:
        signals[key] = signals[key][-50:]
