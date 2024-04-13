import socket
from scapy.all import sniff
from threading import Thread, Event
import keyboard
import psutil

def get_interfaces():
    return psutil.net_if_addrs().keys()

def packet_sniffer(packet):
    protocol_info = extract_protocol_info(packet)
    analyze_and_send(protocol_info)     

def extract_protocol_info(packet):
    protocol_info = {}

    if 'IP' in packet:
        protocol_info.update(extract_ip_info(packet))
    
    if 'TCP' in packet or 'UDP' in packet:
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
    ip_info = {}
    ip_info['source_ip'] = packet['IP'].src
    ip_info['destination_ip'] = packet['IP'].dst
    return ip_info

def extract_transport_info(packet):
    transport_info = {}
    if 'TCP' in packet:
        transport_info['source_port'] = packet.sport
        transport_info['destination_port'] = packet.dport
    elif 'UDP' in packet:
        transport_info['source_port'] = packet.sport
        transport_info['destination_port'] = packet.dport
    return transport_info

def extract_icmp_info(packet):
    icmp_info = {}
    icmp_layer = packet['ICMP']
    icmp_info['type'] = icmp_layer.type
    icmp_info['code'] = icmp_layer.code
    icmp_info['checksum'] = icmp_layer.chksum
    icmp_info['id'] = icmp_layer.id
    icmp_info['sequence'] = icmp_layer.seq
    return icmp_info

def extract_dns_info(packet):
    dns_info = {}
    dns_info['dns_query'] = packet['DNS'].qd.qname.decode('utf-8')
    if packet['DNS'].an:
        dns_info['dns_response'] = packet['DNS'].an.rdata.decode('utf-8')
    return dns_info

def extract_http_info(packet):
    http_info = {}
    http_layer = packet['HTTP']
    http_info['method'] = http_layer.Method.decode('utf-8')
    http_info['uri'] = http_layer.Path.decode('utf-8')
    http_info['version'] = http_layer.Http_Version.decode('utf-8')
    return http_info

def extract_ftp_info(packet):
    ftp_info = {}
    ftp_layer = packet['FTP']
    ftp_info['command'] = ftp_layer.Command.decode('utf-8')
    ftp_info['username'] = ftp_layer.Field_A.decode('utf-8')
    ftp_info['password'] = ftp_layer.Field_B.decode('utf-8')
    return ftp_info

def extract_ssh_info(packet):
    ssh_info = {}
    ssh_layer = packet['SSH']
    ssh_info['version'] = ssh_layer.kex_algorithms.decode('utf-8')
    ssh_info['algorithm'] = ssh_layer.encryption_algorithms_client_to_server.decode('utf-8')
    ssh_info['username'] = ssh_layer.user.decode('utf-8')
    return ssh_info

def analyze_and_send(protocol_info):
    server_address = ('127.0.0.1', 8080)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(server_address)
            message = f"{protocol_info}"
            s.sendall(message.encode())
        except Exception as e:
            print("Error while sending packet to server:", e)

def start_sniffer(interface, stop_event):
    def stop_sniffer(packet):
        return stop_event.is_set()
    sniff(prn=packet_sniffer, iface=interface, stop_filter=stop_sniffer)

if __name__ == "__main__":
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