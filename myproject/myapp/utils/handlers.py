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
    print("============== handle_packet ==============")
    packet = extract_packet(packet)
    if not packet:
        return
    print("============== packet ==============")
    print(packet)

    packet_data = packet["packet_data"]
    logging.info(f"Processing packet data: {packet_data}")

    matched_pattern = ""

    for pattern in rules:
        if pattern.search(packet_data):
            matched_pattern = pattern.pattern
            break

    print("============== pattern ==============")
    print(matched_pattern)

    request = ProtocolInfoRequest(
        protocol_name=packet["protocol_name"],
        source_ip="0.0.0.0",
        target_ip="127.0.0.1",
        pattern=matched_pattern,
    )
    body = asdict(request)

    send_to_server("/protocol-info", body)

    return
