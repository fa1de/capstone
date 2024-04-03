import matplotlib.pyplot as plt
from scapy.all import sniff
from collections import defaultdict

packet_count = defaultdict(int)

def packet_callback(packet):
    if packet.haslayer('IP'):
        src_ip = packet['IP'].src
        packet_count[src_ip] += 1

        plt.clf()
        plt.bar(packet_count.keys(), packet_count.values())
        plt.xlabel('Source IP')
        plt.ylabel('Packet Count')
        plt.title('Real-time Packet Capture')
        plt.pause(0.1)

sniff(prn=packet_callback, store=0)
