# 🚀 FastAPI Crypto WebSocket - Real-Time Tracking

Un projet performant basé sur **FastAPI** démontrant une architecture robuste pour le suivi des prix de crypto-monnaies en temps réel. Ce projet utilise des WebSockets, Redis (Pub/Sub) et une architecture microservices pour diffuser des données provenant de l'API Binance à plusieurs clients authentifiés.

---

## 🏗️ Architecture du Projet

Le projet est divisé en plusieurs composants clés fonctionnant de manière asynchrone :

1.  **🚀 FastAPI App** : Le cœur du système, gérant l'authentification JWT, les préférences utilisateurs et les connexions WebSocket.
2.  **📡 Producer (Binance Wrapper)** : Un service indépendant qui se connecte au flux WebSocket de Binance, simplifie les données et les publie dans Redis.
3.  **🔴 Redis (Pub/Sub)** : Joue le rôle de message broker, permettant de découpler le flux de données Binance de l'application principale.
4.  **🗄️ PostgreSQL** : Stocke les informations des utilisateurs et leurs listes de surveillance (watchlists).
5.  **🛠️ Alembic** : Gère les migrations de base de données de manière asynchrone.

---

## ✨ Fonctionnalités Avancées

-   **Authentification JWT Sécurisée** : Protection des endpoints API et des connexions WebSocket.
-   **Handshake WebSocket JWT** : Utilisation du subprotocol `Sec-WebSocket-Protocol` pour transmettre le token de manière sécurisée lors de la connexion initiale.
-   **Broadcasting Sélectif** : Les clients reçoivent uniquement les données des symboles qu'ils ont définis dans leurs préférences (`prefered_symbols`).
-   **Système Pub/Sub robuste** : L'application s'abonne à un canal Redis global et distribue les messages intelligemment aux clients connectés.
-   **Stack Docker-Ready** : Déploiement simplifié avec Docker Compose incluant des outils de management (Adminer).

---

## 🛠️ Stack Technique

-   **Backend** : FastAPI, Uvicorn, Pydantic v2.
-   **ORM & DB** : SQLAlchemy 2.0 (Async), PostgreSQL, Alembic.
-   **Cache/Broker** : Redis (aioredis).
-   **Sécurité** : JWT (PyJWT), Passlib (Bcrypt).
-   **DevOps** : Docker, Docker Compose.

---

## 🐳 Installation & Lancement

### 1. Prérequis
-   Docker et Docker Compose installés.
-   Un fichier `.env` configuré à la racine (voir section Configuration).

### 2. Démarrage rapide
```bash
docker compose up --build
```
*Cette commande lance la base de données, exécute les migrations via Alembic, démarre Redis, le Producer et l'API FastAPI.*

### 3. Accès aux outils
-   **API (Swagger)** : [http://localhost:8000/docs](http://localhost:8000/docs)
-   **Adminer (Gestion DB)** : [http://localhost:8084](http://localhost:8084) (Serveur: `db`, Utilisateur: voir `.env`)

---

## 🔑 Configuration (.env)

Créez un fichier `.env` à la racine :
```env
# Variables pour Postgres
POSTGRES_USER=admin
POSTGRES_PASSWORD=
POSTGRES_DB=mydatabase
POSTGRES_HOST=db        # correspond au nom du service dans docker-compose
POSTGRES_PORT=5432
SECRET_KEY=

REDIS_HOST=redis
# Variable utilisée par SQLAlchemy
DATABASE_URL=

```

---

## 💻 Utilisation du Client WebSocket

Pour tester la connexion en temps réel, un client Python est fourni. Il automatise le login et la connexion WebSocket.

0.  **Créer un utilisateur** avec `add_user.py`
1.  **Mise à jour des identifiants** dans `python_ws_client.py` (USERNAME et PASSWORD).
2.  **Lancement du client** :
    ```bash
    python python_ws_client.py
    ```

### Handshake Technique :
Le client doit envoyer le token JWT via les sous-protocoles WebSocket :
`subprotocols=["jwt", "<VOTRE_TOKEN_ICI>"]`

---

## 📋 Endpoints Principaux

| Méthode | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/users/` | Création d'un compte utilisateur |
| `POST` | `/users/login` | Login & Récupération du JWT |
| `GET` | `/users/` | Liste des utilisateurs (Audit) |
| `WS` | `/ws/crypto` | Endpoint WebSocket (Nécessite Auth) |

---

## 🛠️ Développement local (sans Docker)

1.  Installez les dépendances : `pip install -r requirements.txt`
2.  Lancez un Redis et Postgres localement.
3.  Exécutez les migrations : `alembic upgrade head`
4.  Lancez l'app : `fastapi dev main.py`
5.  Lancez le producer : `python producer/producer.py`