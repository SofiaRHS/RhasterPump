import asyncio
from lib.Websocket import start_ws
import threading
from api.Server import app
import os

def start_api():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Запуск API в отдельном потоке
    t = threading.Thread(target=start_api)
    t.start()
    
    # Запуск WebSocket мониторинга
    asyncio.run(start_ws())
