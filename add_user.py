import requests

def add_user():
    response = requests.post("http://localhost:8000/users", json={"name": "Omar Elheni", "email": "omar@gmail.com", "password": "password","prefered_symbols": ["bnbusdt", "btcusdt"]})
    return response.json()


if __name__ == "__main__":
    response = add_user()
    print(response)
