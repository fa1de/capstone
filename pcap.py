from scapy.all import sniff, wrpcap
import psutil
from threading import Thread, Event
import keyboard 
import requests

def get_interfaces():
    return psutil.net_if_addrs().keys()

def packet_sniffer(packet):
    print(packet.summary())
    wrpcap('captured_packets.pcap', packet, append=True)
    log_packet(packet)
    send_packet(packet)

def start_scapy_sniffer(interface, stop_event):
    def stop_sniffer(packet):
        return stop_event.is_set() 
    sniff(prn=packet_sniffer, iface=interface, stop_filter=stop_sniffer)

def log_packet(packet):
    
    with open('packet_log.txt', 'a') as file:
        file.write(str(packet) + '\n')

def send_packet(packet):
    
    url = 'http://localhost:5000/packet'  
    headers = {'Content-Type': 'application/json'}  
    packet_data = str(packet)  
    response = requests.post(url, data=packet_data, headers=headers)
    if response.status_code == 200:
        print('Packet sent successfully')
    else:
        print('Failed to send packet')

if __name__ == "__main__":
    stop_event = Event() 

    interfaces = get_interfaces()
    print("Available interfaces: ")
    for index, interface in enumerate(interfaces):
        print(f"{index + 1}. {interface}")
    choice = int(input("Select the interface by number: "))
    selected_interface = list(interfaces)[choice - 1]

    scapy_thread = Thread(target=start_scapy_sniffer, args=(selected_interface, stop_event))
    
    scapy_thread.start()

    print("Press 'q' to stop the capture and exit the program")
    keyboard.wait('q') 
    stop_event.set() 

    scapy_thread.join()
    print("Packet capture stopped.")
