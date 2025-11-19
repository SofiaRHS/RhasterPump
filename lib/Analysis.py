import time

prices = {}

def update_price(pair, price):
    if pair not in prices:
        prices[pair] = []
    prices[pair].append((time.time(), price))
    if len(prices[pair]) > 500:
        prices[pair] = prices[pair][-500:]

def analyze_signal(pair, tf):
    tf_seconds = {"1m": 60, "5m": 300, "15m": 900, "30m": 1800}
    now = time.time()
    history = [p for t, p in prices.get(pair, []) if now - t <= tf_seconds.get(tf, 60)]
    if not history:
        return {"percent": 0, "trend": "neutral"}
    change = (history[-1] - history[0]) / history[0] * 100
    trend = "up" if change > 0 else "down" if change < 0 else "neutral"
    return {"percent": round(change, 2), "trend": trend}
