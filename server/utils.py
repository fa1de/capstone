import threading
import requests
import logging
import socket
import json
import importlib.util
import re
from config import BASE_IP, SERVER_PORT, SERVER_URL, B_SERVER_URL


def load_patterns(patterns: list):
    # rules.py 모듈을 동적으로 로드
    spec = importlib.util.spec_from_file_location("rules", "rules.py")
    rules = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rules)

    # rules.py의 모든 패턴을 불러옴
    for attr_name in dir(rules):
        attr = getattr(rules, attr_name)
        if isinstance(attr, re.Pattern):
            patterns.append(attr)

    if not patterns:
        print("No patterns loaded from rules.py.")
    else:
        print(f"Loaded {len(patterns)} patterns from rules.py.")


def handle_client(client_socket, client_address, patterns: list):
    try:
        request = client_socket.recv(4096)
        if not request:
            raise ValueError("Empty request received")

        data = json.loads(request.decode())
        if "packet_data" not in data:
            raise ValueError("Invalid packets data format")

        print(patterns)

        matched_packets, unmatched_packets = process_packets([data], patterns)

        if matched_packets:
            send_to_django(matched_packets, "/api/matched_packets")
        if unmatched_packets:
            send_to_django(unmatched_packets, "/api/unmatched_packets")

        client_socket.send("Data processed and sent to Django server.".encode())

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()


def process_packets(packets, patterns: list):
    matched_packets = []
    unmatched_packets = []

    if not patterns:
        print("No patterns available for matching.")
        return matched_packets, unmatched_packets

    for packet in packets:
        if not isinstance(packet, dict) or "packet_data" not in packet:
            print("Invalid packet format:", packet)
            continue

        packet_data = packet["packet_data"]
        logging.info(f"Processing packet data: {packet_data}")

        matched = False
        matched_pattern = None

        for pattern in patterns:
            if pattern.search(packet_data):
                matched = True
                matched_pattern = pattern.pattern
                break

        if matched:
            matched_packets.append(packet)
            logging.info(f"Matched packet data: {packet['packet_data']}")
            logging.info(f"Matched with pattern: {matched_pattern}")
            send_notification_to_django("Suspicious packet detected", "/api/notify")
        else:
            unmatched_packets.append(packet)

    return matched_packets, unmatched_packets


def send_notification_to_django(message, endpoint):
    try:
        response = requests.post(f"{B_SERVER_URL}{endpoint}", json={"message": message})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification to Django server: {e}")


def send_to_django(packets, endpoint):
    try:
        response = requests.post(f"{B_SERVER_URL}{endpoint}", json={"packets": packets})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send packets to Django server: {e}")


def start_server(patterns):
    load_patterns(patterns)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((BASE_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {SERVER_URL}:{SERVER_PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = threading.Thread(
                target=handle_client, args=(client_socket, client_address, patterns)
            )
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()
