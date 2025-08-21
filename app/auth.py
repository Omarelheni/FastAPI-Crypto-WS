from datetime import datetime, timedelta
from typing import Optional
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Header
import os
from dotenv import load_dotenv
from fastapi import WebSocket
from jwt import PyJWTError
load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 200)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None


async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

async def get_current_user_ws(websocket: WebSocket):
    # Récupérer les subprotocols proposés par le client
    client_subprotocols = websocket.headers.get("sec-websocket-protocol")
    if not client_subprotocols:
        await websocket.close(code=4401)
        return

    # Les sous-protocoles sont envoyés en CSV → "jwt, <token>"
    parts = [p.strip() for p in client_subprotocols.split(",")]
    if len(parts) != 2 or parts[0] != "jwt":
        await websocket.close(code=4401)
        return

    token = parts[1]
    print(f"Token reçu : {token}")
    if not token:
        print("Invalid token")

        await websocket.close(code=1008)
        return None
    try:
        return verify_token(token)
    except PyJWTError:
        await websocket.close(code=1008)
        print("Invalid token")
        return None
