from data.Storage import price_data, signals
from lib.Utils import send_email
from Config import PUMP_THRESHOLD

def analyze(symbol_interval, new_close):
    old_close = price_data.get(symbol_interval, {}).get("close")
    if old_close:
        percent = (new_close - old_close)/old_close*100
        price_data[symbol_interval]["percent"] = percent
        signal = "none"
        if percent >= PUMP_THRESHOLD:
            signal = "pump"
            send_email(f"{symbol_interval} Pump Alert", f"{symbol_interval} increased {percent:.2f}%")
        elif percent <= -PUMP_THRESHOLD:
            signal = "drop"
            send_email(f"{symbol_interval} Drop Alert", f"{symbol_interval} decreased {percent:.2f}%")
        signals[symbol_interval] = signal
    else:
        price_data[symbol_interval] = {"close": new_close, "percent":0}
        signals[symbol_interval] = "none"
