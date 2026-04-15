# app/subscriber.py
import redis.asyncio as redis
from app.routers.coins import manager
import os
from dotenv import load_dotenv

load_dotenv()


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")  # fallback à localhost si pas défini
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
import json
CHANNEL = "crypto"

async def redis_subscriber():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(CHANNEL)

    async for message in pubsub.listen():
        if message["type"] == "message":
            data = message["data"]

            # 🔥 broadcast vers clients WebSocket locaux
            if isinstance(data, str):
                data = json.loads(data)  # convertir en dict si c'est une string

            if "symbol" in data:
                await manager.broadcast(data["symbol"], str(data))
