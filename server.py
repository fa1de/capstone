import socket
import threading
import json
import re
import requests

patterns = []

def load_patterns():
    with open('정규표현식.txt', 'r') as file:
        for pattern in file:
            patterns.append(re.compile(pattern.strip()))

def handle_client(client_socket):
    try:
        request = client_socket.recv(4096)
        if not request:
            raise ValueError("Empty request received")

        data = json.loads(request.decode())
        if 'packets' not in data or not isinstance(data['packets'], list):
            raise ValueError("Invalid packets data format")

        matched_packets = []
        unmatched_packets = []

        for packet in data['packets']:
            if not isinstance(packet, dict) or 'data' not in packet:
                print("Invalid packet format:", packet)
                continue

            if any(pattern.search(packet['data']) for pattern in patterns):
                matched_packets.append(packet)
            else:
                unmatched_packets.append(packet)

        if matched_packets:
            response = requests.post('http://your-django-server.com/api/matched_packets', json={'packets': matched_packets})
            response.raise_for_status()
        if unmatched_packets:
            response = requests.post('http://your-django-server.com/api/unmatched_packets', json={'packets': unmatched_packets})
            response.raise_for_status() 

        client_socket.send("Data processed and sent to Django server.".encode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    load_patterns()
    server_host = '127.0.0.1'  
    server_port = 8080  
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_host}:{server_port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()

if __name__ == "__main__":
    start_server()