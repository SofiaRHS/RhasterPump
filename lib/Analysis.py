from datetime import datetime
from data.Storage import price_history, volume_history, add_signal
from Config import PUMP_THRESHOLD, VOLUME_MULTIPLIER

def check_pump(symbol, interval):
    key = f"{symbol}_{interval}"
    pri = price_history[key]
    vol = volume_history[key]
    if len(pri) < 2 or len(vol) < 2:
        return None

    old_price = pri[0][1]
    current_price = pri[-1][1]
    change = (current_price - old_price) / old_price * 100
    avg_vol = sum(v for (_, v) in vol)/len(vol)
    current_vol = vol[-1][1]

    if change >= PUMP_THRESHOLD and current_vol >= avg_vol * VOLUME_MULTIPLIER:
        signal = {
            "time": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "interval": interval,
            "change": round(change, 2),
            "volume": current_vol,
            "avg_volume": avg_vol
        }
        add_signal(symbol, interval, signal)
        return signal
    return None
