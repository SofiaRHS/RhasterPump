import asyncio
import threading
from api.Server import app
from lib.Websocket import start_ws
import os

def run_api():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_api).start()
    asyncio.run(start_ws())
