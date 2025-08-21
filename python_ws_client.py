import asyncio
import httpx
import websockets

API_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws/crypto"

USERNAME = "omar@gmail.com"
PASSWORD = "omar"

# 🔑 Authentification pour récupérer le JWT
async def login():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/users/login",
            json={"email": USERNAME, "password": PASSWORD}
        )
        if response.status_code != 200:
            raise Exception(f"Login failed: {response.text}")
        data = response.json()
        print("✅ Login successful, token received:", data)
        return data["access_token"]

# 🔗 Connexion WebSocket avec le JWT dans Sec-WebSocket-Protocol
async def ws_client(token: str):
    async with websockets.connect(
        WS_URL,
        subprotocols=["jwt", token]
    ) as websocket:
        print("🔗 Connecté au serveur WebSocket")

        # Boucle pour recevoir des messages
        while True:
            try:
                # Réception d’un message
                response = await websocket.recv()
                print("📩 Message reçu:", response)
            except websockets.ConnectionClosed:
                print("🔌 Connexion fermée")
                break
            except Exception as e:
                print(f"Erreur lors de la réception du message: {e}")
                break
        # Réception d’un message
        response = await websocket.recv()
        print("📩 Message reçu:", response)

async def main():
    token = await login()
    await ws_client(token)

if __name__ == "__main__":
    asyncio.run(main())
