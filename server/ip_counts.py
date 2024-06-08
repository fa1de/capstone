import requests
from config import B_SERVER_URL


def send_packet_ipcounts_to_server(ipcounts):
    try:
        response = requests.post(
            f"{B_SERVER_URL}/ippacket", json={"ip_counts": ipcounts}
        )
        response.raise_for_status()
        print("IP packet counts sent to Django server successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send IP packet counts to Django server: {e}")
