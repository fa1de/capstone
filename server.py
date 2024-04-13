import socket
import threading
import json
import re
import requests

def handle_client(client_socket):
    try:
        request = client_socket.recv(4096)
        print(f"Received data from client: {request.decode()}")

        data = json.loads(request.decode())
        matched_packets = []
        unmatched_packets = []

        with open('정규표현식.txt', 'r') as file:
            patterns = file.readlines()

        for packet in data.get('packets', []):
            if any(re.search(pattern.strip(), packet['data']) for pattern in patterns):
                matched_packets.append(packet)
            else:
                unmatched_packets.append(packet)

        if matched_packets:
            response = requests.post('http://your-django-server.com/api/matched_packets', json={'packets': matched_packets})
            print(f"Matched packets sent with status code {response.status_code}")
        if unmatched_packets:
            response = requests.post('http://your-django-server.com/api/unmatched_packets', json={'packets': unmatched_packets})
            print(f"Unmatched packets sent with status code {response.status_code}")

        client_socket.send("Data processed and sent to Django server.".encode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    server_host = '127.0.0.1'  
    server_port = 8080  

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_host}:{server_port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()

if __name__ == "__main__":
    start_server()
