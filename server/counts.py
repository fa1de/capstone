import requests
from config import B_SERVER_URL
import json


def send_packet_counts_to_server(protocol_counts):
    protocol_counts_str = json.dumps(protocol_counts)
    try:
        response = requests.post(
            f"{B_SERVER_URL}/packet/",
            json={"protocol_counts": protocol_counts_str},
        )
        response.raise_for_status()
        print("Packet counts sent to Django server successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send packet counts to Django server: {e}")
