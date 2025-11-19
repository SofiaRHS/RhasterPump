from data.Storage import add_signal, price_history
from Config import PUMP_THRESHOLD, VOLUME_MULTIPLIER, AVG_VOLUME_CANDLES

def analyze_candle(symbol, interval, close, volume):
    key = f"{symbol}_{interval}"
    candles = price_history.get(key, [])
    if len(candles) < AVG_VOLUME_CANDLES:
        return

    avg_vol = sum([v for t, c, v in candles[-AVG_VOLUME_CANDLES:]]) / AVG_VOLUME_CANDLES
    last_close = candles[-1][1]
    change = ((close - last_close) / last_close) * 100

    if change >= PUMP_THRESHOLD and volume >= avg_vol * VOLUME_MULTIPLIER:
        add_signal(symbol, interval, change, volume, avg_vol)
