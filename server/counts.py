import requests
from config import *
import json
from dataclasses import dataclass, asdict


@dataclass
class ProtocolInfoRequest:
    protocol_name: str
    src_IP: str
    dest_IP: str
    count: int


def send_packet_counts_to_server(protocol_count, protocol_name):
    print("==============send_packet_counts_to_server=============")

    request = ProtocolInfoRequest(
        protocol_name=protocol_name,
        src_IP="0.0.0.0",
        dest_IP="0.0.0.0",
        count=protocol_count,
    )
    url = f"{SERVER_URL}/protocol-info/"
    body = asdict(request)

    print(url)
    print(body)

    try:
        response = requests.post(
            f"{SERVER_URL}/protocol-info/",
            json=body,
        )
        response.raise_for_status()
        print("Packet counts sent to Django server successfully.")
    except requests.exceptions.RequestException as e:
        print(
            f"[send_packet_counts_to_server] Failed to send packet counts to Django server: {e}"
        )
