import requests
from server import django_server_url

def send_packet_ipcounts_to_server(ipcounts):
    try:
        response = requests.post(f'{django_server_url}/ippacket', json={'ip_counts': ipcounts})
        response.raise_for_status()
        print("IP packet counts sent to Django server successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send IP packet counts to Django server: {e}")
