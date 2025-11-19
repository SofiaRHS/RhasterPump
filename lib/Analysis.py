from data.Storage import price_data, signals

def analyze():
    for key, v in price_data.items():
        change = (v["close"] - v["open"]) / v["open"] * 100
        if change >= 10:  # порог
            signals[key] = "pump"
        elif change <= -5:
            signals[key] = "drop"
        else:
            signals[key] = "normal"
