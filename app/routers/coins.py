from fastapi import APIRouter, WebSocket,WebSocketDisconnect,Depends
from typing import List
from app.auth import get_current_user_ws
from app.service import get_watchlists_symbols_by_user_id
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db


class ConnectionManager():
    def __init__(self):
        self.connected_sockets: List[dict] = []
    
    async def connect(self, websocket: WebSocket,symbols: List[str], subprotocol: str):
        # accepter la connexion avec le subprotocol
        await websocket.accept(subprotocol=subprotocol)
        self.connected_sockets.append({"websocket": websocket, "symbols": symbols})
        print(f"Client connecté : {websocket.client}")
    
    async def broadcast(self, symbol: str, message: str):
        for socket in self.connected_sockets:
            if not socket["symbols"] or symbol in socket["symbols"]:
                print(f"Envoi du message : {message} à {socket['websocket'].client}")
                await socket['websocket'].send_text(message)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)


router  = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws/crypto")
async def websocket_endpoint(websocket: WebSocket, 
                            current_user: str = Depends(get_current_user_ws),
                            db: AsyncSession = Depends(get_db)):
    if not current_user:
        return
    symbols = await get_watchlists_symbols_by_user_id(db, current_user["id"])
    await manager.connect(websocket, symbols, subprotocol="jwt")
    try:
        await websocket.receive_text()
    except WebSocketDisconnect:
        print("Client déconnecté")