import websocket, json, threading
from lib.Analysis import update_price

SOCKET_URL = "wss://stream.binance.com:9443/ws"

def start_ws(storage):
    def on_message(ws, message):
        data = json.loads(message)
        pair = data['s'].upper()
        price = float(data['c'])
        update_price(pair, price)

    def run():
        pairs = [p.lower() + "@ticker" for p in storage.get_pairs()]
        ws_url = SOCKET_URL + "/" + "/".join(pairs)
        ws = websocket.WebSocketApp(ws_url, on_message=on_message)
        ws.run_forever()

    threading.Thread(target=run).start()
