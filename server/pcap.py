from scapy.all import sniff
from threading import Thread, Event
import keyboard
import psutil
import socket
import json
import subprocess
import time
from pro_counts import send_packet_counts_to_server
from ip_counts import send_packet_ipcounts_to_server

def get_interfaces():
    return psutil.net_if_addrs().keys()

def packet_sniffer(packet):
    protocol_info = extract_protocol_info(packet)
    if protocol_info:
        send_packet_to_server(protocol_info)
    update_packet_counts(packet)
    update_ip_packet_counts(packet)

def extract_protocol_info(packet):
    protocol_info = {}

    if 'IP' in packet:
        protocol_info.update(extract_ip_info(packet))
        protocol_info['protocol'] = packet['IP'].proto 

    if packet.haslayer('TCP'):
        protocol_info['protocol_name'] = 'TCP'
    elif packet.haslayer('UDP'):
        protocol_info['protocol_name'] = 'UDP'
    elif packet.haslayer('ICMP'):
        protocol_info['protocol_name'] = 'ICMP'
    elif packet.haslayer('DNS'):
        protocol_info['protocol_name'] = 'DNS'
    elif packet.haslayer('HTTP'):
        protocol_info['protocol_name'] = 'HTTP'
    elif packet.haslayer('FTP'):
        protocol_info['protocol_name'] = 'FTP'
    elif packet.haslayer('SSH'):
        protocol_info['protocol_name'] = 'SSH'

    if packet.haslayer('TCP') or packet.haslayer('UDP'):
        protocol_info.update(extract_transport_info(packet))

    if packet.haslayer('ICMP'):
        protocol_info.update(extract_icmp_info(packet))

    if packet.haslayer('DNS'):
        protocol_info.update(extract_dns_info(packet))

    if packet.haslayer('HTTP'):
        protocol_info.update(extract_http_info(packet))

    if packet.haslayer('FTP'):
        protocol_info.update(extract_ftp_info(packet))

    if packet.haslayer('SSH'):
        protocol_info.update(extract_ssh_info(packet))

    protocol_info['packet_data'] = packet.show(dump=True)

    return protocol_info if protocol_info else None

def extract_ip_info(packet):
    return {
        'source_ip': packet['IP'].src,
        'destination_ip': packet['IP'].dst
    }

def extract_transport_info(packet):
    transport_info = {}
    if packet.haslayer('TCP'):
        transport_info['source_port'] = packet['TCP'].sport
        transport_info['destination_port'] = packet['TCP'].dport
    elif packet.haslayer('UDP'):
        transport_info['source_port'] = packet['UDP'].sport
        transport_info['destination_port'] = packet['UDP'].dport
    return transport_info

def extract_icmp_info(packet):
    icmp_layer = packet['ICMP']
    return {
        'type': icmp_layer.type,
        'code': icmp_layer.code,
        'checksum': icmp_layer.chksum,
        'id': icmp_layer.id,
        'sequence': icmp_layer.seq
    }

def extract_dns_info(packet):
    dns_info = {}
    if packet['DNS'].qd:
        dns_info['dns_query'] = packet['DNS'].qd.qname.decode('utf-8')
    if packet['DNS'].an:
        # rdata가 이미 문자열인 경우 decode 제거
        dns_info['dns_response'] = str(packet['DNS'].an.rdata)
    return dns_info

def extract_http_info(packet):
    http_layer = packet['HTTP']
    return {
        'method': http_layer.Method.decode('utf-8'),
        'uri': http_layer.Path.decode('utf-8'),
        'version': http_layer.Http_Version.decode('utf-8')
    }

def extract_ftp_info(packet):
    ftp_layer = packet['FTP']
    return {
        'command': ftp_layer.Command.decode('utf-8'),
        'username': ftp_layer.Field_A.decode('utf-8'),
        'password': ftp_layer.Field_B.decode('utf-8')
    }

def extract_ssh_info(packet):
    ssh_layer = packet['SSH']
    return {
        'version': ssh_layer.kex_algorithms.decode('utf-8'),
        'algorithm': ssh_layer.encryption_algorithms_client_to_server.decode('utf-8'),
        'username': ssh_layer.user.decode('utf-8')
    }

# 전역 변수로 각 프로토콜에 대한 카운트를 저장하는 딕셔너리 초기화
protocol_counts = {
    'TCP': 0,
    'UDP': 0,
    'ICMP': 0,
    'DNS': 0,
    'HTTP': 0,
    'FTP': 0,
    'SSH': 0
}

def update_packet_counts(packet):
    if packet.haslayer('TCP'):
        protocol_counts['TCP'] += 1
    elif packet.haslayer('UDP'):
        protocol_counts['UDP'] += 1
    elif packet.haslayer('ICMP'):
        protocol_counts['ICMP'] += 1
    elif packet.haslayer('DNS'):
        protocol_counts['DNS'] += 1
    elif packet.haslayer('HTTP'):
        protocol_counts['HTTP'] += 1
    elif packet.haslayer('FTP'):
        protocol_counts['FTP'] += 1
    elif packet.haslayer('SSH'):
        protocol_counts['SSH'] += 1

    send_packet_counts_to_server(protocol_counts)
    print(protocol_counts)

ip_packet_counts = {}

def update_ip_packet_counts(packet):
    # IP 주소별 패킷 카운트 업데이트하는 로직 추가
    if 'IP' in packet:
        source_ip = packet['IP'].src
        if source_ip in ip_packet_counts:
            ip_packet_counts[source_ip] += 1
        else:
            ip_packet_counts[source_ip] = 1
    send_packet_ipcounts_to_server(ip_packet_counts)
    print(ip_packet_counts)

B_SERVER_ADDRESS = '127.0.0.1'
B_SERVER_PORT = 8002

def send_packet_to_server(packet_info):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((B_SERVER_ADDRESS, B_SERVER_PORT))
            message = json.dumps(packet_info)
            s.sendall(message.encode())
            print("Packet information sent to B server successfully.") 
    except Exception as e:
        print("Error while sending packet information to B server:", e)
        
def start_sniffer(interface, stop_event):
    def stop_sniffer(packet):
        return stop_event.is_set()
    sniff(prn=packet_sniffer, iface=interface, stop_filter=stop_sniffer)

if __name__ == "__main__":
    server_process = subprocess.Popen(['python', 'server.py'])
    time.sleep(5)

    stop_event = Event()

    interfaces = get_interfaces()
    print("Available interfaces: ")
    for index, interface in enumerate(interfaces):
        print(f"{index + 1}. {interface}")
    choice = int(input("Select the interface by number: "))
    selected_interface = list(interfaces)[choice - 1]

    sniffer_thread = Thread(target=start_sniffer, args=(selected_interface, stop_event))
    sniffer_thread.start()
    print("Press 'q' to stop the capture")
    keyboard.wait('q')
    stop_event.set()

    sniffer_thread.join()
    print("Packet capture stopped.")
    
    server_process.terminate()
    print("Server process terminated.")