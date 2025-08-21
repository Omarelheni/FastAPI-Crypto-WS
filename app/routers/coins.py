from fastapi import APIRouter, WebSocket,WebSocketDisconnect,Depends
from typing import List
from app.auth import get_current_user_ws

class ConnectionManager():
    def __init__(self):
        self.connected_sockets: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket, subprotocol: str):
        # accepter la connexion avec le subprotocol
        await websocket.accept(subprotocol=subprotocol)
        self.connected_sockets.append(websocket)
        print(f"Client connecté : {websocket.client}")
    
    async def broadcast(self,message: str):
        print(f" connected_sockets: {self.connected_sockets}")
        for socket in self.connected_sockets:
            print(f"Envoi du message : {message} à {socket.client}")
            await socket.send_text(message)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)


router  = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws/crypto")
async def websocket_endpoint(websocket: WebSocket, 
                            current_user: str = Depends(get_current_user_ws)):
    if not current_user:
        return
    await manager.connect(websocket, subprotocol="jwt")
    try:
        await websocket.receive_text()
    except WebSocketDisconnect:
        print("Client déconnecté")