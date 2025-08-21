from fastapi import APIRouter, WebSocket,WebSocketDisconnect
from typing import List

class ConnectionManager():
    def __init__(self):
        self.connected_sockets: List[WebSocket] = []
    
    async def connect(self,websocket):
        await websocket.accept()
        self.connected_sockets.append(websocket)
    
    async def broadcast(self,message: str):
        for socket in self.connected_sockets:
            await socket.send_text(message)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)


router  = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws/crypto")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.receive_text()
    except WebSocketDisconnect:
        print("Client déconnecté")