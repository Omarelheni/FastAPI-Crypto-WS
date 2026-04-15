import asyncio
import websockets
import json 
import redis.asyncio as redis


symbols = ["bnbusdt", "btcusdt"]
stream = "/".join([f"{s}@aggTrade" for s in symbols])
url = f"wss://fstream.binance.com/stream?streams={stream}"

REDIS_HOST = "redis"
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


CHANNEL = "crypto"


async def binance_ws_multi():
    async with websockets.connect(url) as ws:
        async for message in ws:
            msg = json.loads(message)
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
            await redis_client.publish(CHANNEL, json.dumps(simplified))


asyncio.run(binance_ws_multi())