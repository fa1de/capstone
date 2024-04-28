import socket
import threading
import json
import re
import requests
import redis
import logging

logging.basicConfig(filename='packet_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

patterns = []
redis_client = redis.Redis(host='localhost', port=6379, db=0)

django_server_url = '192.168.0.46'

def load_patterns():
    with open('RE.py', 'r') as file:
        for pattern in file:
            patterns.append(re.compile(pattern.strip()))

def handle_client(client_socket, client_address):
    ip_address = client_address[0]
   
    if redis_client.get(f"blacklist:{ip_address}"):
        print(f"Blocked IP: {ip_address}")
        client_socket.close()
        return

    try:
        request = client_socket.recv(4096)
        if not request:
            raise ValueError("Empty request received")

        data = json.loads(request.decode())
        if 'packets' not in data or not isinstance(data['packets'], list):
            raise ValueError("Invalid packets data format")
  
        process_packets(data['packets'])
  
        client_socket.send("Data processed and sent to Django server.".encode())
        
    except Exception as e:
        print(f"Error: {e}")
        redis_client.setex(f"blacklist:{ip_address}", 3600, 'blocked')

    finally:
        client_socket.close()

def process_packets(packets):
    matched_packets = []
    unmatched_packets = []

    for packet in packets:
        if not isinstance(packet, dict) or 'data' not in packet:
            print("Invalid packet format:", packet)
            continue

        if any(pattern.search(packet['data']) for pattern in patterns):
            matched_packets.append(packet)
            logging.info(f"Matched packet: {packet}")
            send_notification_to_django("Suspicious packet detected", '/api/notify')

        else:
            unmatched_packets.append(packet)

    if matched_packets:
        send_to_django(matched_packets, '/api/matched_packets')
    if unmatched_packets:
        send_to_django(unmatched_packets, '/api/unmatched_packets')

def send_notification_to_django(message, endpoint):
    try:
        response = requests.post(f'{django_server_url}{endpoint}', json={'message': message})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification to Django server: {e}")

def send_to_django(packets, endpoint):
    try:
        response = requests.post(f'{django_server_url}{endpoint}', json={'packets': packets})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send packets to Django server: {e}")

def monitor_traffic(ip_address):
    current_count = redis_client.incr(ip_address)
    if current_count == 1:
        redis_client.expire(ip_address, 10)

    if current_count > 100:
        redis_client.setex(f"blacklist:{ip_address}", 3600, "true")
        print(f"DDOS detected, IP blocked: {ip_address}")

def start_server():
    load_patterns()
    server_host = '192.168.0.46'  
    server_port = 8000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_host}:{server_port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
            monitor_traffic(client_address[0])
    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()

if __name__ == "__main__":
    start_server()