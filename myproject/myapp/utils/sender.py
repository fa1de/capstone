import requests


import requests
from .config import SERVER_URL


def send_to_server(endpoint, body):
    try:
        response = requests.post(f"{SERVER_URL}{endpoint}", json=body, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send packets to Django server: {e}")
