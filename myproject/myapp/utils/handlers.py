import logging

from dataclasses import dataclass, asdict
from .rules import rules
from .extractor import extract_packet
from .sender import send_to_server
from .rules import rules


@dataclass
class ProtocolInfoRequest:
    protocol_name: str
    source_ip: str
    target_ip: str
    pattern: str


def handle_packet(packet):
    try:
        print("============== handle_packet ==============")
        print(packet)
        packet = extract_packet(packet)
        if not packet:
            print("packet is None")
            return
        print("============== packet ==============")
        print(packet)

        packet_data = packet["packet_data"]
        logging.info("Processing packet data: %s", packet_data)

        matched_pattern = ""

        for pattern in rules:
            if searched := pattern.search(packet_data):
                matched_pattern = searched.group()
                break

        print("============== pattern ==============")
        print(matched_pattern)

        request = ProtocolInfoRequest(
            protocol_name=packet["protocol_name"],
            source_ip=packet["source_ip"] if "source_ip" in packet else "127.0.0.1",
            target_ip=packet["target_ip"] if "target_ip" in packet else "127.0.0.1",
            pattern=matched_pattern,
        )
        body = asdict(request)

        print(body)

        send_to_server("/protocol", body)
    except Exception as e:
        logging.error(f"Failed to send data to server: {e}")

    return
