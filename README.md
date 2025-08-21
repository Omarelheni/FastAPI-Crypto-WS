# FastAPI Crypto WebSocket

Un projet **FastAPI** démontrant l’asynchronisation et les WebSockets pour suivre les prix des cryptomonnaies en temps réel via l’API publique Binance, avec Docker.

---

## 🚀 Fonctionnalités

- Connexion à plusieurs streams Binance en **temps réel** (`aggTrade`)  
- Diffusion des données vers tous les clients connectés via WebSockets  
- Gestion des clients connectés et des déconnexions  
- Utilisation complète de **FastAPI async** pour un traitement non bloquant  
- Base de données Postgresql initialisée automatiquement 
- Conteneurisé avec **Docker Compose** pour un déploiement facile  

---

## 🐳 Installation avec Docker

### Démarrage rapide :

```bash
docker compose up --build
```

##  Connexion WebSocket :
Exemple avec websocat :

```bash
websocat ws://localhost:8000/ws/crypto
```