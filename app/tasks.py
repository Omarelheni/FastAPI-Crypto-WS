from app.routers import coins
import asyncio
import os
from dotenv import load_dotenv
import asyncio
import websockets
import json 
from .routers.coins import manager

load_dotenv()

symbols = ["bnbusdt", "btcusdt"]
stream = "/".join([f"{s}@aggTrade" for s in symbols])
url = f"wss://fstream.binance.com/stream?streams={stream}"

async def binance_ws_multi():
    async with websockets.connect(url) as ws:
        async for message in ws:
            msg = json.loads(message)
            stream_name = msg["stream"]
            data = msg["data"]
            
            # Message compréhensible
            simplified = {
                "symbol": data["s"],
                "price": float(data["p"]),
                "quantity": float(data["q"]),
                "trade_id": data["a"],
                "timestamp": data["T"],
                "is_buyer_maker": data["m"]
            }
            print(f"Received data for {stream_name}: {simplified}")
            await manager.broadcast(f"{stream_name} → {simplified}")


async def broadcast_task():
    while True:
        try:
            await binance_ws_multi()
            await asyncio.sleep(1)  # retry après 1s
        except Exception as e:
            print("WebSocket error:", e)
            await asyncio.sleep(5)  # retry après 5s