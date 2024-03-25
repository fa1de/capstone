from scapy.all import sniff, wrpcap
import pyshark
#from scapy.layers.inet import 프로토콜명  // 특정 프로토콜만 캡쳐하기 위해 임포트

def packet_sniffer(packet):
    print(packet.summary())
    wrpcap('captured_packets.pcap', packet, append=True)

def pyshark_sniffer():
    capture = pyshark.LiveCapture(interface='ethernet')
    for packet in capture.sniff_continuously(packet_count=10):
        print(packet)
        #file_path = "저장 파일경로 작성"
        with open('captured_packets.txt', 'a') as f:
            f.write(str(packet) + '\n')

sniff(prn=packet_sniffer, count=10)
#sniff(prn=packet_sniffer, filter="tcp", count=10) // 특정 프로토콜 필터링을 걸기 위함
#pyshark_sniffer()