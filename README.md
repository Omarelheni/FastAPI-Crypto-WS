# FastAPI Crypto WebSocket

A **FastAPI** project demonstrating asynchronous processing and WebSockets to track cryptocurrency prices in real-time via the Binance public API, with Docker support.

---

## 🚀 Features

- Connect to multiple Binance streams in **real-time** (`aggTrade`)  
- Broadcast data to all connected clients via WebSockets  
- Manage connected clients and handle disconnections  
- Fully leverage **FastAPI async** for non-blocking processing  
- Automatically initialize a PostgreSQL database  
- Containerized with **Docker Compose** for easy deployment  

---

## 🐳 Installation with Docker

### Quick Start

```bash
docker compose up --build

```

## WebSocket Connection:
Use the Python client _ws_client.py script:

Update USERNAME and PASSWORD in the script.

Run the client:
```bash
python python_ws_client.py
```