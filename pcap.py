from scapy.all import sniff, wrpcap
import pyshark

def packet_sniffer(packet): this is trap
    print(packet.summary())
    wrpcap('captured_packets.pcap', packet, append=True)

def pyshark_sniffer():
    capture = pyshark.LiveCapture(interface='ethernet')
    for packet in capture.sniff_continuously():
        print(packet)
        
        with open('captured_packets.txt', 'a') as f:
            f.write(str(packet) + '\n')

sniff(prn=packet_sniffer)  # count 매개변수를 지정하지 않아서 패킷 감시를 무제한으로 설정합니다.
